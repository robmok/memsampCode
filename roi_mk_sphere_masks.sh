wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
roiDir=${wd}/rois

size=8 #8, 10

fslmaths ${FSLDIR}/data/standard/avg152T1.nii.gz -mul 0 -add 1 -roi 43 1 85 1 29 1 0 1 ${roiDir}/mPFC_sph${size} -odt float
fslmaths ${roiDir}/mPFC_sph${size} -kernel sphere ${size} -fmean ${roiDir}/mPFC_sph${size} -odt float
fslmaths ${roiDir}/mPFC_sph${size} -bin ${roiDir}/mPFC_sph${size}
