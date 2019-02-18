#! /bin/bash
# with FSL preprocessing (not fmriprep)

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'

fwhm=6 #6/8
standardScript="memsamp_fsl_run-01_block_fwhm6"

cd ${wd}
while read subject; do
   for iRun in {1..3}; do
     epi_file="${bidsDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_bold"
     vols=`fslnvols ${epi_file}`
     voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
     #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
     sed -e s:sub-01:${subject}:g \
       -e s:run-01:run-0${iRun}:g \
       -e s:"fwhm6":"fwhm${fwhm}":g \
       -e s:"set fmri(smooth) 6.0":"set fmri(smooth) ${fwhm}":g \
     	 -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
     	 -e s:"set fmri(totalVoxels) 42926080":"set fmri(totalVoxels) ${voxels}":g \
       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_fsl_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
     feat ${fsfDir}/run_memsamp_fsl_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
   done #for iRun
  #extra runs
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
    iRun=4
    epi_file="${bidsDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_bold"
    vols=`fslnvols ${epi_file}`
    voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
    sed -e s:sub-01:${subject}:g \
      -e s:run-01:run-0${iRun}:g \
      -e s:"fwhm6":"fwhm${fwhm}":g \
      -e s:"set fmri(smooth) 6.0":"set fmri(smooth) ${fwhm}":g \
      -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
      -e s:"set fmri(totalVoxels) 42926080":"set fmri(totalVoxels) ${voxels}":g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_fsl_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
      feat ${fsfDir}/run_memsamp_fsl_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
  fi #if ["subject" == "sub-09"]...
done < ${fsfDir}/subject_list_full.txt #while read subject; do
