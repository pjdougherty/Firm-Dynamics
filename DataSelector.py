# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 11:43:36 2015

@author: pdougherty

This script is designed to select sales and employment figures from a dataframe of NETS data. It includes relevant header names in col_names.

getMDData() is designed to select sales and employment figures for firms during the time that they are located in the State of Maryland.
sumMDData() generates two data frames, one for employment and one for sales, with aggregated Maryland data, organized by year. The column containing year values is in datetime format.
"""
import pandas as pd
import numpy as np

def col_names():
    '''
    Returns a list of column names for the standard NETS database and for the NETS database joined with the NETS relocation database.
    '''
    col_names = pd.read_csv(r'G:\Publications\2015\Regional Clustering\NETS2012_MD_EAGB.txt', nrows=1, delimiter='\t')
    col_names = list(col_names.columns)
    # Turn this on ONLY when an EAGB industry has been assigned to each company
    col_names.append('EAGBIndustry')
    move_col_names = 'DunsNumber	MoveYear	Company	TradeName	MoveSIC	OriginCity	OriginState	OriginZIP	OriginFIPSCounty	OriginCounty	DestCity	DestState	DestZIP	DestFIPSCounty	DestCounty	MoveEmp	EmpC	MoveSales	MoveSalesC	MoveOften	Active	SizeCat	EstCat	Subsidiary	OriginLatitude	OriginLongitude	OriginLevelCode	DestLatitude	DestLongitude	DestLevelCode	Distance'
    move_col_names = move_col_names.split('\t')
    move_col_names = list(move_col_names)
    for i in range(0, len(move_col_names)):
        move_col_names[i] = move_col_names[i] + '_r'
        
    return col_names, move_col_names

def getMDData(g):
    '''
    getMDData() is designed to select sales and employment figures for firms during the time that they are located in the State of Maryland.
    
    parameters:
        - g: data frame from NETS database with column headers
    '''
    emp_dict = {k:[] for k in range(1990,2013)}
    sales_dict = {k:[] for k in range(1990,2013)}
    
    first00 = int(sum(emp_dict[2000]))

    for i, estab in g.iterrows():
        if np.isnan(g['LastMove'][i]) and g['State_First'][i]=='MD':
            for k in emp_dict.keys():
                emp_dict[k].append(g['{}'.format('Emp'+str(k)[2:4])][i])
            for k in sales_dict.keys():
                sales_dict[k].append(g['{}'.format('Sales'+str(k)[2:4])][i])
        else:
            if g['State_First'][i] == 'MD' and g['DestState'][i]=='MD':
                for k in emp_dict.keys():
                    emp_dict[k].append(g['{}'.format('Emp'+str(k)[2:4])][i])
                for k in sales_dict.keys():
                    sales_dict[k].append(g['{}'.format('Sales'+str(k)[2:4])][i])
            else:
                year = g['LastMove'][i]
                if g['State_First'][i] == 'MD':
                    emp_years = range(1990,int(year+1))
                    sales_years = range(1990,int(year+1))
                    for k in emp_years:
                        emp_dict[k].append(g['{}'.format('Emp'+str(k)[2:4])][i])
                    for k in sales_years:
                        sales_dict[k].append(g['{}'.format('Sales'+str(k)[2:4])][i])
                elif g['DestState'][i]=='MD':
                    emp_years = range(int(year),2013)
                    sales_years = range(int(year),2013)
                    for k in emp_years:
                        emp_dict[k].append(g['{}'.format('Emp'+str(k)[2:4])][i])
                    for k in sales_years:
                        sales_dict[k].append(g['{}'.format('Sales'+str(k)[2:4])][i])
                        
    last00 = int(sum(emp_dict[2000]))
    
    if first00==last00:
        print 'There seems to be an issue. No new data was added to the dataframe - unless nobody in Maryland was employed in this industry in 2000.'
    
    return emp_dict, sales_dict

def sumMDData(emp_dict, sales_dict):
    '''
    sumMDData() generates two data frames, one for employment and one for sales, with aggregated Maryland data, organized by year. The column containing year values is in datetime format.
    
    parameters:
        - emp_dict: dictionary of employment valeus for Maryland companies organized by year. Keys must be integers.
        - sales_dict: dictionary of employment valeus for Maryland companies organized by year. Keys must be integers.
    '''
    e={}
    s={}
    for k in emp_dict.keys():
        e[k] = float(sum(emp_dict[k]))
    for k in sales_dict.keys():
        s[k] = [n for n in sales_dict[k] if np.isnan(n)==False]
        s[k] = float(sum(s[k]))
        
    e = pd.DataFrame(e, index=[0]).T.reset_index().rename(columns={'index':'year', 0:'employment'})
    e['year'] = pd.to_datetime(e.year, format='%Y')
    s = pd.DataFrame(s, index=[0]).T.reset_index().rename(columns={'index':'year', 0:'sales'})
    s['year'] = pd.to_datetime(s.year, format='%Y')

    return e, s