
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Searchlight (4-5 cores) - tstat_niNorm, cope_noNorm, tstat_noNorm
#tstat_niNorm
python mvpa_searchlight_memsamp.py

#tstat_noNorm
sed -e s:'niNormalised':'noNorm':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py

#cope_noNorm
sed -e s:'niNormalised':'noNorm':g \
  -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py
