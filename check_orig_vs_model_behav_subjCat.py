#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:12:57 2020

@author: robert.mok
"""

import numpy as np

mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'  # love06

fname = mainDir + 'mvpa_roi/subjCat.pkl'
dforig = pd.read_pickle(fname)

fname = mainDir + 'behav/modelsubjcat4.pkl'
dfmodel = pd.read_pickle(fname)

fname = mainDir + 'behav/modelsubjcat_guess.pkl'
dfguess = pd.read_pickle(fname)


# orig subjCat vs model diffs: subs 3, 4, 5, 12,14,16,23, 26, 28, 31
for isub in range(0,33):
    pattern1 = (np.array_equal(dforig.loc[isub][0], dfmodel['a'].loc[isub]))
    pattern2 = (np.array_equal(dforig.loc[isub][0], dfmodel['b'].loc[isub]))
    if not (pattern1 | pattern2):
        print('basic model sub %d catA dif to orig' % isub)    
    pattern1 = (np.array_equal(dforig.loc[isub][1], dfmodel['b'].loc[isub]))
    pattern2 = (np.array_equal(dforig.loc[isub][1], dfmodel['a'].loc[isub]))
#    if not (pattern1 | pattern2):
#        print('basic model sub %d catB dif to orig' % isub)    
#        print(dforig.loc[isub])
#        print(dfmodel['a'].loc[isub],dfmodel['b'].loc[isub])




# model vs guess model diffs: subs
for isub in range(0,33):
    pattern1 = (np.array_equal(dfmodel['a'].loc[isub], dfguess['a'].loc[isub]))
    pattern2 = (np.array_equal(dfmodel['a'].loc[isub], dfguess['b'].loc[isub]))
    if not (pattern1 | pattern2):
        print('basic model sub %d catA dif to guess model' % isub)    
    pattern1 = (np.array_equal(dfmodel['b'].loc[isub], dfguess['a'].loc[isub]))
    pattern2 = (np.array_equal(dfmodel['b'].loc[isub], dfguess['b'].loc[isub]))
#    if not (pattern1 | pattern2):
#        print('basic model sub %d catB dif to guess model' % isub)    
#        print(dforig.loc[isub])
#        print(dfmodel['a'].loc[isub],dfmodel['b'].loc[isub])