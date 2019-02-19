#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
dataDir=${wd}/fmriprep_output/fmriprep

fwhm=5
standardScript="memsamp_exemplarLocaliser_T1_fwhm5"
#standardScript="memsamp_exemplarLocaliser_T1_fwhm5_brainmask" #very similar if not same

cd ${wd}
while read subject; do
  epi_file="${dataDir}/${subject}/func/${subject}_task-exemplarLocaliser_space-T1w_desc-preproc_bold.nii.gz"
  vols=`fslnvols ${epi_file}`
  voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
  #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
  sed -e s:sub-01:${subject}:g \
    -e s:"set fmri(smooth) 5.0":"set fmri(smooth) ${fwhm}":g \
  	-e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
  	-e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
    <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_exemplarLocaliser_T1_fwhm${fwhm}_${subject}.fsf
  feat ${fsfDir}/run_memsamp_exemplarLocaliser_T1_fwhm${fwhm}_${subject}.fsf
done < ${fsfDir}/subject_list.txt
