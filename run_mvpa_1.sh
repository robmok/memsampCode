#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# -e s:"reRun = False":"reRun = True":g \
# -e s:"#rois":"rois":g \

#love06 - decode from feedback time

# -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \

#decode feedback stimulus
#fwhm2
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'feedstim'":g \
    -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \
    -e s:"fwhm = None":"fwhm = 2":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
