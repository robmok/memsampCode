#! /bin/bash

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'



	# • Left IPS: 5.00003
	# • Right IPS: 6.9999
	# • Left Precentral gyrus:13.99 - for motor?
	# • Right precentral gyrus 13.0002
	# • Left IFG - 11.00
	# • Left IFG - 10.00
	# • Left Dlpfc-8C (MFG, inferior PFC, FEF) - 23.999
	# • Right dlpfc-8C - 21.999
	# • Left dlpfc-9 (area9-46) - 23.000
  #  Right dlpfc-9 - 20.999

fslmaths ${roiDir}/MDROI.nii -thr 5 -uthr 5.1 -bin ${roiDir}/MDroi_ips_lh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 6.9 -uthr 7 -bin ${roiDir}/MDroi_ips_rh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 13.9 -uthr 14 -bin ${roiDir}/MDroi_pcg_lh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 13 -uthr 13.1 -bin ${roiDir}/MDroi_pcg_rh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 11 -uthr 11.1 -bin ${roiDir}/MDroi_ifg_lh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 10 -uthr 10.1 -bin ${roiDir}/MDroi_ifg_rh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 23.9 -uthr 24 -bin ${roiDir}/MDroi_area8c_lh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 21.9 -uthr 22 -bin ${roiDir}/MDroi_area8c_rh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 23 -uthr 23.1 -bin ${roiDir}/MDroi_area9_lh.nii.gz
fslmaths ${roiDir}/MDROI.nii -thr 20.9 -uthr 21 -bin ${roiDir}/MDroi_area9_rh.nii.gz
