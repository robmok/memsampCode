#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

#searchlight:
#subjCat/orth - mahalnobis distance

# #sl6 fwhmNone
# #subjCat cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'mNobis'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#subjCat-orth cope, noNorm
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
    -e s:"distMeth = 'svm'":"distMeth = 'mNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# #sl9 fwhmNone
# #subjCat cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'mNobis'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#subjCat-orth cope, noNorm
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
    -e s:"slSiz = 6":"slSiz = 9":g \
    -e s:"distMeth = 'svm'":"distMeth = 'mNobis'":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# #motor
# #sl6 fwhmNone
# #motor svm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
#     -e s:"slSiz = 6":"slSiz = 8":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'motor'":g \
    -e s:"slSiz = 6":"slSiz = 9":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# #sl8 fwhm1
# #subjCat cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz = 6":"slSiz = 8":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #subjCat-orth cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"slSiz = 6":"slSiz = 8":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #sl10 fwhmNone
# #subjCat cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz = 6":"slSiz = 10":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # sl10 continued in script 2
#




#
# #ori
# # sl8, sl9, sl10, fwhmNone/fwhm1
# # sl6 fwhm1
#
# #sl8 fwhmNone
# #ori cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"slSiz = 6":"slSiz = 8":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #ori cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #ori cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"slSiz = 6":"slSiz = 10":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py



# # 12-way sl9,10 fwhmNone
# #12-way cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #12-way  cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
#     -e s:"slSiz = 6":"slSiz = 10":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
