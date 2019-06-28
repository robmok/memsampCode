#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#sl10 fwhmNone
#subjCat cope, noNorm
sed -e s:"slSiz = 6":"slSiz = 10":g \
    -e s:"distMeth = 'svm'":"distMeth = 'mNobis'":g \
    -e s:"nCores = 22":"nCores = 4":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#subjCat-orth cope, noNorm
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
    -e s:"slSiz = 6":"slSiz = 10":g \
    -e s:"distMeth = 'svm'":"distMeth = 'mNobis'":g \
    -e s:"nCores = 22":"nCores = 4":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
