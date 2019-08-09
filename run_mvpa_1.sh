#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# -e s:"reRun = False":"reRun = True":g \
# -e s:"#rois":"rois":g \

#love06

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-minus-motor'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# #controls - lock2resp for subjCat-orth, ori, dir, 12-way
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"lock2resp = False":"lock2resp = True":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-minus-motor'":g \
#     -e s:"lock2resp = False":"lock2resp = True":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
#     -e s:"lock2resp = False":"lock2resp = True":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"lock2resp = False":"lock2resp = True":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"lock2resp = False":"lock2resp = True":g \
#     -e s:"reRun = False":"reRun = True":g \
#     -e s:"#rois":"rois":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
