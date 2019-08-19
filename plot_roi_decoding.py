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
from numpy.polynomial.polynomial import polyfit

import statsmodels.api as sm

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
distMeth = 'svm' # 'svm', 'crossNobis', 'mNobis' - for subjCat-orth and -all
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-minus-motor' # subjCat-orth, '12-way', 'dir' (opposite dirs), 'ori' (orthogonal angles)

fname = os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + 
                      '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                      str(fwhm) + '_' + imDat)

#if looking at motor, uncomment:
#fname = fname + '_lock2resp'

df=pd.read_pickle(fname + '.pkl')

#load in subjCat
subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))
#load in behav acc
behav=np.load(os.path.join(behavDir, 'memsamp_acc_subjCat.npz'))
locals().update(behav) #load in each variable into workspace

#%% plot bar / errorbar plot
#plt.rcdefaults()
plt.style.use('seaborn-darkgrid')

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
if (decodeFeature=="subjCat-orth")|(decodeFeature=="objCat-orth")|(decodeFeature=="subjCat-minus-motor"):
    chance = 0
elif decodeFeature == "12-way":
    chance = 1/12
else:
    chance = .5    
    
ylims = [-.0275,.0375]
fig, ax = plt.subplots(figsize=(8,5))
(df.iloc[indSubs,:].mean()-chance).plot(ax=ax,kind="bar",yerr=stdAll,ylim=ylims,title=decodeFeature)
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
#stats.ttest_rel(df1['hMT_lh'].iloc[indSubs],df['hMT_lh'].iloc[indSubs]-.5)
#stats.ttest_rel(df1['MDroi_area8c_lh'].iloc[indSubs],df['MDroi_area8c_lh'].iloc[indSubs]-.5)

#%% univariate scatter plots, violin plots

ax = sns.catplot(data=df.iloc[indSubs,:],height=3.5,aspect=4.25, kind="swarm")
df.iloc[indSubs,:].mean().plot(yerr=stdAll, fmt='o')

g = sns.catplot(data=df.iloc[indSubs,:],height=3,aspect=5, kind="violin", inner=None)
sns.swarmplot(color="k", size=3, data=df.iloc[indSubs,:], ax=g.ax);

#%% plotting within area, across decoders

plt.rcdefaults()
#plt.style.use('seaborn-darkgrid')

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
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
decodeFeature = '12-way'
df12way=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth 
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
decodeFeature = 'ori'
dfOri=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth 
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))
decodeFeature = 'dir'
dfDir=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth  
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))

decodeFeature = 'motor'
dfMotor=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth  
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '_lock2resp.pkl')))

dfHeader=['Category','12-way','Ori','Dir','Motor']

#extra
decodeFeature = 'motor'
dfMotorCue=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth  
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))

decodeFeature = 'subjCat-minus-motor'
dfSubjCatMotor=pd.read_pickle((os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + '_' + normMeth 
                                        + '_' + trainSetMeth + '_fwhm' + str(fwhm) + '_' + imDat + '.pkl')))

 
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
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5,dfMotor[roi].iloc[indSubs]-.5],axis=1)
svm_area8c.columns=dfHeader
g = sns.catplot(data=svm_area8c,height=5,aspect=1, kind="bar", ci=None)
svm_area8c.mean().plot(yerr=svm_area8c.sem(),ylim=(-.115,.15), title='Left dlPFC (area 8)',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_area8c, ax=g.ax);
plt.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
    #plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.eps'))
plt.show()

roi='hMT_lh' #category
svm_MT_lh = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12, 
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5,dfMotor[roi].iloc[indSubs]-.5],axis=1)
svm_MT_lh.columns=dfHeader
g = sns.catplot(data=svm_MT_lh,height=5,aspect=1, kind="bar", ci=None)
svm_MT_lh.mean().plot(yerr=svm_MT_lh.sem(),ylim=(-.115,.15), title='Left MT (motion sensitive)',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_MT_lh, ax=g.ax);
plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()

