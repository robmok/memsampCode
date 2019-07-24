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
import scipy.stats as stats
from statsmodels.stats.multitest import fdrcorrection as fdr
#from statsmodels.stats.multitest import multipletests as multest

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06

codeDir=os.path.join(mainDir,'memsampCode')
#codeDir='/Users/robertmok/Documents/Postdoc_ucl/memsampCode' #laptop

roiDir=os.path.join(mainDir,'mvpa_roi')
#roiDir=os.path.join(mainDir,'mvpa_roi/bilateral')
roiDir=os.path.join(mainDir,'mvpa_roi/rois_0.25')
#roiDir=os.path.join(mainDir,'mvpa_roi/rois_0.5')
#roiDir=os.path.join(mainDir,'mvpa_roi/rois_nosmooth')

figDir=os.path.join(mainDir,'mvpa_roi/figs_mvpa_roi')
behavDir=os.path.join(mainDir,'behav')

# laptop
#roiDir='/Users/robertmok/Documents/Postdoc_ucl/mvpa_roi/' 
                                
os.chdir(codeDir)
from memsamp_RM import kendall_a

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'crossNobis' # 'svm', 'crossNobis', 'mNobis' - for subjCat-orth and -all
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-all' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))

#load in subjCat
subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))
#load in behav acc
behav=np.load(os.path.join(behavDir, 'memsamp_acc_subjCat.npz'))
locals().update(behav) #load in each variable into workspace

#%% plot bar / errorbar plot

exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
#    indSubs[:]=True # reset if don't include excl above
    indSubs[[8,11,15,30]] = False #trying without subs that couldn't flip motor response well - worse here always, but better for RDm cat pfc (w/out excluding above)
else:
    indSubs=np.ones(33,dtype=bool)
    
stdAll = df.iloc[indSubs,:].sem()

#barplot
#ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(.5,.525))
#ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(1/12,0.097))
ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(-.01,.05)) #subjCat-orth

#errorbar plot
#ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),yerr=stdAll, fmt='o')

# without excluding, V2 p=0.1 MT: p=0.02715; area8c_lhp= 0.00855  - NOTE: pvals are 2-tailed; should be 1, so halve them
# after excluding, V2 p=0.3449, MT: p=0.0346, area8c_lh: p=0.00337 
print(stats.ttest_1samp(df['V2vd_rh'].iloc[indSubs],0))
print(stats.ttest_1samp(df['hMT_lh'].iloc[indSubs],0))
print(stats.ttest_1samp(df['MDroi_area8c_lh'].iloc[indSubs],0))
# 
#stats.ttest_1samp(df['MDroi_area9_rh'].iloc[indSubs],0)

#loaded in subjCat-orth first, saved to df1, then loaded in dir to compare. MT and PFC sig
#stats.ttest_rel(df1['V2vd_rh'].iloc[indSubs],df['V2vd_rh'].iloc[indSubs]-.5)
#stats.ttest_rel(df1['hMT_lh'].iloc[indSubs],df['hMT_lh'].iloc[indSubs]-.5)
#stats.ttest_rel(df1['MDroi_area8c_lh'].iloc[indSubs],df['MDroi_area8c_lh'].iloc[indSubs]-.5)

#%% univariate scatter plots, violin plots

ax = sns.catplot(data=df.iloc[indSubs,:],height=4,aspect=4, kind="swarm")
df.iloc[indSubs,:].mean().plot(yerr=stdAll, fmt='o')

#g = sns.catplot(data=df.iloc[0:33,:],height=4,aspect=4, kind="box")

g = sns.catplot(data=df.iloc[indSubs,:],height=4,aspect=4.2*2, kind="violin", inner=None)
sns.swarmplot(color="k", size=3, data=df.iloc[indSubs,:], ax=g.ax);


#%% plotting within area, across decoders

saveFigs = False

exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
#    indSubs[:]=True # reset if don't include excl above
#    indSubs[[8,11,15,30]] = False #trying without subs that couldn't flip motor response well - worse here always, but better for RDm cat pfc (w/out excluding above)
else:
    indSubs=np.ones(33,dtype=bool)
    
