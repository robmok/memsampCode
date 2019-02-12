wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files

for iCope in 1; do #just replace cope numbers when running a loop (iCope) of the gfeats
while read subject; do
  #echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_block_fwhm6_2ndlvl.gfeat/cope${iCope}.feat/stats/cope${iCope}.nii.gz" >> ${wd}/gfeatDirLists/gfeat_dirs_cope${iCope}_fwhm6.txt
  #echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_block_fwhm6_2ndlvl_nofmaps.gfeat/cope${iCope}.feat/stats/cope${iCope}.nii.gz" >> ${wd}/gfeatDirLists/gfeat_dirs_cope${iCope}_fwhm6_nofmaps.txt

#localisers - feat folders
echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_motionLocaliser_fwhm6.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_motionLoc_fwhm6.txt
echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_motionLocaliser_fwhm6_nofmaps.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_motionLoc_fwhm6_nofmaps.txt
echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_exemplarLocaliser_fwhm6.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_exemplarLoc_fwhm6.txt
echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_exemplarLocaliser_fwhm6_nofmaps.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_exemplarLoc_fwhm6_nofmaps.txt

done < ${fsfDir}/subject_list_full.txt #while read subject; do
done
