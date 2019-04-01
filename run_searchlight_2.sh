#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#blocks

#Blocks
#svm cope
# sed -e s:"#mainDir":"mainDir":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# crossNobis
sed -e s:"#mainDir":"mainDir":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


# # dir cope 6mm, fwhm1-  not sure why did 1 here, do none below
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz=5":"slSiz=6":g \
#     -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# # dir  6mm cope, fwhmNone - done
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# # dir tstat 6mm, fwhmNone - done
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
#     -e s:'cope':'tstat':g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

#crossnobis
# ori cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# dir cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
