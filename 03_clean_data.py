#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import numpy as np
import re
import time
import random


# In[53]:


# set race
city = 'barcelona'
year = '2019'
race = 'half'


# In[121]:


# set outlier boarders
if race == 'half':
    race_length = 21.0975
    floor = race_length - 3
    cap = race_length + 3
if race == 'full':
    race_length = 42.195
    floor = race_length - 6
    cap = race_length + 6   


# In[106]:


race_table = pd.read_csv('data/'+city+'_'+race+'_'+year+'.csv')


# In[107]:


#Clear wath info
race_table.Watch = race_table.Watch.map(lambda x: x.lstrip("['").strip("']"))
race_table.Watch = race_table.Watch.str.replace('<a href="/', '')
race_table.Watch = race_table.Watch.str.replace('</a>', '')
race_table.Watch = race_table.Watch.str.replace('mobile">Strava ', '')
race_table.Watch = race_table.Watch.str.replace('android-wear">', '')
race_table.Watch = race_table.Watch.str.replace('apple-watch">', '')


# In[109]:


#Extract watch brand
race_table['Watch_Brand'] = race_table.Watch.str.split().str[0]


# In[116]:


# Clear distance
race_table.Distance = race_table.Distance.map(lambda x: x.lstrip("['").strip("']"))
race_table.Distance = pd.to_numeric(race_table.Distance)


# In[110]:


# Clear shoes
race_table.Shoes = race_table.Shoes.map(lambda x: x.lstrip("['").strip("']"))


# In[122]:


#filter outliers
race_table = race_table[(race_table.Distance<cap) & (race_table.Distance>floor)]


# In[124]:


race_table['Watch_Error'] = race_table.Distance - race_length


# In[126]:


import matplotlib.pyplot as plt


# In[130]:


plt.hist(race_table['Watch_Error'], bins = 50)
plt.title('Error Check')


# In[135]:


plt.hist(race_table[race_table.Watch_Brand == 'Huami']['Watch_Error'], bins = 50)
plt.title('Amazefit Error Check')


# In[137]:


plt.hist(race_table[race_table.Watch_Brand == 'Garmin']['Watch_Error'], bins = 50)
plt.title('Garmin Error Check')


# In[138]:


race_table.to_csv(('data/'+city+'_'+race+'_'+year+'_final'+'.csv'))

