#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#re-run subjCat-orth - add on motor ROI


#reRunROIs motor cortex subjCat

# # subjCat cope trials - ran first
# sed -e s:"reRun = False":"reRun = True":g \
#     -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat cope block
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat crossnobis trials
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# tstat
# subjCat cope trials
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat cope block
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#niNormalised
#subjCat cope niNormalised
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat cope block
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat crossnobis trials
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#tstat niNormalised
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat tstat block
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#demeaned_stdNorm
#subjCat cope demeaned_stdNorm
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat cope block
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat crossnobis trials
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#tstat demeaned_stdNorm
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat tstat block
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
