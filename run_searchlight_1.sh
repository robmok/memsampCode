
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Searchlight (4-5 cores) - tstat_niNorm, cope_noNorm, tstat_noNorm

#tstat_niNorm
python mvpa_searchlight_memsamp_blocks.py

#cope_niNorm
sed -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${codeDir}/mvpa_searchlight_memsamp_blocks1.py
python mvpa_searchlight_memsamp_blocks1.py

#tstat_noNorm
sed -e s:'niNormalised':'noNorm':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${codeDir}/mvpa_searchlight_memsamp_blocks1.py
python mvpa_searchlight_memsamp_blocks1.py

#cope_noNorm
sed -e s:'niNormalised':'noNorm':g \
  -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${codeDir}/mvpa_searchlight_memsamp_blocks1.py
python mvpa_searchlight_memsamp_blocks1.py
