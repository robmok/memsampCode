#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
# Rois
# run tstat_noNorm
python mvpa_memsamp.py

# tstat_demeaned
sed -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# cope_demeaned
sed -e s:'noNorm':'demeaned':g \
  -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# cope_demeaned_stdNorm
sed -e s:'noNorm':'demeaned_stdNorm':g \
  -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# tstat_demeaned_stdNorm
sed -e s:'noNorm':'demeaned_stdNorm':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py
