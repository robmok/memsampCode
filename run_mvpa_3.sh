#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# #normalized
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'feedstim'":g \
    -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py




#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
#     -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
