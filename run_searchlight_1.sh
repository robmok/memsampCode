#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight



## to restrict regions to do SL over
# -e s:"(fmriprepDir,'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')":"(roiDir, 'sub-' + subNum + '_visRois_lrh.nii.gz')":g \





# #above didin't actually run 1:19... - rerun!
# #12-way sl6 niNorm svm tstat blocks
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"for iSub in range(1,34)":"for iSub in range(5,19)":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     -e s:"imDat   = 'cope'":"imDat   = 'tstat'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
