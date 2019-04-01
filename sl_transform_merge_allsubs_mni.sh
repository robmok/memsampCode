#! /bin/bash
#- concat images into 1 4D im; fslmerge: -t is time dimesion, -a  is auto; both do the same here

## merge images into one 4D image - just run once. M
# Note: fslmerge -t outputImage.nii.gz inputIm.nii.gz

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'

# slSiz=5 #searchlight size
# distMeth='svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
# fwhm=1 # smoothing - set to None if no smoothing



#sl6_dirDecoding_svm_noNorm_blocks_fwhmNone_tstat
#sl6_subjCatDecoding_svm_noNorm_blocks_fwhmNone_cope
#sl6_subjCatDecoding_svm_noNorm_blocks_fwhmNone_tstat

#trials
trainSetMeth='blocks'
slSiz=6
normMeth='noNorm'
decodeFeature='dir'
distMeth='svm'
fwhm='None'
imDat='tstat' # cope or tstat images
fslmerge -t ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_sub-*mni.nii.gz
echo "Merged: sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz"

slSiz=6
normMeth='noNorm'
decodeFeature='subjCat'
distMeth='svm'
fwhm='None'
imDat='cope' # cope or tstat images
fslmerge -t ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_sub-*mni.nii.gz
echo "Merged: sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz"

imDat='tstat' # cope or tstat images
fslmerge -t ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_sub-*mni.nii.gz
echo "Merged: sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz"
