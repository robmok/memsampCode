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
roiDir='/Users/robertmok/Documents/Postdoc_ucl/mvpa_roi/' 

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

#stdAll = df.iloc[0:33,df.loc['stats']:].std()/np.sqrt(33)
stdAll = df.iloc[0:33,:].sem()


#ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll)
ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(.5,.525))
#ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(1/12,0.097))
#ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(-.01,.05)) #subjCat-orth

#ax=df.iloc[0:33,:].mean().plot(figsize=(20,5),yerr=stdAll, fmt='o')
#ax = plt.errorbar(range(0,np.size(df,axis=1)),df.iloc[0:33,:], yerr=stdAll, fmt='-o')

#%% univariate scatter plots, violin plots

ax = sns.catplot(data=df.iloc[0:33,:],height=4,aspect=4, kind="swarm")
df.iloc[0:33,:].mean().plot(yerr=stdAll, fmt='o')

#g = sns.catplot(data=df.iloc[0:33,:],height=4,aspect=4, kind="box")

g = sns.catplot(data=df.iloc[0:33,:],height=4,aspect=4.2, kind="violin", inner=None)
sns.swarmplot(color="k", size=3, data=df.iloc[0:33,:], ax=g.ax);

#%% subjCat-all - organise


#if iSub==5: #move 240 and 270 to catA
#elif iSub==10: #move 270 to cat B
#elif iSub == 17:#move 30 to cat B
#elif iSub==24: #move 120 to cat A
#elif iSub==27:#move 270 to cat A



#exclude subjects with unequal directions in each category
# - NOTE: need to check if equal but not continous as well

exclSubs = True
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(df['subjCat'].iloc[iSub][0])
        nDirInCat[1,iSub]=len(df['subjCat'].iloc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)
    
#df1 = pd.DataFrame(columns=df.columns,index=['mean', 'sem'])

#for roi in df.columns.values[0:-1]:
#
#roi='dlPFC_lh'
#roi='dlPFC_rh'
#roi='MDroi_ips_lh'
#roi='MDroi_ips_rh'
#roi='V1vd_lh'
#roi='V3a_lh'

#subjCat sig
roi='V2vd_rh'
roi='hMT_lh'
roi='MDroi_area8c_lh'


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
rdmSE  = rdmAll[:,:,indSubs].std(axis=2)/np.sqrt(np.count_nonzero(indSubs))

#% subjCat-all - plot 1

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
rdmSEA = np.nanstd(np.nanmean(rdmAll[0:nCond//2,0:nCond,indSubs],axis=0),axis=1)

ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanA, yerr=rdmSEA, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])

ctuple=np.array((0.5,0.3,0.1))
#rdmMeanB = np.nanmean(rdmMean[nCond//2:nCond,0:nCond],axis=0)
rdmMeanB = np.nanmean(rdmAll[nCond//2:nCond,0:nCond,indSubs],axis=0).mean(axis=1)
rdmSEB = np.nanstd(np.nanmean(rdmAll[nCond//2:nCond,0:nCond,indSubs],axis=0),axis=1)

ax = plt.figure(figsize=(4,3))
ax = plt.errorbar(range(0,12),rdmMeanB, yerr=rdmSEB, fmt='-o', color=ctuple)
ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])


#average values within the training example category (e.g. av cat A, but plot all values for cat B) - 




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


#%% plot RDM
#roi='dlPFC_rh'
#roi='dlPFC_lh'
#roi='MDroi_ips_lh'
#roi='MDroi_ips_rh'
#roi='V1vd_lh'
#roi='V3a_rh'
#roi='V3a_lh'
    
    
roi='V2vd_rh'
roi='hMT_lh'
roi='MDroi_area8c_lh'

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


#%%12-way-all

    
#roi='V3a'


#ax=df.iloc[0:33,].mean().plot(figsize=(15,5),kind="bar")
#plt.errorbar(range(0,12),np.mean(df[roi].iloc[0:33]), fmt='-o')


#rois = ['V1vd_lh','V1vd_rh', 'V2vd_lh','V2vd_rh','V3vd_lh','V3vd_rh','V3a_lh','V3a_rh',
#        'V3b_lh','V3b_rh', 'hMT_lh','hMT_rh', 'IPS0_lh','IPS0_rh','IPS1-5_lh','IPS1-5_rh', 
#        'MDroi_ips_lh','MDroi_ips_rh','MDroi_ifg_lh','MDroi_ifg_rh', 'MDroi_area8c_lh',
#        'MDroi_area8c_rh', 'MDroi_area9_lh','MDroi_area9_rh', 'dlPFC_lh','dlPFC_rh',
#        'HIPP_HEAD_lh','HIPP_HEAD_rh','HIPP_BODY_TAIL_lh','HIPP_BODY_TAIL_rh',
#        'HIPP_HEAD_BODY_TAIL_lh','HIPP_HEAD_BODY_TAIL_rh', 'motor_lh', 'motor_rh']


rois = list(df)

dfMean = pd.DataFrame(columns=rois,index=range(0,12))
dfSem  = pd.DataFrame(columns=rois,index=range(0,12))

for roi in rois:
    dfMean[roi] = np.mean(np.asarray(np.stack(df[roi].iloc[0:33])),axis=0)
    dfSem[roi] = np.asarray(np.stack(df[roi].iloc[0:33])).std(axis=0)/np.sqrt(33)
     
    
#ax=dfMean.iloc[0:33,:].T.plot(figsize=(20,5),kind="bar",yerr=dfSem.T,ylim=(.55,.65))

roi='V1vd_lh'
roi='V1vd_rh'

roi='V2vd_rh'
#roi='hMT_lh'
#roi='MDroi_area8c_lh'


ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o')



#single subs
#plt.plot(np.stack(df[roi].iloc[0:33]).T)
  
#plt.plot(np.stack(df[roi].iloc[3]).T)



