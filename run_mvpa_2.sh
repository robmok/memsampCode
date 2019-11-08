#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# bilateralRois
vpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py


sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
