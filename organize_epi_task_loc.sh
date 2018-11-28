
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampData'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
#codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

cd ${wd}

#get subject directory names
if ! [ -f subNames.txt ]; then
  s=`ls -d *0*` #all dirs with subs have 0s
  echo "${s}" >> subNames.txt #"" so outputs line by line
fi

#organize and rename GRE/EPI/task_epi/localizer_epi files
#subCounter=1
subCounter=1 #3 since i did 2 already manually

printf "Starting script organize_epi_task.sh. This will organise memsamp fMRI data into BIDS compliant directories. \n"
while read iSub; do
  subCounterP=`printf "%.2d" ${subCounter}` #zero pad subject number
  printf "Organising subject ${subCounterP}, aka ${iSub} \n"
  mkdir ${bidsDir}/sub-${subCounterP}
  mkdir ${bidsDir}/sub-${subCounterP}/fmap
  mkdir ${bidsDir}/sub-${subCounterP}/func
  mkdir ${bidsDir}/sub-${subCounterP}/anat

  cd ${wd}/${iSub}

  runCounter=1 #for task epi - set here so it increases in the iDir loop
  runCounter=`printf "%.2d" ${runCounter}`
  # rm ${bidsDir}/sub-${subCounterP}/func/sub-${subCounterP}*bold*tsv

  #dirs=`ls -d *`
  dirs=`find . -regex '.*/[0-9]*' | sort -V` #only dirs with numbers; sorts in ascending order even without zeropadding
  for iDir in ${dirs}; do #go through each dir

  #FIELDMAPS
  # fname=`ls ${iDir}/*gre*.nii 2> /dev/null` # 2> /dev/null suppresses error messages (here, file doesnt exist) (sends them away)
  # for iFile in ${fname}; do
  #     if [ -f ${iFile} ]; then
  #       #rename gre file depending on type
  #       grefnames[1]='gre_field_mapping_1acq_rl_e1.nii'
  #       grefnames[2]='gre_field_mapping_1acq_rl_e2.nii'
  #       grefnames[3]='gre_field_mapping_1acq_rl_e2_ph.nii'
  #       if [[ ${iFile} == ${iDir}/${grefnames[1]} ]]; then #~= means ==; Use the =~ operator to make regular expression comparsions:
  #         scp ${iFile} ${bidsDir}/sub-${subCounterP}/fmap/sub-${subCounterP}_magnitude1.nii
  #         scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounterP}/fmap/sub-${subCounterP}_magnitude1.json # ${#iFile}-4 - to remove .nii
  #       elif [[ ${iFile} == ${iDir}/${grefnames[2]} ]]; then
  #         scp ${iFile} ${bidsDir}/sub-${subCounterP}/fmap/sub-${subCounterP}_magnitude2.nii
  #         scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounterP}/fmap/sub-${subCounterP}_magnitude2.json
  #       elif [[ ${iFile} == ${iDir}/${grefnames[3]} ]]; then
  #         scp ${iFile} ${bidsDir}/sub-${subCounterP}/fmap/sub-${subCounterP}_phasediff.nii
  #         scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounterP}/fmap/sub-${subCounterP}_phasediff.json
  #       fi
  #     fi
  # done

  #EPIs - figure out epi task vs localisers based on trials.tsv, put into appropriate dir
  #go through each dir, if there is a tsv file then check first line, if task, associate with task_epi. if loc, check which
  fname=`ls ${iDir}/*epi*.nii 2> /dev/null`
  for iFile in ${fname}; do
    if [ -f ${iFile} ]; then
      firstline=`head -n 1 ${iDir}/trials.tsv`
      if ((${#firstline} == 218)); then
        #"main" - move to func - but also need to rename - sub-01_task, also depending on how many RUNS, _run01..
        # scp ${iFile} ${bidsDir}/sub-${subCounterP}/func/sub-${subCounterP}_task-memsamp_run-${runCounter}_bold.nii
        # scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounterP}/func/sub-${subCounterP}_task-memsamp_run-${runCounter}_bold.json
        scp ${iDir}/trials.tsv ${bidsDir}/sub-${subCounterP}/func/sub-${subCounterP}_task-memsamp_run-${runCounter}_events.tsv
        let runCounter=runCounter+1 #only for main task, with more than 1 run
        runCounter=`printf "%.2d" ${runCounter}`
      elif ((${#firstline} == 179)); then
        # motion or exemplar/category localiser
        locTask=`awk 'NR==5 {print $(NF-2)}' ${iDir}/trials.tsv`;#this outputs 'motion' or 'exemplar'
        # scp ${iFile} ${bidsDir}/sub-${subCounterP}/func/sub-${subCounterP}_task-${locTask}Localiser_bold.nii
        # scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounterP}/func/sub-${subCounterP}_task-${locTask}Localiser_bold.json
        scp ${iDir}/trials.tsv ${bidsDir}/sub-${subCounterP}/func/sub-${subCounterP}_task-${locTask}Localiser_events.tsv
      fi
    fi
  done

  #T1
 #  fname=`ls ${iDir}/*T1*.nii 2> /dev/null`
 #  for iFile in ${fname}; do
 #    if [ -f ${iFile} ]; then
 #      scp ${iFile} ${bidsDir}/sub-${subCounterP}/anat/sub-${subCounterP}_T1w.nii
 #      scp ${iFile:0:${#iFile}-4}.json ${bidsDir}/sub-${subCounterP}/anat/sub-${subCounterP}_T1w.json
 #    fi
 #  done
 # done # for iDir
#zip
# gzip ${bidsDir}/sub-${subCounterP}/fmap/*.nii
# gzip ${bidsDir}/sub-${subCounterP}/func/*.nii
# gzip ${bidsDir}/sub-${subCounterP}/anat/*.nii
#subject counter
let subCounter=subCounter+1
done < ${wd}/subNames.txt #while read
