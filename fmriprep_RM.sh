hd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
inDir=${hd}/memsampBids
outDir=${hd}/fmriprep_preproc

fmriprep --no-submm-recon ${inDir} ${outDir} participant
