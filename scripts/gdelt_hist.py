# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 10:55:32 2016

@author: Julian
"""
import pymongo
import pandas as pd
import numpy as np
import pycountry

#helper function
def percents(item, role, sumtype, quadclass='4'):
    denom = 0
    for i in range(1, 5):
        denom += int(item[role][0][str(i)][sumtype])
    if denom == 0:
        return 100.0
    else:
        return 100.0-(100.0*int(item[role][0][quadclass][sumtype])/denom)

def df_ret(coll):
    
    
    #find all dates
    dates = coll.find().distinct("week")
    dates = sorted(dates,reverse=True)
    
    #select the dates necessary
    #taking last year plus extra to allow for rolling avg
    weekdates=dates[:55]
    
    
    
  
    safetydata = []
    items = gdelt_coll.find({"country" : {"$in" :countries},"week" : {"$in" :weekdates}})
    for item in items:
        date = item['week']
        country = item['country']
        pct_quad_4=(percents(item, 'Target', 'SumNumMentions'))
        safetydata.append([date,country,pct_quad_4])
                                 
    df = pd.DataFrame(safetydata, columns=['date','country','pct_quad_4'])


    start = True
    for c in countries:
        sub_df = df[df['country']==c]
    
        #3 month rolling avg of percent
        sub_df.insert(3, 'roll_pct',pd.rolling_mean(sub_df['pct_quad_4'], window=3))
        
        if start == True:
            perc_df = sub_df
            start = False
        else:
            perc_df = pd.concat([perc_df, sub_df])           
      
    #drop rows that are NA, these were used for rolling pct calc
    perc_df = perc_df.dropna()
    #drop pct_quad_4 col as the one to be graphed is the rolling pct 
    perc_df = perc_df.drop('pct_quad_4',1)
            
    return perc_df



countries = ["AFG","AGO","ALB","ARE","ARG","ARM","ATG","AUS","AUT","AZE","BDI","BEL","BEN","BFA","BGD","BGR","BHR","BHS","BLR",
             "BLZ","BMU","BOL","BRA","BRB","BRN","BTN","BWA","CAF","CAN","CHE","CHL","CHN","CIV","CMR","COD","COG","COL","COM",
             "CRI","CUB","CYP","CZE","DEU","DJI","DNK","DOM","DZA","ECU","EGY","ERI","ESP","EST","ETH","FIN","FJI","FRA","FSM",
             "GAB","GBR","GEO","GHA","GIN","GMB","GNB","GNQ","GRC","GRD","GTM","GUY","HND","HRV","HTI","HUN","IDN","IND","IRL",
             "IRN","IRQ","ISL","ISR","ITA","JAM","JOR","JPN","KAZ","KEN","KGZ","KHM","KNA","KOR","KWT","LAO","LBN","LBR","LBY",
             "LCA","LIE","LKA","LSO","LTU","LUX","LVA","MAR","MCO","MDA","MDG","MDV","MEX","MKD","MLI","MLT","MMR","MNG","MOZ",
             "MRT","MWI","MYS","NAM","NER","NGA","NIC","NLD","NOR","NPL","NZL","OMN","PAK","PAN","PER","PHL","PNG","POL","PRK",
             "PRT","PRY","QAT","ROM","RUS","RWA","SAU","SDN","SEN","SGP","SLE","SLV","SOM","SRB","SUR","SVK","SWE","SWZ",
             "SYR","TCD","TGO","THA","TJK","TKM","TMP","TTO","TUN","TUR","TWN","TZA","UGA","UKR","URY","UZB","VAT","VEN",
             "VNM","YEM","ZAF","ZMB","ZWE"]
             

db_name = 'db_tourist'   
dbclient=pymongo.MongoClient('mongodb://mids:1X49ilWN@198.23.108.210:27017/' + db_name)   
db = dbclient['db_tourist']
gdelt_coll = db.db_gdelt

gdelt_hist = df_ret(gdelt_coll)

#create lookup to go from 2 to 3 digits

country_info = []
for country in pycountry.countries:
    country_info.append([country.name,country.alpha2,country.alpha3])
country_info = pd.DataFrame(country_info,columns=['Name','Iso2','country'])


#we have different codes for two countries   

rom_lu = country_info.loc[country_info['country'] == 'ROU'].index.values[0]
et_lu = country_info.loc[country_info['country'] == 'TLS'].index.values[0]

country_info.ix[et_lu,'country_code_3'] = 'TMP'
country_info.ix[rom_lu,'country_code_3'] = 'ROM'

country_info = country_info.set_index('country')

#merge, rename and take columns that we want.
gdelt_hist = gdelt_hist.merge(country_info,on='country')
gdelt_hist = gdelt_hist[[u'date', u'Iso2', u'roll_pct', u'Name']]
gdelt_hist.columns = [u'date', u'country_code', u'roll_pct', u'Name']

#find median and append
gdelt_hist.head()

dates = gdelt_hist.date.unique()

med_vals = []
for d in dates:
    df = gdelt_hist
    sub_df = df[df['date']==d]
    mv = sub_df['roll_pct'].median()
    med_vals.append([d, 'Med', mv, 'Median' ])

meds = pd.DataFrame(med_vals, columns = ['date','country_code','roll_pct','Name'])

gdelt_hist = pd.concat([gdelt_hist,meds])

gdelt_hist.to_json('C:/Users/Julian/Documents/W210/data/gdelt_hist.json',orient='records',  date_unit = 's')