decodeFeature = 'subjCat-orth'
dfSubjCat=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth 
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_goodone.pkl')))
decodeFeature = '12-way'
df12way=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth 
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
decodeFeature = 'ori'
dfOri=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth 
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
decodeFeature = 'dir'
dfDir=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth  
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
dfHeader=['subjCat-orth','12-way','ori','dir']


#subjCat-orth
#seaborn - but errorbars are bootstrapped CIs (larger)
#roi='MDroi_area8c_lh'
#svm_area8c = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12,
#                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5],axis=1)
#svm_area8c.columns=dfHeader
#g = sns.catplot(data=svm_area8c.iloc[indSubs,:],height=6,aspect=1, kind="bar")
#sns.stripplot(color="k", alpha=0.3, size=3, data=svm_area8c.iloc[indSubs,:], ax=g.ax);
#g.fig.suptitle('area8c_lh')
#g.set_ylim=(-0.125,0.15)
#plt.show()

##subjCat-orth
##matplotlib
#roi='MDroi_area8c_lh'
#svm_area8c = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12,
#                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5],axis=1)
#svm_area8c.columns=dfHeader
#ax=svm_area8c.mean().plot(figsize=(5,6),kind="bar",yerr=svm_area8c.sem(),ylim=(-0.125,0.15), title='area8c_lh')
#sns.stripplot(color="k", alpha=0.3, size=3, data=svm_area8c.iloc[indSubs,:])
#plt.show()


#combining - seaborn colours, sem errorbars
roi='MDroi_area8c_lh'
svm_area8c = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12,
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5],axis=1)
svm_area8c.columns=dfHeader
g = sns.catplot(data=svm_area8c.iloc[indSubs,:],height=6,aspect=1, kind="bar", ci=None)
svm_area8c.mean().plot(yerr=svm_area8c.iloc[indSubs,:].sem(),ylim=(-0.125,0.15), title='area8c_lh',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_area8c.iloc[indSubs,:], ax=g.ax);
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
    #plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.eps'))
plt.show()


roi='hMT_lh'
svm_MT = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12,
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5],axis=1)
svm_MT.columns=dfHeader
g = sns.catplot(data=svm_MT.iloc[indSubs,:],height=6,aspect=1, kind="bar", ci=None)
svm_MT.mean().plot(yerr=svm_MT.iloc[indSubs,:].sem(),ylim=(-0.125,0.15), title='hMT_lh',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_MT.iloc[indSubs,:], ax=g.ax);
plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()

roi='V2vd_rh'
svm_V2_rh = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12,
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5],axis=1)
svm_V2_rh.columns=dfHeader
g = sns.catplot(data=svm_V2_rh.iloc[indSubs,:],height=6,aspect=1, kind="bar", ci=None)
svm_V2_rh.mean().plot(yerr=svm_V2_rh.iloc[indSubs,:].sem(),ylim=(-0.125,0.15), title='V2vd_rh',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_V2_rh.iloc[indSubs,:], ax=g.ax);
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()


roi='V1vd_rh'
svm_V1_rh = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12,
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5],axis=1)
svm_V1_rh.columns=dfHeader
g = sns.catplot(data=svm_V1_rh.iloc[indSubs,:],height=6,aspect=1, kind="bar", ci=None)
svm_V1_rh.mean().plot(yerr=svm_V1_rh.iloc[indSubs,:].sem(),ylim=(-0.125,0.15), title='V1vd_rh',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_V1_rh.iloc[indSubs,:], ax=g.ax);
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()

#%% behav corr svm

exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
#    indSubs[:]=True # reset if don't include excl above
#    indSubs[[8,11,15,30]] = False #trying without subs that couldn't flip motor response well - worse here always, but better for RDm cat pfc (w/out excluding above)
else:
    indSubs=np.ones(33,dtype=bool)
    
