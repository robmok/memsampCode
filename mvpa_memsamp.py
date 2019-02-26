#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:48:06 2019

@author: robert.mok
"""

import os
#import glob
#import pandas as pd
import numpy as np
np.set_printoptions(precision=2, suppress=True) # Set numpy to print only 2 decimal digits for neatness
# import nibabel as nib
from nilearn import plotting
from nilearn import image # Import image processing tool

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'

os.chdir(featDir)


#sub-01_run-01_block_T1_fwhm2.feat 
#sub-01_run-01_trial_T1_fwhm2.feat

subs=range(1,34)
#for iSub in subs:
iSub=1
subNum=f'{iSub:02d}'
iRun=1
iCope=1



datDir=os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun) +'_block_T1_fwhm2.feat/stats/cope' + str(iCope) + '.nii.gz')



