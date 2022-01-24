#! /bin/bash

# At the very end, I removed some of the files - I think mainly from when I tried some FSL GLMs

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

mv ${wd}/memsampBids/*hdr* ${wd}/not-bids-compliant-files

for iSub in {1..33}; do
  sub=`printf "sub-%.2d" ${iSub}`

  mv ${wd}/memsampBids/${sub}/anat/*_brain.nii.gz ${wd}/not-bids-compliant-files
  mv ${wd}/memsampBids/${sub}/anat/*reorient.nii.gz ${wd}/not-bids-compliant-files

  mv ${wd}/memsampBids/${sub}/fmap/*_brain.nii.gz ${wd}/not-bids-compliant-files
  mv ${wd}/memsampBids/${sub}/fmap/*_fieldmap.nii.gz ${wd}/not-bids-compliant-files

  mv ${wd}/memsampBids/${sub}/func/*reorient.nii.gz ${wd}/not-bids-compliant-files

done
