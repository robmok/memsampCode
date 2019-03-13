#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:56:22 2019

@author: robertmok


For this 'blocks' script, don't run multiple searchlight scripts at the same time, since it save block-wise images to a temporary file, which is overwritten for each sub.
One option is to name them with subject number, etc., then delete them at the end of the subject loop
"""
#
import sys
sys.path.append('/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/')
import os
#import glob
import numpy as np
from nilearn import image as nli # Import image processing tool
import clarte as cl # on love06 - normally just clarte is fine
import pandas as pd
#import matplotlib.pyplot as plt
#import nilearn.plotting as nip
import nibabel as nib
from sklearn.model_selection import cross_val_score, LeaveOneGroupOut
from sklearn.svm import LinearSVC
    
mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'
featDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampFeat'
bidsDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampBids'
fmriprepDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/fmriprep_output/fmriprep'
roiDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/rois'
os.chdir(featDir)

imDat   = 'cope' # cope or cope images
slSiz=5 #searchlight size
normMeth = 'noNorm' # 'noNorm', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'blocks' # 'trials' or 'block'
fwhm = 1 # smoothing - set to None if no smoothing
nCores = 4 #number of cores for searchlight - up to 6 on love06 (i think 8 max)
#%% load in trial log and append image paths

for iSub in range(1,34):
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
        
    #start setting up brain data
    T1_mask_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz') #whole brain
    #T1_mask_path = os.path.join(roiDir, 'sub-' + subNum + '_V1vd_lrh.nii.gz') 
    T1_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz') 
    
    #set up block-wise
    if iSub in {9,12,16,26}:
        blocks = np.array((1,2,3,4))
    else:
        blocks = np.array((1,2,3))
    
    tmpPath = []
    for iRun in runs:
        dfCondRuns=dfCond[dfCond['run']==iRun] #get test set
        
        imPath=[]
        for iBlk in blocks[blocks!=iRun]:       
            copeNum=1 #counter
            for iCond in conds:
                tmp=dfCond[dfCond['direction']==iCond] #just get a random row to get the same structure - key is direction and run are right
                dfRun = tmp.iloc[0]
                dfRun['run']=iBlk
                dfRun['imPath'] = os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iBlk) +'_block_T1_fwhm0.feat', 'stats',imDat + (str(copeNum)) + '.nii.gz')
                dfCondRuns = dfCondRuns.append(dfRun)
                copeNum=copeNum+1
    
        dat = cl.fmri_data(dfCondRuns['imPath'].values,T1_mask_path, fwhm=fwhm)  #optional smoothing param: fwhm=1 
        dat.sessions = dfCondRuns['run'].values # info about the sessions
        dat.y  = dfCondRuns['direction'].values # conditions / stimulus
    
        # normalise voxels - demean and norm by var - across conditions; try to do only within sphere? also try demean only or demean + norm variance
        if normMeth == 'noNorm':
            dat.cleaner(standardizeVox=True)
    
        #set up cv
        cv     = LeaveOneGroupOut()
        cv.get_n_splits(dat.dat, dat.y, dat.sessions) #group param is sessions
        clf = LinearSVC(C=.1)
        
        # the pipeline function - function defining the computation performed in each sphere
        # - add demean / normalize variance within sphere?
        def pipeline(X,y):
            cvAcc =  cross_val_score(clf,X,y=y,scoring='accuracy',cv=cv.split(dat.dat,dat.y,dat.sessions)) #no mean here
            return cvAcc[iRun-1] #return only the relevant test block

        dat.pipeline = pipeline
    
    #%% run  searchlight with sphere radius=5mm using 1 core:
        im = cl.searchlightSphere(dat,slSiz,n_jobs=nCores) #n_jobs - cores
        # save block-wise image
        tmpPath.append(os.path.join(mainDir, 'mvpa_searchlight', 'tmp_mvpa_searchlight_block_run-0' + str(iRun) + '.nii.gz'))
        nib.save(im, tmpPath[iRun-1])
        del im
            
    #average image over blocks
    im = nli.mean_img(tmpPath)        
        
    #save each subject's image then load up later
    nib.save(im, os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_dirDecoding_' + 
                                  distMeth + '_' + normMeth + '_'  + trainSetMeth + '_fwhm' + 
                                  str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))

    del im
   
