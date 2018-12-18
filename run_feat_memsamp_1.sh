#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampData'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
#codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'


results_dir=''

cat ${results_dir}/subject_list_1  | while read subject
do

epi_file="${results_dir}/${subject}/${subject}_FH.nii.gz"

vols=`fslnvols ${epi_file}`
voxels=`fslstats ${epi_file} -v | awk '{print $1}'`

sed -e s:subject:${subject}:g  \
	-e s:nvols:${vols}:g   \
	-e s:nvox:${voxels}:g   \
	<${results_dir}/glm_FH_sub_subsmem1_170228.fsf >${results_dir}/run_glm_FH_${subject}_subsmem1.fsf

feat ${results_dir}/run_glm_FH_${subject}_subsmem1.fsf

done