roiList=list(df)
rAcc=pd.DataFrame(columns=roiList,index=range(0,2))
rAccA=pd.DataFrame(columns=roiList,index=range(0,2))
rAccB=pd.DataFrame(columns=roiList,index=range(0,2))
rObjAcc=pd.DataFrame(columns=roiList,index=range(0,2))
for roi in roiList:
    rAcc[roi][0], rAcc[roi][1]=stats.pearsonr(acc[indSubs],df[roi].iloc[indSubs])
    rAccA[roi][0], rAccA[roi][1]=stats.pearsonr(accA[indSubs],df[roi].iloc[indSubs])
    rAccB[roi][0], rAccB[roi][1]=stats.pearsonr(accB[indSubs],df[roi].iloc[indSubs])
    rObjAcc[roi][0], rObjAcc[roi][1]=stats.pearsonr(objAcc[indSubs],df[roi].iloc[indSubs])


plt.scatter(df['V1vd_rh'].iloc[indSubs],acc[indSubs])
plt.show()
plt.scatter(df['hMT_lh'].iloc[indSubs],acc[indSubs])
plt.show()
plt.scatter(df['MDroi_area8c_lh'].iloc[indSubs],acc[indSubs])
plt.show()
plt.scatter(df['MDroi_area9_rh'].iloc[indSubs],acc[indSubs])
plt.show()

#%% subjCat-all - organise

