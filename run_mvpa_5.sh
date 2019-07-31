#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#love01

#SPL1
#svm subjCat-orth, objCat, objCat-orth, subjCat-all, 12-way-all, dir-all

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-minus-motor'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
