#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# subjCat-all, svm
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"#rois":"rois":g \
    -e s:"reRun = False":"reRun = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-all, crossnobis
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'mNobis'":g \
    -e s:"#rois":"rois":g \
    -e s:"reRun = False":"reRun = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
