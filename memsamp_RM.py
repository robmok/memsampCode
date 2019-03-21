#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:25:56 2019

memsamp functions
@author: robert.mok
"""
import numpy as np
from sklearn.covariance import LedoitWolf
#from scipy.linalg import fractional_matrix_power

def getConds2comp(decodeFeature):
    if decodeFeature == "dir":
        conds2comp = [[0,180], [30,210], [60,240], [90,270],[120,300],[150,330]]
    elif decodeFeature == "ori":
        conds2comp = [[0,90], [0,270], [30,120], [30,300], [60,150], [60,300], [90,180], [120,210],[150,240],[180,270],[210,300],[240,330]]
    elif decodeFeature == "12-way-all":
        allDirs = np.arange(0,330,30)
        conds2comp = [[0,np.setxor1d(0,allDirs)],  [30,np.setxor1d(0,allDirs)], [60,np.setxor1d(0,allDirs)], [90,np.setxor1d(0,allDirs)],
                      [120,np.setxor1d(0,allDirs)],[150,np.setxor1d(0,allDirs)],[180,np.setxor1d(0,allDirs)],[210,np.setxor1d(0,allDirs)],
                      [240,np.setxor1d(0,allDirs)],[270,np.setxor1d(0,allDirs)],[300,np.setxor1d(0,allDirs)],[330,np.setxor1d(0,allDirs)]]
        
    return conds2comp


def crossEuclid(x,y,cv):
    """ 

    Compute cross-validated Euclidean distance score over crossvalidation folds
    Based on cross_val_score from skleanrn (esp. comments)
    Using np.dot rather than np.inner - quick check shows its a bit faster

    Parameters
    ----------
    X : array-like
        The data to fit. Can be for example a list, or an array.

    y : array-like, optional
        The target variable to try to predict in the case of
        supervised learning.
        
    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy. e.g.:
        cv = LeaveOneGroupOut()
        cv.get_n_splits(fmri_masked_cleaned, y, groups)
        cv = cv.split(fmri_data,y,groups)
    """
    
    cv_iter = list(cv) # list the cv splits to access as indices
    conds=np.unique(y) # two conds to compare
    dist = np.empty((len(cv_iter)))
    for iRun in range(0,len(cv_iter)): #n-folds
        trainIndA  = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[0])) #first 0 indexes train set, second 0/1 is the condition
        trainIndB  = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[1]))
        testIndA   = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[0])) # first 1 indexes test set, second 0/1 is the condition
        testIndB   = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[1]))  
        trainDat   = x[trainIndA,].mean(axis=0)-x[trainIndB,].mean(axis=0)
        testDat    = x[testIndA,].mean(axis=0)-x[testIndB,].mean(axis=0)
        dist[iRun] = np.dot(trainDat,testDat) #first dim volumes (trials), second dim voxels        
    return dist


def crossNobis(x,y,cv,var):
    """ 
    Compute cross-validated Mahalanobis distance score over crossvalidation folds
    
    var : array-like
    [run x] voxel x time variance matrix from feat output
    
    """
    cv_iter = list(cv) # list the cv splits to access as indices
    conds=np.unique(y) # two conds to compare
    dist = np.empty((len(cv_iter)))
    runs = np.array((0,1,2)) #note this changed from runs=1,2,3, in main script
    for iRun in range(0,len(cv_iter)): #n-folds
        trainIndA  = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[0])) #first 0 indexes train set, second 0/1 is the condition
        trainIndB  = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[1]))
        testIndA   = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[0])) # first 1 indexes test set, second 0/1 is the condition
        testIndB   = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[1]))  
        
        #compute covariance matrix from training runs
        ind = np.where(runs!=iRun) #better way? next line is a bit annoying...
        ind = ind[0]
        nVox = np.size(var,axis=2)
        covMat = np.empty((nVox,nVox,len(runs)-1))
        for i in range(0,len(ind)):
            cov = LedoitWolf().fit(var[ind[i]])
#            cov = LedoitWolf().fit(var[ind[i],:,:]) #clarte fmri object structure
            covMat[:,:,i] = cov.covariance_
        covMatAv = np.linalg.inv(covMat.mean(axis=2)) #also compute the inv here
        
        #use testSet cov for pre-whitening test set
        covTestTmp = LedoitWolf().fit(var[iRun])
        covTest = np.linalg.inv(covTestTmp.covariance_)
        
        trainDat   = x[trainIndA,].mean(axis=0)-x[trainIndB,].mean(axis=0)
        testDat    = x[testIndA,].mean(axis=0)-x[testIndB,].mean(axis=0)
        dist[iRun] = np.dot(np.dot(trainDat,covMatAv),np.dot(testDat,covTest)) #first dim volumes (trials), second dim voxels    
    return dist



def compCovMat(var):
    covTmp = LedoitWolf().fit(var)
    covMat = np.linalg.inv(covTmp.covariance_)
#    covMat = fractional_matrix_power(covTmp.covariance_,-0.5)
    return covMat














