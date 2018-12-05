
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampData'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
#codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

cd ${wd}

subCounter=1

printf "Starting script sed_jsons.sh. This will add required info into json files to be BIDS compliant. \n"
for iSub in {01..33}; do
  subCounterP=`printf "%.2d" ${subCounter}` #zero pad subject number
  printf "Organising subject ${subCounterP} \n"
  subDir=${bidsDir}/sub-${subCounterP}

  #anat
  dir=${subDir}/anat
  fname=`ls ${dir}/*.json 2> /dev/null`
  for iFile in ${fname}; do
    #edit "PatientSex" value to "" for ALL json files - anat, fmap, func
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
    jq '.RepetitionTime = 2' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #
  done

  #fmap
  dir=${subDir}/fmap
  fname=`ls ${dir}/*.json 2> /dev/null`
  for iFile in ${fname}; do
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
  done
  # get TE1 from mag1, and add "EchoTime1" and "EchoTime2" to phasediff .json (TE2 already in 'EchoTime' in phasediff json)
  fname=${subDir}/fmap/sub-${subCounterP}_magnitude1.json
  TE1=`jq -r '.EchoTime' ${fname}` #get TE1
  fname=${subDir}/fmap/sub-${subCounterP}_phasediff.json
  tmp=$(mktemp)
  jq '. + {"EchoTime2": .EchoTime} | del(.EchoTime)' ${fname} > ${tmp} && mv "$tmp" ${fname} #change TE to TE2, remove TE
  jq --argjson TE1val ${TE1} '. + {EchoTime1: $TE1val}' ${fname} > ${tmp} && mv "$tmp" ${fname} # add TE1; argjson for number

  #EPIs - add TaskName, edit TR?
  dir=${subDir}/func
  fname=`ls ${dir}/*memsamp*.json 2> /dev/null`
  for iFile in ${fname}; do
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
    jq --arg TaskName memsamp '. + {TaskName: $TaskName}' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #works
    jq '.RepetitionTime = 2.8' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #
  done
  fname=`ls ${dir}/*motionLoc*.json 2> /dev/null`
  for iFile in ${fname}; do
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
    jq --arg TaskName motionLocaliser '. + {TaskName: $TaskName}' ${iFile} > ${tmp} && mv "$tmp" ${iFile}
    jq '.RepetitionTime = 2.8' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #
  done
  fname=`ls ${dir}/*exemplarLoc*.json 2> /dev/null`
  for iFile in ${fname}; do
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
    jq --arg TaskName exemplarLocaliser '. + {TaskName: $TaskName}' ${iFile} > ${tmp} && mv "$tmp" ${iFile}
    jq '.RepetitionTime = 2.8' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #
  done

  let subCounter=subCounter+1
done
