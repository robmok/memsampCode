#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:38:39 2019

@author: robert.mok
"""

# subjCat/Raw-orth - diff sl size and smoothing
# #fwhm=3, sph=9 - subjCat/orth cope/tstat, crossnobis, noNorm
# #fwhm=3, sph=12 - subjCat/orth cope/tstat, noNorm


#love01
#sl9_subjCatDecoding_svm_noNorm_trials_fwhmNone_cope_sub-33.nii.gz
#sl9_subjCatDecoding_svm_noNorm_trials_fwhmNone_tstat_sub-33.nii.gz
#sl9_subjCatDecoding_crossNobis_noNorm_trials_fwhmNone_cope_sub-33.nii.gz

#sl12_subjCatDecoding_svm_noNorm_trials_fwhmNone_cope_sub-33.nii.gz
#sl12_subjCatDecoding_svm_noNorm_trials_fwhmNone_tstat_sub-33.nii.gz
#sl12_subjCatDecoding_svm_noNorm_trials_fwhm5_tstat_sub-33.nii.gz



#subjCatRaw-orth cope, noNorm, sl12, fwhm5 
#subjCatRaw-orth tstat, noNorm, sl12, fwhm5 - randomised the subjCat but not orth
#subjCatRaw-orth crossnobis, noNorm, sl12, fwhm5
#subjCatRaw-orth crossnobis, noNorm, sl12, fwhmNone
#%%
import os
import nipype.interfaces.ants as ants
from subprocess import call
from nilearn import image as nli # Import image processing tool
import nibabel as nib

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'
fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep/'
slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'

at = ants.ApplyTransforms() #define function
imDat   = 'cope' # cope or tstat images
slSiz = 12 #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'crossNobis' # 'svm', 'crossNobis'
trainSetMeth = 'trials' # 'trials' or 'blocks' 
fwhm = None # smoothing - set to None if no smoothing

decodeFeature = 'subjCat-orth' #'12-way', 'dir', 'ori', ..., 'subjCat', 'objCat'

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

#compute a mean image for visualisation
im = nli.mean_img(os.path.join(slDir, 'sl'+ str(slSiz) +'_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_allsubs_mni.nii.gz')) 
nib.save(im, os.path.join(slDir, 'sl'+ str(slSiz) +'_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_allsubs_mni_meanIm.nii.gz'))


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