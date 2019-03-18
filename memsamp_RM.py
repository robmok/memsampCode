#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:25:56 2019

memsamp functions
@author: robert.mok
"""
import numpy as np
from sklearn.covariance import LedoitWolf

def crossEuclid(x,y,cv):
    """ 

    Compute cross-validated Euclidean distance score over crossvalidation folds
    Based on cross_val_score from skleanrn (esp. comments)
    Using np.dot rather than np.inner - quick check shows its a bit faster

    Parameters
    ----------
    estimator : estimator object implementing 'fit'
        The object to use to fit the data.

    X : array-like
        The data to fit. Can be for example a list, or an array.

    y : array-like, optional
        The target variable to try to predict in the case of
        supervised learning.
        
    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        e.g.:
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
    Using np.dot rather than np.inner - quick check shows its a bit faster
    
    var : array-like
    voxel x time variance matrix from feat output
    
    """

    cv_iter = list(cv) # list the cv splits to access as indices
    conds=np.unique(y) # two conds to compare
    dist = np.empty((len(cv_iter)))
    runs = np.array((0,1,2))
    for iRun in range(0,len(cv_iter)): #n-folds
        trainIndA  = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[0])) #first 0 indexes train set, second 0/1 is the condition
        trainIndB  = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[1]))
        testIndA   = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[0])) # first 1 indexes test set, second 0/1 is the condition
        testIndB   = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[1]))  
        
        #compute covariance matrix
        ind = np.where(runs!=iRun)
        ind = ind[0]
        nVox = var.shape
        covMat = np.empty((nVox[1],nVox[1],len(runs)-1))
        for i in range(0,len(ind)):
            cov = LedoitWolf().fit(var[:,:,ind[i]])
            covMat[:,:,i] = cov.covariance_
        covMatAv = np.linalg.inv(covMat.mean(axis=2)) #also compute the inv here
        

      #
        
        trainDat   = x[trainIndA,].mean(axis=0)-x[trainIndB,].mean(axis=0)
        testDat    = x[testIndA,].mean(axis=0)-x[testIndB,].mean(axis=0)
        dist[iRun] = np.dot(np.dot(trainDat,covMatAv),np.dot(testDat,covMatAv)) #first dim volumes (trials), second dim voxels    
        
        #testing
        np.dot(np.dot(trainDat,covMatAv),np.dot(testDat,covMatAv))
        np.dot(np.dot(trainDat,covMatAv),testDat) #quite diff
        
        #double check if np.dot does inner product properly for cov mat
        
        #also - same as first one above
        trainDat   = np.dot(x[trainIndA,].mean(axis=0),covMatAv)-np.dot(x[trainIndB,].mean(axis=0),covMatAv)
        testDat    = np.dot(x[testIndA,].mean(axis=0),covMatAv)-np.dot(x[testIndB,].mean(axis=0),covMatAv)
        dist[iRun] = np.dot(trainDat,testDat) #first dim volumes (trials), second dim voxels        
        
        
        
    return dist



















