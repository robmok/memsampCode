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

from scipy import optimize as opt



#mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'  # love06
mainDir = '/Users/robertmok/Documents/Postdoc_ucl/'  # mac laptop
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)


# %% load in data

#for iSub in range(1, nSubs+1):
iSub = 2

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

# bound 1 and 2
angdiff1 = angdiff(np.radians(dat['direction'].values), np.radians(params[0]))
angdiff2 = angdiff(np.radians(dat['direction'].values), np.radians(params[1]))

# closest to bound 1 or 2 
ind1 = abs(angdiff1) < abs(angdiff2)  # True: closer to bound 1, False: to 2
ind2 = abs(angdiff1) > abs(angdiff2)

# get the dat closer to bound 1 - is it positive or negative (so cat A or B)
# if positive, then compute pr for category A one
# if negative, compute 1-pr for category B
    # - should I double the probabilities, since it's one-tailed?

ind1pos = angdiff1 > 0
ind1neg = angdiff1 < 0
ind2pos = angdiff2 > 0
ind2neg = angdiff2 < 0


# for ind1pos (ind2pos), comput pr cat A (cat B) given that bound
# for ~ind1pos (~ind2pos), comput pr cat B (cat A) given that bound

# - assess clockwise from 15 if it's cat A. if its closer to 15 (30, 60, 90) 
# then compute 1-pr from 15. if closer to other bound 195 (120, 150, 180), assess
# if cat A, but comput 1-pr from 195
# - assess clockwise from 195 if it's cat A. if it's closer to 195, then compute
# pr (opposite of above) from 195. if closer to 15, compute pr from 15.

# - note need to code to figure this out. when unequal num of conds across cats,
# not always 3-3. ACTUALLY i already do this with which is closer (pos / neg).. maybe ok

# catA
angdiff1[ind1 & ind1pos]
angdiff2[ind2 & ind2neg]
# catB
angdiff1[ind1 & ind1neg]
angdiff2[ind2 & ind2pos]

# conditions
catA1 = sorted(dat['direction'][ind1 & ind1pos].unique())
catA2 = sorted(dat['direction'][ind2 & ind2neg].unique())
catB1 = sorted(dat['direction'][ind1 & ind1neg].unique())
catB2 = sorted(dat['direction'][ind2 & ind2pos].unique())

# normal distribution
rv = norm(0, params[2])

## catA
#1-rv.pdf(angdiff1[dat['direction'].isin(catA1)])
#1-rv.pdf(angdiff2[dat['direction'].isin(catA2)])
## cat B
#1-rv.pdf(angdiff1[dat['direction'].isin(catB1)])
#1-rv.pdf(angdiff2[dat['direction'].isin(catB2)])

# response
# if correct, as above - 1-pr
# if incorrect, as above, but take pr
# SO - instead of flipping for cat, do the same thing, but flip the pr's for correct/incorrect

#dat.loc[dat['direction'].isin(catA1), 'key'] == 1  # correct
#dat.loc[dat['direction'].isin(catA1), 'key'] == 6  # incorrect

1-rv.pdf(angdiff1[(dat['direction'].isin(catA1)) & (dat['key'] == 1)])  # correct
rv.pdf(angdiff1[(dat['direction'].isin(catA1)) & (dat['key'] == 6)])  # incorrect

1-rv.pdf(angdiff2[(dat['direction'].isin(catA2)) & (dat['key'] == 1)])
rv.pdf(angdiff2[(dat['direction'].isin(catA2)) & (dat['key'] == 6)])

1-rv.pdf(angdiff1[(dat['direction'].isin(catB1)) & (dat['key'] == 6)])
rv.pdf(angdiff1[(dat['direction'].isin(catB1)) & (dat['key'] == 1)])

1-rv.pdf(angdiff2[(dat['direction'].isin(catA2)) & (dat['key'] == 6)])
rv.pdf(angdiff2[(dat['direction'].isin(catA2)) & (dat['key'] == 1)])

resps1 = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                  (dat['key'] == 1)],
                         angdiff2[(dat['direction'].isin(catA2)) &
                                  (dat['key'] == 1)],
                         angdiff1[(dat['direction'].isin(catB1)) &
                                  (dat['key'] == 6)],
                         angdiff2[(dat['direction'].isin(catA2)) &
                                  (dat['key'] == 6)]))

resps2 = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                  (dat['key'] == 6)],
                         angdiff2[(dat['direction'].isin(catA2)) &
                                  (dat['key'] == 6)],
                         angdiff1[(dat['direction'].isin(catB1)) &
                                  (dat['key'] == 1)],
                         angdiff2[(dat['direction'].isin(catA2)) &
                                  (dat['key'] == 1)]))

# sum of log pr's (to check exp this result, compare to np.prod of pr's)
# neg log? is this is the negLogLik? - so that it's positive and minimize it
negLog = -np.sum(np.log(np.concatenate((1-rv.pdf(resps1), rv.pdf(resps2))))) 


# %%
# ...optimize this with bound1, bound2, and SD param..., with sensible limits
# - will it work if bound is the same? all on one side, maybe error..


bounds = [(0., np.radians(359)), (0., np.radians(359)), [0., 5.]]

