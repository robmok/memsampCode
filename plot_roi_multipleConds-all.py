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

decodeFeature = 'subjCat' # subjCat-orth, '12-way', 'dir' (opposite dirs), 'ori' (orthogonal angles)

fname = (os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                      distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                      '_fwhm' + str(fwhm) + '_' + imDat))

fname = fname + '_trialwise_outputs_MT_lh'  # new, just with subjCat
#fname = fname + '_trialwise_outputs_mMFG_lh'
#
fname = fname + '.pkl'

df=pd.read_pickle(fname)

#load in subjCat
#subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))
#load in behav acc
#behav=np.load(os.path.join(behavDir, 'memsamp_acc_subjCat.npz'))
behav=np.load(os.path.join(behavDir, 'memsamp_acc_subjCat_model.npz'))
locals().update(behav) #load in each variable into workspace


## model estimated subjective category
dfmodel = pd.read_pickle(mainDir + '/behav/modelsubjcatfinal.pkl')


# %% plot subjCat condition wise classifier predictions / probabilities


saveFigs = True

fntSiz=20

# exclude subs with unequal conds in each cat for now
exclSubs = False
if exclSubs:
    indSubs=np.zeros(33,dtype=bool)
    for iSub in range(33):
        if len(dfmodel['a'].loc[iSub]) == len(dfmodel['b'].loc[iSub]):
            indSubs[iSub] = 1
else:
    indSubs=np.ones(33,dtype=bool)

acc_per_dir = np.zeros([33, 12])
proba_per_dir = np.zeros([33, 12])
for iSub in range(0,33):
    acc_per_dir[iSub] = df['acc_per_dir'][iSub]
    proba_per_dir[iSub] = df['proba_per_dir'][iSub]

#plt.plot(acc_per_dir[indSubs].mean(axis=0))
#plt.show()
#
#plt.plot(proba_per_dir[indSubs].mean(axis=0))
#plt.show()
#
#roi = 'mMFG_lh'
roi = 'MT_lh'

acc_mean = acc_per_dir[indSubs].mean(axis=0)
acc_sem = np.std(acc_per_dir[indSubs], axis=0) / np.sqrt(indSubs.sum())

plt.errorbar(np.arange(12), acc_mean, acc_sem)
plt.ylim([.33, .66])
plt.title('Left MT', fontsize=fntSiz)
#plt.title('Left mMFG', fontsize=fntSiz)
plt.xlabel('Direction', fontsize=fntSiz)
plt.ylabel('Category Decoding Accuracy', fontsize=fntSiz)
plt.xticks(fontsize=fntSiz-2)
plt.yticks(fontsize=fntSiz-2)
plt.tight_layout
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_svm_subjCat_12dirs_outputs_' + roi + '.pdf'), bbox_inches="tight")
plt.show()



# t-test on acc
import scipy.stats as stats
stats.ttest_1samp(acc_per_dir[indSubs], .5)
#stats.ttest_1samp(proba_per_dir[indSubs], .5)




#%% subjCat-all - organise
plt.style.use('seaborn-darkgrid')

fntSiz=14

saveFigs = False

# exclude subs with unequal conds in each cat for now
exclSubs = True
if exclSubs:
    indSubs=np.zeros(33,dtype=bool)
    for iSub in range(33):
        if len(dfmodel['a'].loc[iSub]) == len(dfmodel['b'].loc[iSub]):
            indSubs[iSub] = 1
else:
    indSubs=np.ones(33,dtype=bool)
#df1 = pd.DataFrame(columns=df.columns,index=['mean', 'sem'])
#for roi in df.columns.values[0:-1]:

#subjCat sig
roi='hMT_lh'
#roi='MDroi_area8c_lh'

##RDM cat sig
#roi='MDroi_area9_rh'
#
##12-way sig
#roi='hMT_rh'
#
##ori sig
#roi='EVC_lh'

ylims = [0.4875, 0.5225]
ylims = [0.48, 0.53]  # nanmedian below

