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

#import ants
import nipype.interfaces.ants as ants

fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep/'
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/Wang_Kastner_ProbAtlas_v4/subj_vol_all'
roiDirOut='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

#featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'

os.chdir('/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/')


roiNames = ['v1', 'v2']

roiCount=1


#loop subs for iSub in range(1,34):

#loop roiNames ; for roi in roiNames:

#testing
iSub=1


subNum=f'{iSub:02d}'
at = ants.ApplyTransforms()
at.inputs.dimension = 3
at.inputs.input_image = os.path.join(roiDir, 'perc_VTPM_vol_roi1_lh.nii.gz') #left v1
at.inputs.reference_image = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz')
at.inputs.output_image = os.path.join(roiDirOut, 'sub-' + subNum + '_v1_lh.nii.gz')
at.inputs.interpolation = 'NearestNeighbor'
at.inputs.default_value = 0
at.inputs.transforms = [os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5')]
at.inputs.invert_transform_flags = [False]
at.cmdline


#%%

at.inputs.input_image = os.path.join(roiDir, 'perc_VTPM_vol_roi' + str(roiCount) + '_lh.nii.gz') #left
at.inputs.output_image = os.path.join(roiDirOut, 'sub-' + subNum + '_' + roi + '_lh.nii.gz')


at.inputs.input_image = os.path.join(roiDir, 'perc_VTPM_vol_roi' + str(roiCount) + '_rh.nii.gz') #left
at.inputs.output_image = os.path.join(roiDirOut, 'sub-' + subNum + '_' + roi + '_rh.nii.gz')


roiCount = roiCount+1 #for Wang/Kastner file naming system







# if need to run in cmd line via python
from subprocess import call

#to check output:
#print(subprocess.check_output(['ls','-l'])) 