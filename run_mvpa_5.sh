#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


# #subjCat
# #svm trials cope
# python ${codeDir}/mvpa_memsamp.py
#
# #svm trials tstat
# sed -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# #svm block cope
# python ${codeDir}/mvpa_memsamp_blocks.py
#
#
# # #subjCat-all
# #svm trials cope
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# #svm trials tstat
# sed -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memmvpa_memsamp1samp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#


#ABOVE done


# #svm niNorm, demeaned_stdNorm, cope/tstat trials

#svm niNorm cope trials
sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#svm niNorm tstat trials
sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# #svm dm_std cope trials
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#svm  dm_std  tstat trials
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#crossnobis demeaned_stdNorm blocks
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
