#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:36:19 2019

@author: robert.mok
"""

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
codeDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/memsampCode'
os.chdir(codeDir)

from memsamp_RM import crossEuclid

imDat   = 'cope' # cope or cope images
slSiz=5 #searchlight size
normMeth = 'niNormalised' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'crossEuclid' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'trials' # 'trials' or 'block'
fwhm = 1 # smoothing - set to None if no smoothing
nCores = 3 #number of cores for searchlight - up to 6 on love06 (i think 8 max)

decodeFeature = 'dir' # '12-way' (12-way dir decoding), 'dir' (opposite dirs), 'ori' (orthogonal angles)

#%% load in trial log and append image paths

# - first try the LOO one with 'trials'. then load in blocks
    # - load in sub-01_task-memsamp_run-01_events.tsv #in bidsdi
    # - append run number
    # - append path to image - match 0:30:270 degrees to condition 1:12, trialwise (N.B. cope number is not the same for trialwise! 7 trials)
    # - load in all 3 runs then merge the 3 dfs

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
#    T1_mask_path = os.path.join(roiDir, 'sub-' + subNum + '_visRois_lrh.nii.gz') #visRois
    T1_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz')

    dat = cl.fmri_data(dfCond['imPath'].values,T1_mask_path, fwhm=fwhm)  #optional smoothing param: fwhm=1
    dat.sessions = dfCond['run'].values # info about the sessions
    dat.y  = dfCond['direction'].values # conditions / stimulus
    y      = dfCond['direction'].values #does not change
    
    # normalise voxels - demean and norm by var - across conditions; try to do only within sphere? also try demean only or demean + norm variance
    if normMeth == 'niNormalised':
        dat.cleaner(standardizeVox=True)
    
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
        cv  = LeaveOneGroupOut()
        cv.get_n_splits(dat.dat, dat.y, dat.sessions) #group param is sessions
        clf = LinearSVC(C=.1)
    
        # the pipeline function - function defining the computation performed in each sphere
        # - add demean / normalize variance within sphere?
        def pipeline(X,y):
            return cross_val_score(clf,X,y=y,scoring='accuracy',cv=cv.split(dat.dat,dat.y,dat.sessions)).mean()
            #to normalize here instead: get shape of X, X[2]=X_flatten, normalise then get back the shape
            # also check out - stats package of scipy zscore - might just be one function. THEN cross_val_score
            #if normMeth in {'slNorm','slDemeaned'}:        
        
        dat.pipeline = pipeline
        im = cl.searchlightSphere(dat,slSiz,n_jobs=nCores) #run searchlight

        # normalise by chance
        chance   = 1/np.unique(y)
        imVec    = dat.masker(im)
        imVec    = imVec - chance
        im       = dat.unmasker(imVec)        
    else: #all condition-wise comparisons
#        cvAccTmp = np.empty(len(conds2Comp))
        tmpPath = []
        for iPair in range(0,len(conds2Comp)):
            ytmp=y.copy()
            if not decodeFeature == "12-way-all": 
                condInd=np.append(np.where(y==conds2Comp[iPair][0]), np.where(y==conds2Comp[iPair][1]))   
            else: # append multiple conditions in a cell of the array
                condInd=np.where(dat.y==conds2Comp[iPair][0])
                for iVal in conds2Comp[iPair][1]:
                    condInd=np.append(condInd, np.where(y==iVal))
                ytmp[y!=conds2Comp[iPair][0]] = 1 #change the 'other' conditions to 1, comparing to the main value
        
            dat.dat = dat.dat[condInd,]
            dat.y = ytmp[condInd]
            dat.sessions = dat.sessions[condInd]
            cv  = LeaveOneGroupOut()
            cv.get_n_splits(dat.dat, dat.y, dat.sessions) #group param is sessions
            
            if distMeth == 'svm':
                clf   = LinearSVC(C=.1)
#                cvAccTmp[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                def pipeline(X,y):
                    return cross_val_score(clf,X,y=y,scoring='accuracy',cv=cv.split(dat.dat,dat.y,dat.sessions)).mean()
                dat.pipeline = pipeline
                im = cl.searchlightSphere(dat,slSiz,n_jobs=nCores) #run searchlight
                chance   = 1/np.unique(y)
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
                    return crossEuclid(dat.dat,dat.y,cv.split(dat.dat,dat.y,dat.sessions)).mean()
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

    #save each subject's image
    if not decodeFeature == "12-way-all": 
        nib.save(im, os.path.join(mainDir, 'mvpa_searchlight', 'sl'+ str(slSiz) + '_' + decodeFeature + 
                                  'Decoding_' + distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                  '_fwhm' + str(fwhm) + '_' + imDat + '_sub-' + subNum + '.nii.gz'))
    del im
    

#plot
#    nip.plot_stat_map(imThresh,colorbar=True, threshold=0.05,bg_img=T1_path,
#                                      title='Accuracy > Chance (+arbitrary threshold)')
#
#    #interactive -  open the plot in a web browser:
#    view = nip.view_img(imThresh,colorbar=True, threshold=0.05,bg_img=T1_path,
#                                      title='Accuracy > Chance (+arbitrary threshold)')
#    view.open_in_browser()
