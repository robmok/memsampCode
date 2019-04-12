#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

#SLs within allROIsSL

#subjCat sl6 svm cope blocks
sed -e s:"#mainDir":"mainDir":g \
    -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
    -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#subjCat sl6 crossnobis cope blocks
sed -e s:"#mainDir":"mainDir":g \
    -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
    -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#12-way sl6 svm cope blocks
sed -e s:"#mainDir":"mainDir":g \
    -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
    -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#ori sl6 svm cope blocks
sed -e s:"#mainDir":"mainDir":g \
    -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_allROIsSL.nii.gz')":g \
    -e s:"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))":"'_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '_allROIsSL.nii.gz'))":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


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
