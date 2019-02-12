
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files

while read subject; do
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
    standardScript='memsamp_block_2ndlvl_4runs' #4 runs
    #standardScript='memsamp_block_2ndlvl_4runs_nofmaps' #4 runs
    sed -e s:sub-09:${subject}:g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm6_${subject}.fsf
  else
    standardScript='memsamp_block_2ndlvl' #3 runs
    #standardScript='memsamp_block_2ndlvl_nofmaps' #3 runs
    sed -e s:sub-01:${subject}:g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm6_${subject}.fsf
  fi
  feat ${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm6_${subject}.fsf
done < ${fsfDir}/subject_list.txt #while read subject; do
