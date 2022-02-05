#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:10:41 2019

@author: robert.mok
"""
#%%
import os
import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multitest import fdrcorrection as fdr
# from statsmodels.stats.multitest import multipletests as multest

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi'
# laptop
#mainDir='/Users/robertmok/Documents/Postdoc_ucl/' 

subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))

imDat    = 'cope'
normMeth = 'noNorm'
distMeth = 'svm'
trainSetMeth = 'trials'
fwhm = None

# decoders
# 'subjCat-orth' is main result - subj cat minus orthogonal directions
# sensory decoding: 'dir' (opposite dirs), 'ori' (orientation-orthogonal angs)
# '12-way' (12-way dir decoding), 'subjCat'- w/out subtraction, objCat- objective category,
# objCatRaw-orth - objective category minus orthogonal directions
decodeFeature = 'subjCat-orth'

fname = os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + 
                      '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                      str(fwhm) + '_' + imDat)
##if looking at motor, uncomment:
#fname = fname + '_lock2resp'

df=pd.read_pickle(fname + '.pkl')
##df=pd.read_pickle(fname + '_model.pkl')
print(df.loc['stats'])

pvals=np.empty((len(list(df))))
for iRoi in range(0,len(list(df))):
    pvals[iRoi]= df.loc['stats'][iRoi].pvalue

# correcting
# category - correcting over all rois apart from motor (12 ROIS)
#print(fdr(pvals[0:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))

# all rois apart from EVC and motor (10 ROIS) - didn't use this? check
#print(fdr(pvals[2:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))

# no EVC and motor - ? didn't use this? check
#ind = np.concatenate([np.arange(2,11), [len(pvals)-3, len(pvals)-2]])
ind = np.concatenate([np.arange(2,12), [len(pvals)-2, len(pvals)-1]]) # new
ind = np.concatenate([np.arange(2,12)]) # without FFA/PPA
print(fdr(pvals[ind]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[ind]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)
