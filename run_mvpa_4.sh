#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#subjCat
#Blocks

# #crossNobis
# sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#crossNobis
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#svm tstat
sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
