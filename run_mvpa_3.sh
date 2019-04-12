#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# # 12-way svm trials cope
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
#12-way svm trials tstat
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
