#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:32:40 2019

@author: robert.mok
"""
#%%
import os
import pandas as pd


mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi'

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' #  'noNorm', 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'dCentred'
distMeth = 'svm' # 'svm', 'crossNobis', 'lda'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'motor' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 

fname = os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + 
                      '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                      str(fwhm) + '_' + imDat)

#if looking at motor, uncomment:
#fname = fname + '_lock2resp'

df=pd.read_pickle(fname + '.pkl')


list(df)

#%%
#rois = ['V1vd_lh','V1vd_rh', 'V2vd_lh','V2vd_rh','V3vd_lh','V3vd_rh','V3a_lh','V3a_rh',
#        'V3b_lh','V3b_rh', 'hMT_lh','hMT_rh', 'IPS1-5_lh','IPS1-5_rh',
#        'SPL1_lh','SPL1_rh','MDroi_ifg_lh','MDroi_ifg_rh', 'MDroi_area8c_lh',
#        'MDroi_area8c_rh', 'MDroi_area9_lh','MDroi_area9_rh', 'motor_lh', 'motor_rh']

rois = ['EVC_lh','EVC_rh','V3a_lh','V3a_rh','hMT_lh','hMT_rh','IPS1-5_lh','IPS1-5_rh','MDroi_ifg_lh',
        'MDroi_ifg_rh', 'MDroi_area8c_lh', 'MDroi_area8c_rh', 'MDroi_area9_lh',
        'MDroi_area9_rh', 'motor_lh', 'motor_rh']

dfFinal=df.copy()
for roi in list(df):
    if roi not in rois:
        print("Removing %s" % roi)
        dfFinal = dfFinal.drop(columns=roi)

dfFinal=dfFinal[rois] #reorder

print(dfFinal.loc['stats'])

#%%
#save
dfFinal.to_pickle(os.path.join(mainDir, 'mvpa_roi', 'roi_' + decodeFeature + 'Decoding_' 
                               + distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl'))
