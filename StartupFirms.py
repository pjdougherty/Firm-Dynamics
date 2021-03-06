# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:14:50 2015

@author: pdougherty
"""

'''
Plots the number and percentage of firms in a state that are of a given age.
Currently only works as intended at the top and bottom ends of the spectrum:
firms less than 1 and firms older than 26. More work needs to be done to plot
firms between 0 and 5 years old, for example, though the infrastructure is in
place. Also, need to add in 0s for years that have no data in order to
effectively plot older firms, which don't show up until the 2000s.
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

state_data = pd.read_csv(r'G:\Publications\Annual Regional Report\2015\Startup Rate\bds_f_agest_release.csv')
metro_data = pd.read_csv(r'G:\Publications\Annual Regional Report\2015\Startup Rate\bds_f_agemsa_release.csv')
us_data = pd.read_csv(r'G:\Publications\Annual Regional Report\2015\Startup Rate\bds_f_age_release.csv')

def transformDataFrame(df):
    df.rename(columns={'year2':'year', 'fage4':'fage'}, inplace=True)
    if 'msa' in list(df.columns.values):
        df.rename(columns={'msa':'state'}, inplace=True)
    df['fage'] = '('+df.fage
    df['fage'] = df['fage'].str.replace('(.*) ', '')
    df['fage'] = df['fage'].str.replace('+', '')
    df['fage'] = df['fage'].str.replace('Censored', '99')
    df['fage'] = df['fage'].astype(int)
    
def plotNumberFirms(geo, firm_age, FIPS=12580, fignum=1, size=1):
    if geo=='state':
        df = state_data
    elif geo=='metro':
        df = metro_data
    elif geo=='national':
        df = us_data
        
    FIPS_dict = {06:'California', 24:'Maryland', 42:'Pennsylvania', 51:'Virginia',
                 25:'Massachusetts', 48:'Texas', 36:'New York', 12580:'Baltimore', 14460:'Boston',
                 41740:'San Diego', 41860:'San Francisco', 35620:'New York',
                 37980:'Philadelphia', 38300:'Pittsburgh', 47900:'Washington, DC'}
        
    if (geo=='metro') or (geo=='state'):
        plt.plot(df.year.unique(), df[df.state==FIPS][df.fage < firm_age].groupby('year').Firms.sum(), lw=size, label=FIPS_dict[FIPS]+', Firms < %s' % firm_age)
    elif geo=='national':
        plt.plot(df.year.unique(), df[df.fage < firm_age].groupby('year').Firms.sum(), lw=size, label='US, Firms < %s' % firm_age)
    plt.xlabel('Year')
    plt.legend(loc=0)
    if (firm_age > 99):
        plt.title('Total Number of Firms')
    elif (firm_age > 26 and firm_age <= 99):
        plt.title('Total Number of Firms Whose Age is Not Censored')
    else:
        plt.title('Number of Firms Less than %s Years Old' % firm_age)
        
def calcPercentByAge(geo, firm_age, FIPS=12580):
    if geo=='state':
        df = state_data
    elif geo=='metro':
        df = metro_data
    elif geo=='national':
        df = us_data
    if (geo == 'state') or (geo=='metro'):
        f = zip(df[df.state==FIPS][df.fage < firm_age].groupby('year').Firms.sum(), df[df.state==FIPS].groupby('year').Firms.sum())
        f = pd.DataFrame(f, columns=('FirmsWithinAge', 'AllFirms'))    
    elif geo=='national':
        f= zip(df[df.fage < 1].groupby('year').Firms.sum(), df.groupby('year').Firms.sum())
        f = pd.DataFrame(f, columns=('FirmsWithinAge', 'AllFirms'))
        
    years = pd.DataFrame(df.year.unique())
    years.rename(columns={0:'year'}, inplace=True)
    
    df2 = f.join(years)
    df2['pct_age'] = (df2['FirmsWithinAge']/df2['AllFirms'])*100
    return df2
    
def plotPercentByAge(geo, firm_age, FIPS=12580, fignum=1, size=1, SAVE=False):
    FIPS_dict = {06:'California', 24:'Maryland', 42:'Pennsylvania', 51:'Virginia',
                 25:'Massachusetts', 48:'Texas', 36:'New York', 12580:'Baltimore', 14460:'Boston',
                 41740:'San Diego', 41860:'San Francisco', 35620:'New York',
                 37980:'Philadelphia', 38300:'Pittsburgh', 47900:'Washington, DC'}
    if (geo=='state') or (geo=='metro'):
        plt.plot(calcPercentByAge(geo, firm_age, FIPS).year, calcPercentByAge(geo, firm_age, FIPS).pct_age, lw=size, label=FIPS_dict[FIPS]+', Firms < %s' % firm_age)
    elif geo=='national':
        plt.plot(calcPercentByAge(geo, firm_age, FIPS).year, calcPercentByAge(geo, firm_age, FIPS).pct_age, lw=size, label='US, Firms < %s' % firm_age)
    plt.legend(loc=0)
    plt.xlabel('Year')
    plt.ylabel('Percent')
    if (firm_age > 99):
        plt.title('Share of All Firms')
    elif (firm_age > 26 and firm_age <= 99):
        plt.title('Share of Firms Whose Age is Not Censored')
    else:
        plt.title('Share of Firms Less than %(1)s %(2)s Old' % {'1':firm_age, '2':np.where(firm_age==1, 'Year', 'Years')})
        
    if SAVE == True:
        if (geo=='state') or (geo=='metro'):
            plt.savefig(r'G:\Publications\Annual Regional Report\2015\%(1)s_Share of Firm Less Than %(2)s.png' % {'1':FIPS_dict[FIPS], '2':firm_age}, alpha=True, dpi=600)
        elif geo=='national':
            plt.savefig(r'G:\Publications\Annual Regional Report\2015\US_Share of Firms Less Than %s.png' % firm_age, alpha=True, dpi=600)

transformDataFrame(metro_data)
transformDataFrame(state_data)
transformDataFrame(us_data)

''' Create dataframe of all of a geography's startups and startup rate
in a year given by parameter'''

def comparisonAll(geo, Year, save=False):
    if geo=='state':
        df = state_data
    elif geo=='metro':
        df = metro_data
    
    f = zip(df[df.year==Year][df.fage==0].state,
            df[df.year==Year][df.fage==0].Firms,  
            df[df.year==Year].groupby('state').Firms.sum())
    
    f = pd.DataFrame(f, columns=('state','startups','firms'))
    f['pct_startups'] = f['startups']/f['firms']
    
    if save==True:
        f.to_excel(r'G:\Publications\Annual Regional Report\2015\startup rate_all %(1)s_%(2)s.xlsx' %{'1':str(geo), '2':str(Year)}, sheet_name=str(Year))
    
    return f