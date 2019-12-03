#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:56:07 2019

@author: robert.mok
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from scipy.stats import norm


mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'  # love06
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)



# %% load in data

#for iSub in range(1, nSubs+1):
iSub = 1

subNum = f'{iSub:02d}'
dfCond = pd.DataFrame()  # main df with all runs
if iSub in {9, 12, 16, 26}:
    runs = range(1, 5)  # 4 runs
else:
    runs = range(1, 4)  # 3 runs
for iRun in runs:
    condPath = os.path.join(mainDir, 'orig_events', 'sub-' + subNum +
                            '_task-memsamp_run-0' + str(iRun) +'_events.tsv')
    df = pd.read_csv(condPath, sep='\t')
    df['run'] = pd.Series(np.ones((len(df)))*iRun, index=df.index)  # add run number
    dfCond = dfCond.append(df)  # append to main df
    
#flip key when keymap is flipped
ind1=dfCond['keymap']==1 #if dfCond['keymap'] == 1: #flip, if 0, no need flip
ind2=dfCond['key']==6
ind3=dfCond['key']==1
dfCond.loc[ind1&ind2,'key']=5
dfCond.loc[ind1&ind3,'key']=6
dfCond.loc[ind1&ind2,'key']=1


#get responses
conds = dfCond.direction.unique()
conds.sort()
dat = dfCond[['direction','key']]

# remove nans
dat = dat[~np.isnan(dat['key'])]

#for iCond in conds:
#    dat[dat['direction']==iCond]


# %% 
starting_params = [15, 195, 1]  # bound 1, bound 2, and sigma (gaussian SD)


#deterimine which is the closest bound

#dat['direction']-starting_params[0]
#dat['direction']-starting_params[1]




# assign category to each side of the boundary...




# for each trial, check if it's on the right side of the boundary
# then compute (1 - pr it's this far away, one-tailed); gaussian distribution with sigma













