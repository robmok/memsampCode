#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

# tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
tThresh=1.6938 #  - DF = 33-1, one-tailed, p=0.05

vSmooth=5

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

#allROIs eqSubs vSmooth=10
vSmooth=10

#cMass
trainSetMeth='trials'
slSiz=9
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_lock2resp_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_lock2resp_allsubs_mni_allROIsSL.nii.gz -1 -v ${vSmooth} -C ${tThresh}

#vox
trainSetMeth='trials'
slSiz=9
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='vox' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_lock2resp_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_lock2resp_allsubs_mni_allROIsSL.nii.gz -1 -v ${vSmooth} -x

#tfce
trainSetMeth='trials'
slSiz=9
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='tfce' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_lock2resp_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_lock2resp_allsubs_mni_allROIsSL.nii.gz -1 -v ${vSmooth} -T
