mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
#mainDir='/home/robmok/Documents/memsamp_fMRI'#love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#5mm mainly to compare:

# 12-way tstat 5mm, fwhm1
sed -e s:"nCores = 12":"nCores = 4":g \
    -e s:"fwhm = None":"fwhm = 1":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# 12-way cope 5mm, fwhm1
sed -e s:"nCores = 12":"nCores = 4":g \
    -e s:"fwhm = None":"fwhm = 1":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
