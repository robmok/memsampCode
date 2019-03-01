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
import clarte as cl
import pandas as pd
import matplotlib.pyplot as plt
import nilearn.plotting as nip
import nibabel as nib

#roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'

os.chdir(featDir)

# - could first try the LOO one with 'trials'. but check if it takes run into account (i think it does).
# - see if easy to use block as test set

#data
#sub-01_run-01_block_T1_fwhm2.feat
# - looks like  i need to load in the 2 blocks of training data, then single trials for the remaining block (test)
#sub-01_run-01_trial_T1_fwhm2.feat


#sub-01_task-memsamp_run-01_events.tsv #in bidsdir
# - load in this
# - append run number
# - append path to image - match 0:30:270 degrees to condition 1:12, trialwise (N.B. cope number is not the same for trialwise! 7 trials)

# - load in all 3 runs then merge the 3 dfs

iSub=1
subNum=f'{iSub:02d}'
iRun=1

condPath=os.path.join(bidsDir, 'sub-' + subNum, 'func','sub-' + subNum + '_task-memsamp_run-0' + str(iRun) +'_events.tsv')

#temp path for laptop
condPath='/Users/robertmok/Documents/Postdoc_ucl/sub-01_task-memsamp_run-01_events.tsv'
dfCond=pd.read_csv(condPath, sep='\t')
dfCond = dfCond[dfCond['trial_type']=='cue'] #remove feedback trials

#add run number
iRun=1
dfCond['run']=pd.Series(np.ones((len(dfCond)))*iRun,index=dfCond.index)
#dfCond.loc[:,'run2']=pd.Series(np.ones((len(dfCond)))*iRun,index=dfCond.index)

# add path to match cue condition and trial number - cope1:7 is dir0, trial1:7
# /Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat/sub-01_run-01_trial_T1_fwhm0.feat/stats/cope1.nii.gz

conds=dfCond.direction.unique
iCope=1
for iCond in conds:
    for iTrial in range(1,8): #calculate cope number
        #make a list and append to it
        imPath=os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun) +'_trial_T1_fwhm0.feat','stats','cope' + (str(iCope)) + '.nii.gz')


        iCope=iCope+1


#how to load in runs into dfCond? can it be multidimensional df? or hardcode nRuns?
        
        
#%%

subs=range(1,34)
#for iSub in subs:

iRun=1
iCope=1

datDir=os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun) +'_block_T1_fwhm2.feat/stats/cope' + str(iCope) + '.nii.gz')
