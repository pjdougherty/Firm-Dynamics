# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 09:13:45 2015

@author: pdougherty

These functions will calculate the change in sales and employment from the previous year
and from the first year an establishment opened until the year in which it moved or,
if it never relocated, the most recent year.
"""

import pandas as pd
import numpy as np

col_names = pd.read_csv(r'G:\Publications\2015\Regional Clustering\NETS2012_MD_EAGB.txt', nrows=1, delimiter='\t')
col_names = list(col_names.columns)
# Turn this on ONLY when an EAGB industry has been assigned to each company
col_names.append('EAGBIndustry')
move_col_names = 'DunsNumber	MoveYear	Company	TradeName	MoveSIC	OriginCity	OriginState	OriginZIP	OriginFIPSCounty	OriginCounty	DestCity	DestState	DestZIP	DestFIPSCounty	DestCounty	MoveEmp	EmpC	MoveSales	MoveSalesC	MoveOften	Active	SizeCat	EstCat	Subsidiary	OriginLatitude	OriginLongitude	OriginLevelCode	DestLatitude	DestLongitude	DestLevelCode	Distance'
move_col_names = move_col_names.split('\t')
move_col_names = list(move_col_names)
for i in range(0, len(move_col_names)):
    move_col_names[i] = move_col_names[i] + '_r'

all_col_names = col_names+move_col_names

def oneYearChange(df):
    one_year_change_emp = []
    one_year_change_sales = []
    
    for i, estab in df.iterrows():
        # If the establishment never moved, calculate its most recent one-year
        # growth in employment and sales
        if np.isnan(df['LastMove'][i])==True:
            if df['LastYear'][i] <= 1990:
                emp_ch = np.nan
                one_year_change_emp.append(emp_ch)
                sales_ch = np.nan
                one_year_change_sales.append(sales_ch)
            else:
                # Employment
                new_emp = 'Emp' + str(df['LastYear'][i])[2:4]
                old_emp = 'Emp' + str(df['LastYear'][i]-1)[2:4]
                
                emp_ch = (df['%s' % new_emp][i]-df['%s' % old_emp][i])/df['%s' % old_emp][i].astype(float)
                
                one_year_change_emp.append(emp_ch)
                
                # Sales
                new_sales = 'Sales' + str(df['LastYear'][i])[2:4]
                old_sales = 'Sales' + str(df['LastYear'][i]-1)[2:4]
                
                sales_ch = (df['%s' % new_sales][i]-df['%s' % old_sales][i])/df['%s' % old_sales][i].astype(float)
                
                one_year_change_sales.append(sales_ch)
        # If the establishment did move, calculate the one-year growth in employment
        # and sales in the year leading up to the relocation
        else:
            if df['LastMove'][i] <= 1990:
                emp_ch = np.nan
                one_year_change_emp.append(emp_ch)
                sales_ch = np.nan
                one_year_change_sales.append(sales_ch)
            else:
                # Employment
                new_emp = 'Emp' + str(df['LastMove'][i])[2:4]
                old_emp = 'Emp' + str(df['LastMove'][i]-1)[2:4]
                
                emp_ch = (df['%s' % new_emp][i]-df['%s' % old_emp][i])/df['%s' % old_emp][i].astype(float)
                
                one_year_change_emp.append(emp_ch)
                
                # Sales
                new_sales = 'Sales' + str(df['LastMove'][i])[2:4]
                old_sales = 'Sales' + str(df['LastMove'][i]-1)[2:4]
                
                sales_ch = (df['%s' % new_sales][i]-df['%s' % old_sales][i])/df['%s' % old_sales][i].astype(float)
                
                one_year_change_sales.append(sales_ch)
    
    # Create dataframes from list of growth rates
    one_ch = pd.DataFrame(zip(one_year_change_emp, one_year_change_sales), columns=['pctCh_oneyear_Emp', 'pctCh_oneyear_Sales'])
    one_ch.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    return one_ch
    
def changeSinceOpen(df):
    change_since_open_emp = []
    change_since_open_sales = []
    
    for i, estab in df.iterrows():
        # If the establishment has never relocated, calculate employment and sales
        # growth since  they opened
        if np.isnan(df['LastMove'][i]) == True:
            if df['LastYear'][i] <= 1990:
                emp_ch = np.nan
                change_since_open_emp.append(emp_ch)
                sales_ch = np.nan
                change_since_open_sales.append(sales_ch)
            elif df['FirstYear'][i] < 1990:
                emp_ch = np.nan
                change_since_open_emp.append(emp_ch)
                sales_ch = np.nan
                change_since_open_sales.append(sales_ch)
            else:
                # Employment
                new_emp = 'Emp' + str(df['LastYear'][i])[2:4]
                old_emp = 'Emp' + str(df['FirstYear'][i]+1)[2:4]
            
                emp_ch = (df['%s' % new_emp][i]-df['%s' % old_emp][i])/df['%s' % old_emp][i].astype(float)
            
                change_since_open_emp.append(emp_ch)
                
                # Sales
                new_sales = 'Sales' + str(df['LastYear'][i])[2:4]
                old_sales = 'Sales' + str(df['FirstYear'][i]+1)[2:4]
            
                sales_ch = (df['%s' % new_sales][i]-df['%s' % old_sales][i])/df['%s' % old_sales][i].astype(float)
            
                change_since_open_sales.append(sales_ch)
        # If the establishment did move, calculate employment and sales growth
        # from the time they opened until the time of their last move
        else:
            if df['LastMove'][i] <= 1990:
                emp_ch = np.nan
                change_since_open_emp.append(emp_ch)
                sales_ch = np.nan
                change_since_open_sales.append(sales_ch)
            elif df['FirstYear'][i] < 1990:
                emp_ch = np.nan
                change_since_open_emp.append(emp_ch)
                sales_ch = np.nan
                change_since_open_sales.append(sales_ch)
            else:
                # Employment
                new_emp = 'Emp' + str(df['LastMove'][i])[2:4]
                old_emp = 'Emp' + str(df['FirstYear'][i]+1)[2:4]
                
                emp_ch = (df['%s' % new_emp][i]-df['%s' % old_emp][i])/df['%s' % old_emp][i].astype(float)
                
                change_since_open_emp.append(emp_ch)
                
                # Sales
                new_sales = 'Sales' + str(df['LastMove'][i])[2:4]
                old_sales = 'Sales' + str(df['FirstYear'][i]+1)[2:4]
                
                sales_ch = (df['%s' % new_sales][i]-df['%s' % old_sales][i])/df['%s' % old_sales][i].astype(float)
                
                change_since_open_sales.append(sales_ch)
            
    # Create dataframes from list of growth rates
    since_open = pd.DataFrame(zip(change_since_open_emp, change_since_open_sales), columns=['pctCh_sinceopen_Emp', 'pctCh_sinceopen_Sales'])
    #since_open.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    return since_open
    
def getGrowth(df):
    try:
        pct_change_one_year = oneYearChange(df)
        df = df.join(pct_change_one_year)
    except:
        print 'One year growth rates were not calculated, or the dataframe was not joined.'
        
    try:
        pct_change_since_open = changeSinceOpen(df)
        df = df.join(pct_change_since_open)
    except:
        print 'Growth rates since establishment opening were not calculated, or the dataframe was not joined.'
        
    return df