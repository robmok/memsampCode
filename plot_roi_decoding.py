#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 18:31:03 2019

Plotting decoding analyses (svms)

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

#%% plot bar / errorbar plot

saveFigs = False

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
if (decodeFeature=="subjCat-orth")|(decodeFeature=="objCat-orth"):
    chance = 0
elif decodeFeature == "12-way":
    chance = 1/12
else:
    chance = .5    
    
ylims = [-.025,.0375]
ax=(df.iloc[indSubs,:].mean()-chance).plot(figsize=(8,5),kind="bar",yerr=stdAll,ylim=ylims,title=decodeFeature)
plt.tight_layout()
#ax=df.iloc[indSubs,:].mean().plot(figsize=(20,5),yerr=stdAll, fmt='o')

if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barPlot_allROIs_' + decodeFeature + '.pdf'))

# without excluding, V2 p=0.1 MT: p=0.02715; area8c_lhp= 0.00855  - NOTE: pvals are 2-tailed; should be 1, so halve them
# after excluding, V2 p=0.3449, MT: p=0.0346, area8c_lh: p=0.00337 
#print(stats.ttest_1samp(df['V2vd_rh'].iloc[indSubs],0))
#print(stats.ttest_1samp(df['hMT_lh'].iloc[indSubs],0))
#print(stats.ttest_1samp(df['MDroi_area8c_lh'].iloc[indSubs],0))

#loaded in subjCat-orth first, saved to df1, then loaded in dir to compare. MT and PFC sig
#stats.ttest_rel(df1['V2vd_rh'].iloc[indSubs],df['V2vd_rh'].iloc[indSubs]-.5)
#stats.ttest_rel(df1['hMT_lh'].iloc[indSubs],df['hMT_lh'].iloc[indSubs]-.5)
#stats.ttest_rel(df1['MDroi_area8c_lh'].iloc[indSubs],df['MDroi_area8c_lh'].iloc[indSubs]-.5)

#%% univariate scatter plots, violin plots

ax = sns.catplot(data=df.iloc[indSubs,:],height=4,aspect=4, kind="swarm")
df.iloc[indSubs,:].mean().plot(yerr=stdAll, fmt='o')

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