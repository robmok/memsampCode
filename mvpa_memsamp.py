#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:48:06 2019

@author: robert.mok
"""
import sys
sys.path.append('/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/')
import os
import glob
import numpy as np
#np.set_printoptions(precision=2, suppress=True) # Set numpy to print only 2 decimal digits for neatness
#from nilearn import image # Import image processing tool
#import clarte as cl
import pandas as pd
import matplotlib.pyplot as plt
#import nilearn.plotting as nip
#import nibabel as nib

#roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'

os.chdir(featDir)

#%%

# - first try the LOO one with 'trials'. then load in blocks

#sub-01_task-memsamp_run-01_events.tsv #in bidsdir
# - load in this
# - append run number
# - append path to image - match 0:30:270 degrees to condition 1:12, trialwise (N.B. cope number is not the same for trialwise! 7 trials)

# - load in all 3 runs then merge the 3 dfs

iSub=1
subNum=f'{iSub:02d}'

dfCond=pd.DataFrame() #main df with all runs


if iSub in {9,12,16,26}:
    runs = range(1,5) #4 runs
else:
    runs = range(1,4) #3 runs

for iRun in runs:
    condPath=os.path.join(bidsDir, 'sub-' + subNum, 'func','sub-' + subNum + 
                          '_task-memsamp_run-0' + str(iRun) +'_events.tsv')
    #temp path for laptop
    #condPath='/Users/robertmok/Documents/Postdoc_ucl/sub-01_task-memsamp_run-0' + str(iRun) + '_events.tsv'
    
    # df to load in and organise run-wise data
    df = pd.read_csv(condPath, sep='\t')
    df = df[df['trial_type']=='cue'] #remove feedback trials
    df['run'] = pd.Series(np.ones((len(df)))*iRun,index=df.index) #add run number
    #df.loc[:,'run2']=pd.Series(np.ones((len(df)))*iRun,index=df.index) #alt way - better/worse?
    
    # add path to match cue condition and trial number - cope1:7 is dir0 trial1:7   
    conds=df.direction.unique()
    conds.sort()
    copeNum=1 #counter
    imPath=[]
    for iCond in conds:
        for iTrial in range(1,8): #calculate cope number
            #make a list and append to it
            imPath.append(os.path.join(featDir, 'sub-' + subNum + '_run-0'
                                       + str(iRun) +'_trial_T1_fwhm0.feat',
                                       'stats','cope' + (str(copeNum)) + '.nii.gz'))
            copeNum=copeNum+1
    df['imPath']=pd.Series(imPath,index=df.index)
    dfCond = dfCond.append(df) #append to main df
        
#%%

subs=range(1,34)
#for iSub in subs:

iRun=1
iCope=1

datDir=os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun) +'_block_T1_fwhm2.feat/stats/cope' + str(iCope) + '.nii.gz')
