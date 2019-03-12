#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Rois - block

# cope_demeaned_stdNorm
sed -e s:'noNorm':'demeaned_stdNorm':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py
