#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
dataDir=${wd}/fmriprep_output/fmriprep
#codeDir=${wd}/memsampCode

fwhm=8 #6/8
standardScript="memsamp_motionLocaliser_fwhm${fwhm}"
standardScript="memsamp_motionLocaliser_fwhm${fwhm}_noTD"

#no fieldmaps
#dataDir=${wd}/fmriprep_output_nofmaps/fmriprep
#standardScript='memsamp_motionLocaliser_fwhm${fwhm}_nofmaps'

cd ${wd}
while read subject; do
  epi_file="${dataDir}/${subject}/func/${subject}_task-motionLocaliser_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
  vols=`fslnvols ${epi_file}`
  voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
  #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
  sed -e s:sub-01:${subject}:g \
  	-e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
  	-e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
    <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_${standardScript}_${subject}.fsf

  feat ${fsfDir}/run_${standardScript}_${subject}.fsf
done < ${fsfDir}/subject_list.txt
