#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:00:52 2019

@author: robert.mok
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks", color_codes=True)
#import bootstrapped.bootstrap as bs
#import bootstrapped.stats_functions as bs_stats

# bootstrap CIs - over subjects....
#print(bs.bootstrap(np.asarray(df.iloc[0:33,0]), stat_func=bs_stats.mean))

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/'
#roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/bilateral'

# laptop
#roiDir='/Users/robertmok/Documents/Postdoc_ucl/mvpa_roi/' 

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'svm' # 'svm', 'crossNobis'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-all' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
#%% plot bar / errobar plot

#stdAll = df.iloc[0:33,:].std()/np.sqrt(33)
stdAll = df.iloc[0:33,:].sem()


#ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll)
#ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(.5,.525))
#ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(1/12,0.097))
ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(-.01,.05)) #subjCat-orth

#ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),yerr=stdAll, fmt='o')
#ax = plt.errorbar(range(0,np.size(df,axis=1)),df.iloc[0:33,:], yerr=stdAll, fmt='-o')

#%% univariate scatter plots, violin plots

ax = sns.catplot(data=df.iloc[0:33,:],height=4,aspect=4, kind="swarm")
df.iloc[0:33,:].mean().plot(yerr=stdAll, fmt='o')

#g = sns.catplot(data=df.iloc[0:33,:],height=4,aspect=4, kind="box")

g = sns.catplot(data=df.iloc[0:33,:],height=4,aspect=4.2, kind="violin", inner=None)
sns.swarmplot(color="k", size=3, data=df.iloc[0:33,:], ax=g.ax);

#%% subjCat-all - organise

#df1 = pd.DataFrame(columns=df.columns,index=['mean', 'sem'])

#for roi in df.columns.values[0:-1]:
#
#roi='dlPFC_lh'
#roi='dlPFC_rh'
#roi='MDroi_ips_lh'
#roi='MDroi_ips_rh'
#roi='V1vd_lh'
#roi='V3a_lh'
roi='V3a_rh'

ylims = [0.45, 0.55]

# plot mean and std across subs and plot for now (ignoring some might have diff nConds per cat)
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

rdmMean = rdmAll.mean(axis=2)
rdmSE  = rdmAll.std(axis=2)/np.sqrt(nSubs)

#%% subjCat-all - plot 1

ax = plt.figure(figsize=(8,4))
ctuple=np.array((0.1,0.3,0.5))
for iCond in range(0,6):
    ax = plt.figure(figsize=(4,3))
    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
    ctuple = ctuple+0.05
    ylim1, ylim2 = plt.ylim()
    plt.ylim(ylims[0],ylims[1])

ax = plt.figure(figsize=(8,4))
ctuple=np.array((0.5,0.3,0.1))
for iCond in range(6,12):
    ax = plt.figure(figsize=(4,3))
    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
    ctuple = ctuple+0.05
    ylim1, ylim2 = plt.ylim()
    plt.ylim(ylims[0],ylims[1])

    
#ax = plt.errorbar(range(0,11),rdmMean[0,1:-1], yerr=rdmSE[0,1:-1], fmt='-o')

#%% subjCat-all - plot 2

#prototype - 6 conds each, for prototype is middle of conds 3&4

#catA
    
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


#%% plot RDM
#roi='dlPFC_rh'
#roi='dlPFC_lh'
#roi='MDroi_ips_lh'
#roi='MDroi_ips_rh'
#roi='V1vd_lh'
roi='V3a_rh'
#roi='V3a_lh'

rdm = np.zeros((12,12))

iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
rdm[iu] = df[roi].iloc[0:33].mean(axis=0)

#tstat (double check formula)
rdm[iu] = df[roi].iloc[0:33].mean(axis=0)/np.stack(df[roi].iloc[0:33]).std(axis=0)/np.sqrt(33)

#make it a symmetric matrix 
il = np.tril_indices(12,-1) 
rdm[il] = rdm.T[il]

ax = plt.figure(figsize=(25,4))
ax = plt.imshow(rdm,cmap='viridis')
plt.colorbar()
plt.show()

from sklearn import manifold
seed = np.random.RandomState(seed=3)
mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
pos = mds.fit(rdm).embedding_

ctuple=np.tile(np.array((0.0,1.0,0.0)),(12,1))
cnt = np.array((0.0,0.0,0.0))
for icol in range(0,12):
    ctuple[icol,:] = ctuple[icol,:]+cnt
    cnt = cnt+np.array((0,-0.085,0))

plt.scatter(pos[:,0],pos[:,1],color=ctuple)
plt.show()