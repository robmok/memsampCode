#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#motor
#sl6 fwhmNone
#motor svm
sed -e s:"nCores = 22":"nCores = 4":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

sed -e s:"nCores = 22":"nCores = 4":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"slSiz = 6":"slSiz = 8":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

sed -e s:"nCores = 22":"nCores = 4":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"slSiz = 6":"slSiz = 9":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
