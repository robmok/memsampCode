#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# -e s:"reRun = False":"reRun = True":g \
# -e s:"#rois":"rois":g \

#love06

#re-run with EVC lh, rh, lrh (bilateral)
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py


# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"lock2resp = False":"lock2resp = True":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
