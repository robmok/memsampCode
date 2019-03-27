#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:48:06 2019

@author: robert.mok
"""
import os
import nipype.interfaces.ants as ants
from subprocess import call

fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep/'
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

#roiNames = ['V1v', 'V1d', 'V2v', 'V2d', 'V3v', 'V3d', 'hV4','V01','V02','PHC1','PHC2','MST','hMT','L02','L01','V3b','V3a','IPS0','IPS1','IPS2','IPS3','IPS4','IPS5','SPL1','FEF']
roiNames = ['MDroi_ips','MDroi_pcg','MDroi_ifg','MDroi_area8c','MDroi_area9']
at = ants.ApplyTransforms() #define function

#loop subs 
for iSub in range(1,34):
    subNum=f'{iSub:02d}'
    roiCount=1 #for Wang/Kastner file naming system
    for roi in roiNames:
        print('Transforming ROIs from MNI to T1 space: sub-%s, %s' % (subNum, roi))
        #left
        at.inputs.dimension = 3
        at.inputs.input_image = os.path.join(roiDir, 'roi' + str(roiCount) + '_lh.nii.gz') #left
        at.inputs.reference_image = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz')
        at.inputs.output_image = os.path.join(roiDir, 'sub-' + subNum + '_' + roi + '_lh.nii.gz')
        at.inputs.interpolation = 'NearestNeighbor'
        at.inputs.default_value = 0
        at.inputs.transforms = [os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5')]
        at.inputs.invert_transform_flags = [False]
        runCmd='/Users/robert.mok/bin/ants/bin/' + at.cmdline
        call(runCmd,shell=True) # run in cmd line via python. to check output, use subprocess.check_output: from subprocess import check_output
        #right
        at.inputs.input_image = os.path.join(roiDir, 'roi' + str(roiCount) + '_rh.nii.gz')
        at.inputs.output_image = os.path.join(roiDir, 'sub-' + subNum + '_' + roi + '_rh.nii.gz')
        runCmd='/Users/robert.mok/bin/ants/bin/' + at.cmdline
        call(runCmd,shell=True)
        roiCount = roiCount+1 #for Wang/Kastner file naming system