#! /bin/bash
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files

#*********************************************
#RUN fmriprep2fsl_fixfiles.sh for group level analysis
#*********************************************

# fwhm=6
# while read subject; do
#   if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
#     standardScript="memsamp_block_2ndlvl_4runs_fwhm${fwhm}"
#     #standardScript="memsamp_block_2ndlvl_4runs_fwhm${fwhm}_noTD"
#     #standardScript="memsamp_fsl_block_2ndlvl_4runs_fwhm${fwhm}"
#     sed -e s:sub-09:${subject}:g \
#       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm${fwhm}_${subject}.fsf
#   else
#     standardScript="memsamp_block_2ndlvl_fwhm${fwhm}"
#     #standardScript="memsamp_block_2ndlvl_fwhm${fwhm}_noTD"
#     #standardScript="memsamp_fsl_block_2ndlvl_fwhm${fwhm}"
#     sed -e s:sub-01:${subject}:g \
#       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm${fwhm}_${subject}.fsf
#   fi
#   feat ${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm${fwhm}_${subject}.fsf
# done < ${fsfDir}/subject_list_full.txt #while read subject; do

#lock2resp
fwhm=6
while read subject; do
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
    standardScript="memsamp_block_2ndlvl_4runs_fwhm${fwhm}"
    sed -e s:sub-09:${subject}:g \
        -e s:"block_fwhm":"block_lock2resp_fwhm":g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm${fwhm}_${subject}.fsf
  else
    standardScript="memsamp_block_2ndlvl_fwhm${fwhm}"
    sed -e s:sub-01:${subject}:g \
        -e s:"block_fwhm":"block_lock2resp_fwhm":g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm${fwhm}_${subject}.fsf
  fi
  feat ${fsfDir}/run_memsamp_block_2ndlvl_block_fwhm${fwhm}_${subject}.fsf
done < ${fsfDir}/subject_list_full.txt #while read subject; do
