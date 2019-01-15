hd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
inDir=${hd}/memsampBids
outDir=${hd}# /fmriprep_preproc
#hd ${hd} #makes a participant directory in current dir. don't want it in code directory

#fmriprep-docker --fs-license-file ${FS_LICENSE} ${inDir} ${outDir} participant --participant_label 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 --output-space fsaverage template --fs-no-reconall --mem_mb 32000 --nthreads 6

#fmriprep-docker --fs-license-file ${FS_LICENSE} ${inDir} ${outDir} participant --participant_label 01 --output-space T1w template --fs-no-reconall --mem_mb 32000 --nthreads 2

fmriprep-docker --fs-license-file ${FS_LICENSE} ${inDir} ${outDir} participant --participant_label 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 --output-space fsaverage template --fs-no-reconall --mem_mb 32000 --nthreads 7 -w ${hd}/fmriprep_scratch
