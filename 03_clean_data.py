#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import numpy as np
import re
import time
import random
import matplotlib.pyplot as plt
import os
import glob


# In[21]:


#os.chdir('..')
path = 'C:\\Users\\matej.karkalik\\Documents\\strava_realvonmit\\data\\full'
files = [f for f in glob.glob(path + "**/*.csv", recursive=True)]


# In[2]:


# set race
city = 'valencia'
year = '2018'
race = 'halfmarathon'


# In[3]:


# set outlier boarders
if race == 'halfmarathon':
    race_length = 21.0975
    floor = race_length - 3
    cap = race_length + 3
    time_cap = 3.5
if race == 'marathon':
    race_length = 42.195
    floor = race_length - 6
    cap = race_length + 6
    time_cap = 7


# In[4]:


#race_table = pd.read_csv('data/full/'+city+'_'+race+'_'+year+'_full.csv', index_col = 0)
#race_table = race_table.drop(columns=['Name', 'Strava Activity'])


# In[86]:


def clear_table(race_table, city, race, year):
    
    if race == 'halfmarathon':
        race_length = 21.0975
        floor = race_length - 3
        cap = race_length + 3
        time_cap = 3.5
    if race == 'marathon':
        race_length = 42.195
        floor = race_length - 6
        cap = race_length + 6
        time_cap = 7
    
    race_table = race_table.drop(columns = ['Name', 'Strava Activity'])
    
    # Clear distance
    race_table.Distance = race_table.Distance.astype(str).map(lambda x: x.lstrip("['").strip("']"))
    race_table.Distance = pd.to_numeric(race_table.Distance, errors='coerce')
    # Filter outliers
    race_table = race_table[(race_table.Distance<cap) & (race_table.Distance>floor)]
    # add info to table
    race_table['City'] = city.replace('_',' ').title()
    race_table['Year'] = year
    race_table['Race_Type'] = race.title()
    # Clear wath info
    race_table.Watch = race_table.Watch.astype(str).map(lambda x: x.lstrip("['").strip("']"))
    race_table.Watch = race_table.Watch.str.replace('<a href="/', '')
    race_table.Watch = race_table.Watch.str.replace('</a>', '')
    race_table.Watch = race_table.Watch.str.replace('mobile">Strava ', '')
    race_table.Watch = race_table.Watch.str.replace('android-wear">', '')
    race_table.Watch = race_table.Watch.str.replace('apple-watch">', '')
    # Jebnute nazvy garminov
    race_table.Watch = race_table.Watch.str.replace('vívo', 'vivo')
    race_table.Watch = race_table.Watch.str.replace('Vívo', 'vivo')
    race_table.Watch = race_table.Watch.str.replace('fēnix', 'fenix')
    # Extract watch brand
    race_table['Watch_Brand'] = race_table.Watch.str.split().str[0]
    # Watch Error
    race_table['Watch_Error'] = race_table.Distance - race_length
    race_table['Watch_Error_Abs'] = race_table.Watch_Error.abs()
    # Clear shoes
    race_table.Shoes = race_table.Shoes.map(lambda x: x.lstrip("['").strip("']"))
    race_table.Shoes = race_table.Shoes.str.replace('—', 'NA')
    race_table.Shoes = [re.sub("[\(\[].*?[\)\]]", "", x.strip().lower()) for x in race_table.Shoes]
    race_table.Shoes = [x.title() for x in race_table.Shoes]
    race_table['Shoes_Brand'] = [x.split(' ', 1)[0] for x in race_table.Shoes]
    race_table.Shoes_Brand = race_table.Shoes_Brand.str.replace('New', 'New Balance')
    race_table.Shoes_Brand = [x.title() for x in race_table.Shoes_Brand]
    race_table.athlet_url = race_table.athlet_url.str.replace('/athletes/', '')
    race_table.race_url = race_table.race_url.str.replace('/activities/', '')
    race_table['H'] = pd.to_numeric(race_table.Finish.map(lambda x: x.split(":")[0]))
    race_table['M'] = pd.to_numeric(race_table.Finish.map(lambda x: x.split(":")[1]))
    race_table['S'] = pd.to_numeric(race_table.Finish.map(lambda x: x.split(":")[2]))
    race_table['Finish_Numeric'] = race_table.H + race_table.M/60 + race_table.S/3600
    race_table = race_table.drop(columns=['H', 'M', 'S'])
    # Filter outliers
    race_table = race_table[race_table.Finish_Numeric<time_cap]
    
    race_table = race_table.replace(['na', 'Na', 'nan', '', None], 'NA')
    race_table = race_table.rename(columns={'athlet_url': 'Athlet_url', 'race_url': 'Race_url'})
    
    return(race_table)


# In[87]:


for f in files:
    
    name_clear = f.rsplit('\\', 1)[-1].replace('_full','')
    name_list = name_clear.replace('.','_').rsplit('_',3)
    
    city = name_list[0]
    race = name_list[1]
    year = name_list[2]
        
    race_table = pd.read_csv(f, index_col = 0)
    race_table = clear_table(race_table, city, race, year)
    race_table.to_csv('data/clean/' + name_clear, index=True)
    #race_table = race_table.drop(columns=['Name', 'Strava Activity'])


# In[ ]:


# commet later
#race_table = race_table.drop(race_table.columns[0], axis=1)


# In[25]:


#race_table.Shoes_Brand.value_counts()


# In[ ]:


#race_table[race_table.Watch_Brand == 'Suunto'][['Watch', 'Watch_Error_Abs']].groupby(['Watch']).mean().sort_values(by='Watch_Error_Abs')


# In[ ]:


#plt.hist(race_table['Watch_Error'], bins = 50)
#plt.title('Error Check')


# In[ ]:


#plt.hist(race_table[race_table.Watch_Brand == 'Huami']['Watch_Error'], bins = 10)
#plt.title('Amazefit Error Check')


# In[ ]:


#plt.hist(race_table[race_table.Watch_Brand == 'Garmin']['Watch_Error'], bins = 10)
#plt.title('Garmin Error Check')


# In[ ]:


#race_table.to_csv(('data/clean/'+city+'_'+race+'_'+year+'.csv'), index=False)

