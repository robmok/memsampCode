#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#svm - cope & tstat, blocks
#mahal - cope blocks

#blocks - mahal - no smooth and with smooth
#Ori
#Dir

#svm, cope/tstat - with smoothing first
#12-way
#Ori
#Dir

#no smoothing, noNorm
## ori crossnobis
python mvpa_memsamp_blocks.py

# dir
sed -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#fwhm=1 smoothing, noNorm
#ori smooth
sed -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py

#dir smooth
sed -e s:"fwhm = None":"fwhm = 1":g \
    -e s:"decodeFeature = 'ori'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py


#SVMs

#svm ori
sed -e s:"distMeth = 'crossNobis'":"distMeth = 'svm'":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_memsamp_blocks.py > ${tmpScrDir}/mvpa_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_memsamp_blocks1.py
