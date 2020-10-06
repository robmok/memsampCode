#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:55:54 2020

@author: robert.mok
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/Johan/data/behavioural/'

fname = mainDir + 'resp_AB160526_behavioural_run00.pickle'

data = pd.read_pickle(fname)

x=data['onresponse_score'].to_numpy()

acc = np.nansum(x)/len(x)


fnames = os.path.join(mainDir, "resp*beha*")
datafiles = sorted(glob.glob(fnames))

ids = []
for iFile in datafiles:
    ids.append(iFile[68:76])

subIDs = list(set(subIDs))

acc = np.empty(len(subIDs))
for iSub in range(len((set(subIDs)))):
    fnames = os.path.join(mainDir, "resp_{}*_behav*".format(subIDs[iSub]))
    datafiles = sorted(glob.glob(fnames))
    
    tmpacc = []
    for iFile in datafiles:
        data = pd.read_pickle(iFile)
        x = data['onresponse_score'].to_numpy()
        meanacc = np.nansum(x)/len(x)
        tmpacc.append(meanacc)
    acc[iSub] = np.array(tmpacc).mean()

print(np.sum(acc < .6))