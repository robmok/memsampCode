#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:38:39 2019

@author: robert.mok
"""

#%%
import os
import nipype.interfaces.ants as ants
from subprocess import call

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'
fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep/'

at = ants.ApplyTransforms() #define function
imDat   = 'cope' # cope or tstat images
slSiz=6 #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'crossNobis' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'trials' # 'trials' or 'blocks' 
fwhm = None # smoothing - set to None if no smoothing

decodeFeature = 'ori' #'12-way', 'dir', 'ori', ...

for iSub in range(1,34):
    subNum=f'{iSub:02d}'
    print('Transforming searchlight imgs from T1 to MNI space: sub-%s, %s, %s, %s, %s' % (subNum, imDat, distMeth, normMeth, trainSetMeth))
    at.inputs.dimension = 3
    at.inputs.input_image = os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) +
                                         '_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth +
                                         '_'  + trainSetMeth + '_fwhm' + str(fwhm) +
                                         '_' + imDat + '_sub-' + subNum + '.nii.gz')

    at.inputs.reference_image = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-'
                                             + subNum + '_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')

    at.inputs.output_image = os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) +
                                         '_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth +
                                         '_'  + trainSetMeth + '_fwhm' + str(fwhm) +
                                         '_' + imDat + '_sub-' + subNum + '_mni.nii.gz')
    at.inputs.interpolation = 'NearestNeighbor'
    at.inputs.default_value = 0
    at.inputs.transforms = [os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' +
                                         subNum + '_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5')]
    at.inputs.invert_transform_flags = [False]
    runCmd='/Users/robert.mok/bin/ants/bin/' + at.cmdline
    call(runCmd,shell=True) # run in cmd line via python. to check output, use subprocess.check_output: from subprocess import check_output