exclSubs = True
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
roi='V2vd_rh'
#roi='hMT_lh'
#roi='MDroi_area8c_lh'

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
ax = plt.figure(figsize=(8,4))
ctuple=np.array((0.1,0.3,0.5))
for iCond in range(0,nCond//2):
    ax = plt.figure(figsize=(4,3))
    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
    ctuple = ctuple+0.05
    ylim1, ylim2 = plt.ylim()
    plt.ylim(ylims[0],ylims[1])

ax = plt.figure(figsize=(8,4))
ctuple=np.array((0.5,0.3,0.1))
for iCond in range(nCond//2,nCond):
    ax = plt.figure(figsize=(4,3))
    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
    ctuple = ctuple+0.05
    ylim1, ylim2 = plt.ylim()
    plt.ylim(ylims[0],ylims[1])
    
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

#%% plot RDM
    
saveFigs = False
fntSiz = 14
    
exclSubs = True
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)
    
#decoding subjCat sig    
roi='V2vd_rh'
roi='hMT_lh'
roi='MDroi_area8c_lh'

#rdmModel category sig - crossnobis
roi='SPL1_rh'
roi='MDroi_area9_rh'

rdm = np.zeros((12,12))
iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
rdm[iu] = df[roi].iloc[indSubs].mean(axis=0)
#tstat (double check formula)
rdm[iu] = df[roi].iloc[indSubs].mean(axis=0)/np.stack(df[roi].iloc[indSubs]).std(axis=0)/np.sqrt(sum(indSubs))
#make it a symmetric matrix 
il = np.tril_indices(12,-1) 
rdm[il] = rdm.T[il]

#RDM plot
plt.figure(figsize=(25,4))
plt.imshow(rdm,cmap='viridis')
plt.title(roi,fontsize=fntSiz)
plt.colorbar()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_crossNobis_RDM' + roi + '.pdf'))
plt.show()

#MDS
from sklearn import manifold
seed = np.random.RandomState(seed=3)
mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
pos = mds.fit(rdm).embedding_

#MDS plot
ctuple=np.append(np.tile(np.array((0.0,1.0,0.0)),(6,1)),np.tile(np.array((0.0,0.065,0.0)),(6,1)),axis=0)
plt.scatter(pos[:,0],pos[:,1],color=ctuple)
plt.title(roi,fontsize=fntSiz)
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_crossNobis_MDScat_' + roi + '.pdf'))
plt.show()

#MDS plot with gradation by direction condition
ctuple=np.tile(np.array((0.0,1.0,0.0)),(12,1))
cnt = np.array((0.0,0.0,0.0))
ctuple[:,1] = [.6,.8,1,1,.8,.6,.4,.2,0,0,.2,.4]

plt.scatter(pos[:,0],pos[:,1],color=ctuple)
plt.title(roi,fontsize=fntSiz)
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_crossNobis_MDSdir_' + roi + '.pdf'))
plt.show()
#%% #single sub RDMs
iSub=0

rdm = np.zeros((12,12))
rdm[iu] = df[roi].iloc[iSub]
il = np.tril_indices(12,-1) 
rdm[il] = rdm.T[il]
ax = plt.figure(figsize=(25,4))
ax = plt.imshow(rdm,cmap='viridis')
plt.colorbar()
plt.show()

#ctuple=np.append(np.tile(np.array((0.0,1.0,0.0)),(6,1)),np.tile(np.array((0.0,0.065,0.0)),(6,1)),axis=0)
ctuple[:,1] = [.6,.8,1,1,.8,.6,.4,.2,0,0,.2,.4]

pos = mds.fit(rdm).embedding_
plt.scatter(pos[:,0],pos[:,1],color=ctuple)
plt.show()
#%% models visualise
saveFigs = False

modelRDM = np.zeros((12,12))
il = np.tril_indices(12,-1) 

#category
modelRDM[0:6,6:12]=np.ones((6,6))
modelRDM[il] = modelRDM.T[il]
ax = plt.imshow(modelRDM,cmap='viridis')
plt.colorbar()
if saveFigs:
    plt.savefig(os.path.join(figDir,'modelRDM_category.pdf'))
plt.show()

 #direction
angDist=np.empty((66)) #number of upper diagonal cells
conds = np.arange(0,360,30)
i=0
for iCond in range(0,len(conds)):
    for compCond in conds[len(conds)-len(conds[iCond:len(conds)])+1:len(conds)]:
        angDist[i] = abs(((conds[iCond]-compCond) + 180) % 360 - 180)
        i=i+1

iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
modelRDM[iu] = angDist
modelRDM[il] = modelRDM.T[il]
ax = plt.imshow(modelRDM,cmap='viridis')
plt.colorbar()
if saveFigs:
    plt.savefig(os.path.join(figDir,'modelRDM_dir.pdf'))
plt.show()

#orientation
angDist=np.empty((66)) #number of upper diagonal cells
conds = np.arange(0,360,30)
conds[conds>180]=conds[conds>180]-180
i=0
for iCond in range(0,len(conds)):
    for compCond in conds[len(conds)-len(conds[iCond:len(conds)])+1:len(conds)]:
        angDist[i] = abs(((conds[iCond]-compCond) + 90) % 180 - 90)
        i=i+1

iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
modelRDM[iu] = angDist
modelRDM[il] = modelRDM.T[il]
ax = plt.imshow(modelRDM,cmap='viridis')
plt.colorbar()
if saveFigs:
    plt.savefig(os.path.join(figDir,'modelRDM_ori.pdf'))
plt.show()

#%% model RDMs - category
saveFigs = False
fontsize = 14

#include subjects with unequal conds in categories (manually made their RDMs)
inclUneqSubs = True
uneqSubs=np.array((4, 12, 16, 26, 31))

#exclude subs with unequal conds
exclSubs = False
if exclSubs:
#    inclUneqSubs = False
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
    
    # very similar in any way - p~0.02.  
            #area9rh: excl uneq p=.0238, excl uneq+excl below p=.0261 , include uneq p=0.0207, include unEq+exclude below p=0.0228/0.0261
            #SPL1rh excl uneq p=.166, excl uneq+excl below p=.38 , include uneq p=.0784, include unEq+exclude below p=.38 
#    indSubs[:]=1 # reset if include unequal conds
#    indSubs[[8,11,15,30]] = False #trying without subs that couldn't flip motor response well - worse here always, but better for RDm cat pfc (w/out excluding above)
else:
    indSubs=np.ones(33,dtype=bool)

#model
catRDM = np.zeros((12,12))
iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
catRDM[0:6,6:12]=np.ones((6,6)) #category

#data
rdm = np.zeros((12,12)) 
rho = np.empty((sum(indSubs)))
tau = np.empty((sum(indSubs)))
pval = np.empty((sum(indSubs)))

useSubs=np.where(indSubs)
roiList=list(df)
roiList.remove('subjCat')
rhoCat = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
tauCat = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))

rhoPcat=np.empty((len(roiList)))
tauPcat=np.empty((len(roiList)))