roi='hMT_rh' #12-way (ori is p=0.04, one-tailed, uncorrected)
svm_MT_rh = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12, 
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5,dfMotor[roi].iloc[indSubs]-.5],axis=1)
svm_MT_rh.columns=dfHeader
g = sns.catplot(data=svm_MT_rh,height=5,aspect=1, kind="bar", ci=None)
svm_MT_rh.mean().plot(yerr=svm_MT_rh.sem(),ylim=(-.115,.15), title='Right MT (motion sensitive)',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_MT_rh, ax=g.ax);
plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()


roi='EVC_rh'
svm_V1_rh = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12, 
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5,dfMotor[roi].iloc[indSubs]-.5],axis=1)
svm_V1_rh.columns=dfHeader
g = sns.catplot(data=svm_V1_rh,height=5,aspect=1, kind="bar", ci=None)
svm_V1_rh.mean().plot(yerr=svm_V1_rh.sem(),ylim=(-.06,.1), title='Right Early Visual Cortex',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_V1_rh, ax=g.ax);
plt.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()

roi='motor_rh'
svm_motor_rh = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12, 
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5,dfMotor[roi].iloc[indSubs]-.5],axis=1)
svm_motor_rh.columns=dfHeader
g = sns.catplot(data=svm_motor_rh,height=5,aspect=1, kind="bar", ci=None)
svm_motor_rh.mean().plot(yerr=svm_motor_rh.sem(),ylim=(-.06,.1), title='Right Primary Motor Cortex',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_motor_rh, ax=g.ax);
plt.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()

roi='motor_lh'
svm_motor_lh = pd.concat([dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12, 
                        dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5,dfMotor[roi].iloc[indSubs]-.5],axis=1)
svm_motor_lh.columns=dfHeader
g = sns.catplot(data=svm_motor_lh,height=5,aspect=1, kind="bar", ci=None)
svm_motor_lh.mean().plot(yerr=svm_motor_lh.sem(),ylim=(-.06,.1), title='Left Primary Motor Cortex',elinewidth=2.5,fmt='k,',alpha=0.8)
sns.stripplot(color="k", alpha=0.2, size=3, data=svm_motor_lh, ax=g.ax);
plt.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_barStripPlot_' + roi + '.pdf'))
plt.show()

roi='MDroi_area8c_lh'
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],dfDir[roi].iloc[indSubs]-.5) # one-tailed p=0.003
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],dfOri[roi].iloc[indSubs]-.5) # one-tailed p=0.003
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12) #one-tailed 0.0035
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],dfMotor[roi].iloc[indSubs]-.5) # one-tailed p=0.049

roi='hMT_lh'
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],dfDir[roi].iloc[indSubs]-.5) # one-tailed p=0.03
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],dfOri[roi].iloc[indSubs]-.5) # one-tailed p=0.03
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12) #one-tailed 0.019
stats.ttest_rel(dfSubjCat[roi].iloc[indSubs],dfMotor[roi].iloc[indSubs]-.5) # one-tailed p=0.42

roi='hMT_rh' #pairwise all n.s.
stats.ttest_rel(df12way[roi].iloc[indSubs]-1/12,dfDir[roi].iloc[indSubs]-.5) #
stats.ttest_rel(df12way[roi].iloc[indSubs]-1/12,dfOri[roi].iloc[indSubs]-.5) # 
stats.ttest_rel(df12way[roi].iloc[indSubs]-1/12,dfSubjCat[roi].iloc[indSubs]) #
stats.ttest_rel(df12way[roi].iloc[indSubs]-1/12,dfMotor[roi].iloc[indSubs]-.5) #
#stats.ttest_rel(df12way[roi].iloc[indSubs]-1/12,dfSubjCatMotor[roi].iloc[indSubs]) #0.06


