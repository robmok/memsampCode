#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


# -e s:"reRun = False":"reRun = True":g \


sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py



# 12-way-all rerun

# # 12-way-all, crossnobis
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way-all'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py

# # subjCat-orth
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# #12-way-all svm - no run for no smooth
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way-all'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'svm'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
