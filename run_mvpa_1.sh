#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#unilateral Rois

# 12-way cope trials
# 12-way tstat trials
# 12-way cope block
# 12-way tstat block
# Ori Svm tstat trials
# Ori Svm tstat block
# Ori - crossnobis trials
# dir - svm trials cope
# dir - svm trials tstat

# also NOW: dir - svm cope/tstat block and crossnobis trials

# 12-way cope trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# 12-way tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# 12-way cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# 12-way tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


# Ori - crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# Ori Svm tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# Ori Svm tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#dir - only done crossnobis Blocks
# - svm trials cope
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# - svm trials tstat
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py


# tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#  crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py





#just run:
# #subjCat-orth
# #svm cope trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
#   python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# #svm tstat trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"imDat = 'cope'":"imDat    = 'tstat'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
#   python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # Crossnobis dm_std trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
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
