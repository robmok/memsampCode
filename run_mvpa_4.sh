#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'feedstim'":g \
    -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \
    -e s:"fwhm = None":"fwhm = 3":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py


sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \
    -e s:"fwhm = None":"fwhm = 3":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
