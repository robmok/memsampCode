wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files

standardScript='memsamp_block_cope1_3rdlvl'
standardScript='memsamp_block_cope1_3rdlvl_nofmaps'

for iCope in {1..13}; do
    sed -e s:cope1.feat/stats/cope1.nii.gz:cope${iCope}.feat/stats/cope1.nii.gz:g \
        -e s:cope1_fwhm6:cope${iCope}_fwhm6:g \
      <${fsfDir}/${standardScript}.fsf >${fsfDir}/run_memsamp_block_cope${iCope}_3rdlvl.fsf
  feat ${fsfDir}/run_memsamp_block_cope${iCope}_3rdlvl.fsf
done
