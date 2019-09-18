#! /bin/bash
# check if this flips anything around - after dcm2bids (in memsampBids) and after fmriprep (in fmriprep_output)


wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files
bidsDir=${wd}/memsampBids
dataDir=${wd}/fmriprep_output/fmriprep

codeDir=${mainDir}/'memsampCode'

cd ${wd}
while read subject; do
  mri="${bidsDir}/${subject}/anat/${subject}_T1w"
  mri_out="${mri}_reorient"
  for iRun in {1..3}; do #only runs 1:3 now
    epi="${bidsDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_bold" # after dcm2bids
    epi_out="${epi}_reorient"
    fslreorient2std ${mri} ${mri_out}
    fslreorient2std ${epi} ${epi_out}

    epi="${dataDir}/${subject}/func/${subject}_task-memsamp_run-0${iRun}_space-T1w_desc-preproc_bold" #after fmriprep
    epi_out="${epi}_reorient"
    fslreorient2std ${epi} ${epi_out}
    done
done < ${fsfDir}/subject_list_full.txt #while read subject; do



#NOTES after manual checks for each subject (maybe a handful needed reorienting?)

# in memsampBids - anat and epis after dcm2bids
# sub-01 - OK both



# after fmriprep - epis





# NEXT: remove the orient files
