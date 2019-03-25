#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#svm dir
sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#svm 12-way
sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#svm tstat
#svm ori
sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#svm dir
sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#svm 12-way
sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
