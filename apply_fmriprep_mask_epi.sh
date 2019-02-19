#! /bin/bash
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
dataDir=${wd}/fmriprep_output/fmriprep

while read subject; do
  mkdir ${dataDir}/${subject}/func/orig_epi
  #MNI space
  for iRun in {1..3}; do
    epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    mask_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz"
    mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
    fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file} #multiply by binary mask (-mas also works)
  done
  #exemplarLoc
  epi_file="${dataDir}/${subject}/func/${subject}_task-exemplarLocaliser_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
  epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-exemplarLocaliser_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
  mask_file="${dataDir}/${subject}/func/${subject}_task-exemplarLocaliser_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz"
  mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
  fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file}
  #motionLoc
  epi_file="${dataDir}/${subject}/func/${subject}_task-motionLocaliser_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
  epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-motionLocaliser_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
  mask_file="${dataDir}/${subject}/func/${subject}_task-motionLocaliser_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz"
  mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
  fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file}

  #T1
  for iRun in {1..3}; do
    epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold.nii.gz"
    epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold.nii.gz"
    mask_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-brain_mask.nii.gz"
    mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
    fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file} #multiply by binary mask (-mas also works)
  done
  #exemplarLoc
  epi_file="${dataDir}/${subject}/func/${subject}_task-exemplarLocaliser_space-T1w_desc-preproc_bold.nii.gz"
  epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-exemplarLocaliser_space-T1w_desc-preproc_bold.nii.gz"
  mask_file="${dataDir}/${subject}/func/${subject}_task-exemplarLocaliser_space-T1w_desc-brain_mask.nii.gz"
  mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
  fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file}
  #motionLoc
  epi_file="${dataDir}/${subject}/func/${subject}_task-motionLocaliser_space-T1w_desc-preproc_bold.nii.gz"
  epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-motionLocaliser_space-T1w_desc-preproc_bold.nii.gz"
  mask_file="${dataDir}/${subject}/func/${subject}_task-motionLocaliser_space-T1w_desc-brain_mask.nii.gz"
  mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
  fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file}

  #4 runs
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
    iRun=4
    #MNI
    epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    mask_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz"
    mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
    fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file} #multiply by binary mask (-mas also works)
    #T1
    epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold.nii.gz"
    epi_file_mv="${dataDir}/${subject}/func/orig_epi/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold.nii.gz"
    mask_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-brain_mask.nii.gz"
    mv ${epi_file} ${dataDir}/${subject}/func/orig_epi
    fslmaths ${epi_file_mv} -mul ${mask_file} ${epi_file} #multiply by binary mask (-mas also works)
  fi
done < ${fsfDir}/subject_list.txt #while read subject; do
