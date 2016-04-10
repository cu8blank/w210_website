# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import requests
import pymongo
import datetime
import operator
import zipfile
import StringIO
import pandas as pd
from datetime import datetime as dt

class Aggregated:
    
    
    #as we are interested in aggregating by week, we will be creating a stopdate variable.
    #this will be updated as we progress
    #initialize the dict and finallist to be used also
    def __init__(self, startdate):
        import datetime
        self.startdate = datetime.datetime.strptime(startdate, "%Y%m%d")
        self.stopdate = self.startdate + datetime.timedelta(days=6)
        self.c1aggdict = {}    
        self.c2aggdict = {}   
        self.c1_finallist =[]        
        self.c2_finallist =[] 
   
    # this is the main function of this class.  It calls all others  
    
    def iterate(self,row):
        self.parse(row)
        
        
        #check to see if we are past the week
        #if so, aggregate, add to list and reset all variables
        if self.sqldate > self.stopdate:           
            
            #print the list by week and reset the dict
            self.printlist('c1',self.c1aggdict)
            self.c1aggdict = {}
            
            
            #country 2
            self.printlist('c2',self.c2aggdict)
            self.c2aggdict = {}
            
            #change start and stopdates and then run combine again as there is a line in there unprocessed
            self.stopdate = self.sqldate + datetime.timedelta(days=6)
            self.startdate = self.sqldate
            
            
            self.combine(self.Country1,self.c1aggdict)
            #if country2 is blank, it does not need to be combined
            if self.Country2 <> '':
                self.combine(self.Country2,self.c2aggdict)
            
        #on later files, there is data that is older.  this will append them all on a list.   
        elif self.sqldate < self.startdate:            
            1+1
            
        else:
            self.combine(self.Country1,self.c1aggdict)
            #if country2 is blank, it does not need to be combined
            if self.Country2 <> '':
                self.combine(self.Country2,self.c2aggdict)
            
    #this function actually adds values based on the keys
    def combine(self,country,dictt):
        self.aggkey = (self.startdate, country, self.QuadClass)
        
        #create a new value if it does not exist.  The last value of 1 there is used as a counter for each
        #key.  This will be used to calculate averages when the end of a week is reached.
        if self.aggkey not in dictt:
            dictt[self.aggkey] = [self.NumMentions,
                                        self.NumSources,
                                        self.NumArticles,
                                        self.GoldsteinScale,
                                        self.AvgTone,
                                        self.TypeArray,
                                        1]
        else: 
            values = dictt.get(self.aggkey)
            values[0] += self.NumMentions
            values[1] += self.NumSources
            values[2] += self.NumArticles
            values[3] += self.GoldsteinScale
            values[4] += self.AvgTone
            values[6] += 1
            values[5] = [x +y for x,y in zip(values[5],self.TypeArray)]
            dictt[self.aggkey] = values
    
    def cleanup(self):
        self.printlist('c1',self.c1aggdict)
        self.printlist('c2',self.c2aggdict)          
            
  
   
      #prints the actual list.  filename based on the startdate currently saved.
    def printlist(self,dirr,dictt):        
        for key, values in dictt.iteritems():
            #unpack key
            week, country, quad= key
            week = week.date()
            #unpack values
            NumMentions, NumSources, NumArticles, GoldsteinScale, AvgTone, TypeArray, Count = values
                
                
            if dirr == 'c1': 
                self.c1_finallist.append([week,country,quad,NumMentions,NumSources,
                                       NumArticles,GoldsteinScale,AvgTone,TypeArray, Count])
                self.c1_finallist.sort(key=operator.itemgetter(1,2,3)) 
            
            if dirr == 'c2': 
                self.c2_finallist.append([week,country,quad,NumMentions,NumSources,
                                       NumArticles,GoldsteinScale,AvgTone,TypeArray, Count])
             
                self.c2_finallist.sort(key=operator.itemgetter(1,2,3))        
        
  
    
    #this function takes the input which is a list and parses them.
    def parse(self,row):
        self.sqldate = datetime.datetime.strptime(row[1],"%Y%m%d")
        self.MonthYear = row[2]
        self.Year = row[3]
        self.FractionDate = row[4]
        self.Country1 = row[5]
        self.Types = [row[6],row[7],row[8]]
        self.Country2 = row[9]
        self.IsRootEvent = row[10]
        self.EventRootCode = row[11]
        self.QuadClass = row[12]
        self.GoldsteinScale = float(row[13])
        self.NumMentions = int(row[14])
        self.NumSources = int(row[15])
        self.NumArticles = int(row[16])
        self.AvgTone = float(row[17])
        
        #create a binary array for all type actors
        self.TypeLookup()
        
        
    #this function creates an array of 1s and 0s reflecting all possible types
    def TypeLookup(self):
        alltypes = ['COP','GOV','INS','JUD','MIL','OPP','REB','SEP','SPY','UAF','AGR','BUS','CRM','CVL','DEV','EDU',
                    'ELI','ENV','HLH','HRI','LAB','LEG','MED','REF','MOD','RAD','AMN','IRC','GRP','UNO','PKO','UIS',
                    'IGO','IMG','INT','MNC','NGM','NGO','UIS','SET']
        
        self.TypeArray = []
        for tp in alltypes:
            if tp in self.Types:
                self.TypeArray.append(1)
            else:
                self.TypeArray.append(0)
                
    def DataReturn(self):
        self.c1_finallist.sort(key=operator.itemgetter(1,2,3)) 
        self.c2_finallist.sort(key=operator.itemgetter(1,2,3)) 
        return self.c1_finallist, self.c2_finallist