def runit(params, dat=dat):      
    
    def angdiff(x, y):
        import numpy as np
        return np.arctan2(np.sin(x-y), np.cos(x-y))
    
    bound1 = params[0]
    bound2 = params[1]
    sigma = params[2]

    # compute stuff
    # bound 1 and 2
    angdiff1 = angdiff(np.radians(dat['direction'].values), np.radians(bound1))
    angdiff2 = angdiff(np.radians(dat['direction'].values), np.radians(bound2))

    # closests to bound 1 or 2
    ind1 = abs(angdiff1) < abs(angdiff2)  # True: closer to bound 1, False: to 2
    ind2 = abs(angdiff1) > abs(angdiff2)

    ind1pos = angdiff1 > 0
    ind1neg = angdiff1 < 0
    ind2pos = angdiff2 > 0
    ind2neg = angdiff2 < 0
    
    # conditions
    catA1 = sorted(dat['direction'][ind1 & ind1pos].unique())
    catA2 = sorted(dat['direction'][ind2 & ind2neg].unique())
    catB1 = sorted(dat['direction'][ind1 & ind1neg].unique())
    catB2 = sorted(dat['direction'][ind2 & ind2pos].unique())
    
    # normal distribution
    rv = norm(0, sigma)
    
    resps1 = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                      (dat['key'] == 1)],
                             angdiff2[(dat['direction'].isin(catA2)) &
                                      (dat['key'] == 1)],
                             angdiff1[(dat['direction'].isin(catB1)) &
                                      (dat['key'] == 6)],
                             angdiff2[(dat['direction'].isin(catA2)) &
                                      (dat['key'] == 6)]))

    resps2 = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                  (dat['key'] == 6)],
                             angdiff2[(dat['direction'].isin(catA2)) &
                                      (dat['key'] == 6)],
                             angdiff1[(dat['direction'].isin(catB1)) &
                                      (dat['key'] == 1)],
                             angdiff2[(dat['direction'].isin(catA2)) &
                                      (dat['key'] == 1)]))

    # sum of log pr's (to check exp this result, compare to np.prod of pr's)
    negLog = -np.sum(np.log(np.concatenate((1-rv.pdf(resps1), rv.pdf(resps2))))) 

    return negLog

method = 'Nelder-Mead'
res = opt.minimize(runit, params, method=method, bounds=bounds)
bestparams = res.x

# ++ better

if bestparams[0] < bestparams[1]:
    n_cata_resps_side1 = (dat.loc[(dat['direction'] > bestparams[0]) & (dat['direction'] < bestparams[1]), 'key'].values == 1).sum()
    n_catb_resps_side1 = (dat.loc[(dat['direction'] > bestparams[0]) & (dat['direction'] < bestparams[1]), 'key'].values == 6).sum()
    # using OR operator here
    n_cata_resps_side2 = (dat.loc[(dat['direction'] > bestparams[1]) | (dat['direction'] < bestparams[0]), 'key'].values == 1).sum()
    n_catb_resps_side2 = (dat.loc[(dat['direction'] > bestparams[1]) | (dat['direction'] < bestparams[0]), 'key'].values == 6).sum()
elif bestparams[0] > bestparams[1]:
    n_cata_resps1_side1 = (dat.loc[(dat['direction'] > bestparams[1]) & (dat['direction'] < bestparams[0]), 'key'].values == 1).sum()
    n_catb_resps1_side1 = (dat.loc[(dat['direction'] > bestparams[1]) & (dat['direction'] < bestparams[0]), 'key'].values == 6).sum()
    # using OR operator here
    n_cata_resps2_side2 = (dat.loc[(dat['direction'] > bestparams[0]) | (dat['direction'] < bestparams[1]), 'key'].values == 1).sum()
    n_catb_resps2_side2 = (dat.loc[(dat['direction'] > bestparams[0]) | (dat['direction'] < bestparams[1]), 'key'].values == 6).sum()

# correct, incorrect, correct, incorrect (so most resps should be on the correct side)
print([n_cata_resps_side1, n_cata_resps_side2, n_catb_resps_side2, n_catb_resps_side1])






#maybe first check params 0 and 1 - if 0 < 1, then use above, else opposite






## compute activation given bound
#mu = 0
#sigma = params[2]
#rv = norm(mu, sigma)
#plt.plot(1-rv.pdf(x))  # for cat A
#plt.show()
#plt.plot(1-rv.pdf(y))  # for cat B
#plt.show()


## testing activations make sense
#x = np.radians(np.array([30., 60., 120., 150., 180., 210., 240, 270, 300., 330., 0.]))
#bound = np.radians(15)
#bound = np.radians(225)

# computed activation given bound
#mu = 0
#sigma = params[2]
#sigma = 0.1
#rv = norm(mu, sigma)
#plt.plot(1-rv.pdf(angdiff(x,bound)))
#plt.ylim((0, 1))

#from scipy.stats import vonmises
#mu = 0
#kappa = 1
#rv = vonmises(kappa, mu)
#plt.plot(1-rv.pdf(angdiff(x,bound)))  # 1-pr



# assign category to each side of the boundary...






# for each trial, check if it's on the right side of the boundary
# then compute (1 - pr it's this far away, one-tailed); gaussian distribution with sigma

# - for each bound point, associate it with cat A or cat B; if far, the pr's will still add up correctly (1-pr)









