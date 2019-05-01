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

from memsamp_RM import crossEuclid, getConds2comp, compCovMat

imDat = 'cope' # cope or tstat images
slSiz = 6  #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'blocks' # 'trials' or 'block'
fwhm = None # smoothing - set to None if no smoothing
nCores = 12 #number of cores for searchlight - up to 6 on love06 (i think 8 max)

decodeFeature = 'subjCat' # '12-way' (12-way dir decoding), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# category: 'objCat' (objective catgeory), 'subjCat' 


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
    
    #get objective category
    catAconds=np.array((range(120,271,30))) 
    catBconds=np.append(np.array((range(0,91,30))),[300,330])

    #get subjective category based on responses
    if decodeFeature[0:7] == 'subjCat':
        #flip responses for runs - need double check if keymap is what i think it is. looks ok
        ind1=dfCond['keymap']==1 #if dat['keymap'] == 1: #flip, if 0, no need flip
        ind2=dfCond['key']==6
        ind3=dfCond['key']==1
        dfCond.loc[ind1&ind2,'key']=5
        dfCond.loc[ind1&ind3,'key']=6
        dfCond.loc[ind1&ind2,'key']=1
        #get subjective category
        conds=dfCond.direction.unique()
        conds.sort()
        respPr = pd.Series(index=conds)
        for iCond in conds:
            respPr[iCond] = np.divide((dfCond.loc[dfCond['direction']==iCond,'key']==6).sum(),len(dfCond.loc[dfCond['direction']==iCond])) #this count nans (prob no resp) as incorrect
        subjCatAconds=np.sort(respPr.index[respPr>0.5].values.astype(int))
        subjCatBconds=np.sort(respPr.index[respPr<0.5].values.astype(int))
        #unless:   
        if iSub==5: #move 240 and 270 to catA
            subjCatAconds = np.append(subjCatAconds,[240,270])
            subjCatBconds = subjCatBconds[np.invert((subjCatBconds==240)|(subjCatBconds==270))] #remove
        elif iSub==10: #move 270 to cat B
            subjCatBconds = np.sort(np.append(subjCatBconds,270))
            subjCatAconds = subjCatAconds[np.invert(subjCatAconds==270)]
        elif iSub == 17:#move 30 to cat B
            subjCatBconds = np.sort(np.append(subjCatBconds,30))
            subjCatAconds = subjCatAconds[np.invert(subjCatAconds==30)]
        elif iSub==24: #move 120 to cat A
            subjCatAconds = np.sort(np.append(subjCatAconds,120))
            subjCatBconds = subjCatBconds[np.invert(subjCatBconds==120)]
        elif iSub==27:#move 270 to cat A
            subjCatAconds = np.sort(np.append(subjCatAconds,270))
            subjCatBconds = subjCatBconds[np.invert(subjCatBconds==270)]
        
    #start setting up brain data
    T1_mask_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz')
    T1_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz') 
    
    #set up block-wise
    if iSub in {9,12,16,26}:
        blocks = np.array((1,2,3,4))
    else:
        blocks = np.array((1,2,3))
    
    tmpPathBlk = []
    for iRun in runs:
        if not distMeth in {'crossEuclid','crossNobis'}:
            dfCondRuns=dfCond[dfCond['run']==iRun] #get test set                
            imPath=[]
            for iBlk in blocks[blocks!=iRun]:       
                copeNum=1 #counter
                for iCond in conds:
                    tmp=dfCond[dfCond['direction']==iCond] #just get a random row to get the same structure - key is direction and run are right
                    dfRun = tmp.iloc[0].copy()
                    dfRun.loc['run']=iBlk
                    dfRun.loc['imPath'] = os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iBlk) +'_block_T1_fwhm0.feat', 'stats',imDat + (str(copeNum)) + '.nii.gz')
                    dfCondRuns = dfCondRuns.append(dfRun)
                    copeNum=copeNum+1
        else:
            dfCondRuns=pd.DataFrame(columns=dfCond.columns.values) #empty - just use blocks
            imPath=[]
            for iBlk in blocks:       
                copeNum=1 #counter
                for iCond in conds:
                    tmp=dfCond[dfCond['direction']==iCond] #just get a random row to get the same structure - key is direction and run are right
                    dfRun = tmp.iloc[0].copy()
                    dfRun.loc['run']=iBlk
                    dfRun.loc['imPath'] = os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iBlk) +'_block_T1_fwhm0.feat', 'stats',imDat + (str(copeNum)) + '.nii.gz')
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
    
    
        if distMeth == 'crossNobis': #get variance to compute covar matrix below
            varIm = np.empty([0,np.size(dat.dat,axis=1)]) #only works since i know nVox
            varImSiz = np.empty((len(runs)),dtype='int')
            imgs = nib.load(dfCond['imPath'].iloc[0])
            T1_mask_resampled =  nli.resample_img(T1_mask_path, target_affine=imgs.affine, 
                                                  target_shape=imgs.shape[:3], interpolation='nearest')
            for iRun1 in range(0,len(runs)): #append to list, since var sometimes has more/less timepoints in each run
                varImTmp = apply_mask(os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun1+1) +'_block_T1_fwhm0.feat', 'stats', 'res4d.nii.gz'),T1_mask_resampled,smoothing_fwhm=fwhm)
                varIm    = np.append(varIm,varImTmp,axis=0)
                varImSiz[iRun1] = len(varImTmp) #to index which volumes to compute matrix in crossnobis function
       
        #set up the conditions you want to classify. if 12-way, no need
        if decodeFeature[0:6] == "objCat":
            conds2comp = [catAconds, catBconds]   #put in conditions to compare, e.g. conditions=[catAconds, catBconds]      
        elif decodeFeature[0:7] == "subjCat": #subjective catgory bound based on responses
            conds2comp = [subjCatAconds, subjCatBconds]    
        else: #stimulus decoding
            conds2comp = getConds2comp(decodeFeature)
            
        if (decodeFeature=="subjCat-resp")|(decodeFeature=="motor"):
            conds2comp = np.empty((1)) #len of 1 placeholder
        
        if (decodeFeature=="subjCatRaw-orth")|(decodeFeature=="objCatRaw-orth"):
            catA90 = conds2comp[0]+90
            catB90 = conds2comp[1]+90
            catA90[catA90>359]=catA90[catA90>359]-360
            catB90[catB90>359]=catB90[catB90>359]-360
            conds2comp = [catA90, catB90] 
        
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
                if (decodeFeature=="subjCat-resp")|(decodeFeature=="motor"):
                    condInd = np.append(np.where(dfCondRuns['key']==1),np.where(dfCondRuns['key']==6))
                    ytmp[np.where(dfCondRuns['key']==1)]=0 #change stim directions to category responses (changed to cat resp from above if decodeFeature[0:7]=="subjCat")
                    ytmp[np.where(dfCondRuns['key']==6)]=1                      
                else:
                    condInd=np.append(np.where(yPerm==conds2comp[iPair][0]), np.where(yPerm==conds2comp[iPair][1]))   

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
                    if not ((decodeFeature=='subjCatRaw')|(decodeFeature=='subjCatRaw-orth')|(decodeFeature=='objCatRaw')|(decodeFeature=='objCatRaw-orth')): #if these, no need norm since need subtract from each other later
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
                    
                elif distMeth in {'crossEuclid', 'crossNobis'}:     
                    if distMeth == 'crossNobis': #get variance to compute covar matrix below
                        dat.dat = np.append(dat.dat,varIm,axis=0) #append residual images to compute covar matrix
                        #use len(dat.y) for number of functional images. use varImSiz to index run-wise variance images (nTimepoints)
                        def pipeline(X,y):
                            Xdat_whitened = np.empty((len(y),np.size(X,axis=1)))
                            cov = np.empty((np.size(X,axis=1),np.size(X,axis=1),len(runs)))
                            Xdat = X[range(0,len(y)),:] #get fmri data
    
                            #normalise each trial by its respective run's noise cov mat
                            varTmp = X[len(y):,:] #get residual images
                            if len(runs) == 3:
                                var = [varTmp[0:varImSiz[0],:], varTmp[varImSiz[0]:varImSiz[0]+varImSiz[1],:], 
                                       varTmp[varImSiz[0]+varImSiz[1]:varImSiz[0]+varImSiz[1]+varImSiz[2],:]]
                            else:
                                var = [varTmp[0:varImSiz[0],:], varTmp[varImSiz[0]:varImSiz[0]+varImSiz[1],:], 
                                       varTmp[varImSiz[0]+varImSiz[1]:varImSiz[0]+varImSiz[1]+varImSiz[2],:],
                                       varTmp[varImSiz[0]+varImSiz[1]+varImSiz[2]:varImSiz[0]+varImSiz[1]+varImSiz[2]+varImSiz[3],:]]
                            
                            for iRun1 in range(0,len(runs)):
                                cov[:,:,iRun1] = compCovMat(var[iRun1]) #compute cov mat per run                     
                                ind = dat.sessions == iRun1+1
                                indTrl= np.where(ind)
                                indTrl=indTrl[0]
                                for iTrl in indTrl: #prewhiten each trial to make mahal dist
                                    Xdat_whitened[iTrl,:] = np.dot(Xdat[iTrl,],cov[:,:,iRun1])                  
                            return crossEuclid(Xdat_whitened,y,cv.split(Xdat_whitened,dat.y,dat.sessions),iRun-1)                  
                    elif distMeth == 'crossEuclid': 
                        def pipeline(X,y):
                            return crossEuclid(X,y,cv.split(dat.dat,dat.y,dat.sessions),iRun-1)

                    dat.pipeline = pipeline
                    im = cl.searchlightSphere(dat,slSiz,n_jobs=nCores) #run searchlight
        
                    tmpPath.append(os.path.join(mainDir, 'mvpa_searchlight', 'tmp_sl' + str(slSiz) + decodeFeature +
                                distMeth + normMeth + trainSetMeth + str(fwhm) + imDat + str(iPair) + '.nii.gz'))
                    nib.save(im, tmpPath[iPair])
                    
            #merge images
            if not decodeFeature in {"12-way", "12-way-all"}: #1st no need avg, 2nd is the indv maps that are interesting (already saved)
                im = nli.mean_img(tmpPath) 
                for tmpImg in tmpPath: 
                    os.remove(tmpImg) #remove temp files        
        # save block-wise image
        tmpPathBlk.append(os.path.join(mainDir, 'mvpa_searchlight', 'tmp_sl_block_run-0' + str(iRun) + str(slSiz) + 
                                       decodeFeature + distMeth + normMeth + trainSetMeth + str(fwhm) + imDat + '.nii.gz'))
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