# plot mean and std across subs and plot (if including all subs, this ignores that some might have diff nConds per cat)
nCond=12
nSubs=33  # uses indSubs below to remove excluded subs
rdmAll = np.zeros((nCond,nCond,nSubs))
rdm = np.zeros((nCond,nCond))
iu = np.triu_indices(nCond,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
il = np.tril_indices(nCond,-1) #to make symmetric rdm
for iSub in range(0,nSubs):
    rdm[iu] = df[roi].iloc[iSub]
    rdm[il] = rdm.T[il]
    rdmAll[:,:,iSub] = rdm

#flip half the subs (direction counterbalanced)- shouldn't matter since sorted by cat, but in case stim direction makes a diff, this might help
ind=np.full((33),True)
for iSub in range(1,34):
    subNum=f'{iSub:02d}'
    fnames    = os.path.join(eventsDir, "sub-" + subNum + "*memsamp*run-01*." + 'tsv')
    iFile = sorted(glob.glob(fnames))
    dfBehav=pd.read_csv(iFile[0], sep="\t")
    if np.any((dfBehav['direction']==0)&(dfBehav['rawdirection']==135)):
        ind[iSub-1] = False
rdmAlltmp = rdmAll.copy()       
rdmAll[0:6,0:6,ind]  = rdmAlltmp[6:12,6:12,ind]
rdmAll[6:12,6:12,ind] = rdmAlltmp[0:6,0:6,ind]
rdmAll[0:6,6:12,ind]  = rdmAlltmp[6:12,0:6,ind]
rdmAll[6:12,0:6,ind]  = rdmAlltmp[0:6,6:12,ind]

rdmMean = rdmAll[:,:,indSubs].mean(axis=2)
rdmSE  = rdmAll[:,:,indSubs].std(axis=2)/np.sqrt(sum(indSubs))

##% subjCat-all - plot 1
#ax = plt.figure(figsize=(8,4))
#ctuple=np.array((0.1,0.3,0.5))
#for iCond in range(0,nCond//2):
#    ax = plt.figure(figsize=(4,3))
#    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
#    ctuple = ctuple+0.05
##    ylim1, ylim2 = plt.ylim()
##    plt.ylim(ylims[0],ylims[1])
#
#ax = plt.figure(figsize=(8,4))
#ctuple=np.array((0.5,0.3,0.1))
#for iCond in range(nCond//2,nCond):
#    ax = plt.figure(figsize=(4,3))
#    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
#    ctuple = ctuple+0.05
##    ylim1, ylim2 = plt.ylim()
##    plt.ylim(ylims[0],ylims[1])
    
#average values, ignoring the current training category (values 0)
rdmAll[rdmAll==0]=np.nan #so can nanmean

ctuple=np.array((0.1,0.3,0.5))
#rdmMeanA = np.nanmean(rdmMean[0:nCond//2,0:nCond],axis=0)
rdmMeanA = np.nanmean(rdmAll[0:nCond//2,0:nCond,indSubs],axis=0).mean(axis=1)
#rdmMeanA = np.nanmedian(np.nanmean(rdmAll[0:nCond//2,0:nCond,indSubs],axis=0), axis=1)
rdmSEA = np.nanstd(np.nanmean(rdmAll[0:nCond//2,0:nCond,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))

ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanA, yerr=rdmSEA, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])

ctuple=np.array((0.5,0.3,0.1))
#rdmMeanB = np.nanmean(rdmMean[nCond//2:nCond,0:nCond],axis=0)
rdmMeanB = np.nanmean(rdmAll[nCond//2:nCond,0:nCond,indSubs],axis=0).mean(axis=1)
#rdmMeanB = np.nanmedian(np.nanmean(rdmAll[nCond//2:nCond,0:nCond,indSubs],axis=0), axis=1)
rdmSEB = np.nanstd(np.nanmean(rdmAll[nCond//2:nCond,0:nCond,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))

ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanB, yerr=rdmSEB, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])

#average across conds
ctuple=np.array((0.1,0.3,0.5))
rdmMeanAll = np.nanmean(rdmAll[:,:,indSubs],axis=0).mean(axis=1)
#rdmMeanAll = np.nanmedian(np.nanmean(rdmAll[:,:,indSubs],axis=0), axis=1)
rdmSEAll = np.nanstd(np.nanmean(rdmAll[:,:,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))
ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanAll, yerr=rdmSEAll, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])
plt.title(roi,fontsize=fntSiz)


# %% new subjcat-all replotting

# each dir is compared to 11 directions, from itself (if dir is 150, the first one is 150-180)
# e.g. cats for iSub=0
#[[150.0, 180.0, 210.0, 240.0, 270.0, 300.0],
# [0.0, 30.0, 60.0, 90.0, 120.0, 330.0]]

roi = 'hMT_lh'
roi = 'MDroi_area8c_lh'

# indices - within is 5, 4, 3, 2, 1 stim. between is always 6
within_a_1 = np.arange(0, 5)
within_a_2 = np.arange(11, 15)
within_a_3 = np.arange(21, 24)
within_a_4 = np.arange(30, 32)
within_a_5 = np.arange(38, 39)

between1 = np.arange(6, 11)
between2 = np.arange(15, 21)
between3 = np.arange(24, 30)
between4 = np.arange(32, 38)
between5 = np.arange(39, 45)
between6 = np.arange(45, 51)

within_b_1 = np.arange(51, 56)
within_b_2 = np.arange(56, 60)
within_b_3 = np.arange(60, 63)
within_b_4 = np.arange(63, 65)
within_b_5 = np.arange(65, 66)

within_a_all = np.concatenate([within_a_1, within_a_2, within_a_3, within_a_4, within_a_5])
within_b_all = np.concatenate([within_b_1, within_b_2, within_b_3, within_b_4, within_b_5])
within_all = np.concatenate([within_a_all, within_b_all])
between_all = np.concatenate([between1, between2, between3, between4, between5, between6])

#print(df[roi].iloc[iSub][within_a_all].mean())
#print(df[roi].iloc[iSub][within_b_all].mean())
#print(df[roi].iloc[iSub][within_all].mean())
#print(df[roi].iloc[iSub][between_all].mean())

within_a = np.zeros(33)
within_b = np.zeros(33)
within = np.zeros(33)
between = np.zeros(33)
for iSub in range(0,33):
    within_a[iSub] = df[roi].iloc[iSub][within_a_all].mean()
    within_b[iSub] = df[roi].iloc[iSub][within_b_all].mean()
    within[iSub] = df[roi].iloc[iSub][within_all].mean()
    between[iSub] = df[roi].iloc[iSub][between_all].mean()

print(within_a[indSubs].mean())
print(within_b[indSubs].mean())
print(within[indSubs].mean())
print(between[indSubs].mean())


# %% plot subjCat-wb

saveFigs = False

# exclude subs with unequal conds in each cat for now
exclSubs = True
if exclSubs:
    indSubs=np.zeros(33,dtype=bool)
    for iSub in range(33):
        if len(dfmodel['a'].loc[iSub]) == len(dfmodel['b'].loc[iSub]):
            indSubs[iSub] = 1
else:
    indSubs=np.ones(33,dtype=bool)

#subjCat sig
roi='hMT_lh'
#roi='MDroi_area8c_lh'

#within = np.zeros(33)
#between = np.zeros(33)
#for iSub in range(33):
#    within_a[iSub] = df[roi].iloc[iSub][0:6].mean()
#    within_b[iSub] = df[roi].iloc[iSub][6:12].mean()
#    within[iSub] = df[roi].iloc[iSub][0:12].mean()
#    between[iSub] = df[roi].iloc[iSub][12:24].mean()
#print(within[indSubs].mean())
#print(between[indSubs].mean())

# inds - need to code to arrange directions when sorted (e.g. [0, 30, 60, 90, 300, 330]), put 300/339 to front
# - just cat B - A all fine
indsort = []
for iSub in range(33):
    indsort.append(np.array(df['subjCat'][iSub][1]) >= 240)

# a keep the same
ind1 = np.arange(0, 6)
ind3 = np.arange(12, 18)
# b diff
ind2 = []
ind4 = []
for iSub in range(33):
    tmp = np.array(df['subjCat'][iSub][1]) >= 240
    ind2.append(np.concatenate([np.nonzero(tmp)[0], np.nonzero(~tmp)[0]]) + 6)
    ind4.append(np.concatenate([np.nonzero(tmp)[0], np.nonzero(~tmp)[0]]) + 18)

within_a = np.zeros([33, 6])
within_b = np.zeros([33, 6])
between_a = np.zeros([33, 6])
between_b = np.zeros([33, 6])
for iSub in np.nonzero(indSubs)[0]:
    within_a[iSub] = df[roi].iloc[iSub][ind1]
    within_b[iSub] = df[roi].iloc[iSub][ind2[iSub]]
    between_a[iSub] = df[roi].iloc[iSub][ind3]
    between_b[iSub] = df[roi].iloc[iSub][ind4[iSub]]
    
within_mean = np.mean(np.mean(np.stack([within_a[indSubs], within_b[indSubs]]), axis=0), axis=0)
between_mean = np.mean(np.mean(np.stack([between_a[indSubs], between_b[indSubs]]), axis=0), axis=0)

within_sem = np.std(np.mean(np.stack([within_a[indSubs], within_b[indSubs]]), axis=0), axis=0) / np.sqrt(indSubs.sum())
between_sem = np.std(np.mean(np.stack([between_a[indSubs], between_b[indSubs]]), axis=0), axis=0) / np.sqrt(indSubs.sum())

plt.errorbar(np.arange(6), within_mean, within_sem, label='within category')
plt.errorbar(np.arange(6), between_mean, between_sem, label='between category')
plt.ylim([.5, .59])
plt.legend(loc="upper left")
#plt.title('Left mMFG')
#plt.title('Left MT')
plt.xlabel('Direction')
plt.ylabel('Decoding Accuracy')
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_svm_subjCat-wb_6dirs_' + roi + '.pdf'))
plt.show()


# 12 dirs
within_mean = np.mean(np.concatenate([within_a[indSubs], within_b[indSubs]], axis=1), axis=0)
between_mean = np.mean(np.concatenate([between_a[indSubs], between_b[indSubs]], axis=1), axis=0)
within_sem = np.std(np.concatenate([within_a[indSubs], within_b[indSubs]], axis=1), axis=0) / np.sqrt(indSubs.sum())
between_sem = np.std(np.concatenate([between_a[indSubs], between_b[indSubs]], axis=1), axis=0) / np.sqrt(indSubs.sum())

plt.errorbar(np.arange(12), within_mean, within_sem, label='within category')
plt.errorbar(np.arange(12), between_mean, between_sem, label='between category')
plt.ylim([.47, .62])
plt.legend(loc="upper right")
#plt.title('Left mMFG')
#plt.title('Left MT')
plt.xlabel('Direction')
plt.ylabel('Decoding Accuracy')
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_svm_subjCat-wb_12dirs_' + roi + '.pdf'))
plt.show()


#%% all dirs - plotting to show above chance decoding for stimulus (similar to 12-way but averaging pair-wise svms)
plt.style.use('seaborn-darkgrid')

fntSiz=14

saveFigs = False

exclSubs = True
if exclSubs:
    indSubs=np.zeros(33,dtype=bool)
    for iSub in range(33):
        if len(dfmodel['a'].loc[iSub]) == len(dfmodel['b'].loc[iSub]):
            indSubs[iSub] = 1
else:
    indSubs=np.ones(33,dtype=bool)

ylims = [0.475, 0.525]

#subjCat sig
roi='hMT_lh'
roi='MDroi_area8c_lh'
#
##RDM cat sig
#roi='MDroi_area9_rh'
#
##12-way sig
#roi='hMT_rh'
#
##ori sig
#roi='EVC_lh'
#
#other
#roi='EVC_rh'
#roi='V3a_lh'
#roi='V3a_rh'

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
        ind[iSub-1] = False

# arrange the directions first (with sorted indices) - using inds in step 1 above, then flip - using inds in step 2 above
rdmArr1 = np.zeros((nCond,nCond,nSubs))
for iSub in range(33):
    rdmArr1[:,:,iSub] = rdmAll[condInd[:,iSub],:,iSub] 
    rdmArr1[:,:,iSub] = rdmArr1[:,condInd[:,iSub],iSub]

#flip half the subs
rdmArr = rdmArr1.copy()
rdmArr[0:6,0:6,ind]  = rdmArr1[6:12,6:12,ind]
rdmArr[6:12,6:12,ind] = rdmArr1[0:6,0:6,ind]
rdmArr[0:6,6:12,ind]  = rdmArr1[6:12,0:6,ind]
rdmArr[6:12,0:6,ind]  = rdmArr1[0:6,6:12,ind]

#average across conds 
ctuple=np.array((0.1,0.3,0.5))
rdmMeanAll = np.nanmean(rdmArr[:,:,indSubs],axis=0).mean(axis=1)
rdmSEAll = np.nanstd(np.nanmean(rdmArr[:,:,indSubs],axis=0),axis=1)/np.sqrt(sum(indSubs))
ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanAll, yerr=rdmSEAll, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])
plt.title(roi,fontsize=fntSiz)
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_svm_pairwiseDirs_' + roi + '.pdf'))
plt.show()

t,p=stats.ttest_1samp(np.nanmean(rdmArr[:,:,indSubs],axis=0).T,0.5)
print(p)

#% plot RDMs for visualisation
plt.rcdefaults()

rdm = np.zeros((12,12))
rdmArr[np.isnan(rdmArr)]=0 # back to zero for mds
rdm = rdmArr.mean(axis=2)
#tstat (double check formula)
#rdm = rdmArr.mean(axis=2)/rdmArr.std(axis=2)/np.sqrt(sum(indSubs))
rdm[np.isnan(rdm)]=0 #dividing by 0 makes nans

#RDM plot
plt.figure(figsize=(4,1.5))
plt.imshow(rdm,cmap='viridis',interpolation='none')
plt.title(roi,fontsize=fntSiz)
plt.colorbar()
#if saveFigs:
#    plt.savefig(os.path.join(figDir,'mvpaROI_crossNobis_RDM' + roi + '.pdf'))
plt.show()

#MDS
from sklearn import manifold
seed = np.random.RandomState(seed=3)
mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
pos = mds.fit(rdm).embedding_

#MDS plot
ctuple=np.append(np.tile(np.array((0.0,1.0,0.0)),(6,1)),np.tile(np.array((0.0,0.065,0.0)),(6,1)),axis=0)
plt.figure(figsize=(1.5,1.5))
plt.scatter(pos[:,0],pos[:,1],color=ctuple)
plt.title(roi,fontsize=fntSiz)
#if saveFigs:
#    plt.savefig(os.path.join(figDir,'mvpaROI_crossNobis_MDScat_' + roi + '.pdf'))
plt.show()

#MDS plot with gradation by direction condition
ctuple=np.tile(np.array((0.0,1.0,0.0)),(12,1))
cnt = np.array((0.0,0.0,0.0))
ctuple[:,1] = [.6,.8,1,1,.8,.6,.4,.2,0,0,.2,.4]
plt.figure(figsize=(1.5,1.5))
plt.scatter(pos[:,0],pos[:,1],color=ctuple)
plt.title(roi,fontsize=fntSiz)
#if saveFigs:
#    plt.savefig(os.path.join(figDir,'mvpaROI_crossNobis_MDSdir_' + roi + '.pdf'))
plt.show()
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
plt.style.use('seaborn-darkgrid')

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

#flip half the subs (direction counterbalanced)- shouldn't matter since sorted by cat, but in case stim direction makes a diff, this might help
ind=np.full((33),True)
for iSub in range(1,34):
    subNum=f'{iSub:02d}'
    fnames    = os.path.join(eventsDir, "sub-" + subNum + "*memsamp*run-01*." + 'tsv')
    iFile = sorted(glob.glob(fnames))
    dfBehav=pd.read_csv(iFile[0], sep="\t")
    if np.any((dfBehav['direction']==0)&(dfBehav['rawdirection']==135)):
        ind[iSub-1] = False
flipSubs = np.where(ind)
flipSubs = flipSubs[0]
        

rois = list(df)
dfMean = pd.DataFrame(columns=rois,index=range(0,12))
dfSem  = pd.DataFrame(columns=rois,index=range(0,12))
#tstat  = []
#pval   = []
df1=df.copy() #reorganise so in stimulus direction order
for roi in rois:
    ind12way=np.empty(33,dtype=int)
    indLen1=np.empty(33,dtype=int) #nDirs in first cat
    for iSub in range(33):
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
    
        if iSub in flipSubs:
            df1[roi].iloc[iSub] = np.concatenate([df1[roi].iloc[iSub][6:12],df1[roi].iloc[iSub][0:6]])
            
    #compute mean sem - note edited to df1  here
    dfMean[roi] = np.mean(np.asarray(np.stack(df1[roi].iloc[indSubs])),axis=0)
    dfSem[roi] = np.asarray(np.stack(df1[roi].iloc[indSubs])).std(axis=0)/np.sqrt(sum(indSubs))
#    statsTmp=stats.ttest_1samp(np.asarray(np.stack(df1[roi].iloc[indSubs])),0.5)
#    tstat.append(statsTmp.statistic)
#    pval.append(statsTmp.pvalue)

roi='EVC_lh' 
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='EVC_rh' 
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')

roi='hMT_lh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='MDroi_area8c_lh'
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')


#%%dir-all
plt.style.use('seaborn-darkgrid')

indSubs=np.ones(33,dtype=bool)

rois = list(df)
dfMean = pd.DataFrame(columns=rois,index=range(0,6))
dfSem  = pd.DataFrame(columns=rois,index=range(0,6))
df1=df.copy()
for roi in rois:
    #compute mean sem
    dfMean[roi] = np.mean(np.asarray(np.stack(df1[roi].iloc[indSubs])),axis=0)
    dfSem[roi] = np.asarray(np.stack(df1[roi].iloc[indSubs])).std(axis=0)/np.sqrt(sum(indSubs))

roi='V1vd_lh' 
plt.figure(figsize=(5,3))
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')
roi='V1vd_rh' 
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
