#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:56:07 2019

@author: robert.mok
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
#from scipy.stats import vonmises
from scipy import optimize as opt

mainDir = '/Users/robert.mok/Documents/Postdoc_ucl/memsamp_fMRI/'  # love06
#mainDir = '/Users/robertmok/Documents/Postdoc_ucl/'  # mac laptop
codeDir=os.path.join(mainDir,'memsampCode')
os.chdir(codeDir)

subjCat = pd.read_pickle(mainDir + 'mvpa_roi/subjCat.pkl')

# %% load in data

import time
t0 = time.time()

dfres = pd.DataFrame(columns=['bestparams','a','b', 'modelacc'], index=range(0, 34))

for iSub in range(1, 34):
#iSub = 2

    subNum = f'{iSub:02d}'
    dfCond = pd.DataFrame()  # main df with all runs
    if iSub in {9, 12, 16, 26}:
        runs = range(1, 5)  # 4 runs
    else:
        runs = range(1, 4)  # 3 runs
    for iRun in runs:
        condPath = os.path.join(mainDir, 'orig_events', 'sub-' + subNum +
                                '_task-memsamp_run-0' + str(iRun) +'_events.tsv')
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

    # objective function - can i add dat in a different way?
    def runit(params, dat=dat):

        import numpy as np
        if np.any(np.isnan(params)):
            negloglik = np.inf
        else:
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

            # normal distribution
            rv = norm(0, params[2])
        #        rv = vonmises(startparams[2], 0)

            resps1 = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                              (dat['key'] == 1)],
                                     angdiff2[(dat['direction'].isin(catA2)) &
                                              (dat['key'] == 1)],
                                     angdiff1[(dat['direction'].isin(catB1)) &
                                              (dat['key'] == 6)],
                                     angdiff2[(dat['direction'].isin(catB2)) &
                                              (dat['key'] == 6)]))

            resps2 = np.concatenate((angdiff1[(dat['direction'].isin(catA1)) &
                                              (dat['key'] == 6)],
                                     angdiff2[(dat['direction'].isin(catA2)) &
                                              (dat['key'] == 6)],
                                     angdiff1[(dat['direction'].isin(catB1)) &
                                              (dat['key'] == 1)],
                                     angdiff2[(dat['direction'].isin(catB2)) &
                                              (dat['key'] == 1)]))
            if len(params) < 4:
                resps1pr = 1-rv.pdf(resps1)
                resps2pr = rv.pdf(resps2)
            else:  # guess rate
                alpha = params[3]  # guess rate
                resps1pr = alpha * 0.5 + (1-alpha) * (1-rv.pdf(resps1))
                resps2pr = alpha * 0.5 + (1-alpha) * rv.pdf(resps2)

            # sum logpr (to check exp this result, comp w np.prod of pr's)
            negloglik = -np.sum(np.log(
                    np.concatenate((resps1pr, resps2pr))))

        return negloglik

    # ...optimize this with bound1, bound2, and SD .., with sensible limits

#    startparams = [0, 180, 1]  # bound 1, bound 2, and sigma (gaussian SD)
#    startparams = [270, 90, 1]  # bound 1, bound 2, and sigma (gaussian SD)
#    startparams = [270, 90, 1, 0.5] # with guess rate


#    # quick runthrough - without multiple starting point
#    method = ['Nelder-Mead', 'SLSQP', 'L-BFGS-B'][0]
#    res = opt.minimize(runit, startparams, method=method)  #, bounds=bounds)
#    bestparams = res.x

#    # multiple starting point (opt.basinhopping)
#    method = 'Nelder-Mead'
#    minimizer_kwargs = {"method": method}
#    res=opt.basinhopping(runit, startparams, niter=20, stepsize=179.,
#                         minimizer_kwargs=minimizer_kwargs)
#    bestparams = res.x

    # multiple starting point (self)
#    starts = [[0, 180, .5], [270, 90, 1], [45, 225, .5], [135, 315, 2]]
#    bounds = [(None, None), (None, None), (0., 50.)]
    bounds = [(-359, 359), (-359, 359), (0., 50.)]
#    bounds = [(-np.radians(359), np.radians(359)), (-np.radians(359), np.radians(359)), (0., 20.), (0., 1.)]

    # looping through starts
    starts = []
    startsb1 = np.arange(15., 345., 60)
    startsb2 = np.arange(45., 360., 60)-360
#    sds = [.5, 1, 2, 5, 10, 15]
    sds = [.5, 1, 2, 3, 5, 8, 10, 15]

    guess = False
    if guess:
        gs = [.1, .3, .6, .8]
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

#    # use objective bounds ±30 as starting points
#    starts = []
#    bs = [[15., 195.], [105., 285.], [195., 15.], [285., 105.],
#          [45., 225.], [135., 315.], [225., 45.], [315., 135.],
#          [-15., 165.], [75., 255.], [165., -15.], [225., 75.],
#          [-345., -165.], [-255.,  -75.], [-165., -345.], [-75., -255.]]
#    sds = [.5, 1., 2., 3., 5., 8., 10., 15.]

    for b in bs:
        for sd in sds:
            starts.append([b[0], b[1], sd])

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

    # fix negative and over 360 bounds
    while bestparams[0] < 0:
        bestparams[0] += 360
    while bestparams[1] < 0:
        bestparams[1] += 360
    while bestparams[0] > 360:
        bestparams[0] -= 360
    while bestparams[1] > 360:
        bestparams[1] -= 360

    # display results
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

#    print('sub %d bestparams: %s' % (iSub, np.array2string(bestparams)))
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

    # correct, incorrect, corr, inc (most resps should be on the correct side)
    ncorr_inc = [n_cata_resps_side1, n_cata_resps_side2,
                 n_catb_resps_side2, n_catb_resps_side1]
    print(ncorr_inc)

#    # checking how it matches up
#    print('subjCat catA: %s' % subjCat[iSub-1][0])
#    print('subjCat catB: %s' % subjCat[iSub-1][1])

    dfres['bestparams'].loc[iSub-1] = bestparams
    dfres['a'].loc[iSub-1] = catA
    dfres['b'].loc[iSub-1] = catB
    dfres['modelacc'].loc[iSub-1] = ncorr_inc

t1 = time.time()
print(t1-t0)
# %%

## testing activations make sense
#x = np.radians(np.array([30., 60., 120., 150., 180., 210., 240, 270, 300., 330., 0.]))
#bound = np.radians(15)
#bound = np.radians(225)

# computed activation given bound
#mu = 0
#sigma = params[2]
#sigma = 0.1
#rv = norm(mu, sigma)
#plt.plot(1-rv.pdf(angdiff(x,bound)))
#plt.ylim((0, 1))

#from scipy.stats import vonmises
#mu = 0
#kappa = 1
#rv = vonmises(kappa, mu)
#plt.plot(1-rv.pdf(angdiff(x,bound)))  # 1-pr

