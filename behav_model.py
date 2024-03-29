#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:56:07 2019

@author: robert.mok

Behavioural model to estimate subjective category
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy import optimize as opt
import time

mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'
codeDir = os.path.join(mainDir, 'memsampCode')
os.chdir(codeDir)

# %% Run behavioural model for each participant

t0 = time.time()
dfres = pd.DataFrame(columns=['bestparams', 'a', 'b', 'modelacc'],
                     index=range(0, 33))
for iSub in range(1, 34):
#iSub = 1
    subNum = f'{iSub:02d}'
    dfCond = pd.DataFrame()  # main df with all runs
    if iSub in {9, 12, 16, 26}:
        runs = range(1, 5)  # 4 runs
    else:
        runs = range(1, 4)  # 3 runs
    for iRun in runs:
        condPath = os.path.join(mainDir, 'orig_events', 'sub-' +
                                subNum + '_task-memsamp_run-0' +
                                str(iRun) + '_events.tsv')
        df = pd.read_csv(condPath, sep='\t')
        df['run'] = pd.Series(np.ones((len(df)))*iRun, index=df.index)  # add run number
        dfCond = dfCond.append(df)  # append to main df

    # flip key when keymap is flipped
    ind1 = dfCond['keymap'] == 1  # if 'keymap' == 1: #flip, if 0, no need
    ind2 = dfCond['key'] == 6
    ind3 = dfCond['key'] == 1
    dfCond.loc[ind1 & ind2, 'key'] = 5
    dfCond.loc[ind1 & ind3, 'key'] = 6
    dfCond.loc[ind1 & ind2, 'key'] = 1

    # get responses
    conds = dfCond.direction.unique()
    conds.sort()
    dat = dfCond[['direction', 'key']]
    # remove nans
    dat = dat[~np.isnan(dat['key'])]

    # model - define objective function
    def runit(params, dat=dat):
        import numpy as np

        def angdiff(x, y):
            return np.arctan2(np.sin(x-y), np.cos(x-y))

        # distance from bound 1 and 2
        angdiff1 = angdiff(
                np.radians(dat['direction'].values),
                np.radians(params[0]))

        angdiff2 = angdiff(
                np.radians(dat['direction'].values),
                np.radians(params[1]))

        # find out if closer to bound 1 or 2, if same, include both
        ind1 = abs(angdiff1) <= abs(angdiff2)  # closer to bound 1
        ind2 = abs(angdiff1) >= abs(angdiff2)

        # clockwise or counterclowise to bound
        ind1pos = angdiff1 >= 0  # = so if on bound, count on bound as pos
        ind1neg = angdiff1 < 0
        ind2pos = angdiff2 >= 0
        ind2neg = angdiff2 < 0

        # conditions
        catA1 = sorted(dat['direction'][ind1 & ind1pos].unique())  # A one side
        catA2 = sorted(dat['direction'][ind2 & ind2neg].unique())  # other side
        catB1 = sorted(dat['direction'][ind1 & ind1neg].unique())
        catB2 = sorted(dat['direction'][ind2 & ind2pos].unique())

        # acc to boundary, resps1==correct, resps2==incorrect
        r1a = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                       (dat['key'] == 1)],
                              angdiff2[(dat['direction'].isin(catB2)) &
                                       (dat['key'] == 6)]))
        r1b = np.concatenate((angdiff2[(dat['direction'].isin(catA2)) &
                                       (dat['key'] == 1)],
                              angdiff1[(dat['direction'].isin(catB1)) &
                                       (dat['key'] == 6)]))

        r2a = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                       (dat['key'] == 6)],
                              angdiff2[(dat['direction'].isin(catB2)) &
                                       (dat['key'] == 1)]))
        r2b = np.concatenate((angdiff2[(dat['direction'].isin(catA2)) &
                                       (dat['key'] == 6)],
                              angdiff1[(dat['direction'].isin(catB1)) &
                                       (dat['key'] == 1)]))

        # put through cdfå
        allresps = np.concatenate((1-norm.cdf(r1a, 0, params[2]),
                                   norm.cdf(r1b, 0, params[2]),
                                   norm.cdf(r2a, 0, params[2]),
                                   1-norm.cdf(r2b, 0, params[2])))

        if len(params) == 4:  # with guess rate
            alpha = params[3]  # guess rate
            allresps = alpha * 0.5 + (1-alpha) * (allresps)

        # sum logpr (to check exp this result, comp w np.prod of pr's)
        negloglik = -np.sum(np.log(allresps))

        return negloglik

    # ...optimize this with bound1, bound2, and SD .., with sensible limits

