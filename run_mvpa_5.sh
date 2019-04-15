#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#subjCat
#svm trials tstat
sed -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# #subjCat-all
#svm trials cope
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#svm trials tstat
sed -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#crossnobis trials
sed -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#subjCat-all
#crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp1.py
