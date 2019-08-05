#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 18:34:15 2019

Plotting '-all' conditions: 12-way-all, subjCat-all, dir-all

@author: robert.mok
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks", color_codes=True)
#import bootstrapped.bootstrap as bs
#import bootstrapped.stats_functions as bs_stats
import scipy.stats as stats
from statsmodels.stats.multitest import fdrcorrection as fdr
#from statsmodels.stats.multitest import multipletests as multest

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06

codeDir=os.path.join(mainDir,'memsampCode')
#codeDir='/Users/robertmok/Documents/Postdoc_ucl/memsampCode' #laptop

roiDir=os.path.join(mainDir,'mvpa_roi')

figDir=os.path.join(mainDir,'mvpa_roi/figs_mvpa_roi')
behavDir=os.path.join(mainDir,'behav')
eventsDir=os.path.join(mainDir,'orig_events')

# laptop
#roiDir='/Users/robertmok/Documents/Postdoc_ucl/mvpa_roi/' 
                                
os.chdir(codeDir)

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'svm' # 'svm', 'crossNobis', 'mNobis' - for subjCat-orth and -all
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-all' # subjCat-orth, '12-way', 'dir' (opposite dirs), 'ori' (orthogonal angles)

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))

#load in subjCat
subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))
#load in behav acc
behav=np.load(os.path.join(behavDir, 'memsamp_acc_subjCat.npz'))
locals().update(behav) #load in each variable into workspace

#%% subjCat-all - organise
plt.style.use('seaborn-darkgrid')

fntSiz=14

saveFigs = False

exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)
    
#df1 = pd.DataFrame(columns=df.columns,index=['mean', 'sem'])
#for roi in df.columns.values[0:-1]:

#subjCat sig
#roi='V2vd_rh'
#roi='hMT_lh'
roi='MDroi_area8c_lh'

#RDM cat sig
#roi='MDroi_area9_rh'

#12-way sig
#roi='V2vd_rh'
#roi='hMT_rh'

#dir sig
#roi='SPL1_rh'

#ori sig
#roi='V1vd_lh'

ylims = [0.45, 0.55]

