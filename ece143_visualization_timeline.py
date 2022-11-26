# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 21:14:47 2022

@author: Shiyuan Wang
"""
import pandas as pd
pd.set_option('display.max_columns', None)
df = pd.read_csv("C:/0-ece143/project/data/Worldwide_Case_Detection_Timeline.csv", encoding='unicode_escape')
import matplotlib.pyplot as plt

date = df['Date_confirmation'].tolist()
country = df['Country'].tolist()
world_counter = {}
us_counter = {}

for i in range(len(date)):
    dat = date[i]
    cou = country[i]
    if dat not in world_counter.keys():
        world_counter[dat] = 1
    else:
        world_counter[dat] += 1
    if cou == 'United States':
        if dat not in us_counter.keys():
            us_counter[dat] = 1
        else:
            us_counter[dat] += 1
            
world_date = list(world_counter.keys())
world_count = list(world_counter.values())
plt.plot(world_date, world_count)
plt.title('Confirmed Cases in the World')
plt.xlabel('Dates')
plt.ylabel('Number of Cases')
plt.savefig('Confirmed Cases in the World.png')
plt.clf()
us_date = list(us_counter.keys())
us_count = list(us_counter.values())
plt.plot(us_date, us_count)
plt.title('Confirmed Cases in the US')
plt.xlabel('Dates')
plt.ylabel('Number of Cases')
plt.savefig('Confirmed Cases in the US.png')