#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
bidsDir=${wd}/memsampBids
fsfDir=${wd}/feat_design_files

cd ${wd}

while read subject; do
  bet ${bidsDir}/${subject}/anat/${subject}_T1w.nii ${bidsDir}/${subject}/anat/${subject}_T1w_brain.nii
  #fieldmaps
  bet ${bidsDir}/${subject}/fmap/${subject}_magnitude2.nii.gz ${bidsDir}/${subject}/fmap/${subject}_magnitude2_brain.nii.gz
  fsl_prepare_fieldmap SIEMENS ${bidsDir}/${subject}/fmap/${subject}_phasediff.nii.gz ${bidsDir}/${subject}/fmap/${subject}_magnitude2_brain.nii.gz ${bidsDir}/${subject}/fmap/${subject}_fieldmap.nii.gz  2.46
done < ${fsfDir}/subject_list.txt #while read subject; do
