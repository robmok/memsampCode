#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:12:57 2020

@author: robert.mok
"""

import numpy as np
import pands as pd
mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'  # love06

fname = mainDir + 'mvpa_roi/subjCat.pkl'
dforig = pd.read_pickle(fname)
fname = mainDir + 'behav/modelsubjcat4.pkl'
dfmodel = pd.read_pickle(fname)
fname = mainDir + 'behav/modelsubjcat_guess.pkl'
dfguess = pd.read_pickle(fname)

# subjCat vs model diffs: 3, 4, 5, 12,14,16,23, 26, 28, 31 (NB: subs from 0)
for isub in range(0, 33):
    pattern1 = (np.array_equal(dforig.loc[isub][0], dfmodel['a'].loc[isub]))
    pattern2 = (np.array_equal(dforig.loc[isub][0], dfmodel['b'].loc[isub]))
    if not (pattern1 | pattern2):
        print('basic model sub %d catA dif to orig' % isub)    
    pattern1 = (np.array_equal(dforig.loc[isub][1], dfmodel['b'].loc[isub]))
    pattern2 = (np.array_equal(dforig.loc[isub][1], dfmodel['a'].loc[isub]))
    if not (pattern1 | pattern2):
        print('basic model sub %d catB dif to orig' % isub)    
        print(dforig.loc[isub])
        print(dfmodel['a'].loc[isub], dfmodel['b'].loc[isub])

# model vs guess model diffs: 3, 4, 14, 16, 28, 31 (NB: subs from 0)
for isub in range(0, 33):
    pattern1 = (np.array_equal(dfmodel['a'].loc[isub], dfguess['a'].loc[isub]))
    pattern2 = (np.array_equal(dfmodel['a'].loc[isub], dfguess['b'].loc[isub]))
    if not (pattern1 | pattern2):
        print('basic model sub %d catA dif to guess model' % isub)    
    pattern1 = (np.array_equal(dfmodel['b'].loc[isub], dfguess['a'].loc[isub]))
    pattern2 = (np.array_equal(dfmodel['b'].loc[isub], dfguess['b'].loc[isub]))
    if not (pattern1 | pattern2):
        print('basic model sub %d catB dif to guess model' % isub)    
        print(dforig.loc[isub])
        print(dfmodel['a'].loc[isub], dfmodel['b'].loc[isub])

# orig vs guess model diffs: 4, 5, 12, 23, 26 (NB: subs from 0)
for isub in range(0, 33):
    pattern1 = (np.array_equal(dforig.loc[isub][0], dfguess['a'].loc[isub]))
    pattern2 = (np.array_equal(dforig.loc[isub][0], dfguess['b'].loc[isub]))
    if not (pattern1 | pattern2):
        print('guess model sub %d catA dif to orig' % isub)    
    pattern1 = (np.array_equal(dforig.loc[isub][1], dfguess['b'].loc[isub]))
    pattern2 = (np.array_equal(dforig.loc[isub][1], dfguess['a'].loc[isub]))
    if not (pattern1 | pattern2):
        print('guess model sub %d catB dif to orig' % isub)    
        print(dforig.loc[isub])
        print(dfguess['a'].loc[isub], dfguess['b'].loc[isub])

# print all different ones (simply all from the sbjCat vs model)
for isub in [3, 4, 5, 12, 14, 16, 23, 26, 28, 31]:
    print('sub %d' % isub)
    print(dforig.loc[isub])
    print(dfmodel['a'].loc[isub], dfmodel['b'].loc[isub])
    print(dfguess['a'].loc[isub], dfguess['b'].loc[isub])
