#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight



#
# #sl8 svm tstat BLOCKS - this is a re-run -.-... should've been 12-way
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz=6":"slSiz=8":g \
#     -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#

# # 8mm 12-way tstat niNorm TRIALS
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz=6":"slSiz=8":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #12-way sl8 svms niNorm, tstat, blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz=6":"slSiz=8":g \
#     -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


# # #sl8 svm tstat BLOCKS
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz=6":"slSiz=8":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#above didin't actually run 1:19... - rerun!
#12-way sl6 niNorm svm tstat blocks
sed -e s:"#mainDir":"mainDir":g \
    -e s:"for iSub in range(1,34)":"for iSub in range(5,19)":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# #ori sl8 - crossnobis - blocks - rerun
sed -e s:"#mainDir":"mainDir":g \
    -e s:"for iSub in range(1,34)":"for iSub in range(4,34)":g \
    -e s:"slSiz=6":"slSiz=8":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
