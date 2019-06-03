#! /bin/bash
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'

#love01
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

#subjCat-orth cope, noNorm
sed -e s:"nCores = 16":"nCores = 7":g \
    -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
    -e s:"slSiz = 6":"slSiz = 12":g \
    -e s:"fwhm = None":"fwhm = 5":g \
  < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
python ${tmpScrDir}/mvpa_searchlight_memsamp1.py


#fwhm=3, sph=9

# #svm  trials
# #subjCat cope, noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #subjCat-orth cope, noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #subjCat tstat, noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# #
# #subjCat-orth tstat, noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #subjCat crossNobis, trials noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#     < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# #subjCat-orth crossNobis, trials noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"slSiz = 6":"slSiz = 9":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#     < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
#
# #fwhm=3, sph=9
#
#
# #svm  trials
# #subjCat cope, noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"slSiz = 6":"slSiz = 12":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# #subjCatRaw-orth cope, noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"slSiz = 6":"slSiz = 12":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# # #subjCat tstat, noNorm
# # sed -e s:"nCores = 16":"nCores = 7":g \
# #     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
# #     -e s:"slSiz = 6":"slSiz = 12":g \
# #     -e s:"fwhm = None":"fwhm = 3":g \
# #   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# # python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
#
# #subjCatRaw-orth tstat, noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"imDat = 'cope'":"imDat = 'tstat'":g \
#     -e s:"slSiz = 6":"slSiz = 12":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#   < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# #subjCat crossNobis, trials noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"slSiz = 6":"slSiz = 12":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#     < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py

# #subjCatRaw-orth crossNobis, trials noNorm
# sed -e s:"nCores = 16":"nCores = 7":g \
#     -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCatRaw-orth'":g \
#     -e s:"distMeth = 'svm'":"distMeth = 'crossNobis'":g \
#     -e s:"slSiz = 6":"slSiz = 12":g \
#     -e s:"fwhm = None":"fwhm = 3":g \
#     < ${codeDir}/mvpa_searchlight_memsamp.py > ${tmpScrDir}/mvpa_searchlight_memsamp1.py
# python ${tmpScrDir}/mvpa_searchlight_memsamp1.py
