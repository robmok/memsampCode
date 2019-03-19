
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Searchlight (4-5 cores) -

# crossnobis

#dir noNorm
python mvpa_searchlight_memsamp.py

#ori noNorm
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
python mvpa_searchlight_memsamp1.py

#next: niNorm? 12-way? normalise within the sphere?
