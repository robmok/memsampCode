wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
fsfDir=${wd}/feat_design_files

fwhm=8 #6/8

for iCope in 1; do #just replace cope numbers when running a loop (iCope) of the gfeats
while read subject; do
  #echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_block_fwhm${fwhm}_2ndlvl.gfeat/cope${iCope}.feat/stats/cope${iCope}.nii.gz" >> ${wd}/gfeatDirLists/gfeat_dirs_cope${iCope}_fwhm${fwhm}.txt
  #echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_block_fwhm${fwhm}_2ndlvl_nofmaps.gfeat/cope${iCope}.feat/stats/cope${iCope}.nii.gz" >> ${wd}/gfeatDirLists/gfeat_dirs_cope${iCope}_fwhm${fwhm}_nofmaps.txt
  #echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_block_fwhm${fwhm}_2ndlvl_noTD.gfeat/cope${iCope}.feat/stats/cope${iCope}.nii.gz" >> ${wd}/gfeatDirLists/gfeat_dirs_cope${iCope}_fwhm${fwhm}_noTD.txt #fwhm8

#localisers - feat folders
echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_motionLocaliser_fwhm${fwhm}.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_motionLoc_fwhm${fwhm}.txt
#echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_motionLocaliser_fwhm${fwhm}_nofmaps.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_motionLoc_fwhm${fwhm}_nofmaps.txt
echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_exemplarLocaliser_fwhm${fwhm}.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_exemplarLoc_fwhm${fwhm}.txt
#echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_exemplarLocaliser_fwhm${fwhm}_nofmaps.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_exemplarLoc_fwhm${fwhm}_nofmaps.txt

#echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_motionLocaliser_fwhm${fwhm}_noTD.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_motionLoc_fwhm${fwhm}_noTD.txt
#echo "/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_exemplarLocaliser_fwhm${fwhm}_noTD.feat" >> ${wd}/gfeatDirLists/gfeat_dirs_exemplarLoc_fwhm${fwhm}_noTD.txt

done < ${fsfDir}/subject_list_full.txt #while read subject; do
done
