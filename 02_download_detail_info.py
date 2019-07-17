#!/usr/bin/env python
# coding: utf-8

# In[1]:


from webbot import Browser
import pandas as pd
import re
import time
import random


# In[2]:


# set race
city = 'london'
year = '2018'
race = 'marathon'


# In[3]:


#get a race data
race_table = pd.read_csv('data/raw/'+city+'_'+race+'_'+year+'_'+'raw.csv', encoding = "ISO-8859-1", index_col = 0)
l = len(race_table)
#open browser
web = Browser()
#strava login infos
names = ['pavol.svrbo@gmail.com','peter.svrbo@gmail.com','juraj.svrbo@gmail.com','jan.svrbo@gmail.com']
passwords = ['akosamas','akosamas','akosamas','akosamas']


# In[7]:


def strava_login(web, name, password):
    web.go_to('https://www.strava.com/login') 
    web.type(name , into='email')
    web.type(password , into='password' , id='password')
    web.click('submit', id = 'login-button')
    return(web)


# In[5]:


def strava_download(web, url):
    regex_watch = r'(?<=device spans8)">(.*)(?=</div><div class="gear spans8)'
    regex_shoes = r'(?<=<span class="gear-name">)(.*)(?=</span></div></div></div>)'
    regex_distance = r'(?<=inline-stats section"><li><strong>)(.*)(?=<abbr class="unit" title="kilometers">km)'
    web.go_to('https://www.strava.com'+url)
    activity = web.get_page_source()
    activity_clear = activity.replace('\n','')
    watch = re.findall(regex_watch, activity_clear)
    shoes = re.findall(regex_shoes, activity_clear)
    distance = re.findall(regex_distance, activity_clear)
    condition = 'Too Many Requests' in activity
    return([condition, watch, shoes, distance])


# In[8]:


watch_list = []
shoes_list = []
distance_list = []
i = 0
strava_login(web, names[0], passwords[0])
time.sleep(10)


# In[ ]:


for url in race_table['race_url']:
    info = strava_download(web, url)
    while info[0]:
        names.append(names[0])
        names.pop(0)
        passwords.append(passwords[0])
        passwords.pop(0)
        web.go_to('https://www.strava.com/logout') 
        strava_login(web, names[0], passwords[0])
        time.sleep(120)
        info = strava_download(web, url)
    watch_list.append(info[1])
    shoes_list.append(info[2])
    distance_list.append(info[3])
    i = i+1
    print(str(i)+' out of '+str(l))


# In[ ]:


#pd.DataFrame(watch_list).to_csv('watch_list.csv')
#pd.DataFrame(shoes_list).to_csv('shoes_list.csv')
#pd.DataFrame(distance_list).to_csv('distance_list.csv')


# In[ ]:


race_table['Watch'] = watch_list
race_table['Shoes'] = shoes_list
race_table['Distance'] = distance_list


# In[ ]:


race_table.to_csv('data/full/'+city+'_'+race+'_'+year+'.csv')


# In[ ]:


# Turn off computer
#import os
#os.system('shutdown -s')


# In[ ]:


# Different aproach

#from requests import Session
#from bs4 import BeautifulSoup as bs
 
#with Session() as s:
#    site = s.get("https://www.strava.com/login")
#    bs_content = bs(site.content, "html.parser")
#    token1 = bs_content.find("meta", {"name":"csrf-token"})["content"]
#    token2 = bs_content.find("input", {"name":"authenticity_token"})["value"]
#    login_data = {"email":"mkarkalik@gmail.com", 
#                  "password":"akosamas", 
#                  "csrf-token":token1,
#                  "authenticity_token":token2}
#    s.post("https://www.strava.com/login", login_data)
#    home_page = s.get("https://www.strava.com/")
#    print(bs(home_page.content, "html.parser"))
#    #print(token2)

