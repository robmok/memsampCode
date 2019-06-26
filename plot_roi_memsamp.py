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


codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode' #love06
codeDir='/Users/robertmok/Documents/Postdoc_ucl/memsampCode' #laptop

os.chdir(codeDir)
from memsamp_RM import kendall_a

# bootstrap CIs - over subjects....
#print(bs.bootstrap(np.asarray(df.iloc[0:33,0]), stat_func=bs_stats.mean))

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/'
#roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/bilateral'

# laptop
roiDir='/Users/robertmok/Documents/Postdoc_ucl/mvpa_roi/' 

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'crossNobis' # 'svm', 'crossNobis'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-all' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
#%% plot bar / errobar plot

#edit to load in EXCLUDE subs
indSubs=np.ones(33,dtype=bool)
    
#stdAll = df.iloc[0:33,df.loc['stats']:].std()/np.sqrt(33)
stdAll = df.iloc[indSubs,:].sem()


#ax=df.iloc[indSubs,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll)
#ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(.5,.525))
#ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(1/12,0.097))
ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),kind="bar",yerr=stdAll,ylim=(-.01,.05)) #subjCat-orth

#ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),yerr=stdAll, fmt='o')
#ax = plt.errorbar(range(0,np.size(df,axis=1)),df.iloc[indSubs,:], yerr=stdAll, fmt='-o')


# without excluding, V2 p=0.1 MT: p=0.02715; area8c_lhp= 0.00855  - NOTE: pvals are 2-tailed; should be 1, so halve them
# after excluding, V2 p=0.3449, MT: p=0.0346, area8c_lh: p=0.00337 
#stats.ttest_1samp(df['V2vd_rh'].iloc[indSubs],0)
#stats.ttest_1samp(df['hMT_lh'].iloc[indSubs],0)
#stats.ttest_1samp(df['MDroi_area8c_lh'].iloc[indSubs],0)

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
roi='dlPFC_lh'
#roi='MDroi_ips_lh'
#roi='MDroi_ips_rh'
#roi='V1vd_lh'
#roi='V3a_rh'
#roi='V3a_lh'
    
#decoding subjCat sig    
#roi='V2vd_rh'
#roi='hMT_lh'
#roi='MDroi_area8c_lh'


#rdmModel category sig - crossnobis
#roi='MDroi_area9_rh'


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

#%% #single sub RDMs
iSub=5

rdm = np.zeros((12,12))
rdm[iu] = df[roi].iloc[iSub]

#make it a symmetric matrix 
il = np.tril_indices(12,-1) 
rdm[il] = rdm.T[il]
ax = plt.figure(figsize=(25,4))
ax = plt.imshow(rdm,cmap='viridis')
plt.colorbar()
plt.show()

pos = mds.fit(rdm).embedding_
plt.scatter(pos[:,0],pos[:,1],color=ctuple)
plt.show()


#%% model visualise

# 0:4 (inclusive) are 0, 0:5 (incl) are 1:5
#iu[0][0:5]
#iu[1][0:5]    
#modelRDM[iu[0][0:5],iu[1][0:5]]=np.ones(5)

# angular distance - direction
# https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles

# using % - modulo
#targetA=90
#sourceA=330
#a = targetA - sourceA
#a = (a + 180) % 360 - 180

#using a function:
#def f(x,y):
#  import math
#  return min(y-x, y-x+2*math.pi, y-x-2*math.pi, key=abs


modelRDM = np.zeros((12,12))

#category
modelRDM[0:6,6:12]=np.ones((6,6))
modelRDM[il] = modelRDM.T[il]

ax = plt.imshow(modelRDM,cmap='viridis')
plt.colorbar()
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
plt.show()

#orientation
angDist=np.empty((66)) #number of upper diagonal cells
conds = np.arange(0,210,30)
condsTmp = np.arange(30,180,30)
condsTmp=condsTmp[::-1]
conds = np.append(conds,condsTmp)
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
plt.show()

#%% model RDMs - category

exclSubs = True
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(df['subjCat'].iloc[iSub][0])
        nDirInCat[1,iSub]=len(df['subjCat'].iloc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)

#model
modelRDM = np.zeros((12,12))

#category
modelRDM[0:6,6:12]=np.ones((6,6))

#data
rdm = np.zeros((12,12)) 
rho = np.empty((sum(indSubs)))
tau = np.empty((sum(indSubs)))
pval = np.empty((sum(indSubs)))

useSubs=np.where(indSubs)
roiList=list(df)
roiList.remove('subjCat')
rhoAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
tauAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))

for iRoi in roiList:
    roi=iRoi
    rdm = np.zeros((12,12)) 
    rho=np.empty((sum(indSubs)))
    tau=np.empty((sum(indSubs)))
    pval=np.empty((sum(indSubs)))
    i=0
    for iSub in useSubs[0]:    
        rdm[iu] = df[roi].iloc[iSub]
        rho[i], pval[i]=stats.spearmanr(rdm[iu],modelRDM[iu])
#        tau[i], pval[i]=stats.kendalltau(rdm[iu],modelRDM[iu])
        tau[i] = kendall_a(rdm[iu],modelRDM[iu])
        i=i+1
    t,p=stats.ttest_1samp(rho,0)
    print('roi: %s' % (iRoi))
    print('spearman: t=%.3f, p=%.4f' % (t,p))
    t,p=stats.ttest_1samp(tau,0)
    print('tau-b: t=%.3f, p=%.4f' % (t,p))
    rhoAll[roi]=rho
    tauAll[roi]=tau
    
