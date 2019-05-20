#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


# -e s:"#mainDir":"mainDir":g \
# -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \


#subjCat
sed -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#subjCat-orth
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#subjCat-all
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    -e s:"#mainDir":"mainDir":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
