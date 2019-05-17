#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#unilateral Rois

# -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
# -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
# -e s:"normMeth = 'noNorm'":"normMeth = 'dCentred'":g \


#mPFC rerunning everything

#subjCat, ori, objCat, objCat-orth ori, dir, noNorm
#12-way-all, subjCat-all
#12-way noNorm  - svms only

#subjCat


#ori
sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#subjCat-orth
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py



sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py



#objCat-orth
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#ori
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"reRun = False":"reRun = True":g \
    -e s:"#rois":"rois":g \
    < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py



# subjCat-all svm tstat noNorm block
# subjCat-all crossnobis demeaned_stdNorm trials
# subjCat-all crossnobis niNormalised trials/block
# subjCat-all dCentred - svm cope/tstat, crossNobism trials/blocks
#12-way-all dCentred - svm cope/tstat, crossNobis trials/blocks
#objCat,objCat-orth - dCentred - svm cope/tstat, crossNobis trials/blocks
#ori-ctrl noNorm - svm cope/tstat, crossNobis trials/blocks


# # subjCat-all svm tstat noNorm block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
#
# # subjCat-all crossnobis demeaned_stdNorm trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'demeaned_stdNorm'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # subjCat-all crossnobis niNormalised trials
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
#
# # subjCat-all crossnobis niNormalised block
# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-all'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_memsamp_blocks1.py
