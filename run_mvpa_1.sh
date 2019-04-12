#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#unilateral Rois

#ori svm trials cope
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#ori svm trials tstat
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# ori crossnobis block
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#ori svm block tstat
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py



# ori crossnobis trials - to run? not run yet






# # #12-way blocks - extras
# #svm copes
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
# #svm tstat
# sed -e s:"decodeFeature = 'ori'":"decodeFeature = '12-way'":g \
#     -e s:"imDat    = 'cope'":"imDat    = 'tstat'":g \
#   < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
