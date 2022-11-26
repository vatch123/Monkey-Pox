# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 22:30:06 2022

@author: Shiyuan Wang
"""
import pandas as pd
pd.set_option('display.max_columns', None)
df = pd.read_csv("C:/0-ece143/project/data/Monkey_Pox_Cases_Worldwide.csv", encoding='unicode_escape')
import matplotlib.pyplot as plt
from statistics import mean

conf = mean(df['Confirmed_Cases'].tolist())
hosp = mean(df['Hospitalized'].tolist())
trav = mean(df['Travel_History_Yes'].tolist())

plt.bar(['US','World'], [24403, conf])
plt.title('Confirmed')
plt.ylabel('Number of Cases')
plt.savefig('Confirmed Histogram.png')
plt.clf()
plt.bar(['US','World'], [4, hosp])
plt.title('Hospitalized')
plt.ylabel('Number of Cases')
plt.savefig('Hospitalized Histogram.png')
plt.clf()
plt.bar(['US','World'], [41, trav])
plt.title('Travel History')
plt.ylabel('Number of Cases')
plt.savefig('Travel Histogram.png')
plt.clf()