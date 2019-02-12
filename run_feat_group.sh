#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
dataDir=${wd}/fmriprep_output/fmriprep

fwhm=8 #6/8
standardScript="memsamp_run-01_block_fwhm${fwhm}"
standardScript="memsamp_run-01_block_fwhm${fwhm}_noTD"

#no fieldmaps
#dataDir=${wd}/fmriprep_output_nofmaps/fmriprep
#standardScript='memsamp_run-01_block_fwhm6_nofmaps'

cd ${wd}
while read subject; do
   for iRun in {1..3}; do
     epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-01_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
     vols=`fslnvols ${epi_file}`
     voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
     #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
     sed -e s:sub-01:${subject}:g \
       -e s:run-01:run-0${iRun}:g \
     	-e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
     	-e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf

     feat ${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
   done #for iRun
  #extra runs
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
    iRun=4
    epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-01_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    vols=`fslnvols ${epi_file}`
    voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
    #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
    sed -e s:sub-01:${subject}:g \
      -e s:run-01:run-0${iRun}:g \
      -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
      -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf

      feat ${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
  fi #if ["subject" == "sub-09"]...
done < ${fsfDir}/subject_list.txt #while read subject; do
