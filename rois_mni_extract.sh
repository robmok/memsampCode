#! /bin/bash

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/Wang_Kastner_ProbAtlas_v4/subj_vol_all'
roiDirOut='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

# -thr : use following number to threshold current image (zero anything below the number)
# -uthr : use following number to upper-threshold current image (zero anything above the number)

for iRoi in {1..25}; do
  fslmaths ${roiDir}/maxprob_vol_lh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin ${roiDirOut}/roi${iRoi}_lh.nii.gz
  fslmaths ${roiDir}/maxprob_vol_rh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin ${roiDirOut}/roi${iRoi}_rh.nii.gz
done
