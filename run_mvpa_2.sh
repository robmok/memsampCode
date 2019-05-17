#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# subjCat-all dCentred - svm cope/tstat, crossNobis trials/blocks

# subjCat-all svm cope trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-all svm tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-all svm cope blocks
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-all svm tstat blocks
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
