
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Searchlight (4-5 cores) -

#blocks - old one 12-way svm

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


# SVM/Euclid dir, cope (stat for svm only), noNorm/niNorm - trials

#SVM - pairwise - dir

#tstat_noNorm_svm
sed -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py

#cope_noNorm_svm
sed -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:'tstat':'cope':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py
