#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:07:13 2018

Make BIDS-compliant event files - run after running 'organize_epi_task_loc.sh' (organises imaging and tsv files from memsampData to memsampBids)

@author: robert.mok
"""
import os
import glob
import pandas as pd

bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
eventsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/orig_events'
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/feat_timing'
os.chdir(bidsDir)

subs = range(1,34) #33 subs - range doesn't include last number
for iSub in subs:
    print(f'{iSub:02d}')
    #iSub=1 #temp
    subNum=f'{iSub:02d}'
    fnames    = os.path.join(bidsDir, "sub-" + subNum, 'func', "*memsamp*." + 'tsv')
    datafiles = sorted(glob.glob(fnames))
    
    for iFile in datafiles:   
        #iFile = datafiles[0] #temp - testing
        dat=pd.read_csv(iFile, sep="\t")
        
        # Variables I want: Onset, duration, trial_type, response_time 
        # variable names: cuetime, feedtime, direction, category, rt, correct, aresp
        # extract cue conditions (time, motionDir), and separately the feedback (time, category); then merge the dataframes after
        #onset, duration, trial_type, response_time 
        trials1=dat[['cuetime', 'direction']] #'category', 'rt', 'correct' - # empty rts sometime, bids doesnt like empty tsv cells
        trials1.insert(1, 'duration', 1) #stim duration
        trials1.insert(2, 'trial_type', 'cue')
        trials1.columns = trials1.columns.str.replace('cuetime', 'onset')
        #trials1.columns = trials1.columns.str.replace('rt','response_time') 
        #trials1.rename(columns={'cuetime': 'onset', 'rt': 'response_time'}, inplace=True) #works, but throws a weird error
        #trials1.rename({'cuetime':'onset', 'rt':'response_time'}, axis='columns') #better, but pandas v0.21
        trials2=dat[['feedtime','direction']] #'category', 'rt', 'correct'
        #trials2=dat[['feedtime','category','cat','rawcategory']] #need to add duration, trial_type (feedback/category)
        trials2.insert(1, 'duration', 1) #feedback duration
        trials2.insert(2, 'trial_type', 'feedback')
        trials2.columns = trials2.columns.str.replace('feedtime', 'onset')
        #trials2.columns = trials1.columns.str.replace('rt','response_time')
        trials=pd.concat([trials1, trials2])
        
        #mv original tsv file out
        os.rename(iFile,  os.path.join(eventsDir, os.path.basename(iFile)))                               
        #save as iFile
        trials.to_csv(iFile,sep='\t', header=True, index=False)
        
        #for FSL timing file
        conds=trials["direction"].sort_values().unique() #gets direction conditions
        for iCond in conds:
            # block-wise estimation of betas
            # cue direction
            tmp=trials.loc[(trials['trial_type'] == 'cue') & (trials['direction'] == iCond)]
            cuetiming=tmp[['onset','duration']]
            cuetiming.insert(2, 'value', 1) #stim value
            fname1=os.path.join(featDir,os.path.splitext(os.path.basename(iFile))[0] + "_" + str(int(iCond)) + "cue_block.txt")
            cuetiming.to_csv(fname1,sep='\t', header=False, index=False)
            #feedback - based on cue direction
            tmp=trials.loc[(trials['trial_type'] == 'feedback') & (trials['direction'] == iCond)]
            feedtiming=tmp[['onset','duration']]
            feedtiming.insert(2, 'value', 1) #stim value
            fname1=os.path.join(featDir,os.path.splitext(os.path.basename(iFile))[0] + "_" + str(int(iCond)) + "feed_block.txt")
            feedtiming.to_csv(fname1,sep='\t', header=False, index=False)
        
            # trial-wise estimation of betas
            trlCnt=1
            for iTrl in range(0,len(cuetiming)): #number of trials in each condition
                # cue direction
                cuetimingTrl=cuetiming.iloc[iTrl]
                cuetimingTrl=cuetimingTrl.reset_index() #for 1 trial, saves as 1 column; here, reset
                cuetimingTrl=pd.pivot_table(cuetimingTrl, columns=cuetimingTrl['index']) #use index from the resetted index above
                cuetimingTrl = cuetimingTrl[['onset','duration','value']]
                fname1=os.path.join(featDir,os.path.splitext(os.path.basename(iFile))[0] + "_" + str(int(iCond)) + "cue_trial" + str(trlCnt) + ".txt")
                cuetimingTrl.to_csv(fname1,sep='\t', header=False, index=False)
                # feedback - based on cue direction
                feedtimingTrl=feedtiming.iloc[iTrl]
                feedtimingTrl=feedtimingTrl.reset_index() #for 1 trial, saves as 1 column; here, reset
                feedtimingTrl=pd.pivot_table(feedtimingTrl, columns=feedtimingTrl['index']) #use index from the resetted index above
                feedtimingTrl = cuetimingTrl[['onset','duration','value']]
                fname1=os.path.join(featDir,os.path.splitext(os.path.basename(iFile))[0] + "_" + str(int(iCond)) + "feed_trial" + str(trlCnt) + ".txt")
                feedtimingTrl.to_csv(fname1,sep='\t', header=False, index=False)
                trlCnt=trlCnt+1
        
        #********
        #feedback - based on category presented (need to figure this out) - separate GLM
        
        
        
        

    #Localisers
    #motion loc
    fnameLoc = os.path.join(bidsDir, "sub-" + subNum, 'func', "*motionLoc*." + 'tsv')
    iFileLoc = glob.glob(fnameLoc)
    trials=dat[['cuetime', 'direction']] #'rt', 'correct' - # empty rts sometime, bids doesnt like empty tsv cells
    trials.insert(1, 'duration', 1) #stim duration
    trials.columns = trials.columns.str.replace('cuetime', 'onset')
    #mv original tsv file out
    os.rename(iFileLoc[0],  os.path.join(eventsDir, os.path.basename(iFileLoc[0])))                               
    #save as iFile
    trials.to_csv(iFileLoc[0],sep='\t', header=True, index=False)

    #exemplar loc
    fnameLoc = os.path.join(bidsDir, "sub-" + subNum, 'func', "*exemplarLoc*." + 'tsv')
    iFileLoc = glob.glob(fnameLoc)
    trials=dat[['cuetime', 'category']] #'rt', 'correct'
    trials.insert(1, 'duration', 1) #stim duration
    trials.columns = trials.columns.str.replace('cuetime', 'onset')

    #mv original tsv file out
    os.rename(iFileLoc[0],  os.path.join(eventsDir, os.path.basename(iFileLoc[0])))                               
    #save as iFile
    trials.to_csv(iFileLoc[0],sep='\t', header=True, index=False)
        
        
        
        
        
        
        
