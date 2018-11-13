
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampData'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
cd ${wd}

#get subject directory names
if ! [ -f subNames.txt ]; then
s=`ls -d *0*` #all dirs with subs have 0s
echo ${s} >> subNames.txt
fi

#organize and rename GRE/EPI/task_epi/localizer_epi files
subCounter=`printf "%.2d" 1` #for zero padding sub-01

while read iSub; do
  mkdir ${bidsDir}/sub-${subCounter}
  mkdir ${bidsDir}/sub-${subCounter}/fmap
  mkdir ${bidsDir}/sub-${subCounter}/func
  mkdir ${bidsDir}/sub-${subCounter}/anat

  cd ${wd}/${iSub}

  runCounter=1 #for task epi - set here so it increases in the iDir loop
  runCounter=`printf "%.2d" ${runCounter}`

  #dirs=`ls -d *`
  dirs=`find . -regex '.*/[0-9]*'` #only dirs with numbers
  for iDir in ${dirs}; do #go through each dir

  #FIELDMAPS
  fname=`ls ${iDir}/*gre*.nii`
  for iFile in ${fname}; do
      if [ -f ${iFile} ]; then
        #rename gre file depending on type
        grefnames[1]='gre_field_mapping_1acq_rl_e1.nii'
        grefnames[2]='gre_field_mapping_1acq_rl_e2.nii'
        grefnames[3]='gre_field_mapping_1acq_rl_e2_ph.nii'
        if [[ ${iFile} == ${iDir}/${grefnames[1]} ]]; then #~= means ==; Use the =~ operator to make regular expression comparsions:
          scp ${iFile} ${bidsDir}/sub-${subCounter}/fmap/sub-${subCounter}_magnitude1.nii
          scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounter}/fmap/sub-${subCounter}_magnitude1.json # ${#iFile}-4 - to remove .nii
        elif [[ ${iFile} == ${iDir}/${grefnames[2]} ]]; then
          scp ${iFile} ${bidsDir}/sub-${subCounter}/fmap/sub-${subCounter}_magnitude2.nii
          scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounter}/fmap/sub-${subCounter}_magnitude2.json
        elif [[ ${iFile} == ${iDir}/${grefnames[3]} ]]; then
          scp ${iFile} ${bidsDir}/sub-${subCounter}/fmap/sub-${subCounter}_phasediff1.nii
          scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounter}/fmap/sub-${subCounter}_phasediff1.json
        fi
      fi
  done

  #EPIs - figure out epi task vs localisers based on trials.tsv, put into appropriate dir
  #go through each dir, if there is a tsv file then check first line, if task, associate with task_epi. if loc, check which
  fname=`ls ${iDir}/*epi*.nii`
  for iFile in ${fname}; do
    if [ -f ${iFile} ]; then
      firstline=`head -n 1 ${iDir}/trials.tsv`
      if ((${#firstline} == 218)); then
        #"main" - move to func - but also need to rename - sub-01_task, also depending on how many RUNS, _run01..
        scp ${iFile} ${bidsDir}/sub-${subCounter}/func/sub-${subCounter}_task-memsamp_run-${runCounter}.nii
        scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounter}/func/sub-${subCounter}_task-memsamp_run-${runCounter}.json
        scp ${iDir}/trials.tsv ${bidsDir}/sub-${subCounter}/func/trials_run-${runCounter}.tsv
        let runCounter=runCounter+1 #only for main task, with more than 1 run
        runCounter=`printf "%.2d" ${runCounter}`
      elif ((${#firstline} == 179)); then
        # motion or exemplar/category localiser
        locTask=`awk 'NR==5 {print $(NF-2)}' ${iDir}/trials.tsv`;#this outputs 'motion' or 'exemplar'
        scp ${iFile} ${bidsDir}/sub-${subCounter}/func/sub-${subCounter}_task-${locTask}Localiser.nii
        scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounter}/func/sub-${subCounter}_task-${locTask}Localiser.json
        scp ${iDir}/trials.tsv ${bidsDir}/sub-${subCounter}/func/trials_${locTask}Localiser.tsv
      fi
    fi
  done

  #T1
  fname=`ls ${iDir}/*T1*.nii`
  for iFile in ${fname}; do
    if [ -f ${iFile} ]; then
      scp ${iFile} ${bidsDir}/sub-${subCounter}/anat/sub-${subCounter}_T1w.nii
      scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounter}/anat/sub-${subCounter}_T1w.json
    fi
  done

  #zip
  gzip ${bidsDir}/sub-${subCounter}/fmap/*.nii
  gzip ${bidsDir}/sub-${subCounter}/func/*.nii
  gzip ${bidsDir}/sub-${subCounter}/anat/*.nii

done # for iDir
let subCounter=subCounter+1
subCounter=`printf "%.2d" ${subCounter}`
done < ${wd}/subNames.txt #while read
