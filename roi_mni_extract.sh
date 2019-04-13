#! /bin/bash

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/Wang_Kastner_ProbAtlas_v4/subj_vol_all'
roiDirOut='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'

# -thr : use following number to threshold current image (zero anything below the number)
# -uthr : use following number to upper-threshold current image (zero anything above the number)

#apply a bit of smoothing then binarize to make some masks continuous / bigger

for iRoi in {1..25}; do
  fslmaths ${roiDir}/maxprob_vol_lh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin -s 0.25 -bin ${roiDirOut}/roi${iRoi}_lh.nii.gz
  fslmaths ${roiDir}/maxprob_vol_rh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin -s 0.25 -bin ${roiDirOut}/roi${iRoi}_rh.nii.gz
done



# rm ${roiDir}/sl_rois_mni.txt
# #note - used MD ips here, not wang/kastner
# for iRoi in 'V1v' 'V1d'  'V2v' 'V2d'  'V3v'  'V3d'  'hV4' 'MST' 'hMT' 'V3b' 'V3a' 'IPS0' 'HIPP_HEAD_BODY_TAIL'; do
#   echo -n "${roiDir}/${subject}_${iRoi}_lh.nii.gz -add " >> ${roiDir}/sl_rois_mni.txt #note the -n (for no new line) and space at the end of ""
#   echo -n "${roiDir}/${subject}_${iRoi}_rh.nii.gz -add " >> ${roiDir}/sl_rois_mni.txt
# done
# iRoi='MDroi_all' #last no '-add' - no lh/rh
# echo -n "${roiDir}/${subject}_${iRoi}.nii.gz " >> ${roiDir}/sl_rois_mni.txt
# roiList=`cat ${roiDir}/sl_rois_mni.txt`
# fslmaths ${roiList} -bin ${roiDir}/allROIsSL.nii.gz
