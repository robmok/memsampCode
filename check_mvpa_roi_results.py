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

from statsmodels.stats.multitest import fdrcorrection as fdr
from statsmodels.stats.multitest import multipletests as multest

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi'

# laptop
#mainDir='/Users/robertmok/Documents/Postdoc_ucl/' 

#subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))
#exclSubs = True
#if exclSubs:
#    nDirInCat=np.empty((2,33))
#    for iSub in range(0,33):
#        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
#        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
#    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
#else:
#    indSubs=np.ones(33,dtype=bool)
#    


imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' #  'noNorm', 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'dCentred'
distMeth = 'svm' # 'svm', 'crossNobis', 'lda'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-orth' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '_goodone.pkl')))
df.loc['stats']


pvals=np.empty((len(list(df))-1))
for iRoi in range(0,len(list(df))-1):
    pvals[iRoi]= df.loc['stats'][iRoi].pvalue

fdr(pvals/2,alpha=0.05,method='indep',is_sorted=False)
multest(pvals/2, alpha=0.05, method='fdr_bh', is_sorted=False, returnsorted=False)


#pSorted=np.sort(pvals)
#fdr(pSorted[0:22]/2,alpha=0.05,method='indep',is_sorted=True)
#multest(pSorted[0:22]/2, alpha=0.05, method='bonferroni', is_sorted=True, returnsorted=False)