#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:52:51 2019

@author: robert.mok

Forgot to normalise by chance in the searchlight maps - randomise --> all sig above zero
"""

import sys
sys.path.append('/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/')
import os
from nilearn import image as nli # Import image processing tool
import nibabel as nib
from nilearn.masking import apply_mask, unmask

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep'

imDat   = 'tstat' # cope or tstat images
slSiz=5 #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'blocks' # 'trials' or 'block'
fwhm = 1 # smoothing - set to None if no smoothing
nCores = 4 #number of cores for searchlight - up to 6 on love06 (i think 8 max)

for iSub in range(1,34):
    subNum=f'{iSub:02d}'
    
    im = nib.load(os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_dirDecoding_' + 
                  distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                  str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))
    T1_mask_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz') 

    T1_mask = nli.resample_img(T1_mask_path, target_affine=im.affine, 
                                            target_shape=im.shape[:3], interpolation='nearest')
    chance   = 1./12
    imVec    = apply_mask(im,T1_mask)
    imVec    = imVec - chance
    imThresh = unmask(imVec,T1_mask)
    nib.save(imThresh, os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_dirDecoding_' + 
                                    distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                                    str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))

print('done')