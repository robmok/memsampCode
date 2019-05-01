#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# motor tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# motor tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#niNorm

# motor cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# motor tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# motor tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


# demeaned_stdNorm
# motor cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# motor tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# motor tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
