#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#trials  - mahal
#Ori
#Dir

#no smoothing, noNorm
# ori
python mvpa_memsamp.py

# # dir
sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#fwhm=1 smoothing, noNorm
#ori smooth
sed -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

#dir smooth
sed -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py
