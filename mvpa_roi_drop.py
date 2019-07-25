#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:32:40 2019

@author: robert.mok
"""
#%%
import os
import numpy as np
import pandas as pd


mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi'

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' #  'noNorm', 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'dCentred'
distMeth = 'svm' # 'svm', 'crossNobis', 'lda'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-all' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))

list(df)

#%%
rois = ['V1vd_lh','V1vd_rh', 'V2vd_lh','V2vd_rh','V3vd_lh','V3vd_rh','V3a_lh','V3a_rh',
        'V3b_lh','V3b_rh', 'hMT_lh','hMT_rh', 'IPS1-5_lh','IPS1-5_rh',
        'SPL1_lh','SPL1_rh','MDroi_ifg_lh','MDroi_ifg_rh', 'MDroi_area8c_lh',
        'MDroi_area8c_rh', 'MDroi_area9_lh','MDroi_area9_rh', 'motor_lh', 'motor_rh']

#rois = ['V1vd_lh','V1vd_rh', 'V2vd_lh','V2vd_rh','V3vd_lh','V3vd_rh','V3a_lh','V3a_rh',
#        'V3b_lh','V3b_rh', 'hMT_lh','hMT_rh', 'IPS1-5_lh','IPS1-5_rh',
#        'MDroi_ifg_lh','MDroi_ifg_rh', 'MDroi_area8c_lh',
#        'MDroi_area8c_rh', 'MDroi_area9_lh','MDroi_area9_rh']

dfFinal=df.copy()
for roi in list(df):
    if roi not in rois:
        print("Removing %s" % roi)
        dfFinal = dfFinal.drop(columns=roi)

dfFinal=dfFinal[rois] #reorder

print(dfFinal.loc['stats'])

dfFinal.to_pickle(os.path.join(mainDir, 'mvpa_roi', 'roi_' + decodeFeature + 'Decoding_' 
                               + distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl'))


#ROIs to run

#love01

#SPL1 
#svm subjCat-orth, objCat, objCat-orth, subjCat-all, 12-way-all, dir-all
#lda - subjCat, subjCat-orth, objCat, subjCat-all, ori, dir, 12-way

#motor
#svm subjCat-all

#all
#lda - objCat-orth, 12-way-all


#love06
#SPL1 
#crossNobis, subjCat, subjCat-orth, objCat, objCat-orth, ori, dir
#mNobis - subjCat-orth, subjCat-all

#motor
#svm subjCat-all

#all
#lda - dir-all

