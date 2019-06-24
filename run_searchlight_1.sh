#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# searchlight

#searchlight:
#subjCat (4)
#sl8, sl10, fwhmNone/fwhm1

#ori (7)
# sl8, sl9, sl10, fwhmNone/fwhm1
# sl6 fwhm1

# 12-way (6)
# sl9,10 fwhmNone
# sl6,8,9,10 fwhm1

# #sl8 fwhmNone
# #subjCat cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"slSiz = 6":"slSiz = 8":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# #
# #subjCat-orth cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"slSiz = 6":"slSiz = 8":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
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



# 12-way sl9,10 fwhmNone
#12-way cope, noNorm
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"slSiz = 6":"slSiz = 9":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

#12-way  cope, noNorm
sed -e s:"#mainDir":"mainDir":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = '12-way'":g \
    -e s:"slSiz = 6":"slSiz = 10":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py









# 12-way sl6,8,9,10 fwhm1?








# #sl8 fwhm1 - ? maybe
# #ori cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"slSiz = 6":"slSiz = 8":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #sl8 fwhmNone
# #ori cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #sl8 fwhmNone
# #ori cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"slSiz = 6":"slSiz = 10":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# sl6 fwhm1 - additionally
# #ori cope, noNorm
# sed -e s:"#mainDir":"mainDir":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
#     -e s:"fwhm = None":"fwhm = 1":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
