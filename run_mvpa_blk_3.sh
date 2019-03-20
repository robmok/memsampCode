#! /bin/bash
# Rois - block

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# tstat_demeaned
sed -e s:'noNorm':'demeaned':g \
  -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#tstat_niNorm
sed -e s:'noNorm':'niNormalised':g \
-e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
