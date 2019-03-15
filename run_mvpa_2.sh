#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
# Rois

# svm, trials

#dir

#tstat_demeaned
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# tstat_demeaned_stdNorm
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#sv, ori

##tstat_demeaned
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# tstat_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#svm ori

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
