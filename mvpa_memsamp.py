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
#np.set_printoptions(precision=2, suppress=True) # Set numpy to print only 2 decimal digits for neatness
from nilearn import image as nli # Import image processing tool
import clarte as cl # on love06 - normally just clarte is fine
import pandas as pd
import matplotlib.pyplot as plt
import nilearn.plotting as nip
import nibabel as nib

#mvpa, searchlight
from sklearn.model_selection import cross_val_score, LeaveOneGroupOut
from sklearn.svm import LinearSVC
    
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep'
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'
os.chdir(featDir)

#%%

# =============================================================================
# # load in trial log and append image paths
# =============================================================================

# - first try the LOO one with 'trials'. then load in blocks
    # - load in sub-01_task-memsamp_run-01_events.tsv #in bidsdi
    # - append run number
    # - append path to image - match 0:30:270 degrees to condition 1:12, trialwise (N.B. cope number is not the same for trialwise! 7 trials)
    # - load in all 3 runs then merge the 3 dfs

for iSub in range(1,2):
    subNum=f'{iSub:02d}'
    dfCond=pd.DataFrame() #main df with all runs
    if iSub in {9,12,16,26}:
        runs = range(1,5) #4 runs
    else:
        runs = range(1,4) #3 runs
    
    for iRun in runs:
        condPath=os.path.join(bidsDir, 'sub-' + subNum, 'func','sub-' + subNum + 
                              '_task-memsamp_run-0' + str(iRun) +'_events.tsv')
        
        # df to load in and organise run-wise data
        df = pd.read_csv(condPath, sep='\t')
        df = df[df['trial_type']=='cue'] #remove feedback trials
        df['run'] = pd.Series(np.ones((len(df)))*iRun,index=df.index) #add run number
        #df.loc[:,'run2']=pd.Series(np.ones((len(df)))*iRun,index=df.index) #alt way - better/worse?
        
        # add path to match cue condition and trial number - cope1:7 is dir0 trial1:7   
        conds=df.direction.unique()
        conds.sort()
        copeNum=1 #counter
        imPath=[]
        for iCond in conds:
            for iTrial in range(1,8): #calculate cope number
                #make a list and append to it
                imPath.append(os.path.join(featDir, 'sub-' + subNum + '_run-0'
                                           + str(iRun) +'_trial_T1_fwhm0.feat',
                                           'stats','cope' + (str(copeNum)) + '.nii.gz'))
                copeNum=copeNum+1
        df['imPath']=pd.Series(imPath,index=df.index)
        dfCond = dfCond.append(df) #append to main df
    print('subject %s, length of df %s' % (subNum, len(dfCond)))
    

# =============================================================================
#     #set up brain data
# =============================================================================

    dat = dfCond['imPath'].values #img paths - keeping same variables as searchlight
    y   = dfCond['direction'].values #conditions / stimulus
    groups  = dfCond['run'].values # info about the sessions   
    
    #define ROI 
    mask_path = os.path.join(roiDir, 'sub-' + subNum + '_visRois_lrh.nii.gz')

    #maybe plot the roi on the brain? optionally
#    T1_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz')




    #turns out epi diff affine to mask. **DOUBLE CHECK** if this is because mask is like T1 in dimensions
    
    
    

    
    from nilearn.masking import apply_mask    
    #resample mask to match epi
    imgs = nib.load(dat[0]) #load in one im to dawnsample mask to match epi
    maskROI = nib.load(mask_path)
    maskROI = nli.resample_img(maskROI, target_affine=imgs.affine, 
                                target_shape=imgs.shape[:3], interpolation='nearest')
    fmri_masked = apply_mask(dat,maskROI,smoothing_fwhm=1)  #optional fwhm=1, or None

    #normalise myself
#    fmri_masked-fmri_masked.mean(axis=1)
    
    

    
    
    
    # normalise mean and std using nilearn
    from nilearn.signal import clean
    fmri_masked_cleaned = clean(fmri_masked, sessions=groups, detrend=False, standardize=True)
# =============================================================================
#     #set up splits and run cv
# =============================================================================
    cv     = LeaveOneGroupOut()
    cv.get_n_splits(fmri_masked_cleaned, y, groups)
    clf   = LinearSVC(C=.1)
    cvAcc = cross_val_score(clf,fmri_masked_cleaned,y=y,scoring='accuracy',cv=cv.split(fmri_masked_cleaned,y,groups)).mean() 
    print('cvAcc = %0.3f' % (cvAcc*100))
    print('cvAcc-chance = %0.3f' % ((cvAcc-(1/12))*100))
    
    #why problem with convergence still? nVoxels? but even less with searchlight




