
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'


#Blocks

# 12-way cope 9mm, fwhm1
python mvpa_searchlight_memsamp_blocks.py

# 12-way tstat 9mm, fwhm1
sed -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# 12-way cope 5mm, fwhm=None
sed -e s:"slSiz=9":"slSiz=5":g \
-e s:"fwhm = 1":"fwhm = None":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# 12-way tstat 5mm, fwhm=None
sed -e s:"slSiz=9":"slSiz=5":g \
    -e s:"fwhm = 1":"fwhm = None":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# 12-way mahal cope 9mm, fwhm=None
sed -e s:"fwhm = 1":"fwhm = None":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


#blocks

# ori mahal cope 9mm, fwhm=None
sed -e s:"decodeFeature = '12-way'":"decodeFeature = 'ori'":g \
    -e s:"fwhm = 1":"fwhm = None":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py

# dir mahal cope 9mm, fwhm=None
sed -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:"fwhm = 1":"fwhm = None":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py










# # Blocks
#
# # Dir, svm, noNorm, cope
# python mvpa_searchlight_memsamp_blocks.py
# #
# # Dir, svm, noNorm tstat
# sed -e s:'cope':'tstat':g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# # Ori, svm, noNorm, cope
# sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# # Ori, svm, noNorm tstat
# sed -e s:'cope':'tstat':g \
#     -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# # Dir, svm, niNorm, cope
# sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# # Dir, svm, niNorm, tstat
# sed -e s:'cope':'tstat':g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# # Ori, svm, niNorm, cope
# sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
#
# # Ori, svm, niNorm tstat
# sed -e s:'cope':'tstat':g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp_blocks.py > ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp_blocks1.py


# 12-way, svm, noNorm, cope - done block
# 12-way, svm, noNorm tstat - done block

# 12-way, svm, niNorm, cope
# 12-way, svm, niNorm tstat
# - running these is sl_1.sh script
