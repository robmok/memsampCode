#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:38:28 2019

@author: robert.mok
"""
# subjCat/Raw-orth

#love06 - subtracted:
# #fwhm=3, sph=9 - subjCat/orth cope/tstat, crossnobis, noNorm
# #fwhm=3, sph=12 - subjCat/orth cope/tstat, noNorm

#love01
#sl9_subjCatDecoding_svm_noNorm_trials_fwhmNone_cope_sub-33.nii.gz
#sl9_subjCatDecoding_svm_noNorm_trials_fwhmNone_tstat_sub-33.nii.gz
#sl9_subjCatDecoding_crossNobis_noNorm_trials_fwhmNone_cope_sub-33.nii.gz

#sl12_subjCatDecoding_svm_noNorm_trials_fwhmNone_cope_sub-33.nii.gz
#sl12_subjCatDecoding_svm_noNorm_trials_fwhmNone_tstat_sub-33.nii.gz
#sl12_subjCatDecoding_svm_noNorm_trials_fwhm5_tstat_sub-33.nii.gz




#missing - running in love06 now
#sl12_subjCatRawDecoding-orth_svm_noNorm_trials_fwhm5_cope_sub-33.nii.gz - almost

#to do
#sl12_subjCatDecoding_crossNobis_noNorm_trials_fwhmNone_cope_sub-33.nii.gz
#sl12_subjCatDecoding_crossNobis_noNorm_trials_fwhm5_cope_sub-33.nii.gz 

#love06 running
#subjCatRaw-orth cope, noNorm, sl12, fwhm5 - almost done
#subjCatRaw-orth tstat, noNorm, sl12, fwhm5
#subjCatRaw-orth crossnobis, noNorm, sl12, fwhm5

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

imDat = 'tstat' # cope or tstat images
slSiz = 12 #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'trials' # 'trials' or 'blocks'
fwhm = 5 # smoothing - set to None if no smoothing

decodeFeature = 'subjCat' # category: 'objCat' (objective catgeory), 'subjCat' 

nSubs=33
for iSub in range(1,nSubs+1):
    subNum=f'{iSub:02d}'
    print('Subtracting %s searchlight imgs from "orth" images: sub-%s, %s, %s, %s, %s, fwhm=%s' % (decodeFeature, subNum,  imDat, distMeth, normMeth, trainSetMeth, str(fwhm)))

    im1 = nib.load(os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                  'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + str(fwhm) + 
                  '_' + imDat + '_sub-' + subNum + '.nii.gz'))
    im2 = nib.load(os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                  'Raw-orth' + 'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                  str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))
        
    im = math_img("im1 - im2", im1=im1, im2=im2)
    
    nib.save(im, os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                              '-orth' + 'Decoding_' + distMeth + '_' + normMeth + '_'  + 
                              trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))
    del im