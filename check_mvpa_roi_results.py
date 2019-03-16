#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:10:41 2019

@author: robert.mok
"""
#%%

imDat    = 'cope' # cope or tstat images
normMeth = 'demeaned_stdNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'crossEuclid' # 'svm', 'crossEuclid', 'crossNobis'
trainSetMeth = 'trials' # 'trials' or 'block' - only tirals in this script
fwhm = 1 # optional smoothing param - 1, or None

decodeFeature = 'ori' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 


df=pd.read_pickle((os.path.join(mainDir, 'mvpa_roi', 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
df.loc['stats']