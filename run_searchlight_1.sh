
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI'#love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# Searchlight (5 cores) -

# trials first
# Dir/Ori, svm, noNorm/niNorm, cope & tstat
# 12-way, svm, noNorm, trials, cope & tstat
# Dir/Ori crossEuclid - trials/blocks

# Dir, svm, noNorm, cope
python mvpa_searchlight_memsamp.py

# Dir, svm, noNorm tstat
sed -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# Dir, svm, niNorm, cope

sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# Dir, svm, niNorm, tstat
sed -e s:'cope':'tstat':g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# Ori, svm, noNorm, cope
sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# Ori, svm, noNorm tstat
sed -e s:'cope':'tstat':g \
    -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py


# # crossnobis
#
# #dir noNorm
# python mvpa_searchlight_memsamp.py
#
# #ori noNorm
# sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
# python mvpa_searchlight_memsamp1.py
#
# #dir svm noNorm
# sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
# python mvpa_searchlight_memsamp1.py
#
# #ori svm noNorm
# sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
#     -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${codeDir}/mvpa_searchlight_memsamp1.py
# python mvpa_searchlight_memsamp1.py
#
# #next: niNorm? 12-way? normalise within the sphere?
