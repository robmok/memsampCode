#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#subjCat-all

#svm block cope
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py


#objCat
#crossnobis block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#objCat
#svm trials tstat
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#objCat
#svm trials cope
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py