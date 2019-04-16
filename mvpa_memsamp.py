#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:48:06 2019

@author: robert.mok
"""
import sys
import os
import numpy as np
from nilearn import image as nli # Import image processing tool
import pandas as pd
import nibabel as nib
from nilearn.masking import apply_mask 
from nilearn.signal import clean 
from sklearn.model_selection import cross_val_score, LeaveOneGroupOut
from sklearn.svm import LinearSVC
import scipy.stats as stats

mainDir='/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI' #love06
#mainDir='/home/robmok/Documents/memsamp_fMRI' #love01

sys.path.append(mainDir)

featDir=os.path.join(mainDir,'memsampFeat')
roiDir=os.path.join(mainDir,'rois')
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)

from memsamp_RM import crossEuclid, compCovMat, getConds2comp

#set to true if rerunning only a few rois, appending it to old df
reRun = False 

imDat = 'cope' # cope or tstat images
normMeth = 'noNorm' # 'niNormalised', 'demeaned', 'demeaned_stdNorm', 'noNorm' # demeaned_stdNorm - dividing by std does work atm
distMeth = 'svm' # 'svm', 'crossEuclid', 'crossNobis'
trainSetMeth = 'trials' # 'trials' or 'block' - only tirals in this script
fwhm = None # optional smoothing param - 1, or None

# stimulus decoding: '12-way' (12-way dir decoding - only svm), '12-way-all' (output single decoder for each dir vs all), 'dir' (opposite dirs), 'ori' (orthogonal angles)
# category: 'objCat' (objective catgeory), 'subjCat' 
decodeFeature = 'subjCat' 

#%%
# =============================================================================
# Set up decoding accuracy dataframe 
# =============================================================================
nSubs=33
#rois = ['V1vd','V2vd','V3vd','V3a','V3b','hV4','MST','hMT','IPS0','IPS1','IPS2',
#        'IPS3','IPS4','IPS5', 'visRois', 'ipsRois', 'visRois_ipsRois',
#        'MDroi_ips','MDroi_ifg','MDroi_area8c','MDroi_area9', 'dlPFC',
#        'HIPP_HEAD','HIPP_BODY_TAIL','HIPP_HEAD_BODY_TAIL'] #dlPFC is a merge of area 8c and 9. # MDroi_pcg - premotor... useful for motor later?
                                                            #hpc - anterior, posterior, whole

rois = ['V1vd_lh','V1vd_rh', 'V2vd_lh','V2vd_rh','V3vd_lh','V3vd_rh','V3a_lh','V3a_rh',
        'V3b_lh','V3b_rh', 'hMT_lh','hMT_rh', 'IPS0_lh','IPS0_rh','IPS1-5_lh','IPS1-5_rh', 
        'MDroi_ips_lh','MDroi_ips_rh','MDroi_ifg_lh','MDroi_ifg_rh', 'MDroi_area8c_lh',
        'MDroi_area8c_rh', 'MDroi_area9_lh','MDroi_area9_rh', 'dlPFC_lh','dlPFC_rh',
        'HIPP_HEAD_lh','HIPP_HEAD_rh','HIPP_BODY_TAIL_lh','HIPP_BODY_TAIL_rh',
        'HIPP_HEAD_BODY_TAIL_lh','HIPP_HEAD_BODY_TAIL_rh']

dfDecode = pd.DataFrame(columns=rois, index=range(0,nSubs+1))
dfDecode.rename(index={nSubs:'stats'}, inplace=True)
if decodeFeature == "subjCat-all":
    dfDecode['subjCat'] = ""

# =============================================================================
# load in trial log and append image paths
# =============================================================================

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
    
    # =============================================================================
    # set up brain data
    # =============================================================================

    dat = dfCond['imPath'].values #img paths - keeping same variables as searchlight
    y   = dfCond['direction'].values #conditions / stimulus
    groups  = dfCond['run'].values # info about the sessions   
    
    for roi in rois:
        #define ROI  mask
#        mask_path = os.path.join(roiDir, 'sub-' + subNum + '_' + roi + '_lrh.nii.gz') 
        mask_path = os.path.join(roiDir, 'sub-' + subNum + '_' + roi + '.nii.gz') #separate L and R
        
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

        if distMeth == 'crossNobis': #get variance to compute covar matrix below
            # compute each run's covariance matrix here, then apply it to fmri_masked_cleaned, then euclid below
            covMat = np.empty((np.size(fmri_masked_cleaned,axis=1),np.size(fmri_masked_cleaned,axis=1),len(runs))) #nVox x nVox
            for iRun1 in runs: #append to list, since var sometimes has more/less timepoints in each run
                varPath = os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun1) +'_trial_T1_fwhm0.feat', 'stats', 'res4d.nii.gz')
#                covMat[:,:,iRun1-1] = compCovMat(apply_mask(varPath,maskROI))
                covMat[:,:,iRun1-1] = compCovMat(apply_mask(varPath,maskROI,smoothing_fwhm=fwhm))
            for iRun1 in runs:
                trlInd = np.where(groups==iRun1)
                trlInd = trlInd[0]
                for iTrl in trlInd:
                    fmri_masked_cleaned[iTrl,] = np.dot(fmri_masked_cleaned[iTrl,],covMat[:,:,iRun1-1])
            
    # =============================================================================
    #     #set up splits and run cv
    # ============================================================================
    
        #set up the conditions you want to classify. if 12-way, no need
        if decodeFeature == "objCat":
            conds2comp = [catAconds, catBconds]   #put in conditions to compare, e.g. conditions=[catAconds, catBconds]      
        elif decodeFeature == "subjCat": #subjective catgory bound based on responses
            conds2comp = [subjCatAconds, subjCatBconds]  
        elif decodeFeature == "subjCat-all":
            condsTmp=list(subjCatAconds)+list(subjCatBconds)
            conds2comp = getConds2comp(decodeFeature,condsTmp)
        else: #stimulus decoding
            conds2comp = getConds2comp(decodeFeature)
        
        #run cv
        if decodeFeature == "12-way": # no need conds2comp, just compare all
            iPair=0
            cv   = LeaveOneGroupOut()
            cv.get_n_splits(fmri_masked_cleaned, y, groups)
            cv   = cv.split(fmri_masked_cleaned,y,groups)   
            clf  = LinearSVC(C=.1)
            cvAccTmp = cross_val_score(clf,fmri_masked_cleaned,y=y,scoring='accuracy',cv=cv).mean() # mean over crossval folds
            print('ROI: %s, Sub-%s cvAcc = %0.3f' % (roi, subNum, (cvAccTmp*100)))
            print('ROI: %s, Sub-%s cvAcc-chance = %0.3f' % (roi, subNum, (cvAccTmp-(1/len(np.unique(y))))*100))
            y_indexed = y #for computing chance
        else: #all condition-wise comparisons
            cvAccTmp = np.empty(len(conds2comp))
            for iPair in range(0,len(conds2comp)):
                ytmp=y.copy()
                if not decodeFeature == "12-way-all": 
                    condInd=np.append(np.where(y==conds2comp[iPair][0]), np.where(y==conds2comp[iPair][1]))   
                else:
                    condInd=np.where(y==conds2comp[iPair][0])
                    for iVal in conds2comp[iPair][1]:
                        condInd=np.append(condInd, np.where(y==iVal))
                    ytmp[y!=conds2comp[iPair][0]] = 1 #change the 'other' conditions to 1, comparing to the main value
            
                fmri_masked_cleaned_indexed= fmri_masked_cleaned[condInd,]
                y_indexed = ytmp[condInd]
                groups_indexed = groups[condInd]
        
                cv    = LeaveOneGroupOut()
                cv.get_n_splits(fmri_masked_cleaned_indexed, y_indexed, groups_indexed)
                cv    = cv.split(fmri_masked_cleaned_indexed,y_indexed,groups_indexed)    
                if distMeth == 'svm':
                    clf   = LinearSVC(C=.1)
                    cvAccTmp[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
#                    print('ROI: %s, Sub-%s cvAcc-chance = %0.3f' % (roi, subNum, (cvAccTmp[iPair]-(1/len(np.unique(y_indexed))))*100))
                elif distMeth in {'crossEuclid','crossNobis'}:
                    cvAccTmp[iPair] = crossEuclid(fmri_masked_cleaned_indexed,y_indexed,cv).mean() # mean over crossval folds
        
        if not (decodeFeature=="12-way-all")|(decodeFeature=="subjCat-all"): 
            cvAcc = cvAccTmp.mean() #mean over pairs
            print('ROI: %s, Sub-%s %s measure = %0.3f' % (roi, subNum, distMeth, cvAcc))    

        else:
            cvAcc = cvAccTmp #save all pairs
        dfDecode[roi].iloc[iSub-1]=cvAcc #store to main df
            
    if decodeFeature=="subjCat-all": #add subjCat info to df
        dfDecode['subjCat'][iSub-1] = [list(subjCatAconds), list(subjCatBconds)]
#compute t-test, append to df
if distMeth == 'svm':
    chance = 1/len(np.unique(y_indexed))
else: 
    chance = 0 #for crossvalidated distances

if not (decodeFeature=="12-way-all")|(decodeFeature=="subjCat-all"): #stores several values in each cell, so can't do t-test here
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