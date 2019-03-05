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
#from nilearn import image # Import image processing tool
import clarte.clarte as cl # on love06 - normally just clarte is fine
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

#%% load in trial log and append image paths

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
        #temp path for laptop
        #condPath='/Users/robertmok/Documents/Postdoc_ucl/sub-01_task-memsamp_run-0' + str(iRun) + '_events.tsv'
        
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
    
    #start
    T1_mask_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-brain_mask.nii.gz') #whole brain
 #   T1_mask_path = os.path.join(roiDir, 'sub-' + subNum + '_visRois_lrh.nii.gz') #visRois
    T1_path = os.path.join(fmriprepDir, 'sub-' + subNum, 'anat', 'sub-' + subNum + '_desc-preproc_T1w.nii.gz')
    dat = cl.fmri_data(dfCond['imPath'].values,T1_mask_path, fwhm=1)  #optional smoothing param: fwhm=1 
    
#    #from kurt demo
#    print('type(dat)',type(dat))
#    print('dat.dat.shape:',dat.dat.shape)
#    print('dat affine:\n',dat.volInfo['affine'])
#    print('')
#    nip.plot_stat_map(dat.mask['niimg'],title='T1 mask',cut_coords=(0,40,41),
#                 bg_img=T1_path,colorbar=True)
#    print('unique mask values:',np.unique(dat.masker(dat.mask['niimg'])))
#    print('nVoxels in mask:',np.sum(dat.masker(dat.mask['niimg'])))
#    
#    #plot a volume
#    im1 = dat.unmasker(dat.dat[1,:]) # first row of the data matrix
#    print('im1 shape:',im1.shape)
#    nip.plot_stat_map(im1,title='im1: the first volume', colorbar=True, 
#                  bg_img=T1_path, 
#                  threshold=.0, cut_coords=(0,40,41))

    #run searchlight
    # first we give the dat object info about the sessions:
    dat.sessions = dfCond['run'].values
    
    #demean - across conditions; try to do only within sphere? also try demean only or demean + norm variance
    voxels2check = [0, 500, 1000]#[1000,5000,10000]
    print('mean and std of each voxel before preproc:\n',
            ['%.3f'%np.mean(dat.dat[:,i]) for i in voxels2check],
            ['%.3f'%np.std(dat.dat[:,i]) for i in voxels2check])    
    dat.cleaner(standardizeVox=True)
    print('\nmean and std of each voxel after preproc:\n',
        ['%.3f'%np.mean(dat.dat[:,i]) for i in voxels2check],
        ['%.3f'%np.std(dat.dat[:,i]) for i in voxels2check])
    

    groups=dat.sessions
    dat.y  = dfCond['direction'].values #conditions / stimulus
    cv     = LeaveOneGroupOut()
    cv.get_n_splits(dat.dat, dat.y,groups)
    clf = LinearSVC(C=.1)
    
    # the pipeline function - function defining the computation performed in each sphere
    # - add demean / normalize variance within sphere?
    def pipeline(X,y):
        return cross_val_score(clf,X,y=y,scoring='accuracy',cv=cv.split(dat.dat,dat.y,groups)).mean()    

    dat.pipeline = pipeline
    
    # searchlight with sphere radius=5mm using 1 core:
    im = cl.searchlightSphere(dat,5,n_jobs=6) #n_jobs - cores

    #%%
    chance   = 1./12
    imVec    = dat.masker(im)
    imVec    = imVec - chance 
    imThresh = dat.unmasker(imVec)
    
    nip.plot_stat_map(imThresh,colorbar=True, threshold=0.05,bg_img=T1_path,
                                      title='Accuracy > Chance (+arbitrary threshold)')
#    plt.show()

    #interactive -  open the plot in a web browser:
    view = nip.view_img(imThresh,colorbar=True, threshold=0.05,bg_img=T1_path,
                                      title='Accuracy > Chance (+arbitrary threshold)')
    view.open_in_browser()     