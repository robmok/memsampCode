#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:00:52 2019

@author: robert.mok
"""

import os
import numpy as np
import pandas as pd
#from matplotlib.pyplot import plot as plt

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/'
#roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/bilateral'

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'svm' # 'svm', 'crossNobis'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = '12-way' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
#%%


#p = avg_time.plot(figsize=15,5),legend=False,kind="bar",rot=45,color="blue",fontsize=16,yerr=std);

stdAll = df.iloc[0:33,:].std()/np.sqrt(33)
ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll)
#ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll,ylim=(.5,.537))
#ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll,ylim=(1/12,0.09))
