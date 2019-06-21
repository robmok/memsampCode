#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#sl10 fwhmNone

#subjCat-orth cope, noNorm
sed -e s:"nCores = 24":"nCores = 6":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
    -e s:"slSiz = 6":"slSiz = 10":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#sl8 fwhm1
#subjCat cope, noNorm
sed -e s:"nCores = 24":"nCores = 6":g \
    -e s:"slSiz = 6":"slSiz = 10":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#subjCat-orth cope, noNorm
sed -e s:"nCores = 24":"nCores = 6":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
    -e s:"slSiz = 6":"slSiz = 10":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
