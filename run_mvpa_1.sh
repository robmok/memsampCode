#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
# Rois

# cope_noNorm
python mvpa_memsamp.py #note this is WITHOUT the 1

# cope_demeaned
sed -e s:'noNorm':'demeaned':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# cope_demeaned_stdNorm
