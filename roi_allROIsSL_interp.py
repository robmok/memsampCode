#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:53:28 2019

#interpolate masks to searchlight mni space
#to use mask for randomise for searchlight analysis need the mask to be in the same space  

@author: robert.mok
"""
import os
from nilearn import image as nli # Import image processing tool
import nibabel as nib

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

#select one whole brain sl that was run already
imgs = nib.load('/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight/sl6_12-wayDecoding_svm_noNorm_trials_fwhmNone_cope_sub-01_mni.nii.gz')

mask_path = os.path.join(roiDir, 'allROIsSL_1.nii.gz') 
mask = nib.load(mask_path)
mask = nli.resample_img(mask, target_affine=imgs.affine, 
                        target_shape=imgs.shape[:3], interpolation='nearest')
nib.save(mask, os.path.join(roiDir,'allROIsSL_1_interp2sl.nii.gz'))

mask_path = os.path.join(roiDir, 'allROIsSL_2.nii.gz') 
mask = nib.load(mask_path)
mask = nli.resample_img(mask, target_affine=imgs.affine, 
                        target_shape=imgs.shape[:3], interpolation='nearest')
nib.save(mask, os.path.join(roiDir,'allROIsSL_2_interp2sl.nii.gz'))

mask_path = os.path.join(roiDir, 'MDroi_all.nii.gz') 
mask = nib.load(mask_path)
mask = nli.resample_img(mask, target_affine=imgs.affine, 
                        target_shape=imgs.shape[:3], interpolation='nearest')
nib.save(mask, os.path.join(roiDir,'MDroi_all_interp2sl.nii.gz'))


