from bs4 import BeautifulSoup as bs

import requests
import lxml.html as lh
import pandas as pd
import re

# set race
url_race = '2018-medio-maratn-valencia-trinidad-alfonso'
city = 'valencia'
year = '2018'
race = 'halfmarathon'

url = 'https://www.strava.com/running_races/' + url_race + '/results?page='
race_table = pd.DataFrame({
    'Rank' : [],
    'Name' : [],
    'Gender' : [],
    'Age' : [],
    'Strava activity' : [],
    'athlet_url' : [],
    'race_url' : []
})

def strava_scrape(url, i):
    page = requests.get(url + str(i))
    soup = bs(page.content, 'html.parser')

    athlete_rank = [x.text for x in soup.find_all('td', attrs = {'class':'athlete-rank'})]
    athlete_name = [x.text.replace('\n','') for x in soup.find_all('td', attrs = {'class':'athlete-name'})]
    athlete_gender = [x.text.replace('\n','') for x in soup.find_all('td', attrs = {'class':'athlete-gender'})]
    athlete_age = [x.text for x in soup.find_all('td', attrs = {'class':'athlete-age'})]
    strava_activity = [x.text.replace('\n','') for x in soup.find_all('td', attrs = {'class':'athlete-activity'})]

    athlet_url = []
    for link in soup.findAll('a', attrs={'href': re.compile("/athletes/")}):
            athlet_url.append(link.get('href'))
    athlet_url = athlet_url[0::2]

    race_url = []
    for link in soup.findAll('a', attrs={'href': re.compile("/activities/")}):
            race_url.append(link.get('href'))
            
    data = pd.DataFrame({
    'Rank' : athlete_rank,
    'Name' : athlete_name,
    'Gender' : athlete_gender,
    'Age' : athlete_age,
    'Strava activity' : strava_activity,
    'athlet_url' : athlet_url,
    'race_url' : race_url})
    
    return(data)

i = 0
check = True

while check:
    i += 1
    race_table_i = strava_scrape(url, i)
    check = len(race_table_i) != 0
    if not check: break
    race_table = race_table.append(race_table_i)

race_table.to_csv('data/raw/'+city+'_'+race+'_'+year+'_raw.csv')