iRoi=0
for roi in roiList:
    rdm = np.zeros((12,12)) 
    rho=np.empty((sum(indSubs)))
    tau=np.empty((sum(indSubs)))
    pval=np.empty((sum(indSubs)))
    i=0
    for iSub in useSubs[0]:    
        rdm[iu] = df[roi].iloc[iSub]
        
        if inclUneqSubs&np.any(iSub==uneqSubs):
            nCondA=len(df['subjCat'].loc[iSub][0])
            nCondB=len(df['subjCat'].loc[iSub][1])
            catRDM = np.zeros((12,12))
            catRDM[0:nCondB,nCondA:12]=np.ones((nCondB,nCondB))
        else:
            catRDM = np.zeros((12,12))
            catRDM[0:6,6:12]=np.ones((6,6))
        
        rho[i], pval[i]=stats.spearmanr(rdm[iu],catRDM[iu])
#        tau[i], pval[i]=stats.kendalltau(rdm[iu],modelRDM[iu])
        tau[i] = kendall_a(rdm[iu],catRDM[iu])
        i+=1
    t,p=stats.ttest_1samp(rho,0)
    rhoPcat[iRoi]=p
    print('roi: %s' % (roi))
    print('spearman: t=%.3f, p=%.4f' % (t,p))
    t,p=stats.ttest_1samp(tau,0)
    tauPcat[iRoi]=p
    print('tau-b: t=%.3f, p=%.4f' % (t,p))
    rhoCat[roi]=rho
    tauCat[roi]=tau
    iRoi+=1
    
#ax=rhoCat.mean().plot(figsize=(20,5),kind="bar",yerr=rhoCat.sem(),ylim=(-0.075,0.075))
ax=tauCat.mean().plot(figsize=(20,5),kind="bar",yerr=tauCat.sem(),ylim=(-0.04,0.04))
ax.set_title('Category RDM correlation (tau-A)',fontsize=fntSiz)
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaRSA_crossNobis_barplotByROI_RDMcat.pdf'))
    
