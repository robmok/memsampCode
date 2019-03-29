# rough script i used to copy cope images over (1st part) and anat files (2nd part) - script was used by copying and pasting

#both - # copy to a single directory (forlove01) then move to love01

#########
## copying over feats  - only send over cope and zstats
#########

mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/

## on love06
while read subject; do
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_block_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-01_block_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-01_block_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-01_block_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_block_T1_fwhm0.feat/stats/

  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_block_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-02_block_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-02_block_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-02_block_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_block_T1_fwhm0.feat/stats/

  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_block_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-03_block_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-03_block_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-03_block_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_block_T1_fwhm0.feat/stats/

  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_trial_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-01_trial_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-01_trial_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-01_trial_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-01_trial_T1_fwhm0.feat/stats/

  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_trial_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-02_trial_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-02_trial_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-02_trial_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-02_trial_T1_fwhm0.feat/stats/

  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_trial_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-03_trial_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-03_trial_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-03_trial_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-03_trial_T1_fwhm0.feat/stats/

done < /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/feat_design_files/subject_list_full.txt

for subject in sub-09 sub-12 sub-16 sub-26; do
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_block_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-04_block_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-04_block_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_block_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-04_block_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_block_T1_fwhm0.feat/stats/

  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_trial_T1_fwhm0.feat/
  mkdir /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-04_trial_T1_fwhm0.feat/stats/cope* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-04_trial_T1_fwhm0.feat/stats/tstat* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_trial_T1_fwhm0.feat/stats/
  scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/${subject}_run-04_trial_T1_fwhm0.feat/stats/res* /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01/${subject}_run-04_trial_T1_fwhm0.feat/stats/
done

#then send  dir over to love01
scp -r forlove01/ robmok@love01.psychol.ucl.ac.uk:/home/robmok/Documents/memsamp_fMRI/

# on love01 then scp to memsampFeat dir
#scp -r /home/robmok/Documents/memsamp_fMRI/forlove01/* /home/robmok/Documents/memsamp_fMRI/memsampFeat


########
## for copying over anat
########

#on love01
cd /home/robmok/Documents/memsamp_fMRI/
mkdir fmriprep_output
cd fmriprep_output
mkdir fmriprep
cd /home/robmok/Documents/memsamp_fMRI/fmriprep_output/fmriprep

## on love06
while read subject; do
  mkdir ${subject}
  cd ${subject}
  scp -r /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep/${subject}/anat .
  cd /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/forlove01
done < /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/feat_design_files/subject_list_full.txt

#then send  dir over to love01
scp -r forlove01/ robmok@love01.psychol.ucl.ac.uk:/home/robmok/Documents/memsamp_fMRI/

#then scp to fmriprep dir
scp -r /home/robmok/Documents/memsamp_fMRI/forlove01/* .



#for when i sent res images later

#then send  dir over to love01
# scp -r forlove01/ robmok@love01.psychol.ucl.ac.uk:/home/robmok/Documents/

#subj list
#scp /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/feat_design_files/subject_list_full.txt robmok@love01.psychol.ucl.ac.uk:/home/robmok/Documents/
#then scp to  dir

#
# while read subject; do
#
# scp /home/robmok/Documents/forlove01/${subject}_run-01_trial_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-01_trial_T1_fwhm0.feat/stats/
# scp /home/robmok/Documents/forlove01/${subject}_run-02_trial_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-02_trial_T1_fwhm0.feat/stats/
# scp /home/robmok/Documents/forlove01/${subject}_run-03_trial_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-03_trial_T1_fwhm0.feat/stats/
# scp /home/robmok/Documents/forlove01/${subject}_run-04_trial_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-04_trial_T1_fwhm0.feat/stats/

#scp /home/robmok/Documents/forlove01/${subject}_run-01_block_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-01_block_T1_fwhm0.feat/stats/
#scp /home/robmok/Documents/forlove01/${subject}_run-02_block_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-02_block_T1_fwhm0.feat/stats/
#scp /home/robmok/Documents/forlove01/${subject}_run-03_block_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-03_block_T1_fwhm0.feat/stats/
#scp /home/robmok/Documents/forlove01/${subject}_run-04_block_T1_fwhm0.feat/stats/res* /home/robmok/Documents/memsamp_fMRI/memsampFeat/${subject}_run-04_block_T1_fwhm0.feat/stats/

# done < /home/robmok/Documents/subject_list_full.txt
