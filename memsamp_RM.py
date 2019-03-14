#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:25:56 2019

memsamp functions
@author: robert.mok
"""
import numpy as np

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

    #list the cv splits to access as indices
    cv_iter = list(cv)
    conds=np.unique(y)
    
    dist = np.empty((len(cv_iter)))
    for iRun in range(0,len(cv_iter)): #n-folds
        trainIndA = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[0]))
        trainIndB = np.intersect1d(cv_iter[iRun][0],np.where(y==conds[1]))
        testIndA = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[0]))
        testIndB = np.intersect1d(cv_iter[iRun][1],np.where(y==conds[1]))        
        trainDat = x[trainIndA,].mean(axis=0)-x[trainIndB,].mean(axis=0)
        testDat = x[testIndA,].mean(axis=0)-x[testIndB,].mean(axis=0)
        dist[iRun] = np.dot(trainDat,testDat) #first dim volumes (trials), second dim voxels        

    return dist