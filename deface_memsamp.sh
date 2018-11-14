bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
cd ${bidsDir}
source activate py36
for iSub in {17..33}; do
  subNum=`printf "%.2d" ${iSub}` #zero padding
  anatDir="${bidsDir}/sub-${subNum}/anat"
  printf "Defacing subject ${subNum} \n"
  t1fname=`ls ${anatDir}/*T1*.nii.gz`
  pydeface ${t1fname}
  mv "${anatDir}/sub-${subNum}_T1w.nii.gz" "${anatDir}/sub-${subNum}_T1w_orig.nii.gz"
  mv "${anatDir}/sub-${subNum}_T1w_defaced.nii.gz" "${anatDir}/sub-${subNum}_T1w.nii.gz"
  #if move originals out of the BIDS directory
  mv "${anatDir}/sub-${subNum}_T1w_orig.nii.gz" "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/orig_t1/sub-${subNum}_T1w_orig.nii.gz"
done
