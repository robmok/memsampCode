#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Rois - block

# block_cope_noNorm
python mvpa_memsamp_blocks.py

#block_cope_demeaned
sed -e s:'noNorm':'demeaned':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#block_tstat_niNorm
sed -e s:'noNorm':'niNormalised':g \
  -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#block_tstat_noNorm
sed -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#block_tstat_demeaned
sed -e s:'noNorm':'demeaned':g \
  -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py