print(fdr(tauPcat[0:len(tauPcat)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#print(multest(pvals[0:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False))

#print(fdr(tauPcat[11:len(tauPcat)-2]/2,alpha=0.05,method='indep',is_sorted=False))

#%% model RDMs - angular distance - direction
saveFigs = False
fontsize = 14

exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)

modelRDM = np.zeros((12,12))
iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)

#data
rdm = np.zeros((12,12)) 
rho=np.empty((sum(indSubs)))
tau=np.empty((sum(indSubs)))
pval=np.empty((sum(indSubs)))

useSubs=np.where(indSubs)

roiList=list(df)
roiList.remove('subjCat')
rhoDir = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
tauDir = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
rhoPdir=np.empty((len(roiList)))
tauPdir=np.empty((len(roiList)))
iRoi=0
for roi in roiList:
    rdm = np.zeros((12,12)) 
    rho=np.empty((sum(indSubs)))
    tau=np.empty((sum(indSubs)))
    pval=np.empty((sum(indSubs)))
    i=0
    for iSub in useSubs[0]:    
        rdm[iu] = df[roi].iloc[iSub]
        #get direction conditions from ordering here, then compute circular dist
#        conds=np.append(df['subjCat'].loc[iSub][0],df['subjCat'].loc[iSub][1],axis=0)
        conds=np.append(subjCat.loc[iSub][0],subjCat.loc[iSub][1],axis=0)
        iC=0
        angDist=np.empty((66)) #number of upper diagonal cells
        for iCond in range(0,len(conds)):
            for compCond in conds[len(conds)-len(conds[iCond:len(conds)])+1:len(conds)]:
                angDist[iC] = abs(((conds[iCond]-compCond) + 180) % 360 - 180)
                iC=iC+1
        modelRDM[iu] = angDist        
        rho[i], pval[i]=stats.spearmanr(rdm[iu],modelRDM[iu])
#        tau[i], pval[i]=stats.kendalltau(rdm[iu],modelRDM[iu])
        tau[i] = kendall_a(rdm[iu],modelRDM[iu])
        i=i+1
    t,p=stats.ttest_1samp(rho,0)
    rhoPdir[iRoi]=p
    print('roi: %s' % (roi))
    print('spearman: t=%.3f, p=%.4f' % (t,p))
    t,p=stats.ttest_1samp(tau,0)
    tauPdir[iRoi]=p
    print('tau-b: t=%.3f, p=%.4f' % (t,p))
    rhoDir[roi]=rho
    tauDir[roi]=tau
    iRoi+=1
    
#ax=rhoDir.mean().plot(figsize=(20,5),kind="bar",yerr=rhoDir.sem(),ylim=(-0.075,0.075))
ax=tauDir.mean().plot(figsize=(20,5),kind="bar",yerr=tauDir.sem(),ylim=(-0.065,0.065))
ax.set_title('Direction RDM correlation (tau-A)',fontsize=fntSiz)
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaRSA_crossNobis_barplotByROI_RDMdir.pdf'))
    
print(fdr(tauPdir[0:len(tauPdir)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#print(multest(pvals[0:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False))

#%% model RDMs - angular distance - orientation
saveFigs = False
fontsize = 14

exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)
    
modelRDM = np.zeros((12,12))
iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)

rdm = np.zeros((12,12)) 
rho=np.empty((sum(indSubs)))
tau=np.empty((sum(indSubs)))
pval=np.empty((sum(indSubs)))
useSubs=np.where(indSubs)

roiList=list(df)
roiList.remove('subjCat')
rhoOri = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
tauOri = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
rhoPori=np.empty((len(roiList)))
tauPori=np.empty((len(roiList)))
iRoi=0
for roi in roiList:
    rdm = np.zeros((12,12)) 
    rho=np.empty((sum(indSubs)))
    tau=np.empty((sum(indSubs)))
    pval=np.empty((sum(indSubs)))
    i=0
    for iSub in useSubs[0]:    
        rdm[iu] = df[roi].iloc[iSub]
        #get direction conditions from ordering here, then compute circular dist
#        conds=np.append(df['subjCat'].loc[iSub][0],df['subjCat'].loc[iSub][1],axis=0)
        conds=np.append(subjCat.loc[iSub][0],subjCat.loc[iSub][1],axis=0)

        iC=0
        angDist=np.empty((66)) #number of upper diagonal cells
        for iCond in range(0,len(conds)):
            for compCond in conds[len(conds)-len(conds[iCond:len(conds)])+1:len(conds)]:
                angDist[iC] = abs(((conds[iCond]-compCond) + 90) % 180 - 90)
                iC=iC+1
        modelRDM[iu] = angDist        
        rho[i], pval[i]=stats.spearmanr(rdm[iu],modelRDM[iu])
#        tau[i], pval[i]=stats.kendalltau(rdm[iu],modelRDM[iu])
        tau[i] = kendall_a(rdm[iu],modelRDM[iu])
        i=i+1
    t,p=stats.ttest_1samp(rho,0)
    rhoPori[iRoi]=p
    print('roi: %s' % (roi))
    print('spearman: t=%.3f, p=%.4f' % (t,p))
    t,p=stats.ttest_1samp(tau,0)
    tauPori[iRoi]=p
    print('tau-b: t=%.3f, p=%.4f' % (t,p))
    rhoOri[roi]=rho
    tauOri[roi]=tau
    iRoi+=1
    
#ax=rhoOri.mean().plot(figsize=(20,5),kind="bar",yerr=rhoOri.sem(),ylim=(-0.075,0.075))
ax=tauOri.mean().plot(figsize=(20,5),kind="bar",yerr=tauOri.sem(),ylim=(-0.065,0.065))
ax.set_title('Orientation RDM correlation (tau-A)',fontsize=fntSiz)
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaRSA_crossNobis_barplotByROI_RDMori.pdf'))
    
#print(fdr(tauPori[0:len(tauPori)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#print(multest(pvals[0:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False))

print(fdr(tauPori[0:12]/2,alpha=0.05,method='indep',is_sorted=False))


#%% plotting within area, across models

saveFigs = False
fntsiz = 14

modelR_area9=pd.concat([tauCat['MDroi_area9_rh'],tauOri['MDroi_area9_rh'],tauDir['MDroi_area9_rh']],axis=1)
modelR_SPL1=pd.concat([tauCat['SPL1_rh'],tauOri['SPL1_rh'],tauDir['SPL1_rh']],axis=1)
modelR_v2=pd.concat([tauCat['V2vd_lh'],tauOri['V2vd_lh'],tauDir['V2vd_lh']],axis=1)

dfHeader=['category','ori','dir']
modelR_area9.columns = dfHeader
modelR_SPL1.columns = dfHeader
modelR_v2.columns = dfHeader

#bar
#ax=modelR_area9.iloc[indSubs,:].mean().plot(figsize=(5,5),kind="bar",yerr=modelR_area9.iloc[indSubs,:].sem(),ylim=(-0.04,0.04))
#plt.show()
#ax=modelR_SPL1.iloc[indSubs,:].mean().plot(figsize=(5,5),kind="bar",yerr=modelR_SPL1.iloc[indSubs,:].sem(),ylim=(-0.04,0.04))
#plt.show()
#ax=modelR_v2.iloc[indSubs,:].mean().plot(figsize=(5,5),kind="bar",yerr=modelR_v2.iloc[indSubs,:].sem(),ylim=(-0.04,0.04))
#plt.show()

#bar strip plots
roi='MDroi_area9_rh'
g = sns.catplot(data=modelR_area9.iloc[indSubs,:],height=6,aspect=1, kind="bar", ci=None)
modelR_area9.iloc[indSubs,:].mean().plot(yerr=modelR_area9.iloc[indSubs,:].sem(),ylim=(-0.125,0.15), title=roi,elinewidth=2.5,fmt='k,',alpha=0.8,fontsize=fntsiz)
sns.stripplot(color="k", alpha=0.2, size=3, data=modelR_area9.iloc[indSubs,:], ax=g.ax);
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaRSA_crossNobis_barStripPlotByModel_RDM_' + roi + '.pdf'))
plt.show()

roi='SPL1_rh'
g = sns.catplot(data=modelR_SPL1.iloc[indSubs,:],height=6,aspect=1, kind="bar", ci=None)
modelR_SPL1.iloc[indSubs,:].mean().plot(yerr=modelR_SPL1.iloc[indSubs,:].sem(),ylim=(-0.125,0.15), title=roi,elinewidth=2.5,fmt='k,',alpha=0.8,fontsize=fntsiz)
sns.stripplot(color="k", alpha=0.2, size=3, data=modelR_SPL1.iloc[indSubs,:], ax=g.ax);
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaRSA_crossNobis_barStripPlotByModel_RDM_' + roi + '.pdf'))
plt.show()

roi='V2vd_lh'
g = sns.catplot(data=modelR_v2.iloc[indSubs,:],height=6,aspect=1, kind="bar", ci=None)
modelR_v2.iloc[indSubs,:].mean().plot(yerr=modelR_v2.iloc[indSubs,:].sem(),ylim=(-0.125,0.15), title=roi, elinewidth=2.5,fmt='k,',alpha=0.8,fontsize=fntsiz)
sns.stripplot(color="k", alpha=0.2, size=3, data=modelR_v2.iloc[indSubs,:], ax=g.ax);
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaRSA_crossNobis_barStripPlotByModel_RDM_' + roi + '.pdf'))
plt.show()

#%% behav corr RDM

exclSubs = False # MDroi_area9_rh - false p=0.0768; true p=0.0575 (two-tailed, divide by 2)
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
#    indSubs[:]=True # reset if don't include excl above
#    indSubs[[8,11,15,30]] = False #trying without subs that couldn't flip motor response well - worse here always, but better for RDm cat pfc (w/out excluding above)
else:
    indSubs=np.ones(33,dtype=bool)
    
roiList=list(df)
roiList.remove('subjCat')
rAcc_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
rAccA_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
rAccB_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
rObjAcc_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
for roi in roiList:
    rAcc_RDM[roi][0], rAcc_RDM[roi][1]=stats.pearsonr(acc[indSubs],tauCat[roi].iloc[indSubs])
    rAccA_RDM[roi][0], rAccA_RDM[roi][1]=stats.pearsonr(accA[indSubs],tauCat[roi].iloc[indSubs])
    rAccB_RDM[roi][0], rAccB_RDM[roi][1]=stats.pearsonr(accB[indSubs],tauCat[roi].iloc[indSubs])
    rObjAcc_RDM[roi][0], rObjAcc_RDM[roi][1]=stats.pearsonr(objAcc[indSubs],tauCat[roi].iloc[indSubs])


plt.scatter(tauCat['MDroi_area9_rh'].iloc[indSubs],acc[indSubs])
plt.show()

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


#%% single subs
#roi='MDroi_area8c_lh'
#plt.plot(np.stack(df[roi].iloc[0:33]).T)

iSub=2

roi='V2vd_rh'
plt.figure(figsize=(5,3))
plt.plot(np.stack(df1[roi].iloc[iSub]).T)
roi='hMT_lh'
plt.figure(figsize=(5,3))
plt.plot(np.stack(df1[roi].iloc[iSub]).T)
roi='MDroi_area8c_lh'
plt.figure(figsize=(5,3))
plt.plot(np.stack(df1[roi].iloc[iSub]).T)

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


#%% Noise ceilings for RDMs - category

#exclude subs with unequal conds - for catgory noise ceiling
exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
    
#    indSubs[:]=1 # reset if don't include excl above
#    indSubs[[1,6,31]] = False #trying without subs that couldn't flip motor response well - better for pfc (p=0.008, without excluding unequal)
else:
    indSubs=np.ones(33,dtype=bool)

rdm = np.zeros((12,12)) 
rho = np.empty((sum(indSubs)))
tau = np.empty((sum(indSubs)))
pval = np.empty((sum(indSubs)))

useSubs=np.where(indSubs)
useSubs=useSubs[0]
roiList=list(df)
roiList.remove('subjCat')
rhoLowAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
tauLowAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
rhoHighAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
tauHighAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))

