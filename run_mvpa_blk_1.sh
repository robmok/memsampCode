#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Rois - block

# cope_noNorm
python mvpa_memsamp_blocks.py

# cope_demeaned
sed -e s:'noNorm':'demeaned':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py
