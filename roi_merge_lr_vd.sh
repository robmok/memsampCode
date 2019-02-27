#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
roiDir=${wd}/rois
fsfDir=${wd}/feat_design_files

while read subject; do
  #make bilateral mask (left + right)
  for iRoi in 'V1v' 'V1d'  'V2v' 'V2d'  'V3v'  'V3d'  'hV4' 'V01' 'V02' 'PHC1' 'PHC2' 'MST' 'hMT' 'L02' 'L01' 'V3b' 'V3a' 'IPS0' 'IPS1' 'IPS2' 'IPS3' 'IPS4' 'IPS5' 'SPL1' 'FEF'; do
    fslmaths ${roiDir}/${subject}_${iRoi}_lh.nii.gz -add ${roiDir}/${subject}_${iRoi}_rh.nii.gz ${roiDir}/${subject}_${iRoi}_lrh.nii.gz
  done
  #make ventral-dorsal mask for V1 to V3 (ventral + dorsal)
  for iRoi in 'V1'  'V2' 'V3'; do
    fslmaths ${roiDir}/${subject}_${iRoi}v_lh.nii.gz -add ${roiDir}/${subject}_${iRoi}d_lh.nii.gz ${roiDir}/${subject}_${iRoi}vd_lh.nii.gz #left vd
    fslmaths ${roiDir}/${subject}_${iRoi}v_rh.nii.gz -add ${roiDir}/${subject}_${iRoi}d_rh.nii.gz ${roiDir}/${subject}_${iRoi}vd_rh.nii.gz #right vd
    fslmaths ${roiDir}/${subject}_${iRoi}v_lrh.nii.gz -add ${roiDir}/${subject}_${iRoi}d_lrh.nii.gz ${roiDir}/${subject}_${iRoi}vd_lrh.nii.gz #bilateral vd
  done
done < ${fsfDir}/subject_list_full.txt