roi='EVC_rh'
stats.ttest_rel(dfOri[roi].iloc[indSubs]-.5,dfDir[roi].iloc[indSubs]-.5) # one-tailed p=0.0487
stats.ttest_rel(dfOri[roi].iloc[indSubs]-.5,dfSubjCat[roi].iloc[indSubs]) 
stats.ttest_rel(dfOri[roi].iloc[indSubs]-.5,df12way[roi].iloc[indSubs]-1/12)
stats.ttest_rel(dfOri[roi].iloc[indSubs]-.5,dfMotor[roi].iloc[indSubs]-.5) # 
#stats.ttest_rel(dfOri[roi].iloc[indSubs]-.5,dfSubjCatMotor[roi].iloc[indSubs])  #.08+

#stats.spearmanr(dfSubjCat[roi].iloc[indSubs],dfOri[roi].iloc[indSubs]-.5)

#extra:
#subjCat-minus-motor
roi='MDroi_area8c_lh'
stats.ttest_rel(dfSubjCatMotor[roi].iloc[indSubs],dfDir[roi].iloc[indSubs]-.5) # one-tailed p=0.004
stats.ttest_rel(dfSubjCatMotor[roi].iloc[indSubs],dfOri[roi].iloc[indSubs]-.5) # one-tailed p=0.01
stats.ttest_rel(dfSubjCatMotor[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12) #one-tailed 0.005

roi='hMT_lh'
stats.ttest_rel(dfSubjCatMotor[roi].iloc[indSubs],dfDir[roi].iloc[indSubs]-.5) # one-tailed p=0.07
stats.ttest_rel(dfSubjCatMotor[roi].iloc[indSubs],dfOri[roi].iloc[indSubs]-.5) # one-tailed p=0.075
stats.ttest_rel(dfSubjCatMotor[roi].iloc[indSubs],df12way[roi].iloc[indSubs]-1/12) #one-tailed 0.055

#%% behav corr svm

saveFigs = False

mrkSiz=15
fntSiz=14
greycol=tuple([0.5,0.5,0.5])

plt.style.use('seaborn-darkgrid')

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
#    rAccA[roi][0], rAccA[roi][1]=stats.pearsonr(accA[indSubs],df[roi].iloc[indSubs])
#    rAccB[roi][0], rAccB[roi][1]=stats.pearsonr(accB[indSubs],df[roi].iloc[indSubs])
#    rObjAcc[roi][0], rObjAcc[roi][1]=stats.pearsonr(objAcc[indSubs],df[roi].iloc[indSubs])

roi = 'MDroi_area8c_lh'
x=acc[indSubs]
y=np.array(df[roi].iloc[indSubs],dtype=float)
b, m = polyfit(x,y, 1) 
xAx=np.linspace(min(x),max(x))
fig, ax = plt.subplots(figsize=(5,3.5))
ax.plot(xAx, b + m * xAx,'-',color=greycol,linewidth=1,alpha=0.5)
ax.scatter(x,y,s=mrkSiz)
ax.set_xlabel('Behavioral Accuracy')
ax.set_ylabel('Decoding Accuracy (normalized)')
ax.set_title('Left dlPFC (area 8)',fontsize=fntSiz)
legTxt='\n'.join(('r = %.2f' % (rAcc[roi][0]), 'p = %.2f' % (rAcc[roi][1]/2)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, legTxt, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
fig.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_behavDecodeCorr_' + roi + '.pdf'))

roi = 'MDroi_area9_rh'

x=acc[indSubs]
y=np.array(df[roi].iloc[indSubs],dtype=float)
b, m = polyfit(x,y, 1) 
xAx=np.linspace(min(x),max(x))
fig, ax = plt.subplots(figsize=(5,3.5))
ax.plot(xAx, b + m * xAx,'-',color=greycol,linewidth=1,alpha=0.5)
ax.scatter(x,y,s=mrkSiz)
ax.set_xlabel('Behavioral Accuracy')
ax.set_ylabel('Decoding Accuracy (normalized)')
ax.set_title('Right dlPFC (area 9)',fontsize=fntSiz)
legTxt='\n'.join(('r = %.2f' % (rAcc[roi][0]), 'p = %.2f' % (rAcc[roi][1]/2)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, legTxt, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
fig.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_behavDecodeCorr_' + roi + '.pdf'))
    
roi = 'hMT_lh'

x=acc[indSubs]
y=np.array(df[roi].iloc[indSubs],dtype=float)
b, m = polyfit(x,y, 1) 
xAx=np.linspace(min(x),max(x))
fig, ax = plt.subplots(figsize=(5,3.5))
ax.plot(xAx, b + m * xAx,'-',color=greycol,linewidth=1,alpha=0.5)
ax.scatter(x,y,s=mrkSiz)
ax.set_xlabel('Behavioral Accuracy')
ax.set_ylabel('Decoding Accuracy (normalized)')
ax.set_title('Left MT',fontsize=fntSiz)
legTxt='\n'.join(('r = %.2f' % (rAcc[roi][0]), 'p = %.2f' % (rAcc[roi][1]/2)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, legTxt, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
fig.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_behavDecodeCorr_' + roi + '.pdf'))

roi = 'EVC_rh'
x=acc[indSubs]
y=np.array(df[roi].iloc[indSubs],dtype=float)
b, m = polyfit(x,y, 1) 
xAx=np.linspace(min(x),max(x))
fig, ax = plt.subplots(figsize=(5,3.5))
ax.plot(xAx, b + m * xAx,'-',color=greycol,linewidth=1,alpha=0.5)
ax.scatter(x,y,s=mrkSiz)
ax.set_xlabel('Behavioral Accuracy')
ax.set_ylabel('Decoding Accuracy (normalized)')
ax.set_title('Right EVC',fontsize=fntSiz)
legTxt='\n'.join(('r = %.2f' % (rAcc[roi][0]), 'p = %.2f' % (rAcc[roi][1]/2)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, legTxt, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
fig.tight_layout()
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_behavDecodeCorr_' + roi + '.pdf'))
    
    
#%% #robust regression
#x=acc[indSubs]
#y=np.array([np.array(df['MDroi_area8c_lh'].iloc[indSubs],dtype=float),np.array(df['hMT_lh'].iloc[indSubs],dtype=float)]).T
##y=np.array([np.array(df['MDroi_area8c_lh'].iloc[indSubs],dtype=float),np.array(df['hMT_lh'].iloc[indSubs],dtype=float),np.array(df['EVC_rh'].iloc[indSubs],dtype=float)]).T
##y=np.array(df['MDroi_area8c_lh'].iloc[indSubs],dtype=float)
##y=np.array(df['hMT_lh'].iloc[indSubs],dtype=float)
##y=np.array(df['EVC_rh'].iloc[indSubs],dtype=float)
#
#huber_t = sm.RLM(x,y, M=sm.robust.norms.HuberT()) 
#hub_results = huber_t.fit()
#print(hub_results.params)
#print(hub_results.bse)
#print(hub_results.summary(yname='behavAcc',
#            xname=['var_%d' % i for i in range(len(hub_results.params))]))

plt.rcdefaults()
#plt.style.use('seaborn-darkgrid')
fntSiz=9.5 #fntSiz>10 cuts offf...

saveFigs = False

robustPlot = True #set to false when testing out things in plotting (takes time) 

#plot with CIs of the slopes
roi = 'MDroi_area8c_lh'
x=acc[indSubs]
y=np.array(df[roi].iloc[indSubs],dtype=float)
huber_t = sm.RLM(x,y, M=sm.robust.norms.HuberT()) 
hub_results = huber_t.fit()
dfPlot=pd.DataFrame(data=[x,y], index=['Behavioral Accuracy','Decoding Accuracy (normalized)'], columns=None)
ax = sns.lmplot(x='Behavioral Accuracy',y='Decoding Accuracy (normalized)',data=dfPlot.T, robust=robustPlot, height=4, aspect=1.1)
plt.title('Left dlPFC (area 8)',fontsize=fntSiz)
legTxt='\n'.join(('b = %.2f' % hub_results.params, 'p < %.3f' % (hub_results.pvalues/2)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.fig.text(0.225, 0.925, legTxt, fontsize=14, verticalalignment='top', bbox=props) #rcdefaults - white bg
#ax.fig.text(0.195, 0.935, legTxt, fontsize=14, verticalalignment='top', bbox=props) #seaborn-darkgrid - grey bg w/ grid
ax.fig.tight_layout
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_behavDecodeCorr_robustReg_' + roi + '.pdf'))
    
roi = 'hMT_lh'
x=acc[indSubs]
y=np.array(df[roi].iloc[indSubs],dtype=float)
huber_t = sm.RLM(x,y, M=sm.robust.norms.HuberT())   
hub_results = huber_t.fit()
dfPlot=pd.DataFrame(data=[x,y], index=['Behavioral Accuracy','Decoding Accuracy (normalized)'], columns=None)
ax = sns.lmplot(x='Behavioral Accuracy',y='Decoding Accuracy (normalized)',data=dfPlot.T, robust=robustPlot, height=4, aspect=1.1)
plt.title('Left MT',fontsize=fntSiz)
legTxt='\n'.join(('b = %.2f' % hub_results.params, 'p < %.3f' % (hub_results.pvalues/2)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.fig.text(0.225, 0.925, legTxt, fontsize=14, verticalalignment='top', bbox=props)
#ax.fig.text(0.195, 0.935, legTxt, fontsize=14, verticalalignment='top', bbox=props)
ax.fig.tight_layout
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_behavDecodeCorr_robustReg_' + roi + '.pdf'))
    
roi = 'EVC_rh'
x=acc[indSubs]
y=np.array(df[roi].iloc[indSubs],dtype=float)
huber_t = sm.RLM(x,y, M=sm.robust.norms.HuberT()) 
hub_results = huber_t.fit()
dfPlot=pd.DataFrame(data=[x,y], index=['Behavioral Accuracy','Decoding Accuracy (normalized)'], columns=None)
ax = sns.lmplot(x='Behavioral Accuracy',y='Decoding Accuracy (normalized)',data=dfPlot.T, robust=robustPlot, height=4, aspect=1.1)
legTxt='\n'.join(('b = %.2f' % hub_results.params, 'p = %.3f' % (hub_results.pvalues)))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.fig.text(0.24, 0.275, legTxt, fontsize=14, verticalalignment='top', bbox=props)
#ax.fig.text(0.21, 0.25, legTxt, fontsize=14, verticalalignment='top', bbox=props)
plt.title('Right EVC',fontsize=fntSiz)
ax.fig.tight_layout
if saveFigs:
    plt.savefig(os.path.join(figDir,'mvpaROI_behavDecodeCorr_robustReg_' + roi + '.pdf'))

##corr between 2 areas
#
#roi1 = 'MDroi_area8c_lh'
#roi2 = 'hMT_lh'
#x=np.array(df[roi1].iloc[indSubs],dtype=float)
#y=np.array(df[roi2].iloc[indSubs],dtype=float)
#b, m = polyfit(x,y, 1) 
#xAx=np.linspace(min(x),max(x))
#fig, ax = plt.subplots(figsize=(5,3.5))
#ax.plot(xAx, b + m * xAx,'-',color=greycol,linewidth=1,alpha=0.5)
#ax.scatter(x,y,s=mrkSiz)
#r,p=stats.pearsonr(df[roi1].iloc[indSubs],df[roi2].iloc[indSubs]) #=0.039
#r,p=stats.spearmanr(df[roi1].iloc[indSubs],df[roi2].iloc[indSubs]) #n.s.!
#legTxt='\n'.join(('r = %.2f' % r, 'p = %.3f' % p))
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#ax.text(0.05, 0.95, legTxt, transform=ax.transAxes, fontsize=14,
#        verticalalignment='top', bbox=props)
#fig.tight_layout()


