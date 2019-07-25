#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 18:32:17 2019

RSA analyses, plotting RDMs

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

decodeFeature = 'subjCat-all' # subjCat-orth, '12-way', 'dir' (opposite dirs), 'ori' (orthogonal angles)

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))

#load in subjCat
subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))
#load in behav acc
behav=np.load(os.path.join(behavDir, 'memsamp_acc_subjCat.npz'))
locals().update(behav) #load in each variable into workspace

#%% plot RDMs (data)
    
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
#%% plot single sub RDMs
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
#%% Visualise RDM models
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
#roiList.remove('subjCat')
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
            nCondA=len(subjCat.loc[iSub][0])
            nCondB=len(subjCat.loc[iSub][1])
            catRDM = np.zeros((12,12))
            catRDM[0:nCondB,nCondA:12]=np.ones((nCondB,nCondB))
        else:
            catRDM = np.zeros((12,12))
            catRDM[0:6,6:12]=np.ones((6,6))
        
        rho[i], pval[i]=stats.spearmanr(rdm[iu],catRDM[iu])
#         rhoTmp=partial_corr(np.stack((stats.rankdata(rdm[iu]),stats.rankdata(catRDM[iu]),stats.rankdata(modelRDM[iu]))).T)
#         rho[i]=rhoTmp[0,1]
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
#roiList.remove('subjCat')
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
#        conds=np.append(subjCat.loc[iSub][0],subjCat.loc[iSub][1],axis=0)
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
#roiList.remove('subjCat')
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
#        conds=np.append(subjCat.loc[iSub][0],subjCat.loc[iSub][1],axis=0)
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


roiList=list(df)
roiList.remove('subjCat')
rAcc_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
rAccA_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
rAccB_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
rObjAcc_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
for roi in roiList:
    rAcc_RDM[roi][0], rAcc_RDM[roi][1]=stats.pearsonr(acc[indSubs],tauOri[roi].iloc[indSubs])
    rAccA_RDM[roi][0], rAccA_RDM[roi][1]=stats.pearsonr(accA[indSubs],tauOri[roi].iloc[indSubs])
    rAccB_RDM[roi][0], rAccB_RDM[roi][1]=stats.pearsonr(accB[indSubs],tauOri[roi].iloc[indSubs])
    rObjAcc_RDM[roi][0], rObjAcc_RDM[roi][1]=stats.pearsonr(objAcc[indSubs],tauOri[roi].iloc[indSubs])


plt.scatter(tauOri['V1vd_lh'].iloc[indSubs],acc[indSubs])
plt.show()


#roiList=list(df)
#roiList.remove('subjCat')
#rAcc_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
#rAccA_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
#rAccB_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
#rObjAcc_RDM=pd.DataFrame(columns=roiList,index=range(0,2))
#for roi in roiList:
#    rAcc_RDM[roi][0], rAcc_RDM[roi][1]=stats.pearsonr(acc[indSubs],tauDir[roi].iloc[indSubs])
#    rAccA_RDM[roi][0], rAccA_RDM[roi][1]=stats.pearsonr(accA[indSubs],tauDir[roi].iloc[indSubs])
#    rAccB_RDM[roi][0], rAccB_RDM[roi][1]=stats.pearsonr(accB[indSubs],tauDir[roi].iloc[indSubs])
#    rObjAcc_RDM[roi][0], rObjAcc_RDM[roi][1]=stats.pearsonr(objAcc[indSubs],tauDir[roi].iloc[indSubs])


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