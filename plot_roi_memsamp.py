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
#roiDir='/Users/robertmok/Documents/Postdoc_ucl/mvpa_roi/' 

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
#roi='dlPFC_lh'
#roi='dlPFC_rh'
roi='V1vd_lh'
    

ylims=(.4,.6)
ylims=(-0.04,0.04)
#ylims=(-0.01,0.01)

stdAll=np.stack(df[roi].iloc[0:33]).std(axis=0)

ax = plt.figure(figsize=(15,4))
#ax = plt.bar(range(0,55),df[roi].iloc[0:33].mean(axis=0),yerr=stdAll)

ax0=plt.errorbar(range(0,55), df[roi].iloc[0:33].mean(axis=0), yerr=stdAll, fmt='-o')

ylim1, ylim2 = plt.ylim()
plt.ylim(ylims[0],ylims[1])


iSub=0

nA=len(df['subjCat'].iloc[iSub][0])
nB=len(df['subjCat'].iloc[iSub][1])

# distance to first stim (more similar = lower acc or shorter distance)
#df[roi].iloc[iSub][0:nA]
#df[roi].iloc[iSub][nA:nA+nB]


df[roi].iloc[iSub][0:nA-1] #because first one is in catA
df[roi].iloc[iSub][nA-1:nA-1+nB]

#indA=np.arange(0,nA)
#indB=np.arange(nA,nA+nB)

#
nCond=12
#ind1=range(0,nCond-1)
#ind2=range(nCond,(nCond*2)-2)
#ind3=range((nCond*2)-2)

ind1=range(0,nCond-1)
ind2=range(nCond,nCond+10)
ind3=range(nCond+10,nCond+10+9)
ind4=range(nCond+10+9,nCond+10+9+8)


#np.reshape? - but need to add the extra ones to all other ones (apart from first)
#df[roi].iloc[iSub]










#or better to make the matrix, make it symmetric then index from there..?

#rdm = np.zeros((11,11))
#iu = np.triu_indices(11,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
#rdm[iu] = df[roi].iloc[0:33].mean(axis=0)
#il = np.tril_indices(11,-1)  #make it a symmetric matrix
#rdm[il] = df[roi].iloc[0:33].mean(axis=0)
#
#iCond=0
#rdm[iCond,1:nA+1]
#rdm[iCond,nA+1:nA+nB] #need +1 to get the 12th value?
#
##for the next cond, need to wrap araound...
#
#
## - nconds in A from the diagonal, then conds in B to the end, 
# then add the rest on the other side of the diagonal. not sure if this makes sense...



#%% plot RDM
#roi='dlPFC_rh'
#roi='dlPFC_lh'
roi='V1vd_lh'

rdm = np.zeros((12,12))

iu = np.triu_indices(12,1) #upper triangle, 1 from the diagonal (i.e. ignores diagonal)
rdm[iu] = df[roi].iloc[0:33].mean(axis=0)

#make it a symmetric matrix - check if this is correct (looks asymmetric...)
#il = np.tril_indices(11,-1) 
#rdm[il] = df[roi].iloc[0:33].mean(axis=0)

ax = plt.figure(figsize=(25,4))
ax = plt.imshow(rdm,cmap='viridis')
plt.colorbar()






