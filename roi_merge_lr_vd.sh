#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
roiDir=${wd}/rois
fsfDir=${wd}/feat_design_files

# note: added -bin to each now after smoothing (some overlap means values became >1)

echo "Running roi_merge_lr_vd.sh"
while read subject; do
  echo "Running ${subject}"
  #make bilateral mask (left + right)
  for iRoi in 'V1v' 'V1d'  'V2v' 'V2d'  'V3v'  'V3d'  'hV4' 'V01' 'V02' 'PHC1' 'PHC2' 'MST' 'hMT' 'L02' 'L01' 'V3b' 'V3a' 'IPS0' 'IPS1' 'IPS2' 'IPS3' 'IPS4' 'IPS5' 'SPL1' 'FEF'; do
    fslmaths ${roiDir}/${subject}_${iRoi}_lh.nii.gz -add ${roiDir}/${subject}_${iRoi}_rh.nii.gz -bin ${roiDir}/${subject}_${iRoi}_lrh.nii.gz
  done
  #make ventral-dorsal mask for V1 to V3 (ventral + dorsal)
  for iRoi in 'V1'  'V2' 'V3'; do
    fslmaths ${roiDir}/${subject}_${iRoi}v_lh.nii.gz -add ${roiDir}/${subject}_${iRoi}d_lh.nii.gz -bin ${roiDir}/${subject}_${iRoi}vd_lh.nii.gz #left vd
    fslmaths ${roiDir}/${subject}_${iRoi}v_rh.nii.gz -add ${roiDir}/${subject}_${iRoi}d_rh.nii.gz -bin ${roiDir}/${subject}_${iRoi}vd_rh.nii.gz #right vd
    fslmaths ${roiDir}/${subject}_${iRoi}v_lrh.nii.gz -add ${roiDir}/${subject}_${iRoi}d_lrh.nii.gz -bin ${roiDir}/${subject}_${iRoi}vd_lrh.nii.gz #bilateral vd
  done
  #make visual and IPS merged rois
  #list the files to merge (txt is replaced over subs, not saved)
  rm ${roiDir}/visual_rois_lh.txt ${roiDir}/visual_rois_rh.txt ${roiDir}/ips_rois_lh.txt ${roiDir}/ips_rois_rh.txt
  #for iRoi in 'V1v' 'V1d'  'V2v' 'V2d'  'V3v'  'V3d'  'hV4' 'V01' 'V02' 'PHC1' 'PHC2' 'MST' 'hMT' 'L02' 'L01' 'V3b'; do
  for iRoi in 'V1v' 'V1d'  'V2v' 'V2d'  'V3v'  'V3d'  'hV4' 'MST' 'hMT' 'V3b'; do #without ventral occipital rois
    echo -n "${roiDir}/${subject}_${iRoi}_lh.nii.gz -add " >> ${roiDir}/visual_rois_lh.txt #note the -n (for no new line) and space at the end of ""
    echo -n "${roiDir}/${subject}_${iRoi}_rh.nii.gz -add " >> ${roiDir}/visual_rois_rh.txt
  done
  iRoi='V3a' #last no '-add'
  echo -n "${roiDir}/${subject}_${iRoi}_lh.nii.gz " >> ${roiDir}/visual_rois_lh.txt
  echo -n "${roiDir}/${subject}_${iRoi}_rh.nii.gz " >> ${roiDir}/visual_rois_rh.txt
  for iRoi in 'IPS0' 'IPS1' 'IPS2' 'IPS3' 'IPS4' 'IPS5'; do
    echo -n "${roiDir}/${subject}_${iRoi}_lh.nii.gz -add " >> ${roiDir}/ips_rois_lh.txt
    echo -n "${roiDir}/${subject}_${iRoi}_rh.nii.gz -add " >> ${roiDir}/ips_rois_rh.txt
  done
  iRoi='SPL1' #last no '-add'
  echo -n "${roiDir}/${subject}_${iRoi}_lh.nii.gz " >> ${roiDir}/ips_rois_lh.txt
  echo -n "${roiDir}/${subject}_${iRoi}_rh.nii.gz " >> ${roiDir}/ips_rois_rh.txt

  #run fslmaths - L/R/bilateral
  roiList=`cat ${roiDir}/visual_rois_lh.txt`
  fslmaths ${roiList} -bin ${roiDir}/${subject}_visRois_lh.nii.gz
  roiList=`cat ${roiDir}/visual_rois_rh.txt`
  fslmaths ${roiList} ${roiDir}/${subject}_visRois_rh.nii.gz
  fslmaths ${roiDir}/${subject}_visRois_lh.nii.gz -add ${roiDir}/${subject}_visRois_rh.nii.gz -bin ${roiDir}/${subject}_visRois_lrh.nii.gz
  roiList=`cat ${roiDir}/ips_rois_lh.txt`
  fslmaths ${roiList} -bin ${roiDir}/${subject}_ipsRois_lh.nii.gz
  roiList=`cat ${roiDir}/ips_rois_rh.txt`
  fslmaths ${roiList} -bin ${roiDir}/${subject}_ipsRois_rh.nii.gz
  fslmaths ${roiDir}/${subject}_ipsRois_lh.nii.gz -add ${roiDir}/${subject}_ipsRois_rh.nii.gz -bin ${roiDir}/${subject}_ipsRois_lrh.nii.gz

  #merge vis and ips rois
  fslmaths ${roiDir}/${subject}_ipsRois_lh.nii.gz -add ${roiDir}/${subject}_visRois_lh.nii.gz -bin ${roiDir}/${subject}_visRois_ipsRois_lh.nii.gz
  fslmaths ${roiDir}/${subject}_ipsRois_rh.nii.gz -add ${roiDir}/${subject}_visRois_rh.nii.gz -bin ${roiDir}/${subject}_visRois_ipsRois_rh.nii.gz
  fslmaths ${roiDir}/${subject}_ipsRois_lrh.nii.gz -add ${roiDir}/${subject}_visRois_lrh.nii.gz -bin ${roiDir}/${subject}_visRois_ipsRois_lrh.nii.gz

done < ${fsfDir}/subject_list_full.txt
