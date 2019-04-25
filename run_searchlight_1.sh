#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

#subjCat-orth svm cope, noNorm, fwhmNone
#subjCat-orth svm cope, noNorm, fwhm1

# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"for iSub in range(1,34)":"for iSub in range(12,34)":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#	• #12-way niNorm tstat, fwhm1 - missed sub 19!
#niNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"for iSub in range(1,34)":"for iSub in range(19,20)":g \
      < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
