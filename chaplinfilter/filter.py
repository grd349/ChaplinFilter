#!/usr/bin/env python3
# -*-  coding: utf-8 -*-

"""
Created on Friday 13 July 2018

@author: Guy R. Davies
"""

import numpy as np
import pandas as pd
import os
from . import PACKAGEDIR

class filter():
    '''A class to manage the training and prediction of filter timescales
    from the Chaplin et al in prep paper.

    The class takes the reference data and trains a random forest in order to
    make new predictions.

    Inputs to the call function should be array-like and all three inputs
    should be off the same length.

    The three inputs are effective temperature (K), log g (dex), and
    luminosity ($L_{\odot}$).

    Arguments
    ---------
    Teff: array_like; size [N]
        An array of stellar effective temperatures in Kelvin.

    logg: array_like; size [N]
        An array of log g's in dex.

    L: array_like; size [N]
        An array of luminosities in units of solar luminosity.

    Returns
    -------
    result: numpy array size [N, 2]
        A 2D array containing tp1 and tpE for each star.  See Chaplin et al.
        for full details of what tp1 and tpE are. (TODO - polish)

    Example
    -------

    Import together with numpy

        from chaplinfilter import filter

        import numpy as np

    Make some basic data

        nstars = 10

        teff = np.random.rand(nstars) * 500 + 5000

        logg = np.random.rand(nstars) *1.0 + 3.5

        L = np.random.rand(nstars) * 2.0 + 1.0

    Setup the filter and run train

        f = filter(verbose=True)

    Use the trained random forest to predict the new filter timescales.

        results = f(teff, logg, L)

        print(results)

    '''
    def __init__(self, verbose=False):
        self.data_file = PACKAGEDIR + os.sep + 'data' + os.sep + 'jitterdata_box4_110818.txt'
        try:
            from sklearn.ensemble import RandomForestRegressor
        except Exception as e:
            raise
        self.df = []
        self.labels = ['Teff', 'logg', 'L']
        self.ylables = ['tpE', 'tp1']
        self.n_estimators = 400
        self.max_depth = 20
        self.random_state = 53
        self.oob_score = True
        self.regr = []
        self.verbose = verbose

    def read_train_data(self):
        '''Reads in the data to train on from the data file.
        '''
        if self.verbose:
            print(f'Reading file: {self.data_file}')
        self.df = pd.read_csv(self.data_file, sep='\s+')

    def train(self):
        '''Trains the random forest on the train data (all the train data).
        '''
        if len(self.df) < 1:
            self.read_train_data()
        X = self.df[self.labels].values
        y = self.df[self.ylables].values
        from sklearn.ensemble import RandomForestRegressor
        self.regr = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=self.random_state,
            oob_score=self.oob_score,
            criterion='mae',
        )
        self.regr.fit(X, y)
        if self.verbose:
            print(f'OOB Score: {self.regr.oob_score_}')
        if self.regr.oob_score_ < 0.98:
            print('Unusually low OOB Score - investigate')

    def __call__(self, Teff, logg, L):
        ''' TODO call '''
        if self.regr == []:
            if self.verbose:
                print('Training ...')
            self.train()
        X = np.column_stack([Teff, logg, L])
        if self.verbose:
            print('Predicting ...')
        return np.array(self.regr.predict(X))

if __name__ == "__main__":
    from chaplinfilter import filter
    f = filter(verbose=True)
    f.read_train_data()
    results = f(f.df.Teff, f.df.logg, f.df.L)
    print(results[:,0].shape)
    print(f.df.tpE.values.shape)
    print(results[:,0] - f.df.tpE.values)
