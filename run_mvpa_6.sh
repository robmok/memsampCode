#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


# subjCat-orth cope trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-orth crossNobis block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-orth tstat trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-orth cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-orth tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-orth crossNobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py



#NEXT:

# # subjCat-orth-ctrl
# # subjCat-orth-ctrl cope trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # subjCat-orth-ctrl crossNobis block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # subjCat-orth-ctrl tstat trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # subjCat-orth-ctrl cope block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # subjCat-orth-ctrl tstat block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # subjCat-orth-ctrl crossNobis trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth-ctrl'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
