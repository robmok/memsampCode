#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
# Rois

# crossEuclid, trials

#cope_noNorm
python mvpa_memsamp.py

#cope_demeaned
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#euclid ori

#cope_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#cope_demeaned
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py