for roi in roiList:
    rdm1 = np.zeros((12,12)) 
    rdm2 = np.zeros((12,12)) 
    rdm3 = np.zeros((12,12)) 
    rhoLow=np.empty((sum(indSubs)))
    tauLow=np.empty((sum(indSubs)))
    rhoHigh=np.empty((sum(indSubs)))
    tauHigh=np.empty((sum(indSubs)))
    i=0
    for iSub in useSubs:    
        rdm1[iu] = df[roi].iloc[iSub]
        rdm2[iu] = df[roi].iloc[useSubs[useSubs!=iSub]].mean(axis=0) #noise ceiling lower-bound (leave-one-subject-out)
        rdm3[iu] = df[roi].iloc[useSubs].mean(axis=0) #higher-bound (include self)
        rhoLow[i], pval=stats.spearmanr(rdm1[iu],rdm2[iu])
        tauLow[i] = kendall_a(rdm1[iu],rdm2[iu])
        rhoHigh[i], pval=stats.spearmanr(rdm1[iu],rdm3[iu])
        tauHigh[i] = kendall_a(rdm1[iu],rdm3[iu])
        rhoLowAll[roi]=rhoLow
        tauLowAll[roi]=tauLow
        rhoHighAll[roi]=rhoHigh
        tauHighAll[roi]=tauHigh
        i+=1
        
#ax=rhoLowAll.mean().plot(figsize=(15,5),kind="bar",yerr=rhoLowAll.sem(),ylim=(-0.075,0.075))
ax=tauLowAll.mean().plot(figsize=(15,5),kind="bar",yerr=tauLowAll.sem(),ylim=(-0.07,0.07))
plt.show()

#ax=rhoHighAll.mean().plot(figsize=(15,5),kind="bar",yerr=rhoHighAll.sem(),ylim=(-0.075,0.075))
ax=tauHighAll.mean().plot(figsize=(15,5),kind="bar",yerr=tauHighAll.sem(),ylim=(0,0.175))
plt.show()


#stats.spearmanr(rdm1[iu],rdm3[iu])
#np.sqrt(scipy.spatial.distance.euclidean(stats.rankdata(rdm1[iu]),stats.rankdata(rdm3[iu])))


#plot low and high togeher - rearrange:
#https://stackoverflow.com/questions/48754179/how-to-pick-pairs-of-columns-plot-them-against-each-other-in-a-bar-chart-pandas


pd.concat(tauLowAll,tauHighAll)