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


"""
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
behavDir=os.path.join(mainDir,'behav')
eventsDir=os.path.join(mainDir,'orig_events')
behavFigDir=os.path.join(mainDir,'behav')


#laptop
#mainDir='/Users/robertmok/Downloads'
#eventsDir=os.path.join(mainDir,'orig_events')

#%%

subs = range(1,34) #33 subs - range doesn't include last number
accA = np.empty(33)
accB = np.empty(33)
acc  = np.empty(33)
objAcc = np.empty(33)
respPrAll = pd.DataFrame(columns=range(12),index=range(33))
for iSub in range(1,34):
#    iSub=1 #temp
    subNum=f'{iSub:02d}'
    fnames    = os.path.join(eventsDir, "sub-" + subNum + "*memsamp*." + 'tsv')
    datafiles = sorted(glob.glob(fnames))
    
    dfCond=pd.DataFrame()
    for iFile in datafiles:   
    #    iFile = datafiles[0] #temp
        df=pd.read_csv(iFile, sep="\t")
        dfCond = dfCond.append(df)
        
    catAconds=np.array((range(120,271,30))) 
    catBconds=np.append(np.array((range(0,91,30))),[300,330])

    #get response and determine subjective category bound
    #flip - need double check if keymap is what i think it is. looks ok
    ind1=dfCond['keymap']==1 #if dfCond['keymap'] == 1: #flip, if 0, no need flip
    ind2=dfCond['key']==6
    ind3=dfCond['key']==1
    dfCond.loc[ind1&ind2,'key']=5
    dfCond.loc[ind1&ind3,'key']=6
    dfCond.loc[ind1&ind2,'key']=1
    #get subjective category
    conds=dfCond.direction.unique()
    conds.sort()
    respPr = pd.Series(index=conds)
    for iCond in conds:
        respPr[iCond] = np.divide((dfCond.loc[dfCond['direction']==iCond,'key']==6).sum(),len(dfCond.loc[dfCond['direction']==iCond])) #this count nans (prob no resp) as incorrect
    
    subjCatAconds=np.sort(respPr.index[respPr>0.5].values.astype(int))
    subjCatBconds=np.sort(respPr.index[respPr<0.5].values.astype(int))
        
    #unless:   
    if iSub==5: #move 240 and 270 to catA
        subjCatAconds = np.append(subjCatAconds,[240,270])
        subjCatBconds = subjCatBconds[np.invert((subjCatBconds==240)|(subjCatBconds==270))] #remove
    elif iSub==10: #move 270 to cat B
        subjCatBconds = np.sort(np.append(subjCatBconds,270))
        subjCatAconds = subjCatAconds[np.invert(subjCatAconds==270)]
    elif iSub == 17:#move 30 to cat B
        subjCatBconds = np.sort(np.append(subjCatBconds,30))
        subjCatAconds = subjCatAconds[np.invert(subjCatAconds==30)]
    elif iSub==24: #move 120 to cat A
        subjCatAconds = np.sort(np.append(subjCatAconds,120))
        subjCatBconds = subjCatBconds[np.invert(subjCatBconds==120)]
    elif iSub==27:#move 270 to cat A
        subjCatAconds = np.sort(np.append(subjCatAconds,270))
        subjCatBconds = subjCatBconds[np.invert(subjCatBconds==270)]
    
    #for respPrAll plot
    subjCatBcondsSorted=np.concatenate([subjCatBconds[subjCatBconds>=300],subjCatBconds[subjCatBconds<300]]) #rearrange to make the directions within a cat next to each other (300 and 330 need to be next to 0)
    subjCatConds = np.concatenate([subjCatBcondsSorted, subjCatAconds])
    cnt=0
    for iCond in subjCatConds:
        respPrAll[cnt].iloc[iSub-1] = respPr[iCond]
        cnt=cnt+1

    #accuracy
    respA=np.empty(0) 
    respB=np.empty(0) 
    for iCond in subjCatAconds:
        respA = np.append(respA, dfCond.loc[dfCond['direction']==iCond,'key'].values)
    for iCond in subjCatBconds:
        respB = np.append(respB, dfCond.loc[dfCond['direction']==iCond,'key'].values)        
        
    accA[iSub-1]=sum(respA==6)/len(respA)
    accB[iSub-1]=sum(respB==1)/len(respB)
    acc[iSub-1]=(sum(respA==6)+sum(respB==1))/(len(respA)+len(respB))
    
    objAcc[iSub-1]=np.nansum(dfCond['resp'])/len(dfCond['resp'])

#save
#np.savez(os.path.join(behavDir, 'memsamp_acc_subjCat'),acc=acc,accA=accA,accB=accB,objAcc=objAcc)


#    if np.any((dfCond['direction']==0)&(dfCond['rawdirection']==135)):
#        print('sub-%s: a' % subNum)
#    elif np.any((dfCond['direction']==0)&(dfCond['rawdirection']==45)):
#        print('sub-%s: b' % subNum)
#    else:
#        print('???')





    # plot respPr for different (counterbalanced) motor response runs - checking if people are not switching responses
    # subs who have a flat resp line ~0.5 for one of the motor resp conds - 1 (worse for the 2 runs!), 16, 31

#    respPr1 = pd.Series(index=conds)
#    respPr2 = pd.Series(index=conds)
#    respPr3 = pd.Series(index=conds)
#    respPr4 = pd.Series(index=conds)
#    for iCond in conds:        
#        respPr1[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0)]))
#        respPr2[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1)]))
#        
#        #respPr3 is with 1 block, respPr4 with 2 (except 4 block subs)
#        if sum(dfCond['keymap']==0)>sum(dfCond['keymap']==1):            
#            respPr3[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1)]))
#            respPr4[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0)]))
#        elif sum(dfCond['keymap']==0)<sum(dfCond['keymap']==1):
#            respPr3[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0)]))
#            respPr4[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1)]))
#        else: #if 4 runs, just select one set - subs 9,12,16,26
#            respPr3[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==0)]))
#            respPr4[iCond] = np.divide((dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1),'key']==6).sum(),len(dfCond.loc[(dfCond['direction']==iCond)&(dfCond['keymap']==1)]))
#        
#        
##    plt.plot(pd.concat([respPr1,respPr2],axis=1))
#    plt.plot(pd.concat([respPr3,respPr4],axis=1))
#    plt.show()
    
#%%
plt.style.use('seaborn-darkgrid')

saveFigs = False
fntSiz=14

#ax = respPrAll.T.plot(legend=False)

fig1, ax1 = plt.subplots()
ax1.plot(range(0,12),respPrAll.T,alpha=0.2)
ax1.errorbar(range(0,12),respPrAll.mean(), yerr=respPrAll.sem(), fmt='-o',color='b')
ax1.set_xlabel('Direction',fontsize=fntSiz)
ax1.set_ylabel('Proportion Responded Category A',fontsize=fntSiz)
ax1.tick_params(axis='both', which='major', labelsize=fntSiz-2)

if saveFigs:
    plt.savefig(os.path.join(behavFigDir,'behav_subjCat_response_curve.pdf'))