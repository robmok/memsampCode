#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

# tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
tThresh=1.6938 #  - DF = 33-1, one-tailed, p=0.05

vSmooth=5

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

#allROIs vSmooth=10 vox
vSmooth=10

#tfce
trainSetMeth='trials'
slSiz=8
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='tfce' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_lock2resp_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_lock2resp_allsubs_mni.nii.gz -1 -v ${vSmooth} -T

#run vs=5
vSmooth=5

#tfce
trainSetMeth='trials'
slSiz=8
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='tfce' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_lock2resp_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_lock2resp_allsubs_mni.nii.gz -1 -v ${vSmooth} -T