ax=rhoAll.mean().plot(figsize=(20,5),kind="bar",yerr=rhoAll.sem(),ylim=(-0.075,0.075))
ax=tauAll.mean().plot(figsize=(20,5),kind="bar",yerr=tauAll.sem(),ylim=(-0.04,0.04))


#%% model RDMs - angular distance - direction / ori 

exclSubs = True
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(df['subjCat'].iloc[iSub][0])
        nDirInCat[1,iSub]=len(df['subjCat'].iloc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
else:
    indSubs=np.ones(33,dtype=bool)

modelRDM = np.zeros((12,12))


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
#modelRDM[il] = modelRDM.T[il]



##orientation
#angDist=np.empty((66)) #number of upper diagonal cells
#conds = np.arange(0,210,30)
#condsTmp = np.arange(30,180,30)
#condsTmp=condsTmp[::-1]
#conds = np.append(conds,condsTmp)
#i=0
#for iCond in range(0,len(conds)):
#    for compCond in conds[len(conds)-len(conds[iCond:len(conds)])+1:len(conds)]:
#        angDist[i] = abs(((conds[iCond]-compCond) + 180) % 360 - 180)
#        i=i+1
#
#iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
#modelRDM[iu] = angDist




#data
rdm = np.zeros((12,12)) 
rho=np.empty((sum(indSubs)))
tau=np.empty((sum(indSubs)))
pval=np.empty((sum(indSubs)))

useSubs=np.where(indSubs)

roiList=list(df)
roiList.remove('subjCat')
rhoAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
tauAll = pd.DataFrame(columns=roiList,index=range(0,sum(indSubs)))
for iRoi in roiList:
    roi=iRoi
    rdm = np.zeros((12,12)) 
    rho=np.empty((sum(indSubs)))
    tau=np.empty((sum(indSubs)))
    pval=np.empty((sum(indSubs)))
    i=0
    for iSub in useSubs[0]:    
        rdm[iu] = df[roi].iloc[iSub]
        rho[i], pval[i]=stats.spearmanr(rdm[iu],modelRDM[iu])
#        tau[i], pval[i]=stats.kendalltau(rdm[iu],modelRDM[iu])
        tau[i] = kendall_a(rdm[iu],modelRDM[iu])
        i=i+1
    t,p=stats.ttest_1samp(rho,0)
    print('roi: %s' % (iRoi))
    print('spearman: t=%.3f, p=%.4f' % (t,p))
    t,p=stats.ttest_1samp(tau,0)
    print('tau-b: t=%.3f, p=%.4f' % (t,p))
    rhoAll[roi]=rho
    tauAll[roi]=tau
    
#ax=rhoAll.mean().plot(figsize=(20,5),kind="bar",yerr=rhoAll.sem(),ylim=(-0.075,0.075))
ax=tauAll.mean().plot(figsize=(20,5),kind="bar",yerr=tauAll.sem(),ylim=(-0.05,0.05))

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

for roi in rois:
    dfMean[roi] = np.mean(np.asarray(np.stack(df[roi].iloc[indSubs])),axis=0)
    dfSem[roi] = np.asarray(np.stack(df[roi].iloc[indSubs])).std(axis=0)/np.sqrt(sum(indSubs))
     
    
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

#plt.plot(np.stack(df[roi].iloc[0:33]).T)
  
iSub=8

roi='V2vd_rh'
plt.figure(figsize=(5,3))
plt.plot(np.stack(df[roi].iloc[iSub]).T)
roi='hMT_lh'
plt.figure(figsize=(5,3))
plt.plot(np.stack(df[roi].iloc[iSub]).T)
roi='MDroi_area8c_lh'
plt.figure(figsize=(5,3))
plt.plot(np.stack(df[roi].iloc[iSub]).T)




#%% univariate scatter plots, violin plots

roi='V2vd_rh'
dfPlt=pd.DataFrame(np.asarray(np.stack(df[roi].iloc[indSubs])))
ax = sns.catplot(data=dfPlt,height=8,aspect=2, kind="swarm",zorder=1)
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
ax2 = sns.catplot(data=dfPlt,height=8,aspect=2, kind="violin", inner=None,zorder=2)
ax2 = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)

roi='hMT_lh'
dfPlt=pd.DataFrame(np.asarray(np.stack(df[roi].iloc[indSubs])))
ax = sns.catplot(data=dfPlt,height=8,aspect=2, kind="swarm",zorder=1)
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
ax2 = sns.catplot(data=dfPlt,height=8,aspect=2, kind="violin", inner=None,zorder=2)
ax2 = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)

roi='MDroi_area8c_lh'
dfPlt=pd.DataFrame(np.asarray(np.stack(df[roi].iloc[indSubs])))
ax = sns.catplot(data=dfPlt,height=8,aspect=2, kind="swarm",zorder=1)
ax = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
ax2 = sns.catplot(data=dfPlt,height=8,aspect=2, kind="violin", inner=None,zorder=2)
ax2 = plt.errorbar(range(0,np.size(dfMean,axis=0)),dfMean[roi], yerr=dfSem[roi], fmt='-o',zorder=2)
