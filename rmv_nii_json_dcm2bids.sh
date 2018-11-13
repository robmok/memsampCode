#!/bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/dicom'
cd ${wd}

while read iSub; do
cd ${wd}/${iSub}
dirs=`ls -d *`
for iDir in ${dirs}; do
rm ${iDir}/*.nii ${iDir}/*json
done # for iDir
done < ${wd}/subNames.txt #while read
