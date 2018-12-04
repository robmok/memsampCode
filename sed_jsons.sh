
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

#add 'TaskName' to epis

#edit "PatientSex" value to ""

#fmap - get TE1 from mag1, and add "EchoTime1" and "EchoTime2" to phasediff .json (TE2 already in 'EchoTime' in phasediff json)

fname=${subDir}/anat/



#temp
fname=${subDir}/func/sub-01_task-memsamp_run-01_bold

#both work now
tmp=$(mktemp)
sed -e 's/"PatientSex": ""/"PatientSex": ""/' ${fname}.json > ${tmp} && mv "$tmp" ${fname}.json #this removes a control character from this "^P"
jq --arg TaskName memsamp '. + {TaskName: $TaskName}' ${fname}.json > ${tmp} && mv "$tmp" ${fname}.json #works


#TE1 and TE2 now




#  ${subDir}/fmap
#  ${subDir}/func




  let subCounter=subCounter+1
done
