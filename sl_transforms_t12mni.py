#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:38:39 2019

@author: robert.mok
"""

#to do

#	• #subjCat crossnobis niNorm fwhmNone
#	• #subjCat crossnobis niNorm fwhm1

#	• #objCat crossNobis noNorm fwhm0
#	• #objCat crossNobis noNorm fwhm1
#
#
#	• #objCat svm noNorm fwhm0
#	• #objCat svm noNorm fwhm1
#
#	• #ori, crossnobis, niNorm, fwhmNone
#	• #ori, crossnobis, niNorm, fwhm1
#	
#	• #12-way niNorm tstat, fwhm1
#	• #12-way niNorm cope, fwhm1

#	• # svm ori niNorm fwhmNone, cope
##      svm ori niNorm fwhm1, cope



#%%
import os
import nipype.interfaces.ants as ants
from subprocess import call

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'
fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep/'
slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'

at = ants.ApplyTransforms() #define function
imDat   = 'cope' # cope or tstat images
slSiz=6 #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'crossNobis' # 'svm', 'crossEuclid', 'crossNobis'
trainSetMeth = 'blocks' # 'trials' or 'blocks' 
fwhm = 1 # smoothing - set to None if no smoothing

decodeFeature = 'objCat' #'12-way', 'dir', 'ori', ..., 'subjCat', 'objCat'

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


#merge all subjects into one .nii.gz file using fslmerge
runCmdMerge='fslmerge -t ' + os.path.join(slDir, 'sl'+ str(slSiz) +'_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_allsubs_mni.nii.gz') +  ' ' + os.path.join(slDir, 'sl'+ str(slSiz) +'_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_sub-*mni.nii.gz')
call(runCmdMerge,shell=True)


##allrois - did searchlight within an roi/a set of rois
#for iSub in range(1,34):
#    subNum=f'{iSub:02d}'
#    print('Transforming searchlight imgs from T1 to MNI space: sub-%s, %s, %s, %s, %s' % (subNum, imDat, distMeth, normMeth, trainSetMeth))
#    at.inputs.dimension = 3
#    at.inputs.input_image = os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) +
#                                         '_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth +
#                                         '_'  + trainSetMeth + '_fwhm' + str(fwhm) +
#                                         '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz')
#
#    at.inputs.reference_image = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-'
#                                             + subNum + '_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')
#
#    at.inputs.output_image = os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) +
#                                         '_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth +
#                                         '_'  + trainSetMeth + '_fwhm' + str(fwhm) +
#                                         '_' + imDat + '_sub-' + subNum + '_allROIsSL_mni.nii.gz')
#    at.inputs.interpolation = 'NearestNeighbor'
#    at.inputs.default_value = 0
#    at.inputs.transforms = [os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' +
#                                         subNum + '_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5')]
#    at.inputs.invert_transform_flags = [False]
#    runCmd='/Users/robert.mok/bin/ants/bin/' + at.cmdline
#    call(runCmd,shell=True) # run in cmd line via python. to check output, use subprocess.check_output: from subprocess import check_output
#
#
##merge all subjects into one .nii.gz file using fslmerge
#runCmdMerge='fslmerge -t ' + os.path.join(slDir, 'sl'+ str(slSiz) +'_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_allROIsSL_allsubs_mni.nii.gz') +  ' ' + os.path.join(slDir, 'sl'+ str(slSiz) +'_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_sub-*_allROIsSL_mni.nii.gz')
#call(runCmdMerge,shell=True)