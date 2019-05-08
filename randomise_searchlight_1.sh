#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

# command templates:
# #orig without mask
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
#
# #with mask:
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allROIsSL_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allROIsSL_allsubs_mni.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -C ${tThresh}
# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allROIsSL_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allROIsSL_allsubs_mni.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -C ${tThresh}

tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
vSmooth=5

# threshMeth='vox' #vox, tfce, cSize, cMass

##subjCat cope, noNorm fwhm0, blocks
#subjCat-orth cope, noNorm
##subjCat cope, tstat fwhm0
#subjCat-orth tstat, noNorm
##subjCat crossNobis, noNorm fwhm0
#subjCat-orth crossNobis, noNorm

#subjCat cope, noNorm fwhm0, trials
#subjCat-orth cope, noNorm fwhm
#subjCat tstat, noNorm fwhm0
#subjCat-orth tstat, noNorm fwhm0

#subjCat-orth cope, noNorm, blocks
trainSetMeth='blocks'
slSiz=6
normMeth='noNorm'
decodeFeature='subjCat-orth'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

##subjCat cope, noNorm fwhm0, blocks
trainSetMeth='blocks'
slSiz=6
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

##subjCat cope, tstat fwhm0
trainSetMeth='blocks'
slSiz=6
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm='None'
imDat='tstat' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
