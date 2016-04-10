# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 14:19:54 2016

@author: Julian
"""

import pymongo
import pycountry
import pandas as pd

db_name = 'db_tourist'   
dbclient=pymongo.MongoClient('mongodb://mids:1X49ilWN@198.23.108.210:27017/' + db_name)   
db = dbclient['tripadvisor']
db_g = dbclient['db_tourist']

country_coll = db.finalAttrRatings
gdelt_coll = db_g.db_gdelt_preds
curr_coll = db_g.curr_preds

working = pd.DataFrame(list(country_coll.find()))

working = working.drop(['_id','rate_7','rate_curr','rate_90','rate_30','curr_week_pct_4','pred_1_month',
                        'pred_1_week','pred_3_months','currency','price'],1)
                        
working = working.set_index('country_code')

#create lookup to go from 2 to 3 digits
country_lookup = []
for country in pycountry.countries:
    country_lookup.append([country.alpha2, country.alpha3])


#we have different codes for two countries    
country_lookup = pd.DataFrame(country_lookup, columns = ['country_code', 'country_code_3'])
rom_lu = country_lookup.loc[country_lookup['country_code_3'] == 'ROU'].index.values[0]
et_lu = country_lookup.loc[country_lookup['country_code_3'] == 'TLS'].index.values[0]

country_lookup.ix[et_lu,'country_code_3'] = 'TMP'
country_lookup.ix[rom_lu,'country_code_3'] = 'ROM'


country_lookup = country_lookup.set_index('country_code')

working = pd.concat([working,country_lookup],join ='inner', axis=1)
working = working.reset_index()
working = working.set_index('country_code_3')

gdelt = pd.DataFrame(list(gdelt_coll.find()))
gdelt =gdelt.drop(['_id'],1)
gdelt = gdelt.set_index('country')
gdelt.index.names =['country_code']

curr = pd.DataFrame(list(curr_coll.find()))
curr = curr.drop(['_id','country_x','date','index'],1)
curr = curr.set_index('country_code')

finaljson = pd.concat([working,gdelt,curr],join ='inner', axis=1)
finaljson.index.name ='country_code_3'
finaljson = finaljson.reset_index()

finaljson.to_json('C:/Users/Julian/Documents/W210/data/finaljson.json', orient = 'records')