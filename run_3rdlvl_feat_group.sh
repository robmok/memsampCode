#! /bin/bash
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files

standardScript='memsamp_block_cope1_3rdlvl'
standardScript='memsamp_block_cope1_3rdlvl_nofmaps'

fwhm=8
standardScript="memsamp_block_cope1_3rdlvl_fwhm${fwhm}"
standardScript="memsamp_block_cope1_3rdlvl_fwhm${fwhm}_noTD"

#for iCope in {1..13}; do
#    sed -e s:cope1.feat/stats/cope1.nii.gz:cope${iCope}.feat/stats/cope1.nii.gz:g \
#        -e s:cope1_fwhm6:cope${iCope}_fwhm6:g \
#      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_cope${iCope}_3rdlvl.fsf
#  feat ${fsfDir}/run_memsamp_block_cope${iCope}_3rdlvl.fsf
#done

for iCope in {1..13}; do
    sed -e s:cope1.feat/stats/cope1.nii.gz:cope${iCope}.feat/stats/cope1.nii.gz:g \
        -e s:cope1_fwhm${fwhm}:cope${iCope}_fwhm${fwhm}:g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_cope${iCope}_3rdlvl_fwhm${fwhm}.fsf
  feat ${fsfDir}/run_memsamp_block_cope${iCope}_3rdlvl_fwhm${fwhm}.fsf
done
