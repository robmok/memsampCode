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
import numpy as np
from nilearn import image as nli # Import image processing tool
import clarte as cl # on love06
import pandas as pd
import nibabel as nib
from sklearn.model_selection import cross_val_score, LeaveOneGroupOut
from sklearn.svm import LinearSVC
from nilearn.masking import apply_mask 

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
#mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

featDir=os.path.join(mainDir,'memsampFeat')
fmriprepDir=os.path.join(mainDir,'fmriprep_output/fmriprep')
roiDir=os.path.join(mainDir,'rois')
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)

from memsamp_RM import crossEuclid, getConds2comp

imDat   = 'cope' # cope or tstat images
slSiz=5  #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'blocks' # 'trials' or 'block'
fwhm = 1 # smoothing - set to None if no smoothing
nCores = 4 #number of cores for searchlight - up to 6 on love06 (i think 8 max)

decodeFeature = '12-way' # '12-way' (12-way dir decoding), 'dir' (opposite dirs), 'ori' (orthogonal angles)
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
    
    tmpPathBlk = []
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
        #make permanent copies, since the dat object needs to be edited to put into the pipeline
        datPerm    = dat.dat.copy()
        yPerm      = dat.y.copy()
        sessPerm   = dat.sessions.copy()
    
        # normalise voxels - demean and norm by var - across conditions; try to do only within sphere? also try demean only or demean + norm variance
        if normMeth == 'niNormalised':
            dat.cleaner(standardizeVox=True)
    
        #set up the conditions you want to classify. if 12-way, doesn't use this
        conds2comp = getConds2comp(decodeFeature)
        
        #run cv
        if decodeFeature == "12-way": # no need conds2comp, just compare all
            cv  = LeaveOneGroupOut()
            cv.get_n_splits(dat.dat, dat.y, dat.sessions) #group param is sessions
            clf = LinearSVC(C=.1)
        
            def pipeline(X,y):
               cvBlock = cross_val_score(clf,X,y=y,scoring='accuracy',cv=cv.split(dat.dat,dat.y,dat.sessions))
               return cvBlock[iRun-1] #get relevant cvAcc measure (test set)

            dat.pipeline = pipeline
            im = cl.searchlightSphere(dat,slSiz,n_jobs=nCores) #run searchlight
    
            # normalise by chance
            chance   = 1/len(np.unique(dat.y))
            imVec    = dat.masker(im)
            imVec    = imVec - chance
            im       = dat.unmasker(imVec)        
        else: #all condition-wise comparisons
            tmpPath = []
            for iPair in range(0,len(conds2comp)):
                ytmp=yPerm.copy() #need to copy this for 12-way-all since will edit ytmp (which will change yPerm if not copy since it's referring to the same object)
                if not decodeFeature == "12-way-all": 
                    condInd=np.append(np.where(yPerm==conds2comp[iPair][0]), np.where(yPerm==conds2comp[iPair][1]))   
                else: # append multiple conditions in a cell of the array
                    condInd=np.where(dat.y==conds2comp[iPair][0])
                    for iVal in conds2comp[iPair][1]:
                        condInd=np.append(condInd, np.where(yPerm==iVal))
                    ytmp[yPerm!=conds2comp[iPair][0]] = 1 #change the 'other' conditions to 1, comparing to the main value
            
                dat.dat = datPerm[condInd,]
                dat.y = ytmp[condInd]
                dat.sessions = sessPerm[condInd]
                cv  = LeaveOneGroupOut()
                cv.get_n_splits(dat.dat, dat.y, dat.sessions) #group param is sessions
                
                if distMeth == 'svm':
                    clf   = LinearSVC(C=.1)
    #                cvAccTmp[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                    def pipeline(X,y):
                        cvBlock = cross_val_score(clf,X,y=y,scoring='accuracy',cv=cv.split(dat.dat,dat.y,dat.sessions))
                        return cvBlock[iRun-1] #get relevant cvAcc measure (test set)
                    dat.pipeline = pipeline
                    im = cl.searchlightSphere(dat,slSiz,n_jobs=nCores) #run searchlight
                    chance   = 1/len(np.unique(dat.y))
                    imVec    = dat.masker(im)
                    imVec    = imVec - chance
                    im       = dat.unmasker(imVec)
                    #save image with 'iPair' appended to it; join it below
                    if not decodeFeature == "12-way-all": 
                        tmpPath.append(os.path.join(mainDir, 'mvpa_searchlight', 'tmp_mvpa_searchlight_' + decodeFeature +
                                                    distMeth + normMeth + trainSetMeth + str(fwhm) + imDat + str(iPair) + '.nii.gz'))
                        nib.save(im, tmpPath[iPair])
                    else: #no need avg - it's the indv maps that are interesting
                        nib.save(im, os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                              'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                              '_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + str(iPair) + '.nii.gz'))
                    del im
                elif distMeth == 'crossEuclid':
                    def pipeline(X,y):
                        cvBlock = crossEuclid(X,y,cv.split(dat.dat,dat.y,dat.sessions))
                        return cvBlock[iRun-1]
                    dat.pipeline = pipeline
                    im = cl.searchlightSphere(dat,slSiz,n_jobs=nCores) #run searchlight
        
                    tmpPath.append(os.path.join(mainDir, 'mvpa_searchlight', 'tmp_mvpa_searchlight_' + decodeFeature +
                                distMeth + normMeth + trainSetMeth + str(fwhm) + imDat + str(iPair) + '.nii.gz'))
                    nib.save(im, tmpPath[iPair])
            #merge images
            if not decodeFeature in {"12-way", "12-way-all"}: #1st no need avg, 2nd is the indv maps that are interesting (already saved)
                im = nli.mean_img(tmpPath) 
                for tmpImg in tmpPath: 
                    os.remove(tmpImg) #remove temp files        
        # save block-wise image
        tmpPathBlk.append(os.path.join(mainDir, 'mvpa_searchlight', 'tmp_mvpa_searchlight_block_run-0' + str(iRun) + '.nii.gz'))
        nib.save(im, tmpPathBlk[iRun-1])
        del im

    #average image over blocks
    im = nli.mean_img(tmpPathBlk)        
    for tmpImgBlk in tmpPathBlk: 
        os.remove(tmpImgBlk) #remove temp files
    
    #save each subject's image
    if not decodeFeature == "12-way-all": 
        nib.save(im, os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                                  'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                  '_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))
    del im