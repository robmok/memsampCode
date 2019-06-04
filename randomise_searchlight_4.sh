#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
vSmooth=5

# roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

# sl12_subjCat-orthDecoding_svm_noNorm_trials_fwhm3_cope_sub-33_mni.nii.gz
# sl12_subjCat-orthDecoding_svm_noNorm_trials_fwhm3_tstat_sub-33_mni.nii.gz
# sl12_subjCatDecoding_svm_noNorm_trials_fwhm3_cope_sub-33_mni.nii.gz
# sl12_subjCatDecoding_svm_noNorm_trials_fwhm3_tstat_sub-33_mni.nii.gz

# subjCat - sl12 fwhm3, cope
trainSetMeth='trials'
slSiz=12
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm=3
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

# subjCat-orth - sl12 fwhm3, cope
trainSetMeth='trials'
slSiz=12
normMeth='noNorm'
decodeFeature='subjCat-orth'
distMeth='svm'
fwhm=3
imDat='cope' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}


# subjCat - sl12 fwhm3, tstat
trainSetMeth='trials'
slSiz=12
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm=3
imDat='tstat' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}

# subjCat-orth - sl12 fwhm3, tstat
trainSetMeth='trials'
slSiz=12
normMeth='noNorm'
decodeFeature='subjCat-orth'
distMeth='svm'
fwhm=3
imDat='tstat' # cope or tstat images
threshMeth='cMass' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
