#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI'#love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# set 2 - Run subjCat 8mm - svm cope/tstat/crossnobis, trials & blocks
#trials
#crossnobis
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=6":"slSiz=8":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#svm cope
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=6":"slSiz=8":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#svm tstat
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=6":"slSiz=8":g \
    -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py


#Blocks
#crossnobis
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=6":"slSiz=8":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#svm cope
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=6":"slSiz=8":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#svm tstat in other script
