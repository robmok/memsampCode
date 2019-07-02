#! /bin/bash

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
codeDir=${mainDir}/'memsampCode'

roiDir=${mainDir}/'Wang_Kastner_ProbAtlas_v4/subj_vol_all'
roiDirOut=${mainDir}/'rois'

# -thr : use following number to threshold current image (zero anything below the number)
# -uthr : use following number to upper-threshold current image (zero anything above the number)

#apply a bit of smoothing then binarize to make some masks continuous / bigger

for iRoi in {1..25}; do
  fslmaths ${roiDir}/maxprob_vol_lh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin -s 0.25 -bin ${roiDirOut}/roi${iRoi}_lh_25.nii.gz
  fslmaths ${roiDir}/maxprob_vol_rh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin -s 0.25 -bin ${roiDirOut}/roi${iRoi}_rh_25.nii.gz
done

#trying no smoothing (smaller ROIs)

#next try 0.5 smoothing (larger ROIs)
for iRoi in {1..25}; do
  fslmaths ${roiDir}/maxprob_vol_lh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin -s 0.5 -bin ${roiDirOut}/roi${iRoi}_lh.nii.gz
  fslmaths ${roiDir}/maxprob_vol_rh.nii.gz -thr ${iRoi} -uthr ${iRoi} -bin -s 0.5 -bin ${roiDirOut}/roi${iRoi}_rh.nii.gz
done


# # new - make MNI version of a set of ROI masks merged for SL analysis
# #need to make masks into the same space so merge first then downsample, then merge
# rm ${roiDirOut}/sl_rois_mni_1.txt
# #note - using MD ips here, not wang/kastner IPS1-5
# for iRoi in {1,2,3,4,5,6,7,12,13,16,17}; do
#   echo -n "${roiDirOut}/roi${iRoi}_lh.nii.gz -add " >> ${roiDirOut}/sl_rois_mni_1.txt #note the -n (for no new line) and space at the end of ""
#   echo -n "${roiDirOut}/roi${iRoi}_rh.nii.gz -add " >> ${roiDirOut}/sl_rois_mni_1.txt
# done
# #last no '-add' - no lh/rh
# iRoi=18
# echo -n "${roiDirOut}/roi${iRoi}_lh.nii.gz -add " >> ${roiDirOut}/sl_rois_mni_1.txt
# echo -n "${roiDirOut}/roi${iRoi}_rh.nii.gz " >> ${roiDirOut}/sl_rois_mni_1.txt
# roiList=`cat ${roiDirOut}/sl_rois_mni_1.txt`
# fslmaths ${roiList} -bin ${roiDirOut}/allROIsSL_1.nii.gz
#
# rm ${roiDirOut}/sl_rois_mni_2.txt
# for iRoi in 'HIPP_HEAD' 'HIPP_BODY'; do
#   echo -n "${roiDirOut}/${iRoi}_lh.nii.gz -add " >> ${roiDirOut}/sl_rois_mni_2.txt
#   echo -n "${roiDirOut}/${iRoi}_rh.nii.gz -add " >> ${roiDirOut}/sl_rois_mni_2.txt
# done
# iRoi='HIPP_TAIL'
# echo -n "${roiDirOut}/${iRoi}_lh.nii.gz -add " >> ${roiDirOut}/sl_rois_mni_2.txt
# echo -n "${roiDirOut}/${iRoi}_rh.nii.gz " >> ${roiDirOut}/sl_rois_mni_2.txt
# roiList=`cat ${roiDirOut}/sl_rois_mni_2.txt`
# fslmaths ${roiList} -bin ${roiDirOut}/allROIsSL_2.nii.gz
#
# #interp to MNI / other space (not sure why MDrois screw up with the fsl function applyxfm or sth) - run python script
# python ${codeDir}/roi_allROIsSL_interp.py
#
# # add together
# fslmaths ${roiDirOut}/allROIsSL_1_interp2sl.nii.gz -add ${roiDirOut}/allROIsSL_2_interp2sl.nii.gz -add ${roiDirOut}/MDroi_all_interp2sl.nii.gz -bin ${roiDirOut}/allROIsSL_final.nii.gz




#motor cortex
fslmaths ${roiDirOut}/harvardoxford-Precentral_Gyrus.nii.gz -mul ${roiDirOut}/harvardoxford-Left_Cortex.nii.gz  -bin ${roiDirOut}/motor_lh.nii.gz
fslmaths ${roiDirOut}/harvardoxford-Precentral_Gyrus.nii.gz -mul ${roiDirOut}/harvardoxford-Right_Cortex.nii.gz  -bin ${roiDirOut}/motor_rh.nii.gz
