#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#reRunROIs motor subjCat-resp


# tstat
# subjCat-resp cope trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-resp cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py



#niNormalised
#subjCat-resp cope niNormalised
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-resp cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-resp crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#tstat niNormalised
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-resp tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#demeaned_stdNorm
#subjCat-resp cope demeaned_stdNorm
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-resp cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-resp crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#tstat demeaned_stdNorm
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-resp tstat block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-resp cope trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

# subjCat-resp cope block
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

# subjCat-resp crossnobis trials
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-resp'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#reRunROIs":"rois = ['motor_lh', 'motor_rh']":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
