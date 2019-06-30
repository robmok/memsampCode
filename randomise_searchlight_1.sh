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
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5  -x

# #with mask:
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -C ${tThresh}
#
# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -x

# tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
tThresh=1.6938 #  - DF = 33-1, one-tailed, p=0.05 - #new 190619 - only re-doing copes for now; old ones in directory: old_randomises_p001
vSmooth=5

#sl6/9 - allROIs subjCat, subjCat-orth, ori, 12-way

# motor - sl6, fwhmNone, cope
trainSetMeth='trials'
slSiz=6
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

# motor - sl6, fwhmNone, cope
trainSetMeth='trials'
slSiz=6
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='vox' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5  -x

# # subjCat - sl6, fwhmNone, cope
# trainSetMeth='trials'
# slSiz=6
# normMeth='noNorm'
# decodeFeature='subjCat'
# distMeth='svm'
# fwhm='None'
# imDat='cope' # cope or tstat images
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -C ${tThresh}
#
# # subjCat - sl6, fwhmNone, cope
# trainSetMeth='trials'
# slSiz=6
# normMeth='noNorm'
# decodeFeature='subjCat'
# distMeth='svm'
# fwhm='None'
# imDat='cope' # cope or tstat images
# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -x

# # subjCat-orth - sl6, fwhmNone, cope
# trainSetMeth='trials'
# slSiz=6
# normMeth='noNorm'
# decodeFeature='subjCat-orth'
# distMeth='svm'
# fwhm='None'
# imDat='cope' # cope or tstat images
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -C ${tThresh}
#
# trainSetMeth='trials'
# slSiz=6
# normMeth='noNorm'
# decodeFeature='subjCat-orth'
# distMeth='svm'
# fwhm='None'
# imDat='cope' # cope or tstat images
# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -x
