#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:10:41 2019

@author: robert.mok
"""
#%%
import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from statsmodels.stats.multitest import fdrcorrection as fdr
from statsmodels.stats.multitest import multipletests as multest

roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/mvpa_roi'

# laptop
#mainDir='/Users/robertmok/Documents/Postdoc_ucl/' 

subjCat=pd.read_pickle(os.path.join(roiDir, 'subjCat.pkl'))

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' #  'noNorm', 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'dCentred'
distMeth = 'svm' # 'svm', 'crossNobis', 'lda'
trainSetMeth = 'trials' # 'trials' or 'block' 
fwhm = None # optional smoothing param - 1, or None

decodeFeature = 'subjCat-orth-ctrl' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 

fname = os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + 
                      '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                      str(fwhm) + '_' + imDat)

##if looking at motor, uncomment:
#fname = fname + '_lock2resp'

#bilateral
#fname = fname + '_bilateral'

##decoding at feedback time
#fname = fname + '_fromfeedback'

#
df=pd.read_pickle(fname + '.pkl')
#df=pd.read_pickle(fname + '_model.pkl')
#df=pd.read_pickle(fname + '_guess.pkl')
#df=pd.read_pickle(fname + '_1.pkl')
#df=pd.read_pickle(fname + '_RMsubjCat.pkl')
print(df.loc['stats'])


# subjCat-orth
#df=pd.read_pickle(fname + '_RMsubjCat.pkl')
#df1=pd.read_pickle(fname + '_model.pkl')    # MT:.017, mMFG: .00519
###
###df1=pd.read_pickle(fname + '_1.pkl')
#ind = np.array([3, 4, 5, 12, 14, 16, 23, 26, 28, 31])  # subjCat vs model diffs
##df1=pd.read_pickle(fname + '_guess.pkl')
##ind = np.array([4, 5, 12, 23, 26])  # subjCat vs guess diffs
##
##
# recomputing tstat and pvals and savings to df
#roinames = list(df)
#chance = 0
#for roi in roinames:
#    df[roi].loc[ind] = df1[roi].loc[ind]
#    df[roi].loc['stats']=stats.ttest_1samp(df[roi].iloc[0:33].astype(float), chance, nan_policy='omit')
#
## add FFA/PPA
#for roi in ['FFA_lrh', 'PPA_lrh']:
#    df[roi] = df1[roi]
#print(df.loc['stats'])
#
#df.to_pickle(fname + '.pkl')

#pvals=np.empty((len(list(df))))
#for iRoi in range(0,len(list(df))):
#    pvals[iRoi]= df.loc['stats'][iRoi].pvalue

# correcting
# all rois apart from motor (12 ROIS)
#print(fdr(pvals[0:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[0:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)
# all rois apart from EVC and motor (10 ROIS)
#print(fdr(pvals[2:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[2:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)

# no EVC and motor - after added ffa/ppa (and also evc, but drop later):
ind = np.concatenate([np.arange(2,11), [len(pvals)-3, len(pvals)-2]])
#ind = np.concatenate([np.arange(2,11), [len(pvals)-2, len(pvals)-1]]) #after drop evc
print(fdr(pvals[ind]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[ind]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)

#%% exclude subs

exclSubs = False
exclParietalSubs = True
if exclSubs:
    indSubs[[1,6,31]] = False #trying without subs that couldn't flip motor response well - worse here always, but better for RDm cat pfc (w/out excluding above)
#    indSubs=np.ones(33,dtype=bool)
elif exclParietalSubs: # same, IPS no diff, others no diff
    indSubs=np.ones(33,dtype=bool)
    indSubs[[0,2,19,23]] = False #subs 1,3,20,24
else:
    indSubs=np.ones(33,dtype=bool)
    

newStats = pd.DataFrame(columns=list(df))
chance = 0 #0, 0.5, 1/12
for roi in list(df):
    newStats[roi] = stats.ttest_1samp(df[roi].iloc[indSubs].astype(float), chance, nan_policy='omit')
print(newStats.T)

pvals=newStats.iloc[1].values