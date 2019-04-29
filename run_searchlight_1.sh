#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

#subjCatRaw, subjCat-orth, trials/blocks, fwhm0/1, cope/tstat

#next: #objCatRaw, objCat-orth, blocks/trials, fwhm0/1

##subjCatRaw tstat & subjCatRaw-orth tstat, block/trial, fwhm1

##subjCatRaw tstat, , noNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#subjCatRaw-orth tstat, -orth, noNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#trials
#svm
#subjCatRaw tstat, , noNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#
# #subjCatRaw, subjCatRaw-orth: blocks svm
#
# ##subjCatRaw, noNorm fwhm0
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# #subjCatRaw-orth, noNorm fwhm0
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# #trials svm
# ##subjCatRaw, noNorm fwhm0
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #subjCatRaw-orth, noNorm fwhm0
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
#
# ##subjCatRaw tstat, noNorm fwhm0
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# #subjCatRaw-orth, tstat, noNorm fwhm0
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
