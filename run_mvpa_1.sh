#! /bin/bash
# Rois

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
# mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

codeDir=${mainDir}/'memsampCode'
tmpScrDir=${mainDir}/'mvpaTmpScripts'

# -e s:"reRun = False":"reRun = True":g \
# -e s:"#rois":"rois":g \

# -e s:"decodeFromFeedback = False":"decodeFromFeedback = True":g \

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat'":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-minus-motor'":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat'":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-minus-motor'":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py


#from 3
sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'ori'":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py

sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'dir'":g \
    -e s:"bilateralRois = False":"bilateralRois = True":g \
        < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
python ${tmpScrDir}/mvpa_memsamp1.py



# sed -e s:"decodeFeature = 'subjCat'":"decodeFeature = 'subjCat-orth'":g \
#     -e s:"lock2resp = False":"lock2resp = True":g \
#         < ${codeDir}/mvpa_memsamp.py > ${tmpScrDir}/mvpa_memsamp1.py
# python ${tmpScrDir}/mvpa_memsamp1.py
