#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 15:32:19 2019

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
os.chdir(featDir)

#set to true if rerunning only a few rois, appending it to old df
reRun = False 

imDat   = 'tstat' # tstat or tstat images
normMeth = 'demeaned_stdNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'demeaned_stdNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'block' # 'trials' or 'block' - only block in this script
fwhm = 1 # optional smoothing param - 1, or None

#%%
# =============================================================================
# Set up decoding accuracy dataframe 
# =============================================================================
nSubs=33
rois = ['V1vd','V2vd','V3vd','V3a','V3b','hV4','MST','hMT','IPS0','IPS1','IPS2',
        'IPS3','IPS4','IPS5','SPL1', 'visRois', 'ipsRois', 'visRois_ipsRois'] # MST - leaving out coz only a few voxels? ; 'V01' 'V02' 'PHC1' 'PHC2' 'MST' 'hMT' 'L02' 'L01'

#rois = ['visRois', 'visRois_ipsRois']

dfDecode = pd.DataFrame(columns=rois, index=range(0,nSubs+1))
dfDecode.rename(index={nSubs:'stats'}, inplace=True)

# =============================================================================
# load in trial log and append image paths
# =============================================================================

for iSub in range(3,nSubs+1):
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
        
        # add path to match cue condition and trial number - tstat1:7 is dir0 trial1:7   
        conds=df.direction.unique()
        conds.sort()
        #sort - arrange df so it matches tstat1:84 image structure
        df2=pd.DataFrame() 
        for iCond in conds:
            df2 = df2.append(df[df['direction']==iCond])
        
        tstatNum=1 #counter
        imPath=[]
        for iCond in conds:
            for iTrial in range(1,8): #calculate tstat number
                #make a list and append to it
                imPath.append(os.path.join(featDir, 'sub-' + subNum + '_run-0'
                                           + str(iRun) +'_trial_T1_fwhm0.feat',
                                           'stats',imDat + (str(tstatNum)) + '.nii.gz'))
                tstatNum=tstatNum+1
        df2['imPath']=pd.Series(imPath,index=df2.index)
        dfCond = dfCond.append(df2) #append to main df
    print('subject %s, length of df %s' % (subNum, len(dfCond)))
        
    # =============================================================================
    # set up brain data
    # =============================================================================
    
    
    for roi in rois:
        #define ROI  mask
        mask_path = os.path.join(roiDir, 'sub-' + subNum + '_' + roi + '_lrh.nii.gz') #ipsRois no stim decoding; visRois_ipsRois bad for all except self demean and std norm...!?
    
        #set up block-wise
        if iSub in {9,12,16,26}:
            blocks = np.array((1,2,3,4))
        else:
            blocks = np.array((1,2,3))
        
        cvAcc = np.zeros((blocks[-1]))
        for iRun in runs:
            dfCondRuns=dfCond[dfCond['run']==iRun] #get test set
            
            imPath=[]
            for iBlk in blocks[blocks!=iRun]:       
                tstatNum=1 #counter
                for iCond in conds:
                    tmp=dfCond[dfCond['direction']==iCond] #just get a random row to get the same structure - key is direction and run are right
                    dfRun = tmp.iloc[0]
                    dfRun['run']=iBlk
                    dfRun['imPath'] = os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iBlk) +'_block_T1_fwhm0.feat', 'stats',imDat + (str(tstatNum)) + '.nii.gz')
                    dfCondRuns = dfCondRuns.append(dfRun)
                    tstatNum=tstatNum+1
    
            dat = dfCondRuns['imPath'].values #img paths - keeping same variables as searchlight
            y   = dfCondRuns['direction'].values #conditions / stimulus
            groups  = dfCondRuns['run'].values # info about the sessions   
        
            #resample mask to match epi - moved roi loop up to compute cv means within an roi, moved this here to clean by session
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
            elif normMeth == 'demeaned_stdNorm':
                fmri_masked_cleaned = fmri_masked    
               
            
            #%%
            # =============================================================================
            #     #set up splits and run cv
            # =============================================================================
            cv     = LeaveOneGroupOut()
            cv.get_n_splits(fmri_masked_cleaned, y, groups)
            clf   = LinearSVC(C=.1)
            cvAccTmp = cross_val_score(clf,fmri_masked_cleaned,y=y,scoring='accuracy',cv=cv.split(fmri_masked_cleaned,y,groups))
            
            #get relevant cvAcc measure - is this the right one? (test set?)
            cvAcc[iRun-1] = cvAccTmp[iRun-1] 
            
        dfDecode[roi].iloc[iSub-1]=cvAcc.mean() #store to main df
        print('ROI: %s, Sub-%s cvAcc = %0.3f' % (roi, subNum, (cvAcc.mean()*100)))
        print('ROI: %s, Sub-%s cvAcc-chance = %0.3f' % (roi, subNum, (cvAcc.mean()-(1/12))*100))
        
#compute t-test, append to df
for roi in rois:
    dfDecode[roi].iloc[-1]=stats.ttest_1samp(dfDecode[roi].iloc[0:nSubs-1],1/12) #compute t-test, append to df

# if re-running / adding, load in first, append new dat to df, then save
if reRun == True:
    dfTmp=pd.read_pickle(os.path.join(mainDir, 'mvpa_roi', 'roi_dirDecoding_' +
                                    distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                    '_fwhm' + str(fwhm) + '_' + imDat + '.pkl'))
    for roi in rois:
        dfTmp[roi]=dfDecode[roi]
    dfDecode=dfTmp
    
#save df
#dfDecode.to_pickle(os.path.join(mainDir, 'mvpa_roi', 'roi_dirDecoding_' +
#                                distMeth + '_' + normMeth + '_'  + trainSetMeth + 
#                                '_fwhm' + str(fwhm) + '_' + imDat + '.pkl'))