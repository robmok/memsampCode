#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'

fwhm=6 #6/8
standardScript="memsamp_fsl_motionLocaliser_fwhm6"

cd ${wd}
while read subject; do
  epi_file="${bidsDir}/${subject}/func/${subject}_task-motionLocaliser_bold.nii.gz"
  vols=`fslnvols ${epi_file}`
  voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
  #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
  sed -e s:sub-01:${subject}:g \
    -e s:"fwhm6":"fwhm${fwhm}":g \
    -e s:"set fmri(smooth) 6.0":"set fmri(smooth) ${fwhm}":g \
  	-e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
  	-e s:"set fmri(totalVoxels) 42926080":"set fmri(totalVoxels) ${voxels}":g \
    <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_fsl_motionLocaliser_fwhm${fwhm}_${subject}.fsf
  feat ${fsfDir}/run_memsamp_fsl_motionLocaliser_fwhm${fwhm}_${subject}.fsf
done < ${fsfDir}/subject_list_full.txt
