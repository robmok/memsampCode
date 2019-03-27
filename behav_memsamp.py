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

Note down: objective category bound, face/scene for each category





Compute subjective catgeories - compute Pr respond category 0 for each dir 
    
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
#codeDir=os.path.join(mainDir,'memsampCode')
#os.chdir(codeDir)

#laptop
#mainDir='/Users/robertmok/Downloads'
#eventsDir=os.path.join(mainDir,'orig_events')

#%%

subs = range(1,34) #33 subs - range doesn't include last number
for iSub in subs:
    #iSub=1 #temp
    subNum=f'{iSub:02d}'
    fnames    = os.path.join(eventsDir, "sub-" + subNum + "*memsamp*." + 'tsv')
    datafiles = sorted(glob.glob(fnames))
    
    dat=pd.DataFrame()
    for iFile in datafiles:   
    #    iFile = datafiles[0] #temp
        df=pd.read_csv(iFile, sep="\t")
        dat = dat.append(df)
        
    #get objective category
    if dat.loc[((dat['direction']==120)|(dat['direction']==270))&(dat['cat']==1),'category'].all():
        catAconds=np.array((range(120,271,30))) 
        catBconds=np.append(np.array((range(0,91,30))),[300,330])
    elif dat.loc[((dat['direction']==210)|(dat['direction']==0))&(dat['cat']==1),'category'].all():
        catAconds=np.append(np.array((range(210,331,30))),0)
        catBconds=np.array((range(30,181,30))) 
    else: 
        print("Error determining category rule")

    #get response and determine subjective category bound
    #flip - need double check if keymap is what i think it is. looks ok
    ind1=dat['keymap']==1 #if dat['keymap'] == 1: #flip, if 0, no need flip
    ind2=dat['key']==6
    ind3=dat['key']==1
    dat.loc[ind1&ind2,'key']=5
    dat.loc[ind1&ind3,'key']=6
    dat.loc[ind1&ind2,'key']=1
    
    #could also check aresp?
    
    #get 1) accuracy for each condition and 2)subjective category
    conds=dat.direction.unique()
    conds.sort()
    respCatPr = pd.Series(index=conds)
    respPr = pd.Series(index=conds)
    for iCond in conds:
        respCatPr[iCond] = np.divide(dat.loc[dat['direction']==iCond,'resp'].sum(),len(dat.loc[dat['direction']==iCond])) #this count nans (prob no resp) as incorrect
        respPr[iCond] = np.divide((dat.loc[dat['direction']==iCond,'key']==6).sum(),len(dat.loc[dat['direction']==iCond])) #this count nans (prob no resp) as incorrect
        
    #subjective catgory bound based on responses
    subjCatAconds=np.sort(respPr.index[respPr>0.5].values.astype(int))
    subjCatBconds=np.sort(respPr.index[respPr<0.5].values.astype(int))
    
    print("sub-%s, objective catA:  %s" % (subNum,np.array2string(catAconds)))
    print("sub-%s, subjective catA: %s" % (subNum,np.array2string(subjCatAconds)))
    print("sub-%s, objective catB:  %s" % (subNum,np.array2string(catBconds)))
    print("sub-%s, subjective catB: %s" % (subNum,np.array2string(subjCatBconds)))

#in subj-01, in run 1, there is one more in one cat than the other....
    # - how to decide when more than one in the other? 
    # - inspect how many have this - and how much (~.5?) are there nans?
    # - how to decide if ~ 0.5?
        # if around this, then revert to prior (obj)?
    
# see a few weird outliers where one direction is the opposite - check how many, and how much > 0.5
    # - is this true or just an error?




#%%
#print(respPr>0.5) # get subjective cat


#    plt.plot(respPr)
#    plt.show()
#    plt.plot(respCatPr)
#    plt.show()


#%%

#dat.loc[dat['direction']==iCond,['rawdirection', 'rawcategory']]


#dat.loc[((dat['direction']==120)|(dat['direction']==270))&(dat['cat']==1),['category', 'key','resp','correct']] #resp and correct are same if cat=1
#dat.loc[((dat['direction']==120)|(dat['direction']==270)),['cat','category', 'key','resp','correct']] #shows diff between resp and correct
        

#  print("cond %s, sum %d, len %d" % (iCond, dat.loc[dat['direction']==iCond,'resp'].sum(), len(dat.loc[dat['direction']==iCond,'resp'])))
#  print(dat.loc[dat['direction']==iCond,'resp'])


#    print(respCatPr) #sub-01 getting it most except 120/300 (most incorrect) - i.e. up-down rule




        



