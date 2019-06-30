#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

# tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
tThresh=1.6938 #  - DF = 33-1, one-tailed, p=0.05

vSmooth=5

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

# motor - sl9, fwhmNone, cope
trainSetMeth='trials'
slSiz=8
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

# motor - sl9, fwhmNone, cope
trainSetMeth='trials'
slSiz=9
normMeth='noNorm'
decodeFeature='motor'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='vox' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5  -x



# # ori - sl9, fwhmNone, cope
# trainSetMeth='trials'
# slSiz=9
# normMeth='noNorm'
# decodeFeature='ori'
# distMeth='svm'
# fwhm='None'
# imDat='cope' # cope or tstat images
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -C ${tThresh}
#
# # ori - sl9, fwhmNone, cope
# trainSetMeth='trials'
# slSiz=9
# normMeth='noNorm'
# decodeFeature='ori'
# distMeth='svm'
# fwhm='None'
# imDat='cope' # cope or tstat images
# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -x
#
# # ori - sl9, fwhmNone, cope
# trainSetMeth='trials'
# slSiz=6
# normMeth='noNorm'
# decodeFeature='ori'
# distMeth='svm'
# fwhm='None'
# imDat='cope' # cope or tstat images
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni_allROIsSL.nii.gz -m ${roiDir}/allROIsSL_final.nii.gz -1 -v 5 -C ${tThresh}
