#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:38:28 2019

@author: robert.mok
"""
#%%
import sys
sys.path.append('/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/')
import os
import nibabel as nib
from nilearn.image import math_img

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06

featDir=os.path.join(mainDir,'memsampFeat')
fmriprepDir=os.path.join(mainDir,'fmriprep_output/fmriprep')
roiDir=os.path.join(mainDir,'rois')
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)

imDat = 'cope' # cope or tstat images
slSiz = 6 #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'trials' # 'trials' or 'blocks'
fwhm = 1 # smoothing - set to None if no smoothing

decodeFeature = 'subjCat' # category: 'objCat' (objective catgeory), 'subjCat' 

#subjCatRaw&subjCatRaw-orth, noNorm fwhm0, cope/tstat, blocks
#subjCatRaw&subjCatRaw-orth, noNorm fwhm0/1, cope, trials

#done:
#sl6_subjCatRaw-orthDecoding_svm_noNorm_blocks_fwhmNone_cope_sub-01.nii.gz
#sl6_subjCatRaw-orthDecoding_svm_noNorm_blocks_fwhmNone_tstat_sub-01.nii.gz
#sl6_subjCatRaw-orthDecoding_svm_noNorm_trials_fwhmNone_cope_sub-01.nii.gz
#sl6_subjCatRaw-orthDecoding_svm_noNorm_blocks_fwhm1_cope_sub-01.nii.gz
#sl6_subjCatRaw-orthDecoding_svm_noNorm_trials_fwhm1_cope_sub-01.nii.gz

#so above missing...
# tstat, block/trial, fwhm1; subjCatRaw/subjCatRaw-orth tstat, noNorm fwhm0trials


nSubs=33
for iSub in range(1,nSubs+1):
    subNum=f'{iSub:02d}'
    print('Subtracting %s searchlight imgs from "orth" images: sub-%s, %s, %s, %s, %s, fwhm=%s' % (decodeFeature, subNum,  imDat, distMeth, normMeth, trainSetMeth, str(fwhm)))

    im1 = nib.load(os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                  'Raw' + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + 
                  '_' + imDat + '_sub-' + subNum + '.nii.gz'))
    im2 = nib.load(os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                  'Raw-orth' + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                  str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))
        
    im = math_img("im1 - im2", im1=im1, im2=im2)
    
    nib.save(im, os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                              '-orth' + 'Decoding_' + distMeth + '_' + normMeth + '_'  + 
                              trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))
    del im