#! /bin/bash

# from johan's roi dir - edit subject number to sub-01, etc.
s=`ls -d *0*`
cnt1=1
for i in $s; do
subCounter=`printf "sub-%.2d" ${cnt1}`
echo mv $i $subCounter
let cnt1=cnt1+1
done


# edit roi names - note not all have left and right rois. if no, e.g. left FFA, then FFA will be unilateral as well

wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois/rois_func'

cd ${wd}
for iSub in {1..33}; do
sub=`printf "sub-%.2d" ${iSub}`

cd ${sub}

mv FFA.nii ${sub}_FFA_lrh.nii
mv r_FFA.nii ${sub}_FFA_lh.nii
mv l_FFA.nii ${sub}_FFA_rh.nii

mv PPA.nii ${sub}_PPA_lrh.nii
mv l_PPA.nii ${sub}_PPA_lh.nii
mv r_PPA.nii ${sub}_PPA_rh.nii

mv OFA.nii ${sub}_OFA_lrh.nii
mv l_OFA.nii ${sub}_OFA_lh.nii
mv r_OFA.nii ${sub}_OFA_rh.nii

mv TOS.nii ${sub}_TOS_lrh.nii
mv l_TOS.nii ${sub}_TOS_lh.nii
mv r_TOS.nii ${sub}_TOS_rh.nii

mv evc.nii ${sub}_evc_lrh.nii

cd ${wd}

done
