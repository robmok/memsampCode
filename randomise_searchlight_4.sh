#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
vSmooth=5

 # ○ 12-way sl6 svm cope noNorm fwhm1, blocks (p=0.43)
 vSmooth=8

 trainSetMeth='blocks'
 slSiz=6
 normMeth='noNorm'
 decodeFeature='12-way'
 distMeth='svm'
 fwhm=1
 imDat='cope' # cope or tstat images
 threshMeth='cMass'
 randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
 -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

 # 12-way sl6 svm cope niNormalised fwhmNone, blocks (p=0.3)
