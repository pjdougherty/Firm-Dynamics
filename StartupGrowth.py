# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 09:51:49 2015

@author: pdougherty

This function calculates the elapsed time between when a firm launched and when it reached at least $1M in revenue, if it ever has. Firms that have never made at least $1M in revenue are ignored. It will print the mean and median elapsed time to go from startup to second stage, and return a dataframe of anonymized, paired dates.
"""

import pandas as pd
import numpy as np

def StartupGrowthRate(df, balt = True):
    '''
    Calculates the mean and median number of years between when a firm opened and when it reached at least $1M in revenue, if ever
    Returns dataframe of anonymized start years and first years of at least $1M in revenue.
    Parameters:
        - df: dataframe of establishments to analyze
        - balt: if balt==True, the dataframe will be pared down to firms that are currently in Greater Baltimore. If False, the calculation will take place on whatever dataframe is passed. 
    '''
    if balt == True:
        ix = np.in1d(df.FipsCounty.ravel(), [24003,24005,24510,24013,24015,24025,24027,24035]).reshape(df.FipsCounty.shape)
        df['GB'] = np.where(ix, True, False)
        df = df[df.GB==True].reset_index(drop=True)

    firstyear = {k:v for (k, v) in zip(df.index.tolist(), (int(y) for y in df.FirstYear.values.tolist()))}

    second_stage = {}
    for i, estab in df.iterrows():
        for year in range(1990, 2013):
            if df['Sales'+str(year)[2:4]][i] >= 1000000:
                second_stage[i] = year
                break
        
    fy = pd.DataFrame(firstyear.items(), columns=['key', 'firstyear'])
    ss = pd.DataFrame(second_stage.items(), columns=['key', 'second_stage'])

    comb = ss.join(fy, on='key', rsuffix='_r')
    comb.drop('key_r', axis=1, inplace=True)

    comb['elapsed_time'] = comb.second_stage - comb.firstyear

    print 'Greater Baltimore firms in this industry that reach a second stage take an average of {mean} years to do so (median {median} years).'.format(mean=comb['elapsed_time'].mean(), median=comb['elapsed_time'].median())
    
    return comb
