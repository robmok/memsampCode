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

#blocks

# ## ori svm cope
# python mvpa_memsamp_blocks.py
#
# # ori svm tstat
# sed -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # ori mahal
# sed -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#ABOVE RAN THROUGH FINE

# ## dir svm cope - ran through but may need to check
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# dir svm tstat
sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# # dir mahal - not running
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py

## 12-way svm cope
sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# dir svm tstat
sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# # dir mahal - not running
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
