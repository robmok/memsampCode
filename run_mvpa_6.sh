#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"distMeth = 'svm'":"distMeth = 'lda'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py


#motor
#svm subjCat-all
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois = ['SPL1_lh','SPL1_rh']":"rois = ['motor_lh', 'motor_rh']":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
