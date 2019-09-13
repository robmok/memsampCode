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

decodeFeature = 'dir' # '12-way' (12-way dir decoding - only svm), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 

fname = os.path.join(roiDir, 'roi_' + decodeFeature + 'Decoding_' + distMeth + 
                      '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                      str(fwhm) + '_' + imDat)

##if looking at motor, uncomment:
#fname = fname + '_lock2resp'

df=pd.read_pickle(fname + '.pkl')
print(df.loc['stats'])


pvals=np.empty((len(list(df))-1))
for iRoi in range(0,len(list(df))-1):
    pvals[iRoi]= df.loc['stats'][iRoi].pvalue

print(fdr(pvals[0:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))
multest(pvals[0:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)

#first bunch for ori/12-way
#print(fdr(pvals[0:16]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[0:16]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)


#pSorted=np.sort(pvals)
#fdr(pSorted[0:22]/2,alpha=0.05,method='indep',is_sorted=True)
#multest(pSorted[0:22]/2, alpha=0.05, method='bonferroni', is_sorted=True, returnsorted=False)


#missed last subject in calculating tstats in mvpa
#chance=0.5
#indSubs=np.ones(33,dtype=bool)
#print(stats.ttest_1samp(df['hMT_lh'].iloc[indSubs],chance))
#print(stats.ttest_1samp(df['MDroi_area8c_lh'].iloc[indSubs],chance))
#print(stats.ttest_1samp(df['EVC_rh'].iloc[indSubs],chance))
#print(stats.ttest_1samp(df['EVC_lh'].iloc[indSubs],chance))





# recomputing tstat and pvals and savings to df
#chance=0
#for roi in list(df):
#    df[roi].loc['stats']=stats.ttest_1samp(df[roi].iloc[indSubs],chance)
##
#print(df.loc['stats'])
#df.to_pickle(fname + '.pkl')

#%% exclude subs

exclSubs = False
if exclSubs:
    nDirInCat=np.empty((2,33))
    for iSub in range(0,33):
        nDirInCat[0,iSub]=len(subjCat.loc[iSub][0])
        nDirInCat[1,iSub]=len(subjCat.loc[iSub][1])
    indSubs=nDirInCat[0,:]==nDirInCat[1,:]
        
#    indSubs[:]=True # reset if don't include excl above
#    indSubs[[1,6,31]] = False #trying without subs that couldn't flip motor response well - worse here always, but better for RDm cat pfc (w/out excluding above)
else:
    indSubs=np.ones(33,dtype=bool)
    

newStats = pd.DataFrame(columns=list(df))
chance = .5 #0, 0.5, 1/12
for roi in list(df):
    newStats[roi]=stats.ttest_1samp(df[roi].iloc[indSubs],chance)
print(newStats.T)


pvals=newStats.iloc[1].values
#print(fdr(pvals[0:len(pvals)-2]/2,alpha=0.05,method='indep',is_sorted=False))
#multest(pvals[0:len(pvals)-2]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)

#print(fdr(pvals[0:len(pvals)-11]/2,alpha=0.05,method='indep',is_sorted=False))
#print(multest(pvals[0:len(pvals)-11]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False))


#12-way (0:12 for visRois, 0:16 incl some IPS but note not same for all)
#print(fdr(pvals[0:12]/2,alpha=0.05,method='indep',is_sorted=False))
#print(multest(pvals[0:12]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False))
#ori
print(fdr(pvals[0:6]/2,alpha=0.05,method='indep',is_sorted=False))
print(multest(pvals[0:6]/2, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False))