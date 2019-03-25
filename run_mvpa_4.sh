#! /bin/bash
# Rois

# mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#LOVE01

#SVMs no smooth

#mainDir='/home/robmok/Documents/memsamp_fMRI'


#svm ori
sed -e s:"#mainDir":"mainDir":g \
    -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#svm dir
sed -e s:"#mainDir":"mainDir":g \
    -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#svm 12-way
sed -e s:"#mainDir":"mainDir":g \
    -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