# plot mean and std across subs and plot (if including all subs, this ignores that some might have diff nConds per cat)
nCond=12
nSubs=33
rdmAll = np.zeros((nCond,nCond,nSubs))
rdm = np.zeros((nCond,nCond))
iu = np.triu_indices(nCond,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
il = np.tril_indices(nCond,-1) #to make symmetric rdm
for iSub in range(0,nSubs):
    rdm[iu] = df[roi].iloc[iSub]
    rdm[il] = rdm.T[il]
    rdmAll[:,:,iSub] = rdm

rdmMean = rdmAll[:,:,indSubs].mean(axis=2)
rdmSE  = rdmAll[:,:,indSubs].std(axis=2)/np.sqrt(sum(indSubs))
#
##% subjCat-all - plot 1
#ax = plt.figure(figsize=(8,4))
#ctuple=np.array((0.1,0.3,0.5))
#for iCond in range(0,nCond//2):
#    ax = plt.figure(figsize=(4,3))
#    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
#    ctuple = ctuple+0.05
#    ylim1, ylim2 = plt.ylim()
#    plt.ylim(ylims[0],ylims[1])
#
#ax = plt.figure(figsize=(8,4))
#ctuple=np.array((0.5,0.3,0.1))
#for iCond in range(nCond//2,nCond):
#    ax = plt.figure(figsize=(4,3))
#    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
#    ctuple = ctuple+0.05
#    ylim1, ylim2 = plt.ylim()
#    plt.ylim(ylims[0],ylims[1])
    
#average values, ignoring the current training category (values 0)
rdmAll[rdmAll==0]=np.nan #so can nanmean

ylims = [0.45, 0.55]
ctuple=np.array((0.1,0.3,0.5))
#rdmMeanA = np.nanmean(rdmMean[0:nCond//2,0:nCond],axis=0)
rdmMeanA = np.nanmean(rdmAll[0:nCond//2,0:nCond,indSubs],axis=0).mean(axis=1)
rdmSEA = np.nanstd(np.nanmean(rdmAll[0:nCond//2,0:nCond,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))

ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanA, yerr=rdmSEA, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])

ctuple=np.array((0.5,0.3,0.1))
#rdmMeanB = np.nanmean(rdmMean[nCond//2:nCond,0:nCond],axis=0)
rdmMeanB = np.nanmean(rdmAll[nCond//2:nCond,0:nCond,indSubs],axis=0).mean(axis=1)
rdmSEB = np.nanstd(np.nanmean(rdmAll[nCond//2:nCond,0:nCond,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))

ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanB, yerr=rdmSEB, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])

#average across conds

ctuple=np.array((0.1,0.3,0.5))
rdmMeanAll = np.nanmean(rdmAll[:,:,indSubs],axis=0).mean(axis=1)
rdmSEAll = np.nanstd(np.nanmean(rdmAll[:,:,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))
ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanAll, yerr=rdmSEAll, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])
plt.title(roi,fontsize=fntSiz)

#%% all dirs - plotting to show above chance decoding for stimulus (similar to 12-way but averaging pair-wise svms)
plt.style.use('seaborn-darkgrid')

#subjCat sig
roi='hMT_lh'
roi='MDroi_area8c_lh'

#RDM cat sig
#roi='MDroi_area9_rh'

#12-way sig
#roi='hMT_rh'

#ori sig
#roi='EVC_lh'

#other
#roi='EVC_rh'
#roi='V3a_lh'
#roi='V3a_rh'

#rdm stuff
nCond=12
nSubs=33
rdmAll = np.zeros((nCond,nCond,nSubs))
rdm = np.zeros((nCond,nCond))
iu = np.triu_indices(nCond,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
il = np.tril_indices(nCond,-1) #to make symmetric rdm
for iSub in range(0,nSubs):
    rdm[iu] = df[roi].iloc[iSub]
    rdm[il] = rdm.T[il]
    rdmAll[:,:,iSub] = rdm
rdmAll[rdmAll==0]=np.nan #so can nanmean

#get indices to rearrange so the directions are the same across subs (since subjCat-all is arranged )
condInd=np.empty((12,33),dtype=int)
for iSub in range(33):
    conds=np.append(subjCat.loc[iSub][0],subjCat.loc[iSub][1],axis=0)
    condInd[:,iSub]=np.argsort(conds)

#load in behav data to rotate the direction conditions around (since 'direction' is coded so its same for all subs [rotated around], and 'rawdirection' is the actual direction presented, or something similar)
# make index for which subjects needs to flipped
ind=np.full((33),True)
for iSub in range(1,34):
    subNum=f'{iSub:02d}'
    fnames    = os.path.join(eventsDir, "sub-" + subNum + "*memsamp*run-01*." + 'tsv')
    iFile = sorted(glob.glob(fnames))
    dfBehav=pd.read_csv(iFile[0], sep="\t")
    if np.any((dfBehav['direction']==0)&(dfBehav['rawdirection']==135)):
        ind[iSub] = False

# arrange the directions first (with sorted indices) - using inds in step 1 above, then flip - using inds in step 2 above
rdmArr = np.zeros((nCond,nCond,nSubs))
for iSub in range(33):
    rdmArr[:,:,iSub] = rdmAll[condInd[:,iSub],:,iSub] 
    rdmArr[:,:,iSub] = rdmArr[:,condInd[:,iSub],iSub]


#average across conds
ctuple=np.array((0.1,0.3,0.5))
rdmMeanAll = np.nanmean(rdmArr[:,:,indSubs],axis=0).mean(axis=1)
rdmSEAll = np.nanstd(np.nanmean(rdmArr[:,:,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))
ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanAll, yerr=rdmSEAll, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])
plt.title(roi,fontsize=fntSiz)

#if saveFigs:
#    plt.savefig(os.path.join(figDir,'mvpaROI_svm_pairwiseDirs_' + roi + '_toedit.pdf'))
#plt.show()


t,p=stats.ttest_1samp(np.nanmean(rdmArr[:,:,indSubs],axis=0).T,0.5)
print(p)

#%% subjCat-all - plot 2
#prototype - 6 conds each, for prototype is middle of conds 3&4
    
#separately
#rdmMean[[3+1,3-1],3] #for row (condition) 3, these are adjacent directions (1 away)
#rdmMean[[3+2,3-2],3] #for row 3, these are 2 away
#
#rdmMean[[4+1,4-1],4] 
#rdmMean[[4+2,4-2],4] 

#for each one - check if coding is right
avDist = np.empty((12,5))
for iDist in range(0,5):
    for iC in range(0,12):
        ind=np.array((iC+iDist+1,iC-(iDist+1)))
#        if np.any(ind>=12):
#            ind[ind>=12] = ind[ind>=12]-12
#        avDist[iC,iDist]=rdmMean[[ind[0],ind[1]],iC].mean()
        avDist[iC,iDist]=rdmMean[[np.mod(iC+iDist+1,12),np.mod(iC-(iDist+1),12)],iC].mean()
        
#plt.imshow(avDist,cmap='viridis')
#plt.colorbar()

#maybe only the 'middle' prototype conditions make sense (for conds 0:11, conds 2,3,8,9)
ax = plt.figure(figsize=(8,4))
ctuple=np.array((0.5,0.3,0.1))
for iCond in 2,3,8,9: #range(0,11):
    ax = plt.figure(figsize=(4,3))
    ax = plt.errorbar(range(0,5),avDist[iCond,:], fmt='-o', color=ctuple)
    ctuple = ctuple+0.025
    ylim1, ylim2 = plt.ylim()
    plt.ylim(ylims[0],ylims[1])


#OR, plot similar to these two, averaged (without checking similarity to each other)
#rdmMean[[3+2,3-1],3]  #3+2=5, 3-1=2
#rdmMean[[4+1,4-2],4] #4+1=5, 4-2=2
#++

#%%12-way-all

# test the shape: 
# more senory modulation, strongest decoding in the middle of each category, lowest at boundary
# task based / abstract - step function

# results
# visualsing; looks more like a noisy U-shaped curve; which is consistent with sensory modulation; lowest decoding acc at boundary

# but may want to test quantitatively on each subject rather than group - more consistent with peak-valley-peak, or inverted-U, or flat-valley-flat (harder to distinguish with first?)

# if look at median, MT looks a bit more like peak-valley-peak; V2 also a little. PFC just flat

#selecting subjects (based on equal number of dirs in each category)
# - atm taking from subjCat-all; since that saved the subjCat conditions) - need to load that in and run the "exclSubs" bit above first

#if not excluding subjects
indSubs=np.ones(33,dtype=bool)
#
rois = list(df)
dfMean = pd.DataFrame(columns=rois,index=range(0,12))
dfSem  = pd.DataFrame(columns=rois,index=range(0,12))
#tstat  = []
#pval   = []
df1=df.copy() #reorganise so in stimulus direction order
for roi in rois:
    ind12way=np.empty(33,dtype=int)
    indLen1=np.empty(33,dtype=int) #nDirs in first cat
    for iSub in range(0,33):
        ind=np.where(np.diff(subjCat[iSub][1])>30)
        ind12way[iSub]=ind[0][0]+1
        indLen1[iSub]=len(subjCat[iSub][0])
        df1[roi].iloc[iSub]=np.append(np.append(df[roi].iloc[iSub][0:indLen1[iSub]],df[roi].iloc[iSub][indLen1[iSub]+ind12way[iSub]:]),df[roi].iloc[iSub][indLen1[iSub]:indLen1[iSub]+ind12way[iSub]])
        #checking if manupulation is correct
    #    print(np.append(subjCat[iSub][0],np.append(subjCat[iSub][1][ind12way[iSub]:],subjCat[iSub][1][0:ind12way[iSub]])))
    #    print(np.diff(np.append(subjCat[iSub][0],np.append(subjCat[iSub][1][ind12way[iSub]:],subjCat[iSub][1][0:ind12way[iSub]]))))
    
    #    print(subjCat[iSub])
    #    print(df[roi].iloc[iSub])
    #    print(np.append(np.append(df[roi].iloc[iSub][0:indLen1[iSub]],df[roi].iloc[iSub][indLen1[iSub]+ind12way[iSub]:]),df[roi].iloc[iSub][indLen1[iSub]:indLen1[iSub]+ind12way[iSub]]))
    
    #compute mean sem - note edited to df1  here
    dfMean[roi] = np.mean(np.asarray(np.stack(df1[roi].iloc[indSubs])),axis=0)
    dfSem[roi] = np.asarray(np.stack(df1[roi].iloc[indSubs])).std(axis=0)/np.sqrt(sum(indSubs))
#    statsTmp=stats.ttest_1samp(np.asarray(np.stack(df1[roi].iloc[indSubs])),0.5)
#    tstat.append(statsTmp.statistic)
#    pval.append(statsTmp.pvalue)

    
#ax=dfMean.iloc[0:33,:].T.plot(figsize=(20,5),kind="bar",yerr=dfSem.T,ylim=(.55,.65))

roi='V1vd_lh' # up and down; median bit more flat
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='V1vd_rh' # U shaped; median U shaped
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')


roi='V2vd_rh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='hMT_lh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='MDroi_area8c_lh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')

#%%dir-all

exclSubs = True
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)

rois = list(df)
dfMean = pd.DataFrame(columns=rois,index=range(0,6))
dfSem  = pd.DataFrame(columns=rois,index=range(0,6))
df1=df.copy()
for roi in rois:
    #compute mean sem
    dfMean[roi] = np.mean(np.asarray(np.stack(df1[roi].iloc[indSubs])),axis=0)
    dfSem[roi] = np.asarray(np.stack(df1[roi].iloc[indSubs])).std(axis=0)/np.sqrt(sum(indSubs))

roi='V1vd_lh' # up and down; median bit more flat
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='V1vd_rh' # U shaped; median U shaped
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')


roi='V2vd_rh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='hMT_lh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='MDroi_area8c_lh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')

#%% univariate scatter plots, violin plots

roi='V2vd_rh'
dfPlt=pd.DataFrame(np.asarray(np.stack(df1[roi].iloc[indSubs])))
ax = sns.catplot(data=dfPlt,height=8,aspect=2, kind="swarm",zorder=1)
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
ax2 = sns.catplot(data=dfPlt,height=8,aspect=2, kind="violin", inner=None,zorder=2)
ax2 = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)

roi='hMT_lh'
dfPlt=pd.DataFrame(np.asarray(np.stack(df1[roi].iloc[indSubs])))
ax = sns.catplot(data=dfPlt,height=8,aspect=2, kind="swarm",zorder=1)
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
ax2 = sns.catplot(data=dfPlt,height=8,aspect=2, kind="violin", inner=None,zorder=2)
ax2 = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)

roi='MDroi_area8c_lh'
dfPlt=pd.DataFrame(np.asarray(np.stack(df1[roi].iloc[indSubs])))
ax = sns.catplot(data=dfPlt,height=8,aspect=2, kind="swarm",zorder=1)
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
ax2 = sns.catplot(data=dfPlt,height=8,aspect=2, kind="violin", inner=None,zorder=2)
ax2 = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
