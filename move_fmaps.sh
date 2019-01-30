#! /bin/bash

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
bidsDir=${wd}/memsampBids

#mkdir ${wd}/fieldmaps

#move from bids directory to temporary fieldmap directory
for iSub in {1..33}; do
  subnum=`printf "%.2d" ${iSub}` #zero pad subject number
  mkdir ${wd}/fieldmaps/sub-${subnum}
  mv ${bidsDir}/sub-${subnum}/fmap ${wd}/fieldmaps/sub-${subnum}
done

#move from temporary fieldmap directory to bids directory
#for iSub in {1..33}; do
#  subnum=`printf "%.2d" ${iSub}` #zero pad subject number
#  mv ${wd}/fieldmaps/sub-${subnum}/fmap ${bidsDir}/sub-${subnum}
#  #mv ${wd}/fieldmaps/sub-${subnum}/fmap/* ${bidsDir}/sub-${subnum}/fmap #if fmap dir exists
#done
