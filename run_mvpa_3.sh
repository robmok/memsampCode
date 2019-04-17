#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#love06

# - 12-way niNorm tstat, fwhm1
sed -e s:"nCores = 12":"nCores = 6":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"imDat = 'cope'":"imDat    = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# 12-way niNorm  cope, fwhm1
sed -e s:"nCores = 12":"nCores = 6":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# - svm ori niNorm fwhmNone/fwhm1, cope - MAYBE TSTAT LATER

#niNorm fwhm0
sed -e s:"nCores = 12":"nCores = 6":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#niNorm fwhm1
sed -e s:"nCores = 12":"nCores = 6":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py















#TO RUN LATER:

# #svm cope block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# #svm tstat trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py


# #crossnobis trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
