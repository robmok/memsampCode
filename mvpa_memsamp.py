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





