#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:48:06 2019

MVPA across ROIs

Options:
imDat - input data: # cope or tstat images
normMeth - normalization of fMRI data. used noNorm for all
    optionss: 'niNormalised','demeaned','demeaned_stdNorm','noNorm','dCentred'

distMeth - classifier / distance measure. used svm for all
    options: 'svm', 'lda', 'crossEuclid', 'crossNobis',
    'mNobis'-only subjCat-all, 12-way-all, and subjCat-orth (else no baseline)

# decoding: 
'12-way' (12-way dir decoding - only svm), 
'12-way-all' (output single decoder for each dir vs all)
'dir' (opposite dirs), 'ori' (orthogonal angles)
category: 'objCat' (objective catgeory), 'subjCat', subjCat-orth 
subjCat-resp - decode on category subject responded


@author: robert.mok
"""
import sys
import os
import numpy as np
from nilearn import image as nli  # Import image processing tool
import pandas as pd
import nibabel as nib
from nilearn.masking import apply_mask
from nilearn.signal import clean
from sklearn.model_selection import cross_val_score, LeaveOneGroupOut
from sklearn.svm import LinearSVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import scipy.stats as stats

mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI'  # love06
#mainDir = '/home/robmok/Documents/memsamp_fMRI' #love01

sys.path.append(mainDir)

featDir = os.path.join(mainDir, 'memsampFeat')
roiDir = os.path.join(mainDir, 'rois')
codeDir = os.path.join(mainDir, 'memsampCode')
os.chdir(codeDir)

from memsamp_RM import crossEuclid, mNobis, compCovMat, getConds2comp

# set to true if rerunning only a few rois, appending it to old df
reRun = False

imDat = 'cope'
normMeth = 'noNorm'
distMeth = 'svm'
trainSetMeth = 'trials'  # 'trials' or 'block' - only trials in this script
fwhm = None  # optional smoothing param - 1, or None

lock2resp = False  # if loading in lock2resp glms (to get motor effect)

# model estimated subjective category
dfmodel = pd.read_pickle(mainDir + '/behav/modelsubjcatfinal.pkl')

guessmodel = False
if guessmodel:
    dfmodel = pd.read_pickle(mainDir + '/behav/modelsubjcat_guess.pkl')

decodeFeature = 'subjCat-wb'

decodeFromFeedback = False

bilateralRois = False
# %%
# =============================================================================
# Set up decoding accuracy dataframe
# =============================================================================
nSubs = 33
rois = ['EVC_lh', 'EVC_rh', 'hMT_lh', 'hMT_rh',
        'IPS1-5_lh', 'IPS1-5_rh', 'MDroi_ifg_lh', 'MDroi_ifg_rh',
        'MDroi_area8c_lh', 'MDroi_area8c_rh', 'MDroi_area9_lh',
        'MDroi_area9_rh', 'motor_lh', 'motor_rh', 'FFA_lrh', 'PPA_lrh']

if bilateralRois:
    rois = ['EVC_lrh', 'V3a_lrh', 'hMT_lrh', 'IPS1-5_lrh', 'MDroi_ifg_lrh',
            'MDroi_area8c_lrh', 'MDroi_area9_lrh', 'motor_lrh']

# reRunROIs
#rois = ['FFA_lrh_sm', 'PPA_lrh_sm'] #functional localisers

dfDecode = pd.DataFrame(columns=rois, index=range(0, nSubs+1))
dfDecode.rename(index={nSubs: 'stats'}, inplace=True)
if (decodeFeature == "subjCat-all") | (decodeFeature=="subjCat-wb"):
    dfDecode['subjCat'] = ""

# =============================================================================
# load in trial log and append image paths
# =============================================================================

for iSub in range(1, nSubs+1):
    subNum = f'{iSub:02d}'
    dfCond = pd.DataFrame()  # main df with all runs
    if iSub in {9, 12, 16, 26}:
        runs = range(1, 5)  # 4 runs
    else:
        runs = range(1, 4)  # 3 runs
    for iRun in runs:
        condPath = os.path.join(mainDir, 'orig_events', 'sub-' + subNum +
                              '_task-memsamp_run-0' + str(iRun) +'_events.tsv')

        # df to load in and organise run-wise data
        df = pd.read_csv(condPath, sep='\t')
        df['run'] = pd.Series(np.ones((len(df)))*iRun, index=df.index)  # add run number
        #df.loc[:,'run2']=pd.Series(np.ones((len(df)))*iRun,index=df.index) #alt way - better/worse?

        # add path to match cue cond and trial num - cope1:7 is dir0 trial1:7
        conds = df.direction.unique()
        conds.sort()
        # sort - arrange df so it matches cope1:84 image structure
        df2 = pd.DataFrame()
        for iCond in conds:
            df2 = df2.append(df[df['direction'] == iCond])

        copeNum = 1  # counter
        imPath = []
        for iCond in conds:
            for iTrial in range(1, 8):  # calculate cope number
                # make a list and append to it
                if decodeFromFeedback:  # get feedback activity
                    imPath.append(os.path.join(
                            featDir, 'sub-' + subNum + '_run-0' + str(iRun)
                            + '_trial_feedback_T1_fwhm0.feat', 'stats', imDat
                            + (str(copeNum)) + '.nii.gz'))
                else:  # otherwise, get cue-evoked activity
                    if lock2resp:  # lock2resp glm - to get motor effects
                        imPath.append(os.path.join(
                                featDir, 'sub-' + subNum + '_run-0' + str(iRun)
                                + '_trial_T1_lock2resp_fwhm0.feat', 'stats',
                                imDat + (str(copeNum)) + '.nii.gz'))
                    else:
                        imPath.append(os.path.join(
                                featDir, 'sub-' + subNum + '_run-0' + str(iRun)
                                + '_trial_T1_fwhm0.feat', 'stats', imDat +
                                (str(copeNum)) + '.nii.gz'))
                copeNum = copeNum+1
        df2['imPath'] = pd.Series(imPath, index=df2.index)
        dfCond = dfCond.append(df2)  # append to main df
    print('subject %s, length of df %s' % (subNum, len(dfCond)))

    # only get 2 out of 3/4 runs that share same response (no counterbalance)
    if (decodeFeature=='subjCat-motor') | (decodeFeature=='subjCat-orth-motor'):
        if sum(dfCond['keymap'] == 0) > sum(dfCond['keymap'] == 1):
            dfCond = dfCond[dfCond['keymap'] == 0]
        elif sum(dfCond['keymap'] == 0) < sum(dfCond['keymap'] == 1):
            dfCond = dfCond[dfCond['keymap'] == 1]
        else:  # if 4 runs, just select one set
            dfCond = dfCond[dfCond['keymap'] == 1]

    if lock2resp:  # remove trials without responses
        indResp = np.where(~np.isnan(dfCond['rt']))
        dfCond = dfCond.iloc[indResp[0]]

    # get objective category
    catAconds = np.array((range(120, 271, 30)))
    catBconds = np.append(np.array((range(0, 91, 30))), [300, 330])

    if decodeFeature == 'subjCat-minus-motor':
        dfCondResp = dfCond['key']

    # get subjective category based on model
    if (decodeFeature[0:7] == 'subjCat') | (decodeFeature == 'dir-all'):
        subjCatAconds = dfmodel['a'].loc[iSub-1]
        subjCatBconds = dfmodel['b'].loc[iSub-1]

    # =============================================================================
    # set up brain data
    # =============================================================================

    dat = dfCond['imPath'].values  # img paths - keeping same variables as sl
    y = dfCond['direction'].values  # conditions / stimulus
    groups = dfCond['run'].values  # info about the sessions

    for roi in rois:
        # define ROI  mask
        mask_path = os.path.join(
                roiDir, 'sub-' + subNum + '_' + roi + '.nii.gz')

        # resample mask to match epi
        if not (((roi[0:7] == 'PPA_lrh') & (subNum in ('05', '08', '09', '24'))) | ((roi[0:7] == 'FFA_lrh') & (subNum in ('08', '15')))):  # no PPA / FFA for these people
            imgs = nib.load(dat[0])  # load 1 im to downsample to match epi
            maskROI = nib.load(mask_path)
            maskROI = nli.resample_img(
                    maskROI, target_affine=imgs.affine,
                    target_shape=imgs.shape[:3], interpolation='nearest')
            fmri_masked = apply_mask(dat, maskROI, smoothing_fwhm=fwhm)
        else:
            fmri_masked = dat
    
        if normMeth == 'niNormalised':
            fmri_masked_cleaned = clean(fmri_masked, sessions=groups, detrend=False, standardize=True)
        elif normMeth == 'demeaned':
            fmri_masked_cleaned=fmri_masked.transpose()-np.nanmean(fmri_masked,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned.transpose()
        elif normMeth == 'demeaned_stdNorm':
            fmri_masked_cleaned=fmri_masked.transpose()-np.nanmean(fmri_masked,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned/np.nanstd(fmri_masked,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned.transpose()
        elif normMeth == 'dCentred': #both niNorm and demeaned stdNorm
            fmri_masked_cleaned = clean(fmri_masked, sessions=groups, detrend=False, standardize=True)
            fmri_masked_cleaned=fmri_masked_cleaned.transpose()-np.nanmean(fmri_masked_cleaned,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned/np.nanstd(fmri_masked,axis=1)
            fmri_masked_cleaned=fmri_masked_cleaned.transpose()
        elif normMeth == 'noNorm':
            fmri_masked_cleaned = fmri_masked                    

        if distMeth in {'crossNobis','mNobis'}:  # get variance to compute covar matrix below
            # compute each run's cov mat here, then apply it to fmri_masked_cleaned, then euclid below
            covMat = np.empty((np.size(fmri_masked_cleaned,axis=1),np.size(fmri_masked_cleaned,axis=1),len(runs))) #nVox x nVox
            for iRun1 in runs: #append to list, since var sometimes has more/less timepoints in each run
                varPath = os.path.join(featDir, 'sub-' + subNum + '_run-0' + str(iRun1) +'_trial_T1_fwhm0.feat', 'stats', 'res4d.nii.gz')
#                covMat[:,:,iRun1-1] = compCovMat(apply_mask(varPath,maskROI))
                covMat[:,:,iRun1-1] = compCovMat(apply_mask(varPath,maskROI,smoothing_fwhm=fwhm))
            if distMeth == 'crossNobis':
                for iRun1 in runs:
                    trlInd = np.where(groups==iRun1)
                    trlInd = trlInd[0]
                    for iTrl in trlInd:
                        fmri_masked_cleaned[iTrl, ] = np.dot(
                                fmri_masked_cleaned[iTrl, ],
                                covMat[:, :, iRun1-1])
            else:  # average covMat over runs
                for iTrl in range(0, len(fmri_masked_cleaned)):
                    fmri_masked_cleaned[iTrl, ] = np.dot(
                            fmri_masked_cleaned[iTrl, ], covMat.mean(axis=2))

    # =============================================================================
    #     #set up splits and run cv
    # ============================================================================
    
        # set up the conditions you want to classify. if 12-way, no need
        if (decodeFeature=="objCat")|(decodeFeature=="objCat-orth"):
            conds2comp = [[catAconds, catBconds]]   #put in conditions to compare, e.g. conditions=[catAconds, catBconds]      
        elif (decodeFeature=="subjCat")|(decodeFeature=="subjCat-orth")|(decodeFeature=="subjCat-motor")|(decodeFeature=="subjCat-orth-motor")|(decodeFeature=="subjCat-minus-motor"): #subjective catgory bound based on responses
            conds2comp = [[subjCatAconds, subjCatBconds]] 
        elif decodeFeature=="subjCat-orth-ctrl":
            conds2comp = [subjCatAconds, subjCatBconds]
            catA90 = conds2comp[0]+90
            catB90 = conds2comp[1]+90
            catA90[catA90>359]=catA90[catA90>359]-360
            catB90[catB90>359]=catB90[catB90>359]-360
            conds2comp = [[catA90, catB90]]  
        elif decodeFeature == "subjCat-all":
            condsTmp=list(subjCatAconds)+list(subjCatBconds)
            conds2comp = getConds2comp(decodeFeature,condsTmp)
        elif (decodeFeature=="subjCat-resp")|(decodeFeature=="motor")|(decodeFeature=="feedstim"):
            conds2comp = np.empty((1)) #len of 1 placeholder
        elif decodeFeature == "dir-all":
            oppDirs = np.array(([subjCatAconds, abs((subjCatAconds-180) % 360)]))
            conds2comp = []
            for iDirPairs in range(0,np.size(oppDirs,1)):
                conds2comp.append(oppDirs[:,iDirPairs])
        elif decodeFeature == "subjCat-wb":  # within-between cateory
            conds2comp = []
            # within
            for icond in range(len(subjCatAconds)): 
                ind = np.ones(len(subjCatAconds), dtype='bool')
                ind[icond] = False
                conds2comp.append([subjCatAconds[icond], subjCatAconds[ind]])
            for icond in range(len(subjCatBconds)): 
                ind = np.ones(len(subjCatBconds), dtype='bool')
                ind[icond] = False
                conds2comp.append([subjCatBconds[icond], subjCatBconds[ind]])
            # between
            for icond in range(len(subjCatBconds)): 
                conds2comp.append([subjCatAconds[icond], subjCatBconds])
            for icond in range(len(subjCatAconds)): 
                conds2comp.append([subjCatBconds[icond], subjCatAconds])
        else:  # stimulus decoding
            conds2comp = getConds2comp(decodeFeature)
        
        # run cv
        if decodeFeature == "12-way": # no need conds2comp, just compare all
            iPair=0
            cv   = LeaveOneGroupOut()
            cv.get_n_splits(fmri_masked_cleaned, y, groups)
            cv   = cv.split(fmri_masked_cleaned,y,groups)   
            if not (((roi[0:7] == 'PPA_lrh') & (subNum in ('05', '08', '09', '24'))) | ((roi[0:7] == 'FFA_lrh') & (subNum in ('08', '15')))):  # no PPA / FFA for these people
                if distMeth == 'svm':
                    clf   = LinearSVC(C=.1)
                elif distMeth == 'lda':
                    clf = LinearDiscriminantAnalysis()
                    clf.fit(fmri_masked_cleaned, y) 
                cvAccTmp = cross_val_score(clf,fmri_masked_cleaned,y=y,scoring='accuracy',cv=cv).mean()  # mean over crossval folds
                print('ROI: %s, Sub-%s cvAcc = %0.3f' % (roi, subNum, (cvAccTmp*100)))
                print('ROI: %s, Sub-%s cvAcc-chance = %0.3f' % (roi, subNum, (cvAccTmp-(1/len(np.unique(y))))*100))
                y_indexed = y  # for computing chance
        else:   # all condition-wise comparisons
            cvAccTmp = np.empty(len(conds2comp))
            for iPair in range(0,len(conds2comp)):
                ytmp=y.copy()
                if (decodeFeature == "12-way-all")|(decodeFeature=="subjCat-wb"): 
                    condInd=np.where(y==conds2comp[iPair][0])
                    for iVal in conds2comp[iPair][1]:
                        condInd=np.append(condInd, np.where(y==iVal))
                    ytmp[y!=conds2comp[iPair][0]] = 1  # change the 'other' conditions to 1, comparing to the main value
                elif (decodeFeature=="subjCat-resp")|(decodeFeature=="motor"):
                    condInd = np.append(np.where(dfCond['key']==1), np.where(dfCond['key']==6))
                    ytmp[np.where(dfCond['key']==1)] = 0  # if subjCat-resp, motor resps flipped across blocks so changed stim directions to responses (changed above if decodeFeature[0:7]=="subjCat")
                    ytmp[np.where(dfCond['key']==6)] = 1
                elif decodeFeature == 'feedstim':
                    condInd = np.append(np.where(dfCond['category']==0), np.where(dfCond['category']==1))
                    ytmp[np.where(dfCond['category']==0)] = 0  # edit ytmp (direction conds) to what you want to test
                    ytmp[np.where(dfCond['category']==1)] = 1
                else:
                    condInd=np.empty(0,dtype=int) 
                    if np.size(conds2comp[iPair][0])>2:  # need to loop through if more stim within one category to decode (no need if ori/dir since pairwise)
                        for iVal in conds2comp[iPair][0]:
                            ytmp[np.where(y==iVal)]=0  # change cat A to 0 and cat B to 1
                            condInd=np.append(condInd, np.where(y==iVal)) # index all conds
                        for iVal in conds2comp[iPair][1]:
                            ytmp[np.where(y==iVal)]=1
                            condInd=np.append(condInd, np.where(y==iVal)) 
                    else:  # ori, dir
                        condInd=np.append(np.where(y==conds2comp[iPair][0]), np.where(y==conds2comp[iPair][1])) 

                fmri_masked_cleaned_indexed= fmri_masked_cleaned[condInd,]
                y_indexed = ytmp[condInd]
                groups_indexed = groups[condInd]
                cv    = LeaveOneGroupOut()
                cv.get_n_splits(fmri_masked_cleaned_indexed, y_indexed, groups_indexed)
                cv    = cv.split(fmri_masked_cleaned_indexed,y_indexed,groups_indexed)    
                if not (((roi[0:7] == 'PPA_lrh') & (subNum in ('05', '08', '09', '24'))) | ((roi[0:7] == 'FFA_lrh') & (subNum in ('08', '15')))):  # no PPA / FFA for these people
                    if distMeth == 'svm':
                        clf   = LinearSVC(C=.1)
                        cvAccTmp[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                    elif distMeth == 'lda':
                        clf = LinearDiscriminantAnalysis()
                        clf.fit(fmri_masked_cleaned, y) 
                        cvAccTmp[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                    elif distMeth in {'crossEuclid','crossNobis'}:
                        cvAccTmp[iPair] = crossEuclid(fmri_masked_cleaned_indexed,y_indexed,cv).mean() # mean over crossval folds
                    elif distMeth == 'mNobis':
                        cvAccTmp[iPair] = mNobis(fmri_masked_cleaned_indexed,y_indexed)

            if (decodeFeature=="subjCat-orth")|(decodeFeature=="objCat-orth")|(decodeFeature=="subjCat-orth-motor")|(decodeFeature=="subjCat-minus-motor"):                
                catA90 = conds2comp[0][0]+90
                catB90 = conds2comp[0][1]+90
                catA90[catA90>359]=catA90[catA90>359]-360
                catB90[catB90>359]=catB90[catB90>359]-360
                conds2comp = [[catA90, catB90]]  
                cvAccTmp90 = np.empty(len(conds2comp))
                for iPair in range(0,len(conds2comp)):
                    ytmp=y.copy()
                    if decodeFeature=="motor":
                        condInd = np.append(np.where(dfCondResp['key']==1),np.where(dfCondResp['key']==6)) #dfCond edited to dfCondResp since in subjCat-minus-motor dfCond, 'key' is flipped
                        ytmp[np.where(dfCond['key']==1)]=0  # if subjCat-resp, motor resps flipped across blocks so changed stim directions to responses (changed above if decodeFeature[0:7]=="subjCat")
                        ytmp[np.where(dfCond['key']==6)]=1  
                        cvAccTmp90 = np.empty((1))  # just keep this naming
                    else:
                        condInd = np.empty(0 ,dtype=int) 
                        for iVal in conds2comp[iPair][0]:
                            ytmp[np.where(y==iVal)]=0  # change cat A to 0 and cat B to 1
                            condInd=np.append(condInd, np.where(y==iVal))  # index all conds
                        for iVal in conds2comp[iPair][1]:
                            ytmp[np.where(y==iVal)]=1
                            condInd=np.append(condInd, np.where(y==iVal)) 
                
                    fmri_masked_cleaned_indexed= fmri_masked_cleaned[condInd,]
                    y_indexed = ytmp[condInd]
                    groups_indexed = groups[condInd]

                    cv    = LeaveOneGroupOut()
                    cv.get_n_splits(fmri_masked_cleaned_indexed, y_indexed, groups_indexed)
                    cv    = cv.split(fmri_masked_cleaned_indexed,y_indexed,groups_indexed)    
                    if not (((roi[0:7] == 'PPA_lrh') & (subNum in ('05', '08', '09', '24'))) | ((roi[0:7] == 'FFA_lrh') & (subNum in ('08', '15')))):  # no PPA / FFA for these people
                        if distMeth == 'svm':
                            clf   = LinearSVC(C=.1)
                            cvAccTmp90[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                        elif distMeth == 'lda':
                            clf = LinearDiscriminantAnalysis()
                            clf.fit(fmri_masked_cleaned, y) 
                            cvAccTmp90[iPair] = cross_val_score(clf,fmri_masked_cleaned_indexed,y=y_indexed,scoring='accuracy',cv=cv).mean() 
                        elif distMeth in {'crossEuclid','crossNobis'}:
                            cvAccTmp90[iPair] = crossEuclid(fmri_masked_cleaned_indexed,y_indexed,cv).mean()  # mean over crossval folds
                        elif distMeth == 'mNobis':
                            cvAccTmp90[iPair] = mNobis(fmri_masked_cleaned_indexed,y_indexed)                    
                cvAccTmp = cvAccTmp-cvAccTmp90
        
        if not (decodeFeature=="12-way-all")|(decodeFeature=="subjCat-all")|(decodeFeature=="objCat-all")|(decodeFeature=="dir-all")|(decodeFeature=="subjCat-wb"): 
            cvAcc = cvAccTmp.mean()  # mean over pairs
            print('ROI: %s, Sub-%s %s measure = %0.3f' % (roi, subNum, distMeth, cvAcc))    
        else:
            cvAcc = cvAccTmp  # save all pairs
        if not (((roi[0:7] == 'PPA_lrh') & (subNum in ('05', '08', '09', '24'))) | ((roi[0:7] == 'FFA_lrh') & (subNum in ('08', '15')))):  # no PPA / FFA for these people
            dfDecode[roi].iloc[iSub-1]=cvAcc #store to main df
        
    if (decodeFeature=="subjCat-all") | (decodeFeature=="subjCat-wb"):  # add subjCat info to df
        dfDecode['subjCat'][iSub-1] = [list(subjCatAconds), list(subjCatBconds)]
# compute t-test, append to df
if ((distMeth=='svm')|(distMeth=='lda'))&((decodeFeature!="subjCat-orth")&(decodeFeature!="objCat-orth")&(decodeFeature!="subjCat-orth-motor")&(decodeFeature!="subjCat-minus-motor")):
    chance = 1/len(np.unique(y_indexed))
else: 
    chance = 0  # for crossvalidated distances or subtractions (e.g. subjCat-orth)

if not (decodeFeature=="12-way-all")|(decodeFeature=="subjCat-all")|(decodeFeature=="objCat-all")|(decodeFeature=="dir-all")|(decodeFeature=="subjCat-wb"): #stores several values in each cell, so can't do t-test here
    for roi in rois:
        dfDecode[roi].iloc[-1]=stats.ttest_1samp(dfDecode[roi].iloc[0:nSubs].astype(float), chance, nan_policy='omit') #compute t-test, append to df

fnameSave = os.path.join(mainDir, 'mvpa_roi', 'roi_' + decodeFeature +'Decoding_' +
                                      distMeth + '_' + normMeth + '_'  + trainSetMeth + 
                                      '_fwhm' + str(fwhm) + '_' + imDat)
if lock2resp:
    fnameSave = fnameSave + '_lock2resp'

if bilateralRois:
    fnameSave = fnameSave + '_bilateral'

if decodeFromFeedback:
    fnameSave = fnameSave + '_fromfeedback'

# if re-running / adding, load in first, append new dat to df, then save
if reRun is True:
    dfTmp = pd.read_pickle(fnameSave + '.pkl')
    for roi in rois:
        dfTmp[roi] = dfDecode[roi]
    dfDecode = dfTmp

if guessmodel:
    fnameSave = fnameSave + '_guess'

# save df
dfDecode.to_pickle(fnameSave + '.pkl')
