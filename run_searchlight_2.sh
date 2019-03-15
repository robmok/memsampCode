
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

#tstat_niNorm_svm
sed -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py

#cope_niNorm_svm
sed -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py



#euclid - no stat

#cope_noNorm
sed -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py


#cope_niNorm
sed -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:'tstat':'cope':g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py
