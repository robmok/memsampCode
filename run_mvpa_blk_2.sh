#! /bin/bash
# Rois - block

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# tstat_demeaned_stdNorm
sed -e s:'noNorm':'demeaned_stdNorm':g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# tstat_demeaned_stdNorm
sed -e s:'noNorm':'demeaned_stdNorm':g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
