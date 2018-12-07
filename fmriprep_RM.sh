hd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
inDir=${hd}/memsampBids
outDir=${hd}/fmriprep_preproc

fmriprep-docker --fs-license-file ${FS_LICENSE} ${inDir} ${outDir} participant --participant_label 01 --output-space fsaverage --fs-no-reconall --mem_mb 32000 --nthreads 2

fmriprep-docker --fs-license-file ${FS_LICENSE} ${inDir} ${outDir} participant --participant_label 01 --output-space T1w --fs-no-reconall --mem_mb 32000 --nthreads 2
