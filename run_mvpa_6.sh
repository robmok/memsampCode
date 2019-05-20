#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#objCat
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#objCat-orth
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#ori
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
