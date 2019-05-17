#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


# objCat-orth crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"#mainDir":"mainDir":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# objCat-orth crossnobis blocks
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"#mainDir":"mainDir":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-orth-ctrl - svm cope/tstat, crossNobis trials/blocks

# subjCat-orth-ctrl svm cope trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"#mainDir":"mainDir":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-orth-ctrl svm tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"#mainDir":"mainDir":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
