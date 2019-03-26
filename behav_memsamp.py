#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:36:03 2018

@author: robert.mok

# category - category of the feedback on that trial (not necessarily the dominant category for that direction). 0 for scene, 1 for face.                                         

# cat - 1 if the current category corresponds to the dominant category for this direction      
                                                      
# cat1 - 1 if the last category corresponds to the currently dominant category                                                                      

# resp - 1 if the subject responded according to the currently dominant category
        
# 'aresp' means 'faceresponse' or whatever 'a' happens to be. 1 if it was a 'face' response (regardless of what the button mapping happened to be - 
# we flipped between runs). This is the raw description of what the subject called the trial, regardless of what the cue or feedback happened to be.
          
#dir and dir1 scoring mirrors resp and resp1, but for the cue.(read more to see logic behin this)


#RM notes

Figure out category bound
- Get 'direction' - cue direction (0:330)
- Only check 'cat' = 1 - dominant category
- Inspect 'category' - 0 = scene, 1 = face
THEN
- Test if 'direction's from 120-270 are the same category, if so, cat bound 1, if not, cat bound2
- If so, check if for that category, if 'category' is 0 or 1

Note down: category bound, face/scene for each category




Next: compute subjective catgeories - compute Pr respond category 0 for each dir 

    
- resp - 1 if the subject responded according to the currently dominant category

- key - the key they pressed - note it flipped between blocks









#later:  read in subjective categories

"""
      

import os
import glob
import numpy as np
import pandas as pd

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
eventsDir=os.path.join(mainDir,'orig_events')
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)

#%%



#subs = range(1,34) #33 subs - range doesn't include last number
#for iSub in subs:
#    print(f'{iSub:02d}')

iSub=1 #temp
subNum=f'{iSub:02d}'
fnames    = os.path.join(eventsDir, "sub-" + subNum + "*memsamp*." + 'tsv')
datafiles = sorted(glob.glob(fnames))

for iFile in datafiles:   
#    iFile = datafiles[1] #temp
    dat=pd.read_csv(iFile, sep="\t")
    
    if dat.loc[((dat['direction']==120)|(dat['direction']==270))&(dat['cat']==1),'category'].all():
        catRule=0
        catAconds=np.array((range(120,271,30))) 
        catBconds=np.append(np.array((range(210,331,30))),0)

    elif dat.loc[((dat['direction']==210)|(dat['direction']==0))&(dat['cat']==1),'category'].all():
        catRule=1
        catAconds=np.append(np.array((range(210,331,30))),0)
        catBconds=np.array((range(120,271,30))) 

    else: 
        catRule=9
        print("Error determining category rule")
    
#    print("Category rule %d" % catRule)


#dat.loc[((dat['direction']==120)|(dat['direction']==270))&(dat['cat']==1),['category', 'key','resp','correct']] #resp and correct are same if cat=1
#dat.loc[((dat['direction']==120)|(dat['direction']==270)),['cat','category', 'key','resp','correct']] #shows diff between resp and correct

    conds=dat.direction.unique()
    conds.sort()
    respCatPr = pd.Series(index=conds)
    for iCond in conds:
        #dat.loc[dat['direction']==iCond]
        #dat.loc[dat['direction']==iCond,['rawdirection', 'rawcategory']]

        respCatPr[iCond] = np.divide(dat.loc[dat['direction']==iCond,'resp'].sum(),len(dat.loc[dat['direction']==iCond,'resp'])) #this count nans (prob no resp) as incorrect
        
#        print("cond %s, sum %d, len %d" % (iCond, dat.loc[dat['direction']==iCond,'resp'].sum(), len(dat.loc[dat['direction']==iCond,'resp'])))
#        print(dat.loc[dat['direction']==iCond,'resp'])
        
        
#    print(respCatPr) #sub-01 getting it most except 120/300 (most incorrect) - i.e. up-down rule
    for iBcond in catBconds:
       respCatPr[iBcond] = 1-respCatPr[iBcond]











        



