#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

# tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
tThresh=1.6938 #  - DF = 33-1, one-tailed, p=0.05

vSmooth=5

# roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'


# subjCat-orth - sl9 fwhm3, cope
trainSetMeth='trials'
slSiz=9
normMeth='noNorm'
decodeFeature='subjCat-orth'
distMeth='svm'
fwhm=3
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

#tfce
# subjCat - sl9 fwhm3, cope
trainSetMeth='trials'
slSiz=9
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm=3
imDat='cope' # cope or tstat images
threshMeth='tfce' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -T

# subjCat-orth - sl9 fwhm3, cope
trainSetMeth='trials'
slSiz=9
normMeth='noNorm'
decodeFeature='subjCat-orth'
distMeth='svm'
fwhm=3
imDat='cope' # cope or tstat images
threshMeth='tfce' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -T










#
# # subjCat - sl12 fwhm3, tstat
# trainSetMeth='trials'
# slSiz=12
# normMeth='noNorm'
# decodeFeature='subjCat'
# distMeth='svm'
# fwhm=3
# imDat='tstat' # cope or tstat images
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
#
# # subjCat-orth - sl12 fwhm3, tstat
# trainSetMeth='trials'
# slSiz=12
# normMeth='noNorm'
# decodeFeature='subjCat-orth'
# distMeth='svm'
# fwhm=3
# imDat='tstat' # cope or tstat images
# threshMeth='cMass' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
