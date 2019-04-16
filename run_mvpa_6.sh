#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'



#objCat
#crossnobis blocks
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#objCat - norm
#svm

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#tstats - extras
#svm
sed -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
