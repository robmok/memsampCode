
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Searchlight (4-5 cores) -

#tstat_noNorm
# python mvpa_searchlight_memsamp_blocks.py

#cope_noNorm
sed -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${codeDir}/mvpa_searchlight_memsamp_blocks1.py
python mvpa_searchlight_memsamp_blocks1.py

#tstat_noNorm
python mvpa_searchlight_memsamp.py

#cope_noNorm
sed -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py


# Euclid dir/ori, cope/stat, noNorm/niNorm

# distMeth = 'svm'
# decodeFeature = '12-way' -> dir/ori

#tstat_noNorm
sed -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py

#cope_noNorm
sed -e s:"distMeth = 'svm'":"distMeth = 'crossEuclid'":g \
    -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py



# niNorm
