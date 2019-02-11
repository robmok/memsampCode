#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
featDir=${wd}/memsampFeat
fsfDir=${wd}/feat_design_files

cd ${wd}
while read subject; do
  for iRun in {1..3}; do
    # 1.replace transformation mat to identity matrix
    rm ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/reg/*.mat
    scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/reg/example_func2standard.mat
    rm ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/reg/*.mat
    scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/reg/example_func2standard.mat
    #2.replace mean_func.nii.gz reg/standard.nii.gz
    scp ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/mean_func.nii.gz ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/reg/standard.nii.gz
    scp ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/mean_func.nii.gz ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/reg/standard.nii.gz
  done #for iRun
  #extra runs
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
      iRun=4
      # 1.replace transformation mat to identity matrix
      rm ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/reg/*.mat
      scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/reg/example_func2standard.mat
      rm ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/reg/*.mat
      scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/reg/example_func2standard.mat
      #2.replace mean_func.nii.gz reg/standard.nii.gz
      scp ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/mean_func.nii.gz ${featDir}/${subject}_run-0${iRun}_block_fwhm6.feat/reg/standard.nii.gz
      scp ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/mean_func.nii.gz ${featDir}/${subject}_run-0${iRun}_block_fwhm6_nofmaps.feat/reg/standard.nii.gz
  fi #if ["subject" == "sub-09"]...
  # 1.replace transformation mat to identity matrix
  #localisers
  rm ${featDir}/${subject}_exemplarLocaliser_fwhm6.feat/reg/*.mat
  scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_exemplarLocaliser_fwhm6.feat/reg/example_func2standard.mat
  rm ${featDir}/${subject}_motionLocaliser_fwhm6.feat/reg/*.mat
  scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_motionLocaliser_fwhm6.feat/reg/example_func2standard.mat
  #no fieldmaps
  rm ${featDir}/${subject}_exemplarLocaliser_fwhm6_nofmaps.feat/reg/*.mat
  scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_exemplarLocaliser_fwhm6_nofmaps.feat/reg/example_func2standard.mat
  rm ${featDir}/${subject}_motionLocaliser_fwhm6_nofmaps.feat/reg/*.mat
  scp ${FSLDIR}/etc/flirtsch/ident.mat ${featDir}/${subject}_motionLocaliser_fwhm6_nofmaps.feat/reg/example_func2standard.mat

  #2.replace mean_func.nii.gz reg/standard.nii.gz
  scp ${featDir}/${subject}_exemplarLocaliser_fwhm6.feat/mean_func.nii.gz ${featDir}/${subject}_exemplarLocaliser_fwhm6.feat/reg/standard.nii.gz
  scp ${featDir}/${subject}_exemplarLocaliser_fwhm6_nofmaps.feat/mean_func.nii.gz ${featDir}/${subject}_exemplarLocaliser_fwhm6_nofmaps.feat/reg/standard.nii.gz
  scp ${featDir}/${subject}_motionLocaliser_fwhm6.feat/mean_func.nii.gz ${featDir}/${subject}_motionLocaliser_fwhm6.feat/reg/standard.nii.gz
  scp ${featDir}/${subject}_motionLocaliser_fwhm6_nofmaps.feat/mean_func.nii.gz ${featDir}/${subject}_motionLocaliser_fwhm6_nofmaps.feat/reg/standard.nii.gz

done < ${fsfDir}/subject_list.txt #while read subject; do