def pymongo_conn():
    db_name = 'db_tourist'   
    dbclient=pymongo.MongoClient('mongodb://mids:1X49ilWN@198.23.108.210:27017/' + db_name)   
    db = dbclient['db_tourist']
    return db.db_gdelt


def find_files():
    url = "http://data.gdeltproject.org/events/index.html"
    soup = BeautifulSoup(requests.get(url).text)

    hrefs = []

    for a in soup.find_all('a'):
        hrefs.append(a['href'])
    hrefs.remove('md5sums')
    hrefs.remove('filesizes')
    hrefs.remove('GDELT.MASTERREDUCEDV2.1979-2013.zip')
    hrefs.remove('GDELT.MASTERREDUCEDV2.1979-2013.zip')
    hrefs.sort()        
        
    return hrefs


#post function
def create_post(T1,T2,T3,T4,A1,A2,A3,A4,curr_week,curr_country):
    
    def divi(N,D):
        if float(D) == 0.0:
            return 0.0
        else:
            return float(N)/float(D)
    
    post = {"week": curr_week,
                    "country":curr_country,
                    "Target": [{
                    "1":{
                        "SumNumMentions": T1[0],
                        "AvgNumMentions": divi(T1[0],T1[6]),
                        "SumNumArticles": T1[1],
                        "AvgNumArticles": divi(T1[1],T1[6]),
                        "SumNumSources": T1[2],
                        "AvgNumSources": divi(T1[2],T1[6]),
                        "AvgGoldsteinScore": divi(T1[3],T1[6]),
                        "AvgTone": divi(T1[4],T1[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(T1[6]),0)}  
                            ,
                    "2":{
                        "SumNumMentions": T2[0],
                        "AvgNumMentions": divi(T2[0],T2[6]),
                        "SumNumArticles": T2[1],
                        "AvgNumArticles": divi(T2[1],T2[6]),
                        "SumNumSources": T2[2],
                        "AvgNumSources": divi(T2[2],T2[6]),
                        "AvgGoldsteinScore": divi(T2[3],T2[6]),
                        "AvgTone": divi(T2[4],T2[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(T2[6]),0)}  
                            ,
                    "3":{
                        "SumNumMentions": T3[0],
                        "AvgNumMentions": divi(T3[0],T3[6]),
                        "SumNumArticles": T3[1],
                        "AvgNumArticles": divi(T3[1],T3[6]),
                        "SumNumSources": T3[2],
                        "AvgNumSources": divi(T3[2],T3[6]),
                        "AvgGoldsteinScore": divi(T3[3],T3[6]),
                        "AvgTone": divi(T3[4],T3[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(T3[6]),0)}  
                            ,
                    "4":{
                        "SumNumMentions": T4[0],
                        "AvgNumMentions": divi(T4[0],T4[6]),
                        "SumNumArticles": T4[1],
                        "AvgNumArticles": divi(T4[1],T4[6]),
                        "SumNumSources": T4[2],
                        "AvgNumSources": divi(T4[2],T4[6]),
                        "AvgGoldsteinScore": divi(T4[3],T4[6]),
                        "AvgTone": divi(T4[4],T4[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(T4[6]),0)} 
                              }],
                   "Acting": [{
                    "1":{
                        "SumNumMentions": A1[0],
                        "AvgNumMentions": divi(A1[0],A1[6]),
                        "SumNumArticles": A1[1],
                        "AvgNumArticles": divi(A1[1],A1[6]),
                        "SumNumSources": A1[2],
                        "AvgNumSources": divi(A1[2],A1[6]),
                        "AvgGoldsteinScore": divi(A1[3],A1[6]),
                        "AvgTone": divi(A1[4],A1[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(A1[6]),0)}  
                            ,
                    "2":{
                        "SumNumMentions": A2[0],
                        "AvgNumMentions": divi(A2[0],A2[6]),
                        "SumNumArticles": A2[1],
                        "AvgNumArticles": divi(A2[1],A2[6]),
                        "SumNumSources": A2[2],
                        "AvgNumSources": divi(A2[2],A2[6]),
                        "AvgGoldsteinScore": divi(A2[3],A2[6]),
                        "AvgTone": divi(A2[4],A2[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(A2[6]),0)}  
                            ,
                    "3":{
                        "SumNumMentions": A3[0],
                        "AvgNumMentions": divi(A3[0],A3[6]),
                        "SumNumArticles": A3[1],
                        "AvgNumArticles": divi(A3[1],A3[6]),
                        "SumNumSources": A3[2],
                        "AvgNumSources": divi(A3[2],A3[6]),
                        "AvgGoldsteinScore": divi(A3[3],A3[6]),
                        "AvgTone": divi(A3[4],A3[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(A3[6]),0)}  
                            ,
                    "4":{
                        "SumNumMentions": A4[0],
                        "AvgNumMentions": divi(A4[0],A4[6]),
                        "SumNumArticles": A4[1],
                        "AvgNumArticles": divi(A4[1],A4[6]),
                        "SumNumSources": A4[2],
                        "AvgNumSources": divi(A4[2],A4[6]),
                        "AvgGoldsteinScore": divi(A4[3],A4[6]),
                        "AvgTone": divi(A4[4],A4[6]),
                        "TypeArray": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "TotalCount": round(float(A4[6]),0)} 
                              }]
               }
    return post


def upload_pymongo(allitems):
   
    curr_country ='empty'        
    postappend=[] 
    
    for index, item in allitems.iterrows():        
        
        if curr_country <> item[1]:
            if curr_country <> 'empty':                
                post = create_post(T1,T2,T3,T4,A1,A2,A3,A4,curr_week,curr_country) 
        
                postappend.append(post)
            
            else:
                curr_country = item[1]
                curr_week = item[0]                 
            
            #resets variables
            curr_country = item[1]
            curr_week = item[0]
            
            T1 = ['0', '0', '0', '0', '0','role', .00001]
            T2 = ['0', '0', '0', '0', '0','role', .00001]
            T3 = ['0', '0', '0', '0', '0','role', .00001]
            T4 = ['0', '0', '0', '0', '0','role', .00001]
            A1 = ['0', '0', '0', '0', '0','role', .00001]
            A2 = ['0', '0', '0', '0', '0','role', .00001]
            A3 = ['0', '0', '0', '0', '0','role', .00001]
            A4 = ['0', '0', '0', '0', '0','role', .00001]
            
            
                
                
        if item[1]==curr_country :
            
            if item[2]=="1":
                T1 = item[3:10]
            if item[2]=="2":
                T2 = item[3:10]
            if item[2]=="3":
                    T3 = item[3:10]
            if item[2]=="4":
                T4 = item[3:10]
            
            if item[2]=="1":
                A1 = item[10:]
            if item[2]=="2":
                A2 = item[10:]
            if item[2]=="3":
                A3 = item[10:]
            if item[2]=="4":
                A4 = item[10:]
   
    #cleanup, ensure last item is also uploaded
    post = create_post(T1,T2,T3,T4,A1,A2,A3,A4,curr_week,curr_country)        
    postappend.append(post)    
    
    return postappend
    





#Connect to Pymongo GDELT collection
gdelt_coll = pymongo_conn()

#find max date
maxdate = gdelt_coll.find_one(sort=[("week", -1)])["week"]

#convert max date to same format as GDELT files
#the max date actually is the start of the week, so we want the file that is a week from the latest start date
maxdate = (maxdate + datetime.timedelta(days=7)).strftime('%Y%m%d')

#Get list of files from GDELT website
list_of_links = find_files()

#only take the links that have not been processed.  Only in multiples of 7 to represent full week
for i, name in enumerate(list_of_links):
    if maxdate in name:
        sub_list_of_links = list_of_links[i:]
        len_sub = len(sub_list_of_links)/7
        end_days = len_sub*7
        sub_list_of_links = sub_list_of_links[:end_days]
        
#sub_list_of_links is the data that needs to be processed.


#initialize class
Agg = Aggregated(maxdate)



#iterate through links and aggregate in class
for link in sub_list_of_links:    
    r = requests.get("http://data.gdeltproject.org/events/"+link)

    with zipfile.ZipFile(StringIO.StringIO(r.content)) as z:
        for filename in z.namelist():
            with z.open(filename) as f:
                for line in f:
                    #this list starts with a blank item as the indices in the class wont align otherwise
                    datarow = ['']
                    #line does have \n at the end.  stripping it
                    line.strip('\n')
                    events = line.split('\t')
                    #older data set does not have SOURCEURL col.  Adding a blank so all data is 58 cols
                    if len(events) <> 58:
                        events.append('')
                    sublist = []
                    for num in [1,2,3,4,7,12,13,14,17,25,28,29,30,31,32,33,34]:
                        datarow.append(events[num])      
                    if datarow[1]=='SQLDATE':
                        continue                    
                    else:
                        #occasionally there are values that are blank and when casting them to ints or floats it fails
                        try:
                            Agg.iterate(datarow)
                        except:
                            continue
                #clean up.  ensure the lists are cleared and everything is written to disk            
                
Agg.cleanup()

c1,c2 = Agg.DataReturn()
                
#reassign the array that showed job type with acting and target as the job type was never used and its easier to overwrite
for i in range(len(c1)):
    c1[i][8] ='Target'   
    
for i in range(len(c2)):
    c2[i][8] ='Acting'   

#merge the datasets on date, country and quad

tardf = pd.DataFrame(c1, columns = ['week','country','quad','NumMentions','NumSources',
                                       'NumArticles','GoldsteinScale','AvgTone','role', 'Count'])

actdf = pd.DataFrame(c2, columns = ['week','country','quad','NumMentions','NumSources',
                                       'NumArticles','GoldsteinScale','AvgTone','role', 'Count'])

fulldf = pd.merge(actdf,tardf, how = 'outer', on=['week','country','quad'])

fulldf = fulldf.fillna('0')
#sort to ensure the next function works as intended
fulldf = fulldf.sort_values(['week','country','quad'],  ascending=[True, True, True])


#create the json needed for uploading to pymongo
upload_file = upload_pymongo(fulldf)

#adjust datetime step for upload
for i in range(len(upload_file)):
    upload_file[i]['week'] = dt.combine(upload_file[i]['week'], dt.min.time())


#upload the json
gdelt_coll.insert_many(upload_file)




#some countries do not have data for the week.  this finds them and uploads an empty set;

items = gdelt_coll.aggregate(
   [
      {
        "$group" : {
           "_id" : "$week",
          
           
           "count": { "$sum": 1 }
        }
      }
   ]
)

dates =[]
for i in items:    
    if i['count'] <>225:
        dates.append(i['_id'])
        
countries = set(gdelt_coll.find().distinct("country"))


missing = []
for date in dates:
    sel_countries = []
    items = gdelt_coll.find({"week":date})
    for i in items:               
        sel_countries.append(i['country'])
    sel_countries = set(sel_countries)
    missing_cs = countries - sel_countries
    missing.append([date, list(missing_cs)])


postappend = []
for row in missing:
    date, countries = row
    for cty in countries:
        curr_country = cty
        curr_week = dt.combine(date, dt.min.time())    
        T1 = ['0', '0', '0', '0', '0','role', .00001]
        T2 = ['0', '0', '0', '0', '0','role', .00001]
        T3 = ['0', '0', '0', '0', '0','role', .00001]
        T4 = ['0', '0', '0', '0', '0','role', .00001]
        A1 = ['0', '0', '0', '0', '0','role', .00001]
        A2 = ['0', '0', '0', '0', '0','role', .00001]
        A3 = ['0', '0', '0', '0', '0','role', .00001]
        A4 = ['0', '0', '0', '0', '0','role', .00001]
        post = create_post(T1,T2,T3,T4,A1,A2,A3,A4,curr_week,curr_country)        
        postappend.append(post) 
        
gdelt_coll.insert_many(postappend)