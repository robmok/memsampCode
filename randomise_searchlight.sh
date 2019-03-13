#! /bin/bash
#- concat images into 1 4D im; fslmerge: -t is time dimesion, -a  is auto; both do the same here
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'

tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
slSiz=5 #searchlight size
distMeth='svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
fwhm=1 # smoothing - set to None if no smoothing

## merge images into one 4D image - just run once. M
# Note: fslmerge -t outputImage.nii.gz inputIm.nii.gz

# imDat='cope' # cope or tstat images
# normMeth='niNormalised' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
# fslmerge -t ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_sub-*mni.nii.gz
#
# imDat='tstat' # cope or tstat images
# normMeth='niNormalised' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
# fslmerge -t ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_sub-*mni.nii.gz
#
# imDat='cope' # cope or tstat images
# normMeth='noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
# fslmerge -t ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_sub-*mni.nii.gz
#
# imDat='tstat' # cope or tstat images
# normMeth='noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
# fslmerge -t ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_sub-*mni.nii.gz

# randomise -x: voxelwise, -c: cluster size, -C: cluster mass, -T: tfce
#one sample t-test, no need design matrix


# trainSetMeth='trials'
# imDat='cope'
# normMeth='niNormalised'

# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -x
# threshMeth='tfce'
# randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -T
# threshMeth='cSize'
# randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -c ${tThresh}
# threshMeth='cMass'
# randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -C ${tThresh}

trainSetMeth='trials'
imDat='cope'
normMeth='noNorm'

threshMeth='vox' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -x
threshMeth='tfce'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -T
threshMeth='cSize'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -c ${tThresh}
threshMeth='cMass'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -C ${tThresh}

trainSetMeth='trials'
imDat='tstat'
normMeth='niNormalised'

threshMeth='vox' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -x
threshMeth='tfce'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -T
threshMeth='cSize'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -c ${tThresh}
threshMeth='cMass'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -C ${tThresh}

trainSetMeth='trials'
imDat='tstat'
normMeth='noNorm'

threshMeth='vox' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -x
threshMeth='tfce'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -T
threshMeth='cSize'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -c ${tThresh}
threshMeth='cMass'
randomise -i ${slDir}/sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_dirDecoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz -1 -C ${tThresh}