#    # multiple starting point
#    starts = [[0, 180, .5], [270, 90, 1], [45, 225, .5], [135, 315, 2]]
    bounds = [(-359, 359), (-359, 359), (0., 20.)]
#
    # looping through starts
    starts = []
    startsb1 = np.arange(15., 345., 60)
    startsb2 = np.arange(45., 360., 60)  # -360
    sds = [.5, 1, 2, 3, 5]

    guess = False
    if guess:
        gs = [.1, .3, .7]
        bounds.append((0., 1.))
    if not guess:
        for b1 in startsb1:
            for b2 in startsb2:
                for sd in sds:
                    starts.append([b1, b2, sd])
    else:
        for b1 in startsb1:
            for b2 in startsb2:
                for sd in sds:
                    for g in gs:
                        starts.append([b1, b2, sd, g])

    negloglik = np.inf
    res = []
    method = ['SLSQP', 'L-BFGS-B'][0]

    for startparams in starts:
        # start optimization
        res = opt.minimize(runit, startparams, method=method, bounds=bounds)
        if res.fun < negloglik:  # if new result is smaller, replace it
            negloglik = res.fun
            bestparams = res.x
#            print('%s' % startparams)
#            print('%s' % np.array2string(bestparams))
#            print('  loss: {0:.2f}'.format(negloglik))
#            print('')

    # fix of estimated negative or over 360 bounds
    while bestparams[0] < 0:
        bestparams[0] += 360
    while bestparams[1] < 0:
        bestparams[1] += 360
    while bestparams[0] > 360:
        bestparams[0] -= 360
    while bestparams[1] > 360:
        bestparams[1] -= 360

    # display results
    if False:
        if bestparams[0] < bestparams[1]:
            n_cata_resps_side1 = (
                    dat.loc[(dat['direction'] > bestparams[0]) &
                            (dat['direction'] < bestparams[1]),
                            'key'].values == 1).sum()
            n_catb_resps_side1 = (
                    dat.loc[(dat['direction'] > bestparams[0]) &
                            (dat['direction'] < bestparams[1]),
                            'key'].values == 6).sum()
            # using OR operator here
            n_cata_resps_side2 = (
                    dat.loc[(dat['direction'] > bestparams[1]) |
                            (dat['direction'] < bestparams[0]),
                            'key'].values == 1).sum()
            n_catb_resps_side2 = (
                    dat.loc[(dat['direction'] > bestparams[1]) |
                            (dat['direction'] < bestparams[0]),
                            'key'].values == 6).sum()
        elif bestparams[0] > bestparams[1]:
            n_cata_resps_side1 = (
                    dat.loc[(dat['direction'] > bestparams[1]) &
                            (dat['direction'] < bestparams[0]),
                            'key'].values == 6).sum()
            n_catb_resps_side1 = (
                    dat.loc[(dat['direction'] > bestparams[1]) &
                            (dat['direction'] < bestparams[0]),
                            'key'].values == 1).sum()
            # using OR operator here
            n_cata_resps_side2 = (
                    dat.loc[(dat['direction'] > bestparams[0]) |
                            (dat['direction'] < bestparams[1]),
                            'key'].values == 6).sum()
            n_catb_resps_side2 = (
                    dat.loc[(dat['direction'] > bestparams[0]) |
                            (dat['direction'] < bestparams[1]),
                            'key'].values == 1).sum()

        print('sub %d bestparams: %s' % (iSub, np.array2string(bestparams)))
        if bestparams[0] < bestparams[1]:
            catA = conds[(conds > bestparams[0]) & (conds <= bestparams[1])]
            catB = conds[(conds > bestparams[1]) | (conds <= bestparams[0])]
            print('catA %s' % np.array2string(catA))
            print('catB %s' % np.array2string(catB))
        elif bestparams[0] > bestparams[1]:
            catA = conds[(conds <= bestparams[0]) & (conds > bestparams[1])]
            catB = conds[(conds <= bestparams[1]) | (conds > bestparams[0])]
            print('catA %s' % np.array2string(catA))
            print('catB %s' % np.array2string(catB))

        # incorrect, correct, inc, corr (most resps should be on the corr side)
        ncorr_inc = [n_cata_resps_side1, n_cata_resps_side2,
                     n_catb_resps_side2, n_catb_resps_side1]
        print(ncorr_inc)

    dfres['bestparams'].loc[iSub-1] = bestparams
    dfres['a'].loc[iSub-1] = catA
    dfres['b'].loc[iSub-1] = catB
    dfres['modelacc'].loc[iSub-1] = ncorr_inc

t1 = time.time()
print(t1-t0)

fnamesave = mainDir + 'behav/modelsubjcat_guess'
dfres.to_pickle(fnamesave + '.pkl')
