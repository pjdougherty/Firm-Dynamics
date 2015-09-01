# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 12:37:52 2015

@author: pdougherty

Returns the D&B Rating and Maximum D&B PayDex score for each establishment in a dataframe
for the year in which that establishment relocated. If the establishment has never relocated,
the most recent values will be returned.
"""

import pandas as pd
import numpy as np

def DBCreditScore(df):
    DnB = []
    PayDex = []
    
    for i, estab in df.iterrows():
        # If the establishment has never relocated, use the D&B Rating from its
        # last year in existence
        if np.isnan(df['LastMove'][i]) == True:
            rating_selector = 'DnBRating' + str(df['LastYear'][i])[2:4]
            paydex_selector = 'PayDexMax' + str(df['LastYear'][i])[2:4]
        # If the establishment has relocated, use the D&B Rating from the year
        # it moved
        else:
            rating_selector = 'DnBRating' + str(df['LastMove'][i])[2:4]
            paydex_selector = 'PayDexMax' + str(df['LastMove'][i])[2:4]
            
        DnB.append(df['%s' % rating_selector][i])
        PayDex.append(df['%s' % paydex_selector][i])
        
        db_rating = pd.DataFrame(zip(DnB, PayDex), columns=['MoveDnBRating', 'MovePayDexMax'])
        
        db_rating['MoveDnBRating'] = np.where(db_rating.MoveDnBRating=='-- ', np.nan, db_rating.MoveDnBRating)
        
    return db_rating

def getCreditScore(df):
    try:
        df = df.join(DBCreditScore(df))
    except:
        print 'Dunn & Bradstreet credit scores were not joined to the original dataframe.'
        
    return df