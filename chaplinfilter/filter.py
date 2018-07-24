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
    ''' TODO main doc '''
    def __init__(self, verbose=False):
        ''' TODO init '''
        self.data_file = PACKAGEDIR + os.sep + 'data' + os.sep + 'jitterdata_box4.txt'
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
        self.verbose=verbose

    def read_train_data(self):
        ''' TODO read data
        '''
        if self.verbose:
            print(f'Reading file: {self.data_file}')
        self.df = pd.read_csv(self.data_file, sep='\s+')

    def train(self):
        ''' TODO train '''
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
        if self.regr.oob_score < 0.98:
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
