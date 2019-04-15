#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:00:52 2019

@author: robert.mok
"""

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#import bootstrapped.bootstrap as bs
#import bootstrapped.stats_functions as bs_stats

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/'
#roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi/bilateral'

# laptop
roiDir='/Users/robertmok/Documents/Postdoc_ucl/mvpa_roi/' 

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'crossNobis' # 'svm', 'crossNobis'
trainSetMeth = 'block' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-all' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)

df=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
#%% plot

#p = avg_time.plot(figsize=15,5),legend=False,kind="bar",rot=45,color="blue",fontsize=16,yerr=std);

#linestyle='None' - makes simple points at the mean

#stdAll = df.iloc[0:33,:].std()/np.sqrt(33)
stdAll = df.iloc[0:33,:].sem()
# bootstrap CIs - over subjects....
#print(bs.bootstrap(np.asarray(df.iloc[0:33,0]), stat_func=bs_stats.mean))


ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll)
#ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll,ylim=(.5,.537))
#ax=df.iloc[0:33,:].mean().plot(figsize=(15,5),kind="bar",yerr=stdAll,ylim=(1/12,0.097))

#%% subjCat-all

#df1 = pd.DataFrame(columns=df.columns,index=['mean', 'sem'])

#for roi in df.columns.values[0:-1]:
#
roi='dlPFC_lh'
#roi='dlPFC_rh'
roi='MDroi_ips_lh'
roi='MDroi_ips_rh'
#roi='V1vd_lh'

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

ax = plt.figure(figsize=(8,4))
ctuple=np.array((0.1,0.3,0.5))
for iCond in range(0,6):
    ax = plt.figure(figsize=(4,3))
    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
    ctuple = ctuple+0.05

ax = plt.figure(figsize=(8,4))
ctuple=np.array((0.5,0.3,0.1))
for iCond in range(6,12):
    ax = plt.figure(figsize=(4,3))
    ax = plt.errorbar(range(0,12),rdmMean[iCond,:], yerr=rdmSE[iCond,:], fmt='-o', color=ctuple)
    ctuple = ctuple+0.05
    
#ax = plt.errorbar(range(0,11),rdmMean[0,1:-1], yerr=rdmSE[0,1:-1], fmt='-o')

#ylim1, ylim2 = plt.ylim()
#plt.ylim(ylims[0],ylims[1])

#%% plot RDM
#roi='dlPFC_rh'
roi='dlPFC_lh'
#roi='V1vd_lh'

rdm = np.zeros((12,12))

iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
rdm[iu] = df[roi].iloc[0:33].mean(axis=0)
#make it a symmetric matrix 
#il = np.tril_indices(12,-1) 
#rdm[il] = rdm.T[il]

#tstat (double check formula)
rdm[iu] = df[roi].iloc[0:33].mean(axis=0)/np.stack(df[roi].iloc[0:33]).std(axis=0)/np.sqrt(33)

ax = plt.figure(figsize=(25,4))
ax = plt.imshow(rdm,cmap='viridis')
plt.colorbar()