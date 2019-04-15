#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#crossnobis blocks
sed -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#subjCat-all
#crossnobis block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#subjCat-all
#crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
