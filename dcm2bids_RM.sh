#!/bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
dicomDir=${wd}/dicom
outDir=${wd}/memsampData

cd ${dicomDir}

#get subject IDs to run
if ! [ -f subNames.txt ]; then
  s=`ls -d *`
  echo ${s} >> subNames.txt
fi

#make directory where the .nii files will go
if ! [ -d ${outDir} ]; then
  cd ${outDir}
  while read iSub; do
    mkdir ${outDir}/${iSub}
    mkdir ${outDir}/${iSub}/anat
    mkdir ${outDir}/${iSub}/func
  done < ${dicomDir}/subNames.txt #while read
fi

#run dcm2bids
while read iSub; do
  cd ${dicomDir}/${iSub}
  dirs=`ls -d *`
  for iDir in ${dirs}; do
    mkdir ${outDir}/${iSub}/${iDir}
    dcm2niix -o ${outDir}/${iSub}/${iDir} -f %p -b y -ba n ${dicomDir}/${iSub}/${iDir}
    #scp ${dicomDir}/${iSub}/${iDir}/*tsv ${outDir}/${iSub}/${iDir}
    #echo ‘dcm2niix -o ${outDir}/${iSub}/${iDir} -f %p -b y -ba n ${dicomDir}/${iSub}/${iDir}’
  done # for iDir
done < ${dicomDir}/subNames.txt #while read
