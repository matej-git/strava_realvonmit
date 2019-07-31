from webbot import Browser
from bs4 import BeautifulSoup as bs

import pandas as pd
import re
import time
import random

# set race
city = 'london'
year = '2018'
race = 'marathon'

#get a race data
race_table = pd.read_csv('data/raw/'+city+'_'+race+'_'+year+'_'+'raw.csv', encoding = "ISO-8859-1", index_col = 0)
l = len(race_table)
#open browser
web = Browser()
#strava login infos
names = ['pavol.svrbo@gmail.com','peter.svrbo@gmail.com','juraj.svrbo@gmail.com','jan.svrbo@gmail.com']
passwords = ['akosamas','akosamas','akosamas','akosamas']

def strava_login(web, name, password):
    web.go_to('https://www.strava.com/login') 
    web.type(name , into='email')
    web.type(password , into='password' , id='password')
    web.click('submit', id = 'login-button')
    return(web)

strava_login(web,names[0],passwords[0])

web.go_to('https://www.strava.com/activities/1737695224')
activity = web.get_page_source()
soup = bs(activity, 'html.parser')

def strava_download(web, url):
    web.go_to('https://www.strava.com'+url)
    activity = web.get_page_source()
    soup = bs(activity, 'html.parser')
    
    watch_l = soup.find_all('div', attrs = {'class':'device spans8'})
    if len(watch_l) == 0: watch = None
    else: watch = watch_l[0].text.replace('\n','')
    
    shoes_l = soup.find_all('span', attrs = {'class':'gear-name'})
    if len(shoes_l) == 0: shoes = None
    else: shoes = shoes_l[0].text.replace('\n','')
        
    distance_l = soup.find_all('ul', attrs = {'class':'inline-stats section'})
    if len(distance_l) == 0: distance = None
    else: distance = distance_l[0].text.replace('\n','')[:5]
    
    condition = 'Too Many Requests' in activity
    return([condition, watch, shoes, distance])

watch_list = []
shoes_list = []
distance_list = []
i = 0
strava_login(web, names[0], passwords[0])
time.sleep(10)

for url in race_table['race_url']:
    info = strava_download(web, url)
    while info[0]:
        names.append(names[0])
        names.pop(0)
        passwords.append(passwords[0])
        passwords.pop(0)
        web.go_to('https://www.strava.com/logout') 
        strava_login(web, names[0], passwords[0])
        time.sleep(30)
        info = strava_download(web, url)
    watch_list.append(info[1])
    shoes_list.append(info[2])
    distance_list.append(info[3])
    i = i+1
    print(str(i)+' out of '+str(l))

race_table['Watch'] = watch_list
race_table['Shoes'] = shoes_list
race_table['Distance'] = distance_list

race_table.to_csv('data/full/'+city+'_'+race+'_'+year+'_full.csv')

# Turn off computer
import os
os.system('shutdown -s')



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

