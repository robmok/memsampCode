#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


# subjCat-orth cope niNorm block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-orth tstat niNorm block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py




















######
#maybe no need to do objCat-orth-ctrl**
####

# # objCat-orth-ctrl
# # objCat-orth-ctrl cope trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth-ctrl'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # objCat-orth-ctrl crossNobis block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth-ctrl'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # objCat-orth-ctrl tstat trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth-ctrl'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # objCat-orth-ctrl cope block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth-ctrl'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # objCat-orth-ctrl tstat block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth-ctrl'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # objCat-orth-ctrl crossNobis trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth-ctrl'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
