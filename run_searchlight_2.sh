#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#blocks

#12-way cope/tstat noNorm

#5mm mainly to compare - runnning some on love06 too:

# # 12-way cope 5mm, fwhm1
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# 12-way tstat 5mm, fwhm1
sed -e s:"#mainDir":"mainDir":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


#then 6mm's noSmooth - later run smooth for a few to compare?

# 12-way cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# 12-way tstat 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


# ori cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# ori tstat 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'ori'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


# dir cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# dir tstat 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


# running  on love06

#crossnobis
# ori cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# dir cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
