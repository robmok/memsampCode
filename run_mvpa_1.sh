#! /bin/bash
# Rois

# mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#trials  - mahal
#Ori
#Dir

#ori smooth
sed -e s:"#mainDir":"mainDir":g \
    -e s:"fwhm = None":"fwhm = 3":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#dir smooth
sed -e s:"#mainDir":"mainDir":g \
    -e s:"fwhm = None":"fwhm = 3":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#svm ori
sed -e s:"#mainDir":"mainDir":g \
    -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"fwhm = None":"fwhm = 3":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#svm dir
sed -e s:"#mainDir":"mainDir":g \
    -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
    -e s:"fwhm = None":"fwhm = 3":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#svm 12-way
sed -e s:"#mainDir":"mainDir":g \
    -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
    -e s:"fwhm = None":"fwhm = 3":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
#
# #svm tstat
# #svm ori
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#     -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# #svm dir
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
#     -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#     -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# #svm 12-way
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
#     -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#     -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
