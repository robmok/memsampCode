
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

# # 12-way tstat 8mm, fwhmNone - finish off
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=8":g \
    -e s:'cope':'tstat':g \
    -e s:'for iSub in range(1,34):':'for iSub in range(24,34):':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# 6mm's noSmooth - later run smooth for a few to compare?

#trials

# 12-way cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# 12-way tstat 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py


# ori cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'ori'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# ori tstat 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'ori'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py


# dir cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# dir tstat 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:'cope':'tstat':g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py


#crossnobis
# ori cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'ori'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# dir cope 6mm, fwhmNone
sed -e s:"#mainDir":"mainDir":g \
    -e s:"slSiz=5":"slSiz=6":g \
    -e s:"decodeFeature = '12-way'":"decodeFeature = 'dir'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py











# Set up scripts for a couple larger searchlights to compare trials and blocks, 8mm
# ○ larger searchlights (8mm) to compare trials and blocks - smooth 1mm
# ○ 5mm - no smoothing (should round up to 6)
# ○ mahal dist 8mm - no smooth

#   § 12-way t-stat, block & trials, 6mm, 8mm, cMass (4)
#   § 12-way cope too (4)

# 12-way t-stat, block & trials, 8mm, cMass (2)
# 12-way cope too (2)

#Trials

# # 12-way cope 8mm, fwhm1
# python mvpa_searchlight_memsamp.py
#
# # 12-way tstat 8mm, fwhm1
# sed -e s:'cope':'tstat':g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # 12-way cope 5mm, fwhm=None
# sed -e s:"slSiz=8":"slSiz=5":g \
# -e s:"fwhm = 1":"fwhm = None":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # 12-way tstat 5mm, fwhm=None
# sed -e s:"slSiz=8":"slSiz=5":g \
#     -e s:"fwhm = 1":"fwhm = None":g \
#     -e s:'cope':'tstat':g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py













# trials first
# Dir/Ori, svm, noNorm/niNorm, cope & tstat
# 12-way, svm, noNorm, trials, cope & tstat
# Dir/Ori crossEuclid - trials/blocks

# #Trials
#
# # Dir, svm, niNorm, cope
# sed -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # Dir, svm, niNorm, tstat
# sed -e s:'cope':'tstat':g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # Ori, svm, niNorm, cope
# sed -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # Ori, svm, niNorm, tstat
# sed -e s:'cope':'tstat':g \
#     -e s:"decodeFeature = 'dir'":"decodeFeature = 'ori'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # 12-way, svm, niNorm, cope
# sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # 12-way, svm, niNorm, tstat
# sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way'":g \
#     -e s:'cope':'tstat':g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# ########
# #Blocks
# ########
#
# # 12-way, svm, niNorm, cope
# sed -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way'":g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # 12-way, svm, niNorm tstat
# sed -e s:'cope':'tstat':g \
#     -e s:"normMeth = 'noNorm'":"normMeth = 'niNormalised'":g \
#     -e s:"decodeFeature = 'dir'":"decodeFeature = '12-way'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
