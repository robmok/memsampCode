#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

# crossnobis blocks
# - subjCat-orth, noNorm/niNorm, fwhmNone/fwhm1
# - subjCat, niNorm, fwhmNone/fwhm1
# - ori, niNorm, fwhmNone/fwhm1

# svm - Blocks
# - subjCat-orth cope, noNorm/niNorm, fwhmNone/fwhm1

#love06 - run 4;
# 12-way niNorm fwhm1, cope, fwhm1
# - 12-way niNorm fwhm1, tstat, fwhm1
# - svm ori noNorm/niNorm fwhm, cope/tstat


###
# - subjCat-orth, noNorm/niNorm, fwhmNone/fwhm1
# #noNorm fwhmNone - done - on love01
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


#noNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# #niNorm fwhmNone - done - on love01
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# #niNorm fwhm1 - done -  on love01
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# - ori, niNorm, fwhmNone/fwhm1

#niNorm fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#niNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


#objCat-orth
# crossnobis blocks
# - obj, noNorm, fwhmNone/fwhm1
# - objCat-orth, noNorm, fwhmNone/fwhm1

# svm - Blocks
# - obj cope, noNorm, fwhmNone/fwhm1
# - obj-orth cope, noNorm, fwhmNone/fwhm1


#crossNobis
#noNorm fwhm0
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py



#noNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#noNorm fwhm0
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#noNorm fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'objCat-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py





# #SLs within allROIsSL
#
# #subjCat sl6 svm cope blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
#     -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# #subjCat sl6 crossnobis cope blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
#     -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# #12-way sl6 svm cope blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
#     -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# #ori sl6 svm cope blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
#     -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


# - next tstats, ++

# -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \



#12-way sl6 svm cope trials




#done
# #above didin't actually run 1:19... - rerun!
# #12-way sl6 niNorm svm tstat blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"for iSub in range(1,34)":"for iSub in range(5,19)":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
