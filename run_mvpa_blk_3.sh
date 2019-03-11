#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Rois - block

# tstat_demeaned
sed -e s:'noNorm':'demeaned':g \
  -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#tstat_niNorm
sed -e s:'noNorm':'niNormalised':g \
-e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py
