# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 16:37:24 2016

@author: Julian
"""
import pymongo
import pandas as pd
import datetime
from scipy import stats
from numpy import mean
import datetime
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import ast


def pymongo_conn():
    db_name = 'db_tourist'   
    dbclient=pymongo.MongoClient('mongodb://mids:1X49ilWN@198.23.108.210:27017/' + db_name)   
    db = dbclient['db_tourist']
    return db.db_gdelt

#get all eligible dates since 2006
def get_dates(coll):
    dates = coll.find().distinct("week")
    dates = sorted(dates,reverse=True)
    
    #add extra days because of rolling average calculated at the end
    endindex = dates.index(datetime.datetime(2006, 1, 2, 0, 0)) +10 
    return dates[:endindex]

#puts them in groups of 7
def date_sets(dates):  
    weekdates =[]
    monthdates =[]
    quarterdates = []
    
    for i, date in  enumerate(dates):
        #break once start date gets into 2006.  below is the last date for 2006
        if date == datetime.datetime(2006, 12, 25, 0, 0):
            break
        weekdates.append([dates[i], dates[i+1], dates[i+2], dates[i+3], dates[i+4], dates[i+5], dates[i+6]])
        monthdates.append([dates[i], dates[i+1*4], dates[i+2*4], dates[i+3*4], dates[i+4*4], dates[i+5*4], dates[i+6*4]])
        quarterdates.append([dates[i], dates[i+1*13], dates[i+2*13], dates[i+3*13], dates[i+4*13], dates[i+5*13], dates[i+6*13]])
        
    return weekdates, monthdates, quarterdates
      
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
#helper function
def percents(item, role, sumtype, quadclass='4'):
    denom = 0
    for i in range(1, 5):
        denom += int(item[role][0][str(i)][sumtype])
    if denom == 0:
        return 1000.0
    else:
        return 100.0-(100.0*int(item[role][0][quadclass][sumtype])/denom)
    
def obtaindata(coll,dates):
    start = True
    for date in dates:
        data = []
        items = coll.find({"country" : {"$in" :countries},"week" : date})
        for item in items:
            date = item['week']
            country = item['country']
            pct_quad_4=(percents(item, 'Target', 'SumNumMentions'))
            data.append([country,pct_quad_4])
                                 
        df= pd.DataFrame(data, columns=['country',date.date()]).set_index('country')
        
        #find percentiles
        
        pct_list_perc_a = stats.rankdata(df[date.date()],"max")/len(df)
        pct_list_perc_b = (stats.rankdata(df[date.date()],"min")-1)/len(df)
        pct_list_perc = [mean([a,b])*100.0 for a,b in zip(pct_list_perc_a,pct_list_perc_b)]       
        
        percdf= pd.DataFrame(zip(df.index.values,pct_list_perc ), columns=['country',date.date()]).set_index('country')
                
        if start == True:
            finaldf = df
            finalpercdf = percdf 
            start = False
        else:
            finaldf = pd.concat([finaldf,df],axis=1)
            finalpercdf = pd.concat([finalpercdf,percdf],axis=1)
    return finaldf[sorted(finaldf.columns)], finalpercdf[sorted(finalpercdf.columns)]    
 

def create_data(pct_df, pct_diff_df, perc_df, perc_diff_df, pct_roll_df, perc_roll_df, perc_diff_roll_df):
    oneweekfinal =[]
    onemonthfinal =[]
    onequarterfinal =[]    
    
    for c in countries:
        
        #create arrays for each of the variables
        sub_pct_df = pct_df.loc[[c]].values[0]
        sub_pct_diff_df = pct_diff_df.loc[[c]].values[0]
        sub_perc_df = perc_df.loc[[c]].values[0]
        sub_perc_diff_df = perc_diff_df.loc[[c]].values[0]        
        sub_perc_roll_df = perc_roll_df.loc[[c]].values[0]
        sub_perc_diff_roll_df = perc_diff_roll_df.loc[[c]].values[0]
        
        #target value needs to be rounded as well
        
        sub_pct_roll_df = pct_roll_df.loc[[c]]
        sub_pct_roll_df = np.round(sub_pct_roll_df/10,0)
        target = sub_pct_roll_df.values[0]
        
        def return_chunk(j):
            return [sub_perc_diff_df[j], sub_pct_diff_df[j], sub_perc_roll_df[j],
                   sub_perc_diff_roll_df[j],sub_perc_df[j], sub_pct_df[j]]
        
        
        
        for i in range(len(target)-50):        
            
            #one week pred
            #append the target and the country index
            oneweek=[target[i],countries.index(c)]
            oneweek_1, oneweek_2, oneweek_3 = return_chunk(i+1), return_chunk(i+2),  return_chunk(i+3)
            
            oneweek.extend(oneweek_1)
            oneweek.extend(oneweek_2)
            oneweek.extend(oneweek_3)
            
            #one month pred
            #append the target and the country index
            onemonth=[target[i],countries.index(c)]
            onemonth_1, onemonth_2, onemonth_3 = return_chunk(i+1*4), return_chunk(i+2*4),  return_chunk(i+3*4)
            
            onemonth.extend(onemonth_1)
            onemonth.extend(onemonth_2)
            onemonth.extend(onemonth_3)
            
            #one quarter pred
            #append the target and the country index
            onequar=[target[i],countries.index(c)]
            onequar_1, onequar_2, onequar_3 = return_chunk(i+1*13), return_chunk(i+2*13),  return_chunk(i+3*13)
            
            onequar.extend(onequar_1)
            onequar.extend(onequar_2)
            onequar.extend(onequar_3)
            
            #append to final
            oneweekfinal.append(oneweek)
            onemonthfinal.append(onemonth) 
            onequarterfinal.append(onequar)  
            
    return oneweekfinal, onemonthfinal, onequarterfinal
 
def create_pred_data(pct_df, pct_diff_df, perc_df, perc_diff_df, pct_roll_df, perc_roll_df, perc_diff_roll_df):
    oneweekfinal =[]
    onemonthfinal =[]
    onequarterfinal =[]    
    
    for c in countries:
        
        #create arrays for each of the variables
        sub_pct_df = pct_df.loc[[c]].values[0]
        sub_pct_diff_df = pct_diff_df.loc[[c]].values[0]
        sub_perc_df = perc_df.loc[[c]].values[0]
        sub_perc_diff_df = perc_diff_df.loc[[c]].values[0]        
        sub_perc_roll_df = perc_roll_df.loc[[c]].values[0]
        sub_perc_diff_roll_df = perc_diff_roll_df.loc[[c]].values[0]
        
        #target value needs to be rounded as well
        
        sub_pct_roll_df = pct_roll_df.loc[[c]]
        sub_pct_roll_df = np.round(sub_pct_roll_df/10,0)
        target = sub_pct_roll_df.values[0]
        
        def return_chunk(j):
            return [sub_perc_diff_df[j], sub_pct_diff_df[j], sub_perc_roll_df[j],
                   sub_perc_diff_roll_df[j],sub_perc_df[j], sub_pct_df[j]]
        
        
        
               
            
        #one week pred
        #append the target and the country index
        oneweek=[c, countries.index(c)]
        oneweek_1, oneweek_2, oneweek_3 = return_chunk(1), return_chunk(2),  return_chunk(3)
            
        oneweek.extend(oneweek_1)
        oneweek.extend(oneweek_2)
        oneweek.extend(oneweek_3)
            
        #one month pred
        #append the target and the country index
        onemonth=[c, countries.index(c)]
        onemonth_1, onemonth_2, onemonth_3 = return_chunk(1*4), return_chunk(2*4),  return_chunk(3*4)           
            
        onemonth.extend(onemonth_1)
        onemonth.extend(onemonth_2)
        onemonth.extend(onemonth_3)
            
            
        #one quarter pred
        #append the target and the country index
        onequar=[c, countries.index(c)]
        onequar_1, onequar_2, onequar_3 = return_chunk(1*13), return_chunk(2*13),  return_chunk(3*13)
            
        onequar.extend(onequar_1)
        onequar.extend(onequar_2)
        onequar.extend(onequar_3)
            
        #append to final
        oneweekfinal.append(oneweek)
        onemonthfinal.append(onemonth) 
        onequarterfinal.append(onequar)  
            
    return oneweekfinal, onemonthfinal, onequarterfinal


           
def splitdata(data, shuffle = True):
    npdata = np.array(data)
    if shuffle:
        np.random.shuffle(npdata) 
    
    X=npdata[:,1:]
    Y =npdata[:, 0]
    
    return X,Y      

def upload_mongo(df):    
    db_name = 'db_tourist'   
    dbclient=pymongo.MongoClient('mongodb://mids:1X49ilWN@198.23.108.210:27017/' + db_name)   
    db = dbclient['db_tourist']
    gdelt_pred = db.db_gdelt_preds

    df_flat = df.reset_index()
    jsons = df_flat.to_json(orient = 'records')
   
    gdelt_pred.insert_many(ast.literal_eval(jsons))

   
#Connect to Pymongo GDELT collection
gdelt_coll = pymongo_conn()
dates = get_dates(gdelt_coll)
df, percdf = obtaindata(gdelt_coll,dates)

#create other tables needed
roll_perc = pd.rolling_mean(percdf, window=3,axis=1)
roll_pct = pd.rolling_mean(df, window=3,axis=1)

df_diff = df.diff(periods=1, axis=1)
percdf_diff = percdf.diff(periods=1, axis=1)
roll_perc_diff = roll_perc.diff(periods=1, axis=1)


#remove the cols that are nan due to rolling averages
nec_cols = df.columns[5:]


df = df[nec_cols]
df_diff = df_diff[nec_cols]
percdf= percdf[nec_cols]
roll_perc= roll_perc[nec_cols]
df_diff= df_diff[nec_cols]
percdf_diff= percdf_diff[nec_cols]
roll_perc_diff= roll_perc_diff[nec_cols]


#sort them from newest to oldest
df = df[sorted(df.columns, reverse = True)]
roll_pct = roll_pct[sorted(roll_pct.columns, reverse = True)]
percdf = percdf[sorted(percdf.columns, reverse = True)]
roll_perc = roll_perc[sorted(roll_perc.columns, reverse = True)]
df_diff = df_diff[sorted(df_diff.columns, reverse = True)]
percdf_diff = percdf_diff[sorted(percdf_diff.columns, reverse = True)]
roll_perc_diff = roll_perc_diff[sorted(roll_perc_diff.columns, reverse = True)]

#data in format for ML
oneweekfinal, onemonthfinal, onequarterfinal = create_data(df, df_diff, percdf, percdf_diff, roll_pct, roll_perc, roll_perc_diff)

#create 3 models, one for each prediction time
gcm1 = GradientBoostingClassifier()
X1,Y1 = (splitdata(oneweekfinal))  
gcm1.fit(X1,Y1)  

gcm4 = GradientBoostingClassifier()
X4,Y4 = (splitdata(onemonthfinal))  
gcm4.fit(X4,Y4) 

gcm13 = GradientBoostingClassifier()
X13,Y13 = (splitdata(onequarterfinal))  
gcm13.fit(X13,Y13) 

#obtain features for prediction
oneweekpred, onemonthpred, onequarterpred = create_pred_data(df, df_diff, percdf, percdf_diff, roll_pct, roll_perc, roll_perc_diff)

#make predictions
labels1, _ = splitdata(oneweekpred, shuffle = False)
preds1 = gcm1.predict(labels1)

labels4, _ = splitdata(onemonthpred, shuffle = False)
preds4 = gcm1.predict(labels4)

labels13, cty = splitdata(onequarterpred, shuffle = False)
preds13 = gcm1.predict(labels13)

#combine predictions into one dataframe
all_preds = pd.DataFrame([cty,preds1,preds4,preds13]).T
all_preds.columns=['country','pred_1_week','pred_1_month','pred_3_months']

all_preds =all_preds.set_index('country')
#find date and current value and insert into same dataframe
curr_data = roll_pct[[max(roll_pct.columns.values)]]
curr_data.columns =['curr_week_pct_4']
all_preds['gdelt_pred_date'] = max(roll_pct.columns.values)

all_preds = pd.concat([all_preds, curr_data], axis=1)

#upload into mongo

upload_mongo(all_preds)