#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
dataDir=${wd}/fmriprep_output/fmriprep

#run feat on images registered to MNI space, use more smoothing (e.g. fwhm=6)

fwhm=8 #6/8
standardScript="memsamp_run-01_block_fwhm6"

# focus on feedback faces vs buildings
# standardScript="memsamp_run-01_block_feedback_fwhm6"

cd ${wd}
while read subject; do
   for iRun in {1..3}; do
     epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
     vols=`fslnvols ${epi_file}`
     voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
     #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
     sed -e s:sub-01:${subject}:g \
         -e s:run-01:run-0${iRun}:g \
         -e s:"set fmri(smooth) 6.0":"set fmri(smooth) ${fwhm}":g \
         -e s:"fwhm6":"fwhm${fwhm}":g \
       	-e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
       	-e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
     feat ${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
   done #for iRun
  #extra runs
  if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
    iRun=4
    epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    vols=`fslnvols ${epi_file}`
    voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
    #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
    sed -e s:sub-01:${subject}:g \
      -e s:run-01:run-0${iRun}:g \
      -e s:"set fmri(smooth) 6.0":"set fmri(smooth) ${fwhm}":g \
      -e s:"fwhm6":"fwhm${fwhm}":g \
      -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
      -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
      feat ${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
  fi #if ["subject" == "sub-09"]...
done < ${fsfDir}/subject_list_full.txt #while read subject; do

#lock2resp - added 190801
# -e s:"cue_block":"cue_lock2resp_block":g \ #event file name
# -e s:"block_fwhm":"block_lock2resp_fwhm":g \ # output directory name

# standardScript="memsamp_run-01_block_lock2resp_fwhm6" #now contrasts only include response and feedback
#
# cd ${wd}
# while read subject; do
#    for iRun in {1..3}; do
#      epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
#      vols=`fslnvols ${epi_file}`
#      voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
#      #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
#      sed -e s:sub-01:${subject}:g \
#          -e s:run-01:run-0${iRun}:g \
#          -e s:"set fmri(smooth) 6.0":"set fmri(smooth) ${fwhm}":g \
#          -e s:"fwhm6":"fwhm${fwhm}":g \
#     	   -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
# 	       -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
#          -e s:"cue_block":"cue_lock2resp_block":g \
#          -e s:"block_fwhm":"block_lock2resp_fwhm":g \
#        <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
#      feat ${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
#    done #for iRun
#   #extra runs
#   if [ "$subject" = "sub-09" ] || [ "$subject" = "sub-12" ] || [ "$subject" = "sub-16" ] || [ "$subject" = "sub-26" ]; then
#     iRun=4
#     epi_file="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
#     vols=`fslnvols ${epi_file}`
#     voxels=`fslstats ${epi_file} -v | awk '{print $1}'`
#     #substitute sub-01 to curr sub, #substitute sub-01 volumes to curr sub - atm same since in standard space
#     sed -e s:sub-01:${subject}:g \
#         -e s:run-01:run-0${iRun}:g \
#         -e s:"set fmri(smooth) 6.0":"set fmri(smooth) ${fwhm}":g \
#         -e s:"fwhm6":"fwhm${fwhm}":g \
#         -e s:"set fmri(npts) 262":"set fmri(npts) ${vols}":g \
#         -e s:"set fmri(totalVoxels) 85235150":"set fmri(totalVoxels) ${voxels}":g \
#         -e s:"cue_block":"cue_lock2resp_block":g \
#         -e s:"block_fwhm":"block_lock2resp_fwhm":g \
#       <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
#       feat ${fsfDir}/run_memsamp_run-0${iRun}_block_fwhm${fwhm}_${subject}.fsf
#   fi #if ["subject" == "sub-09"]...
# done < ${fsfDir}/subject_list_full.txt #while read subject; do
