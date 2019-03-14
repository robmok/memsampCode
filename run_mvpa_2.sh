#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
# Rois

#eucid dir
#cope_demeaned_stdNorm
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#tstat_noNorm
sed -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#euclid ori

#cope_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#tstat_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py
