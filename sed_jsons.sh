
wd='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampData'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
#codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'

# Note - if want to pass BIDS validation, comment out the lines editing RepetitionTime. Siemens give TR per slice, so bids validator will complain diff to jsons
# fmriprep just looks at the jsons so fine to edit it at the final stage

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
  fname=${subDir}/fmap/sub-${subCounterP}_magnitude2.json
  TE2=`jq -r '.EchoTime' ${fname}` #get TE2
  fname=${subDir}/fmap/sub-${subCounterP}_phasediff.json
  tmp=$(mktemp)
  jq --argjson TE1val ${TE1} '. + {EchoTime1: $TE1val}' ${fname} > ${tmp} && mv "$tmp" ${fname} # add TE1; argjson for number
  jq --argjson TE2val ${TE2} '. + {EchoTime2: $TE2val}' ${fname} > ${tmp} && mv "$tmp" ${fname} # add TE2; argjson for number
  jq 'del(.EchoTime)' ${fname} > ${tmp} && mv "$tmp" ${fname}
  #jq '. + {"EchoTime2": .EchoTime} | del(.EchoTime)' ${fname} > ${tmp} && mv "$tmp" ${fname} #change TE to TE2, remove TE

  # add field - 'IntendedFor' with the epi files (.nii.gz) - get names of .nii.gz files from the epi, then insert
  dir=${subDir}/fmap
  fname=`ls ${dir}/*.json 2> /dev/null`
  for iFile in ${fname}; do
    #insert 'IntendedFor' into each fieldmap json in iFile
    epiDir=${subDir}/func
    epiFnames=`ls ${epiDir}/*.nii.gz | xargs -n 1 basename` #must not have whole path, just from /func
    i=1
    for iEpi in ${epiFnames}; do
      tmp=$(mktemp)
      if (($i==1)); then
        jq --arg epi func/${iEpi} '. + {IntendedFor: [$epi]}' ${iFile} > ${tmp} && mv "$tmp" ${iFile} # add the field first
      else
        jq --arg epi func/${iEpi} '.IntendedFor += [$epi]' ${iFile} > ${tmp} && mv "$tmp" ${iFile} # add other fnames to the field
      fi
      (( i++ ))
    done
  done


  #EPIs - add TaskName, edit TR?-no
  dir=${subDir}/func
  fname=`ls ${dir}/*memsamp*.json 2> /dev/null`
  for iFile in ${fname}; do
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
    jq --arg TaskName memsamp '. + {TaskName: $TaskName}' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #works
    jq '.RepetitionTime = 2.8' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #
    #calculate EffectiveEchoSpacing: Effective Echo Spacing (s) = 1/(BandwidthPerPixelPhaseEncode * MatrixSizePhase). in
    #"PhaseEncodingSteps": 64,"PixelBandwidth": 260 - #any of the fmap images have this info; 1/(64*260)
    jq --argjson EES 0.00006009615385 '. + {EffectiveEchoSpacing: $EES}' ${iFile} > ${tmp} && mv "$tmp" ${iFile}
  done
  fname=`ls ${dir}/*motionLoc*.json 2> /dev/null`
  for iFile in ${fname}; do
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
    jq --arg TaskName motionLocaliser '. + {TaskName: $TaskName}' ${iFile} > ${tmp} && mv "$tmp" ${iFile}
    jq '.RepetitionTime = 2.8' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #
    jq --argjson EES 0.00006009615385 '. + {EffectiveEchoSpacing: $EES}' ${iFile} > ${tmp} && mv "$tmp" ${iFile}

  done
  fname=`ls ${dir}/*exemplarLoc*.json 2> /dev/null`
  for iFile in ${fname}; do
    tmp=$(mktemp)
    sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #this removes a control character from this "^P"
    jq --arg TaskName exemplarLocaliser '. + {TaskName: $TaskName}' ${iFile} > ${tmp} && mv "$tmp" ${iFile}
    jq '.RepetitionTime = 2.8' ${iFile} > ${tmp} && mv "$tmp" ${iFile} #
    jq --argjson EES 0.00006009615385 '. + {EffectiveEchoSpacing: $EES}' ${iFile} > ${tmp} && mv "$tmp" ${iFile}
  done

  let subCounter=subCounter+1
done
