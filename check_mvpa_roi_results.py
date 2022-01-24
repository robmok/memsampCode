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
from statsmodels.stats.multitest import multipletests as multest

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi'

# laptop
#mainDir='/Users/robertmok/Documents/Postdoc_ucl/' 

subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' #  'noNorm'
distMeth = 'svm' # 'svm'
trainSetMeth = 'trials' # 'trials'
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-minus-motor' # 'subjCat', '12-way' (12-way dir decoding), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# subjCat, subjCat-orth, objCat, objCatRaw-orth 
# subjCat-resp - decode on category subject responded

fname = os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + 
                      '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                      str(fwhm) + '_' + imDat)

##if looking at motor, uncomment:
#fname = fname + '_lock2resp'

#bilateral
#fname = fname + '_bilateral'

#decoding at feedback time
#fname = fname + '_fromfeedback'

df=pd.read_pickle(fname + '.pkl')
##df=pd.read_pickle(fname + '_model.pkl')
print(df.loc['stats'])

pvals=np.empty((len(list(df))))
for iRoi in range(0,len(list(df))):
    pvals[iRoi]= df.loc['stats'][iRoi].pvalue

# correcting
# all rois apart from motor (12 ROIS)
#print(fdr(pvals[0:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[0:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)
# all rois apart from EVC and motor (10 ROIS)
#print(fdr(pvals[2:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[2:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)

# no EVC and motor
#ind = np.concatenate([np.arange(2,11), [len(pvals)-3, len(pvals)-2]])
ind = np.concatenate([np.arange(2,12), [len(pvals)-2, len(pvals)-1]]) # new
ind = np.concatenate([np.arange(2,12)]) # without FFA/PPA
print(fdr(pvals[ind]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[ind]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)
