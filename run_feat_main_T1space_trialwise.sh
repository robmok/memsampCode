#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
dataDir=${wd}/fmriprep_output/fmriprep

fwhm=0 #0/2
standardScript="memsamp_run-01_trial_fwhm2_T1"

#for feedback decoding
standardScript="memsamp_run-01_trial_fwhm2_T1_feedback"

# single trial in T1 space
# - code for each trial as an EV - looks like 7 trials per run (even run 4)
# - 12 conds * 7 trials = 84 EVs PLUS feedback.
# - all 84 as contrasts, plus 1 for feedback

cd ${wd}
while read subject; do
   for iRun in {1..3}; do
     epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold"
     vols=`fslnvols ${epi_file}`
     voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
     #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
     sed -e s:sub-01:${subject}:g \
       -e s:run-01:run-0${iRun}:g \
       -e s:"fwhm2":"fwhm${fwhm}":g \
       -e s:"set fmri(smooth) 2.0":"set fmri(smooth) ${fwhm}":g \
     	 -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
     	 -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
     feat ${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
   done #for iRun
  #extra runs
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
    iRun=4
    epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold"
    vols=`fslnvols ${epi_file}`
    voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
    #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
    sed -e s:sub-01:${subject}:g \
      -e s:run-01:run-0${iRun}:g \
      -e s:"fwhm2":"fwhm${fwhm}":g \
      -e s:"set fmri(smooth) 2.0":"set fmri(smooth) ${fwhm}":g \
      -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
      -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
      feat ${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
  fi #if ["subject" == "sub-09"]...
done < ${fsfDir}/subject_list_1.txt #while read subject; do

#lock2resp - added 190801
# -e s:"cue_trial":"cue_lock2resp_trial":g \ #event file name
# -e s:"trial_T1_fwhm":"trial_T1_lock2resp_fwhm":g \ # output directory name

# cd ${wd}
# while read subject; do
#    for iRun in {1..3}; do
#      epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold"
#      vols=`fslnvols ${epi_file}`
#      voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
#      #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
#      sed -e s:sub-01:${subject}:g \
#        -e s:run-01:run-0${iRun}:g \
#        -e s:"fwhm2":"fwhm${fwhm}":g \
#        -e s:"set fmri(smooth) 2.0":"set fmri(smooth) ${fwhm}":g \
#      	 -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
#      	 -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
#        -e s:"cue_trial":"cue_lock2resp_trial":g \
#        -e s:"trial_T1_fwhm":"trial_T1_lock2resp_fwhm":g \
#        <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
#      feat ${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
#    done #for iRun
#   #extra runs
#   if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
#     iRun=4
#     epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold"
#     vols=`fslnvols ${epi_file}`
#     voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
#     #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
#     sed -e s:sub-01:${subject}:g \
#       -e s:run-01:run-0${iRun}:g \
#       -e s:"fwhm2":"fwhm${fwhm}":g \
#       -e s:"set fmri(smooth) 2.0":"set fmri(smooth) ${fwhm}":g \
#       -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
#       -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
#       -e s:"cue_trial":"cue_lock2resp_trial":g \
#       -e s:"trial_T1_fwhm":"trial_T1_lock2resp_fwhm":g \
#       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
#       feat ${fsfDir}/run_memsamp_run-0${iRun}_trial_T1_fwhm${fwhm}_${subject}.fsf
#   fi #if ["subject" == "sub-09"]...
# done < ${fsfDir}/subject_list_4.txt #while read subject; do
