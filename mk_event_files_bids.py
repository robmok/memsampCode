#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:07:13 2018

@author: robert.mok
"""
import os
import glob
import pandas as pd

bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
eventsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/orig_events'
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
        trials1=dat[['cuetime', 'direction', 'category','rt', 'correct']]
        trials1.insert(1, 'duration', 1) #stim duration
        trials1.insert(2, 'trial_type', 'cue')
        trials1.columns = trials1.columns.str.replace('cuetime', 'onset')
        trials1.columns = trials1.columns.str.replace('rt','response_time')
        #trials1.rename(columns={'cuetime': 'onset', 'rt': 'response_time'}, inplace=True) #works, but throws a weird error
        #trials1.rename({'cuetime':'onset', 'rt':'response_time'}, axis='columns') #better, but pandas v0.21
        trials2=dat[['feedtime','direction', 'category','rt', 'correct']]
        #trials2=dat[['feedtime','category','cat','rawcategory']] #need to add duration, trial_type (feedback/category)
        trials2.insert(1, 'duration', 1) #feedback duration
        trials2.insert(2, 'trial_type', 'feedback')
        trials2.columns = trials2.columns.str.replace('feedtime', 'onset')
        trials2.columns = trials1.columns.str.replace('rt','response_time')
        trials=pd.concat([trials1, trials2])

        # ??? category and cat are different?
        #check notes - what is cat, cat1 - different to category

        
        #mv original tsv file out
        os.rename(iFile,  os.path.join(eventsDir, os.path.basename(iFile)))                               
        #save as iFile
        trials.to_csv(iFile,sep='\t', header=True, index=False)
        
        #localisers- need timing?