#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
# Rois

# svm, trials

#dir

#cope_noNorm
python mvpa_memsamp.py

#cope_demeaned
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# dir
#cope_demeaned_stdNorm
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#tstat_noNorm
sed -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

# ori

#cope_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py

#cope_demeaned
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned'":g \
  < ${codeDir}/mvpa_memsamp.py > ${codeDir}/mvpa_memsamp1.py
python mvpa_memsamp1.py
