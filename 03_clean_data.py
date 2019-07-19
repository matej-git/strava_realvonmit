import pandas as pd
import numpy as np
import re
import time
import random
import matplotlib.pyplot as plt

# Set race
city = 'valencia'
year = '2018'
race = 'halfmarathon'

# Set outlier boarders
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

race_table = pd.read_csv('data/full/'+city+'_'+race+'_'+year+'_full.csv', index_col = 0)
race_table = race_table.drop(columns=['Name', 'Strava Activity'])

# Clear distance
race_table.Distance = race_table.Distance.astype(str).map(lambda x: x.lstrip("['").strip("']"))
race_table.Distance = pd.to_numeric(race_table.Distance, errors='coerce')
# Filter outliers
race_table = race_table[(race_table.Distance<cap) & (race_table.Distance>floor)]

# Add info to table
race_table['city'] = city.replace('_',' ').title()
race_table['year'] = year
race_table['race_type'] = race.title()

# Clear wath info
race_table.Watch = race_table.Watch.astype(str).map(lambda x: x.lstrip("['").strip("']"))
race_table.Watch = race_table.Watch.str.replace('<a href="/', '')
race_table.Watch = race_table.Watch.str.replace('</a>', '')
race_table.Watch = race_table.Watch.str.replace('mobile">Strava ', '')
race_table.Watch = race_table.Watch.str.replace('android-wear">', '')
race_table.Watch = race_table.Watch.str.replace('apple-watch">', '')
#jebnute nazvy garminov
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

race_table.athlet_url = race_table.athlet_url.str.replace('/athletes/', '')
race_table.race_url = race_table.race_url.str.replace('/activities/', '')

race_table['H'] = pd.to_numeric(race_table.Finish.map(lambda x: x.split(":")[0]))
race_table['M'] = pd.to_numeric(race_table.Finish.map(lambda x: x.split(":")[1]))
race_table['S'] = pd.to_numeric(race_table.Finish.map(lambda x: x.split(":")[2]))

race_table['Finish_num'] = race_table.H + race_table.M/60 + race_table.S/3600
race_table = race_table.drop(columns=['H', 'M', 'S'])
# Filter outliers
race_table = race_table[race_table.Finish_num<time_cap]

# Save output
race_table.to_csv(('data/clean/'+city+'_'+race+'_'+year+'.csv'), index=False)

