#! /bin/bash
#- run randomise

slDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_searchlight'
#love01
# slDir='/home/robmok/Documents/memsamp_fMRI/mvpa_searchlight'

tThresh=2.4486 #  - DF = 33-1, one-tailed, p=0.010002
vSmooth=5

#sl6_dirDecoding_crossNobis_noNorm_trials_fwhmNone_cope
trainSetMeth='trials'
slSiz=6
normMeth='noNorm'
decodeFeature='dir'
distMeth='crossNobis'
fwhm='None'
imDat='cope' # cope or tstat images
threshMeth='cMass'
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
threshMeth='vox' #vox, tfce, cSize, cMass
randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
-o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -x



#trainSetMeth='trials'
#slSiz=5
#normMeth='niNormalised'
#decodeFeature='ori'
#distMeth='svm'
#fwhm=1
#imDat='tstat'
#threshMeth='vox' #vox, tfce, cSize, cMass


# slSiz=8
# normMeth='noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
# decodeFeature='12-way'
# distMeth='svm'
# fwhm='None'
#
# imDat='tstat'
# threshMeth='vox' #vox, tfce, cSize, cMass
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -x
# threshMeth='cMass'
# randomise -i ${slDir}/sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_allsubs_mni.nii.gz \
# -o ${slDir}/randomise_${threshMeth}_sl${slSiz}_${decodeFeature}Decoding_${distMeth}_${normMeth}_${trainSetMeth}_fwhm${fwhm}_${imDat}_vs${vSmooth}_allsubs_mni.nii.gz -1 -v 5 -C ${tThresh}
