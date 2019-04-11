#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
vSmooth=5

# threshMeth='vox' #vox, tfce, cSize, cMass

#TRYING VARIANCE SMOOTHING = 8, only cMass
vSmooth=8

# ○ subjCat - sl6 svm cope trials/block, crossnobis block (around p=0.5)
# ○ 12-way sl6 svm cope noNorm fwhm1, blocks (p=0.43)
# 12-way sl6 svm cope niNormalised fwhmNone, blocks (p=0.3)


####

# fwhm=1
# subjCat svm cope trials/block, noNorm/niNorm
# Crossnobis block

# subjCat svm cope trials noNorm

#NB- vs5 and vs8

vSmooth=5
trainSetMeth='trials'
slSiz=6
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm=1
imDat='cope' # cope or tstat images
threshMeth='cMass'
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

vSmooth=8
trainSetMeth='trials'
slSiz=6
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm=1
imDat='cope' # cope or tstat images
threshMeth='cMass'
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
