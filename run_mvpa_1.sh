#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#unilateral Rois

#niNorm
# 12-way cope trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# 12-way tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# 12-way cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# 12-way tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py





#
#
#
#
#
# #below done
#
# # #ori svm trials cope
# # sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
# #   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# # python ${tmpScrDir}/mvpa_memsamp1.py
# #
# # #ori svm trials tstat
# # sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
# #     -e s:"imDat = 'cope'":"imDat    = 'tstat'":g \
# #     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
# #   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# # python ${tmpScrDir}/mvpa_memsamp1.py
# #
# # # ori crossnobis block
# # sed  -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
# #     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
# #   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# # python ${tmpScrDir}/mvpa_memsamp_blocks1.py
# #
# # #ori svm block tstat
# # sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
# #     -e s:"imDat = 'cope'":"imDat    = 'tstat'":g \
# #   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# # python ${tmpScrDir}/mvpa_memsamp_blocks1.py
# #
# # # ori crossnobis trials - to run? not run yet
