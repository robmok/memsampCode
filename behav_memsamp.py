#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:36:03 2018

@author: robert.mok

Compute plots and accuracy based on model estimated subjective category

Notes on dataframe
- category - category of the feedback on that trial (not necessarily the dominant category for that direction). 0 for scene, 1 for face.                                         
- cat - 1 if the current category corresponds to the dominant category for this direction      
- resp - 1 if the subject responded according to the currently dominant category
        
"""
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
#mainDir = '/Users/robertmok/Documents/Postdoc_ucl/'  # mac laptop
behavDir=os.path.join(mainDir,'behav')
eventsDir=os.path.join(mainDir,'orig_events')
behavFigDir=os.path.join(mainDir,'behav')

#laptop
#mainDir='/Users/robertmok/Downloads'
#eventsDir=os.path.join(mainDir,'orig_events')

dfmodel = pd.read_pickle(mainDir + '/behav/modelsubjcat4.pkl')
#%%

saveaccdata = False

subs = range(1,34) #33 subs - range doesn't include last number
accA = np.empty(33)
accB = np.empty(33)
acc = np.empty(33)
objAcc = np.empty(33)
respPrAll = pd.DataFrame(columns=range(12), index=range(33))
respPrAllsorted = pd.DataFrame(columns=range(12), index=range(33))
for iSub in range(1, 34):
    subNum = f'{iSub:02d}'
    fnames = os.path.join(eventsDir, "sub-" + subNum + "*memsamp*." + 'tsv')
    datafiles = sorted(glob.glob(fnames))

    dfCond = pd.DataFrame()
    for iFile in datafiles:
        df = pd.read_csv(iFile, sep="\t")
        dfCond = dfCond.append(df)

    # get responses
    # flip motor across blocks
    ind1 = dfCond['keymap'] == 1  # if dfCond['keymap']==1 flip, if 0, no flip
    ind2 = dfCond['key'] == 6
    ind3 = dfCond['key'] == 1
    dfCond.loc[ind1 & ind2, 'key'] = 5
    dfCond.loc[ind1 & ind3, 'key'] = 6
    dfCond.loc[ind1 & ind2, 'key'] = 1
    # get pr resp cat A
    conds = dfCond.direction.unique()
    conds.sort()
    respPr = pd.Series(index=conds)
    for iCond in conds:
        respPr[iCond] = np.divide(
                (dfCond.loc[dfCond['direction'] == iCond, 'key'] == 6).sum(),
                len(dfCond.loc[dfCond['direction'] == iCond]))  # this count nans (prob no resp) as incorrect

    # for respPrAll plot   
    # sort conditions based on model estimated subjective cats
    subjCatConds = np.concatenate(
            [dfmodel['b'].loc[iSub-1], dfmodel['a'].loc[iSub-1]])
    cnt = 0
    for iCond in subjCatConds:
        respPrAll[cnt].iloc[iSub-1] = respPr[iCond]
        cnt = cnt+1

    # sort to plot 0:330 for everyone at the bottom of the script
    cnt = 0
    for iCond in conds:
        respPrAllsorted[cnt].iloc[iSub-1] = respPr[iCond]
        cnt = cnt+1

    # accuracy based on model subjCat
    subjCatAconds = dfmodel['a'].loc[iSub-1]
    subjCatBconds = dfmodel['b'].loc[iSub-1]
    respA = np.empty(0)
    respB = np.empty(0)
    for iCond in subjCatAconds:
        respA = np.append(respA,
                          dfCond.loc[dfCond['direction'] == iCond,'key'].values)
    for iCond in subjCatBconds:
        respB = np.append(respB,
                          dfCond.loc[dfCond['direction'] == iCond,'key'].values)
    accA[iSub-1] = sum(respA == 6)/len(respA)
    accB[iSub-1] = sum(respB == 1)/len(respB)
    acc[iSub-1] = (sum(respA == 6)+sum(respB == 1))/(len(respA)+len(respB))
    objAcc[iSub-1] = np.nansum(dfCond['resp'])/len(dfCond['resp'])

# save
if saveaccdata:
    np.savez(os.path.join(behavDir, 'memsamp_acc_subjCat_model'),
             acc=acc, accA=accA, accB=accB, objAcc=objAcc)

# %%
#plt.rcdefaults()
plt.style.use('seaborn-darkgrid')
#
saveFigs = False
fntSiz = 18

fig1, ax1 = plt.subplots()
ax1.errorbar(range(0, 12), respPrAll.mean(), yerr=respPrAll.sem(), fmt='-o')
ax1.plot(range(0, 12), respPrAll.T, '-', alpha=0.15)
ax1.set_xlabel('Direction', fontsize=fntSiz)
ax1.set_ylabel("Proportion Responded Category A", fontsize=fntSiz)
ax1.tick_params(axis='both', which='major', labelsize=fntSiz-2.5)

if saveFigs:
    plt.savefig(os.path.join(behavFigDir,
                             'behav_subjCat_response_curve_model.svg'))

# %% plot single subs - plot according to model estimation

for iSub in range(0, 33):
    plt.plot(range(0, 12), respPrAll.loc[iSub], alpha=0.2)
    plt.show()

# %% plot single subs - conds sorted from 0 to 330 for all subs

ylims = (-.05, 1.05)

for iSub in range(0, 33):
    print(iSub)
#    print(dfmodel.loc[iSub])
#    print(dfmodel['bestparams'].loc[iSub][2])
    plt.plot(range(0, 360, 30), respPrAllsorted.loc[iSub])
    plt.ylim(ylims)
    plt.show()

# %%
saveFigs = False

ylims = (-.05, 1.05)
for isub in 24, 27, 32:
    fig1, ax1 = plt.subplots()
    ax1.plot(range(0, 360, 30), respPrAllsorted.loc[isub])
    plt.ylim(ylims)
    ax1.set_xlabel('Direction', fontsize=fntSiz)
    ax1.set_ylabel("Proportion Responded Category A", fontsize=fntSiz)
    ax1.tick_params(axis='both', which='major', labelsize=fntSiz-2.5)
    plt.show()
    print(dfmodel.loc[isub])
    if saveFigs:
        plt.savefig(os.path.join(behavFigDir,
                                 'behav_subjCat_response_curve_model_sub%s.svg'
                                 % isub))
