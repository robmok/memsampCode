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
import numpy as np
from nilearn import image as nli # Import image processing tool
import clarte as cl
import pandas as pd
import nibabel as nib
from sklearn.model_selection import cross_val_score, LeaveOneGroupOut
from sklearn.svm import LinearSVC
from nilearn.masking import apply_mask 

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

featDir=os.path.join(mainDir,'memsampFeat')
fmriprepDir=os.path.join(mainDir,'fmriprep_output/fmriprep')
roiDir=os.path.join(mainDir,'rois')
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)

from memsamp_RM import crossEuclid, getConds2comp, compCovMat

imDat   = 'cope' # cope or tstat images
slSiz=8 #searchlight size
normMeth = 'noNorm' # 'niNormalised', 'noNorm', 'slNorm', 'sldemeaned' # slNorm = searchlight norm by mean and var
distMeth = 'svm' # 'svm', 'euclid', 'mahal', 'xEuclid', 'xNobis'
trainSetMeth = 'trials' # 'trials' or 'block'
fwhm = None # smoothing - set to None if no smoothing
nCores = 10 #number of cores for searchlight - up to 6 on love06 (i think 8 max)

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
#    T1_mask_path = os.path.join(roiDir, 'sub-' + subNum + '_visRois_lrh.nii.gz') #visRois
    T1_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz')

    dat = cl.fmri_data(dfCond['imPath'].values,T1_mask_path, fwhm=fwhm)  #optional smoothing param: fwhm=1
    dat.sessions = dfCond['run'].values # info about the sessions
    dat.y  = dfCond['direction'].values # conditions / stimulus
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
        for iRun in runs: #append to list, since var sometimes has more/less timepoints in each run
            varImTmp = apply_mask(os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun) +'_trial_T1_fwhm0.feat', 'stats', 'res4d.nii.gz'),T1_mask_resampled)
#            varImTmp = apply_mask(os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun) +'_trial_T1_fwhm0.feat', 'stats', 'res4d.nii.gz'),T1_mask_resampled,smoothing_fwhm=fwhm)
            varIm    = np.append(varIm,varImTmp,axis=0)
            varImSiz[iRun-1] = len(varImTmp) #to index which volumes to compute matrix in crossnobis function
        dat.dat = np.append(dat.dat,varIm,axis=0)
    #set up the conditions you want to classify. if 12-way, doesn't use this
    conds2comp = getConds2comp(decodeFeature)

    #run cv
    if decodeFeature == "12-way": # no need conds2comp, just compare all
        cv  = LeaveOneGroupOut()
        cv.get_n_splits(dat.dat, dat.y, dat.sessions) #group param is sessions
        clf = LinearSVC(C=.1)
#        cv.split(dat.dat,dat.y,dat.sessions)
#        cv = cv.split(dat.dat,dat.y,dat.sessions)
        
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
#            cv = cv.split(dat.dat,dat.y,dat.sessions)
            
            if distMeth == 'svm':
                clf   = LinearSVC(C=.1)
#                cvAccTmp[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                def pipeline(X,y):
                    return cross_val_score(clf,X,y=y,scoring='accuracy',cv=cv.split(dat.dat,dat.y,dat.sessions)).mean()
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
            elif distMeth in {'crossEuclid', 'crossNobis'}:                
                if distMeth == 'crossNobis': #get variance to compute covar matrix below
                    dat.dat = np.append(dat.dat,varIm,axis=0) #append residual images to compute covar matrix
                    #use len(dat.y) for number of functional images. use varImSiz to index run-wise variance images (nTimepoints)
                    def pipeline(X,y):
                        Xdat_whitened = np.empty((len(y),np.size(X,axis=1)))
                        cov = np.empty((np.size(X,axis=1),np.size(X,axis=1),len(runs)))
                        Xdat = X[range(0,len(y)),:] #get fmri data

                        #normalise each trial by its respective run's noise cov mat
#                        varTmp = X[len(y):,:] #get residual images
#                        if len(runs) == 3:
#                            var = [varTmp[0:varImSiz[0],:], varTmp[varImSiz[0]:varImSiz[0]+varImSiz[1],:], 
#                                   varTmp[varImSiz[0]+varImSiz[1]:varImSiz[0]+varImSiz[1]+varImSiz[2],:]]
#                        else:
#                            var = [varTmp[0:varImSiz[0],:], varTmp[varImSiz[0]:varImSiz[0]+varImSiz[1],:], 
#                                   varTmp[varImSiz[0]+varImSiz[1]:varImSiz[0]+varImSiz[1]+varImSiz[2],:],
#                                   varTmp[varImSiz[0]+varImSiz[1]+varImSiz[2]:varImSiz[0]+varImSiz[1]+varImSiz[2]+varImSiz[3],:]]
                        
#                        for iRun in range(0,len(runs)):
#                            cov[:,:,iRun] = compCovMat(var[iRun]) #compute cov mat per run                     
#                            ind = dat.sessions == iRun+1
#                            indTrl= np.where(ind)
#                            indTrl=indTrl[0]
#                            for iTrl in indTrl: #prewhiten each trial to make mahal dist
#                                Xdat_whitened[iTrl,:] = np.dot(Xdat[iTrl,],cov[:,:,iRun])
#                        
                        
                        
                        #compute cov mat over all runs
                        var = X[len(y):,:] 
                        cov = compCovMat(var)
                        
                        for iRun in range(0,len(runs)):
                            ind = dat.sessions == iRun+1
                            indTrl= np.where(ind)
                            indTrl=indTrl[0]
                            for iTrl in indTrl: #prewhiten each trial to make mahal dist
                                Xdat_whitened[iTrl,:] = np.dot(Xdat[iTrl,],cov)
                        
                        
                        return crossEuclid(Xdat_whitened,y,cv = cv.split(Xdat_whitened,dat.y,dat.sessions)).mean()                        

                elif distMeth == 'crossEuclid':
                    def pipeline(X,y):
                        return crossEuclid(X,y,cv.split(dat.dat,dat.y,dat.sessions)).mean()

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
#    import nilearn.plotting as nip
#    nip.plot_stat_map(im,colorbar=True, threshold=0.00005,bg_img=T1_path,
#                                      title='Accuracy > Chance (+arbitrary threshold)')
#
#    #interactive -  open the plot in a web browser:
#    view = nip.view_img(im,colorbar=True, threshold=0.00005,bg_img=T1_path)
#    view.open_in_browser()