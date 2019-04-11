#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

#above didin't actually run 1:19... - rerun!
#12-way sl6 niNorm svm tstat blocks
sed -e s:"#mainDir":"mainDir":g \
    -e s:"for iSub in range(1,34)":"for iSub in range(5,19)":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


#ran this subjCat by accident - 1:19 done. do the rest?
#12-way sl6 niNorm svm tstat blocks - ran this fwhm1





# fwhm=1 testing
# subjCat svm cope trials/block, noNorm/niNorm
# Crossnobis block

# # crossNobis blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# #niNorm
# #cope blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
