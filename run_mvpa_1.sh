#! /bin/bash

codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
# Rois

# blocks:
  # dir - svm/euclid, cope/tstat (cope only for euclid), noNorm/niNorm
  # ori
  # 12-way

###########
#SVM - dir
###########

#cope_noNorm
python mvpa_memsamp_blocks.py

#cope_niNorm
sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#tstat_noNorm
sed -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#tstat_niNorm
sed -e s:'cope':'tstat':g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

# #tstat_demeaned - missing this

# tstat_demeaned_stdNorm
sed -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#euclid

#cope_noNorm
sed -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py


#########
#svm ori
#########
#cope_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

##tstat_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

# tstat_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

# tstat_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#euclid

#cope_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py





#########
#svm 12-way-all
#########
#cope_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

##tstat_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

# tstat_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

# tstat_demeaned_stdNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#euclid

#cope_noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py

#cope_niNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way-all'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${codeDir}/mvpa_memsamp_blocks1.py
python mvpa_memsamp_blocks1.py
