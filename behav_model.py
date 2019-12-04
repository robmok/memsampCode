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


#mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'  # love06
mainDir = '/Users/robertmok/Documents/Postdoc_ucl/'  # mac laptop
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
params = [15, 195, 1]  # bound 1, bound 2, and sigma (gaussian SD)


#deterimine which is the closest bound

def angdiff(x, y):
    import numpy as np
    return np.arctan2(np.sin(x-y), np.cos(x-y))


angdiff1 = angdiff(np.radians(dat['direction'].values), params[0])
angdiff2 = angdiff(np.radians(dat['direction'].values), params[1])

# closests to bound 1 or 2
ind1 = abs(angdiff1) < abs(angdiff2)  # True: closer to bound 1, False: to 2

# get the dat closer to bound 1 - is it positive or negative (so cat A or B)
# if positive, then compute pr for category A one
# if negative, compute 1-pr for category B
    # - should I double the probabilities, since it's one-tailed?

ind1pos = angdiff1 > 0
ind1neg = angdiff1 < 0
ind2pos = angdiff2 > 0
ind2neg = angdiff2 > 0

# indexing 
dat['direction'][ind1 & ind1pos]
dat['direction'][ind1 & ind1neg]

x = angdiff1[ind1 & ind1pos]
y = angdiff1[ind1 & ind1neg]

# for ind1pos (ind2pos), comput pr cat A (cat B) given that bound
# for ~ind1pos (~ind2pos), comput pr cat B (cat A) given that bound

# hmm... need to figure out how to match with behav pr... maybe what brad said is relevant







# compute activation given bound
mu = 0
sigma = params[2]
rv = norm(mu, sigma)
plt.plot(1-rv.pdf(x))  # for cat A
plt.show()
plt.plot(1-rv.pdf(y))  # for cat B
plt.show()





## testing activations make sense
#x = np.radians(np.array([0., 30., 60., 120., 150., 180., 210., 240, 270, 300., 330.]))
#bound = np.radians(15)
#
## computed activation given bound
#mu = 0
#sigma = params[2]
##sigma = 0.1
#rv = norm(mu, sigma)
#plt.plot(1-rv.pdf(angdiff(x,bound)))

#from scipy.stats import vonmises
#mu = 0
#kappa = 1
#rv = vonmises(kappa, mu)
#plt.plot(1-rv.pdf(angdiff(x,bound)))  # 1-pr



# assign category to each side of the boundary...






# for each trial, check if it's on the right side of the boundary
# then compute (1 - pr it's this far away, one-tailed); gaussian distribution with sigma

# - for each bound point, associate it with cat A or cat B; if far, the pr's will still add up correctly (1-pr)









