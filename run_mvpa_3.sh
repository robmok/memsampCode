#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# bilateralRois

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#lock2resp motor
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"lock2resp = False":"lock2resp = True":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py


sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"lock2resp = False":"lock2resp = True":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"lock2resp = False":"lock2resp = True":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
