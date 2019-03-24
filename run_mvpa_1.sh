#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#no smoothing, noNorm
#Ori
#Dir
#12-way

#svm - cope & tstat, trials & blocks
#mahal - cope, trials & blocks

#trials

# ## ori svm cope
# python mvpa_memsamp.py
#
# # ori svm tstat
# sed -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # ori mahal
# sed -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# ## dir svm cope
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # dir svm tstat
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
#     -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # dir mahal
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py

#ABOVE RAN THROUGH

## 12-way svm cope
sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# dir svm tstat
sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# # dir mahal - NOT RUNNING
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
