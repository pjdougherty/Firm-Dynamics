# -*- coding: utf-8 -*-
"""
Created on Wed Sep 02 16:58:34 2015

@author: pdougherty

This script selects employment and sales data from a read-in NETS data or other dataframe with this structure:

 Emp01 | Emp02 | Emp03 | ... | Sales01 | Sales02 | Sales03 | ...
-------+-------+-------+ ... +---------+---------+---------+ ...
 100   | 150   | 155   | ... | 10000   | 15000   | 15000   | ...
 
Company information is left out, and can be added to data = {} dictionary constructors if needed.

May be useful to combine this with a latitude and longitude selector so that coordinated only for companies in Maryland are selected. At the same time, it's possible that companies without OriginState or DestState records of "MD" but exist in Maryland would be omitted.

Useful for plotting sales and employment over time in a given industry.
"""

import pandas as pd
import numpy as np

# Get only companies in Maryland at the time
def selectData(df, year):
    '''
    parameters:
        - df: dataframe to have information pulled from. Typically an dataframe with information from one industry.
        - year: the year for the coordinates to represent. Point representation changes with relocations, openings, and closings.
    '''
    
    data_dict = {}

    for i, estab in df.iterrows():
        if df['FirstYear'][i] <= year and df["LastYear"][i] >= year:
            # If company started in MD and never moved
            if df['OriginState'][i] == 'MD' and np.isnan(df['LastMove'][i]):
                data = {'employment':df['{}'.format('Emp'+str(year)[2:4])][i],
                             'sales':df['{}'.format('Sales'+str(year)[2:4])][i],
                             'year':year}
                data_dict['co'+str(i)] = data
            # If company started in MD and moved after the passed year
            elif df['OriginState'][i] == 'MD' and df['LastMove'][i] >= year:
                data = {'employment':df['{}'.format('Emp'+str(year)[2:4])][i],
                             'sales':df['{}'.format('Sales'+str(year)[2:4])][i],
                             'year':year}
                data_dict['co'+str(i)] = data
            # If the company moved after the passed year and ended up in Maryland
            elif df['LastMove'][i] < year and df['DestState'][i] == 'MD':
                data = {'employment':df['{}'.format('Emp'+str(year)[2:4])][i],
                             'sales':df['{}'.format('Sales'+str(year)[2:4])][i],
                             'year':year}
                data_dict['co'+str(i)] = data
            else:
                pass
                
    df = pd.DataFrame(data_dict).T.reset_index(drop=True)
    
    return df

# Get employment and sales for all years
def allData(df, first_year, last_year):
    '''
    parameters:
        - df:dataframe to have information pulled from. Typically an dataframe with information from one industry.
        - first_year: the first year of data to be represented. Must be 1990 or later.
        - last_year: the most recent year of data to be represented. Must be 2012 or earlier.
    '''
    if first_year >= 1990 and last_year <= 2013:
        pass
    elif first_year < 1990:
        print 'First year must be 1990 or later.'
    elif last_year > 2013:
        print 'Last year must be 2013 or earlier. Data is available through 2012.'
    else:
        pass
    
    dfs = []
    for y in range(first_year, last_year):
        d = selectData(df, y)
        dfs.append(d)
        
    data_df = pd.concat([frame for frame in dfs])
    
    return data_df