#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:10:41 2019

@author: robert.mok
"""
#%%
import os
import pandas as pd
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi'

# laptop
#mainDir='/Users/robertmok/Documents/Postdoc_ucl/' 

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' #  'noNorm', 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'dCentred'
distMeth = 'svm' # 'svm', 'crossNobis', 'lda'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-orth' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 


df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
df.loc['stats']