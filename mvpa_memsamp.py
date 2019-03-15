#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:48:06 2019

@author: robert.mok
"""
import sys
sys.path.append('/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/')
import os
#import glob
import numpy as np
from nilearn import image as nli # Import image processing tool
import pandas as pd
#import matplotlib.pyplot as plt
#import nilearn.plotting as nip
import nibabel as nib
from nilearn.masking import apply_mask 
from nilearn.signal import clean 
from sklearn.model_selection import cross_val_score, LeaveOneGroupOut
from sklearn.svm import LinearSVC
import scipy.stats as stats

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep'
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
os.chdir(codeDir)

from memsamp_RM import crossEuclid

#set to true if rerunning only a few rois, appending it to old df
reRun = False 

imDat    = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'svm' # 'svm', 'crossEuclid', 'crossNobis'
trainSetMeth = 'trials' # 'trials' or 'block' - only tirals in this script
fwhm = 1 # optional smoothing param - 1, or None

decodeFeature = 'dir' # '12-way' (12-way dir decoding - only svm), '12-way-all' (output single decoder for each dir vs all), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# others: 


#%%
# =============================================================================
# Set up decoding accuracy dataframe 
# =============================================================================
nSubs=33
rois = ['V1vd','V2vd','V3vd','V3a','V3b','hV4','MST','hMT','IPS0','IPS1','IPS2',
        'IPS3','IPS4','IPS5','SPL1', 'visRois', 'ipsRois', 'visRois_ipsRois'] # MST - leaving out coz only a few voxels? ; 'V01' 'V02' 'PHC1' 'PHC2' 'MST' 'hMT' 'L02' 'L01'

#no SPL1
rois = ['V1vd','V2vd','V3vd','V3a','V3b','hV4','MST','hMT','IPS0','IPS1','IPS2',
        'IPS3','IPS4','IPS5', 'visRois', 'ipsRois', 'visRois_ipsRois'] # MST - leaving out coz only a few voxels? ; 'V01' 'V02' 'PHC1' 'PHC2' 'MST' 'hMT' 'L02' 'L01'

dfDecode = pd.DataFrame(columns=rois, index=range(0,nSubs+1))
dfDecode.rename(index={nSubs:'stats'}, inplace=True)

# =============================================================================
# load in trial log and append image paths
# =============================================================================

# - first try the LOO one with 'trials'. then load in blocks
    # - load in sub-01_task-memsamp_run-01_events.tsv #in bidsdi
    # - append run number
    # - append path to image - match 0:30:270 degrees to condition 1:12, trialwise (N.B. cope number is not the same for trialwise! 7 trials)
    # - load in all 3 runs then merge the 3 dfs

for iSub in range(1,nSubs+1):
    subNum=f'{iSub:02d}'
    dfCond=pd.DataFrame() #main df with all runs
    if iSub in {9,12,16,26}:
        runs = range(1,5) #4 runs
    else:
        runs = range(1,4) #3 runs
    for iRun in runs:
        condPath=os.path.join(mainDir, 'orig_events','sub-' + subNum + 
                              '_task-memsamp_run-0' + str(iRun) +'_events.tsv')
        
        # df to load in and organise run-wise data
        df = pd.read_csv(condPath, sep='\t')
        df['run'] = pd.Series(np.ones((len(df)))*iRun,index=df.index) #add run number
        #df.loc[:,'run2']=pd.Series(np.ones((len(df)))*iRun,index=df.index) #alt way - better/worse?
        
        # add path to match cue condition and trial number - cope1:7 is dir0 trial1:7   
        conds=df.direction.unique()
        conds.sort()
        #sort - arrange df so it matches cope1:84 image structure
        df2=pd.DataFrame() 
        for iCond in conds:
            df2 = df2.append(df[df['direction']==iCond])
        
        copeNum=1 #counter
        imPath=[]
        for iCond in conds:
            for iTrial in range(1,8): #calculate cope number
                #make a list and append to it
                imPath.append(os.path.join(featDir, 'sub-' + subNum + '_run-0'
                                           + str(iRun) +'_trial_T1_fwhm0.feat',
                                           'stats',imDat + (str(copeNum)) + '.nii.gz'))
                copeNum=copeNum+1
        df2['imPath']=pd.Series(imPath,index=df2.index)
        dfCond = dfCond.append(df2) #append to main df
    print('subject %s, length of df %s' % (subNum, len(dfCond)))
        
    # =============================================================================
    # set up brain data
    # =============================================================================

    dat = dfCond['imPath'].values #img paths - keeping same variables as searchlight
    y   = dfCond['direction'].values #conditions / stimulus
    groups  = dfCond['run'].values # info about the sessions   
    
    for roi in rois:
        #define ROI  mask
        mask_path = os.path.join(roiDir, 'sub-' + subNum + '_' + roi + '_lrh.nii.gz') #ipsRois no stim decoding; visRois_ipsRois bad for all except self demean and std norm...!?
    
        #maybe plot the roi on the brain? optionally
    #    T1_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz')
           
        #resample mask to match epi
        imgs = nib.load(dat[0]) #load in one im to dawnsample mask to match epi
        maskROI = nib.load(mask_path)
        maskROI = nli.resample_img(maskROI, target_affine=imgs.affine, 
                                    target_shape=imgs.shape[:3], interpolation='nearest')
        fmri_masked = apply_mask(dat,maskROI,smoothing_fwhm=fwhm)  #optional fwhm param
        
        # CHECK normalise mean and std using nilearn - how this does it exactly
        if normMeth == 'niNormalised':
            fmri_masked_cleaned = clean(fmri_masked, sessions=groups, detrend=False, standardize=True)
        elif normMeth == 'demeaned':
            fmri_masked_cleaned=fmri_masked.transpose()-np.nanmean(fmri_masked,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned.transpose()
        elif normMeth == 'demeaned_stdNorm':
            fmri_masked_cleaned=fmri_masked.transpose()-np.nanmean(fmri_masked,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned/np.nanstd(fmri_masked,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned.transpose()
        elif normMeth == 'noNorm':
            fmri_masked_cleaned = fmri_masked                    
        
    #%%
    # =============================================================================
    #     #set up splits and run cv
    # ============================================================================
    
        #set up the conditions you want to classify. if 12-way, leave as is without condInd        
        if decodeFeature == "dir":
            conds2Comp = [[0,180], [30,210], [60,240], [90,270],[120,300],[150,330]]
        elif decodeFeature == "ori":
            conds2Comp = [[0,90], [0,270], [30,120], [30,300], [60,150], [60,300], [90,180], [120,210],[150,240],[180,270],[210,300],[240,330]]
        elif decodeFeature == "12-way-all":
            allDirs = np.arange(0,330,30)
            conds2Comp = [[0,np.setxor1d(0,allDirs)],  [30,np.setxor1d(0,allDirs)], [60,np.setxor1d(0,allDirs)], [90,np.setxor1d(0,allDirs)],
                          [120,np.setxor1d(0,allDirs)],[150,np.setxor1d(0,allDirs)],[180,np.setxor1d(0,allDirs)],[210,np.setxor1d(0,allDirs)],
                          [240,np.setxor1d(0,allDirs)],[270,np.setxor1d(0,allDirs)],[300,np.setxor1d(0,allDirs)],[330,np.setxor1d(0,allDirs)]]
        
        #run cv
        if decodeFeature == "12-way": # no need conds2comp, just compare all
            iPair=0
            cv   = LeaveOneGroupOut()
            cv.get_n_splits(fmri_masked_cleaned, y, groups)
            cv   = cv.split(fmri_masked_cleaned,y,groups)   
            clf  = LinearSVC(C=.1)
            cvAccTmp = cross_val_score(clf,fmri_masked_cleaned,y=y,scoring='accuracy',cv=cv).mean() # mean over crossval folds
            print('ROI: %s, Sub-%s cvAcc = %0.3f' % (roi, subNum, (cvAccTmp*100)))
            print('ROI: %s, Sub-%s cvAcc-chance = %0.3f' % (roi, subNum, (cvAccTmp-(1/12))*100))
        else: #all condition-wise comparisons
            cvAccTmp = np.empty(len(conds2Comp))
            for iPair in range(0,len(conds2Comp)):
                ytmp=y.copy()
                if not decodeFeature == "12-way-all": 
                    condInd=np.append(np.where(y==conds2Comp[iPair][0]), np.where(y==conds2Comp[iPair][1]))   
                else:
                    condInd=np.where(y==conds2Comp[iPair][0])
                    for iVal in conds2Comp[iPair][1]:
                        condInd=np.append(condInd, np.where(y==iVal))
                    ytmp[y!=conds2Comp[iPair][0]] = 1 #change the 'other' conditions to 1, comparing to the main value
            
                fmri_masked_cleaned_indexed= fmri_masked_cleaned[condInd,]
                y_indexed = ytmp[condInd]
                groups_indexed = groups[condInd]
        
                cv    = LeaveOneGroupOut()
                cv.get_n_splits(fmri_masked_cleaned_indexed, y_indexed, groups_indexed)
                cv    = cv.split(fmri_masked_cleaned_indexed,y_indexed,groups_indexed)    
                if distMeth == 'svm':
                    clf   = LinearSVC(C=.1)
                    cvAccTmp[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                    print('ROI: %s, Sub-%s cvAcc = %0.3f' % (roi, subNum, (cvAccTmp[iPair]*100)))
                    print('ROI: %s, Sub-%s cvAcc-chance = %0.3f' % (roi, subNum, (cvAccTmp[iPair]-(1/len(np.unique(y_indexed))))*100))
                elif distMeth == 'crossEuclid':
                    cvAccTmp[iPair] = crossEuclid(fmri_masked_cleaned_indexed,y_indexed,cv).mean() # mean over crossval folds
        
        if not decodeFeature == "12-way-all": 
            cvAcc = cvAccTmp.mean() #mean over pairs
        else:
            cvAcc = cvAccTmp
            
        dfDecode[roi].iloc[iSub-1]=cvAcc #store to main df
                
#compute t-test, append to df
if distMeth == 'svm':
    chance = 1/len(np.unique(y_indexed))
else: 
    chance = 0 #for crossvalidated distances

if not decodeFeature == "12-way-all": #stores several values in each cell, so can't do t-test here
    for roi in rois:
        dfDecode[roi].iloc[-1]=stats.ttest_1samp(dfDecode[roi].iloc[0:nSubs-1],chance) #compute t-test, append to df

# if re-running / adding, load in first, append new dat to df, then save
if reRun == True:
    dfTmp=pd.read_pickle(os.path.join(mainDir, 'mvpa_roi', 'roi_' + decodeFeature + 'Decoding_' +
                                      distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                      '_fwhm' + str(fwhm) + '_' + imDat + '.pkl'))
    for roi in rois:
        dfTmp[roi]=dfDecode[roi]
    dfDecode=dfTmp

#save df
dfDecode.to_pickle(os.path.join(mainDir, 'mvpa_roi', 'roi_' + decodeFeature + 'Decoding_' +
                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl'))