"""
Python module which contains all the data visualizations
"""
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from src.utils import get_highest_cases
from statistics import mean

def total_cases_on_map(df_worldwide_cases: pd.DataFrame, df_daily_cases: pd.DataFrame):

    # Find the data for countries with the highest cases
    countries = get_highest_cases(df_worldwide_cases)
    df_worldwide_cases = df_worldwide_cases[df_worldwide_cases["Country"].isin(countries)]

    # Join with the daily cases of those countries.
    # We need to unpivot the daily cases dataframe to have a date column
    df_daily_cases = df_daily_cases.melt(id_vars='Country', var_name='Date', value_name='Cases')
    df = df_worldwide_cases.set_index('Country').join(df_daily_cases.set_index('Country'), how='inner')
    df = df.reset_index()
    df = df[df['Date']>'2022-08-01']

    # Get the cummulative sum of cases
    df['Total Cases'] = df[['Country', 'Cases']].groupby('Country').cumsum()


    fig = px.scatter_geo(df, locations='Country', locationmode='country names', color="Country", animation_frame='Date',
                     text="Country", hover_name="Country", size="Total Cases",
                     hover_data=['Cases', 'Date', 'Confirmed_Cases', 'Suspected_Cases', 'Hospitalized'],
                     projection="equirectangular")
    fig.show()

def case_trends(df_worldwide_cases: pd.DataFrame, df_daily_cases: pd.DataFrame):
    
    # Find the topK countries
    countries = get_highest_cases(df_worldwide_cases)
    df_daily_cases = df_daily_cases[df_daily_cases["Country"].isin(countries)]

    # We need to unpivot the daily cases dataframe to have a date column
    df_daily_cases = df_daily_cases.melt(id_vars='Country', var_name='Date', value_name='Cases')
    df_daily_cases['Total Cases'] = df_daily_cases[['Country', 'Cases']].groupby('Country').cumsum()
    df_daily_cases = df_daily_cases[df_daily_cases['Date']>'2022-05-01']
    fig = px.line(df_daily_cases, x="Date", y="Total Cases", color="Country", title="The total number of cases")
    fig.show()


def daily_changes(df_worldwide_cases: pd.DataFrame, df_daily_cases: pd.DataFrame):
    
    # Find the topK countries
    countries = get_highest_cases(df_worldwide_cases, topK=5)
    df_daily_cases = df_daily_cases[df_daily_cases["Country"].isin(countries)]

    # We need to unpivot the daily cases dataframe to have a date column
    df_daily_cases = df_daily_cases.melt(id_vars='Country', var_name='Date', value_name='Cases')
    df_daily_cases['Total Cases'] = df_daily_cases[['Country', 'Cases']].groupby('Country').cumsum()
    df_daily_cases = df_daily_cases[df_daily_cases['Date']>'2022-08-01']
    fig = px.bar(df_daily_cases,
                 x="Date", y="Cases", color="Country",
                  title="Daily Changes")
    fig.show()

def timeline(df_worldwide_cases: pd.DataFrame):
    df = df_worldwide_cases.copy()
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
    plt.plot(world_date, world_count, label="World")
    us_date = list(us_counter.keys())
    us_count = list(us_counter.values())
    plt.plot(us_date, us_count, label="US")
    plt.legend()
    plt.xticks(world_date[25::25])
    plt.title('Confirmed Cases in the World and the US')
    plt.xlabel('Dates')
    plt.ylabel('Number of Cases')
    plt.show()
    
def histogram(df_cases_worldwide: pd.dataframe):
    df = df_cases_worldwide.copy()
    conf = mean(df['Confirmed_Cases'].tolist())
    hosp = mean(df['Hospitalized'].tolist())
    trav = mean(df['Travel_History_Yes'].tolist())

    plt.bar(['US','World'], [24403, conf])
    plt.title('Confirmed')
    plt.ylabel('Number of Cases')
    plt.show()
    plt.clf()
    plt.bar(['US','World'], [4, hosp])
    plt.title('Hospitalized')
    plt.ylabel('Number of Cases')
    plt.show()
    plt.clf()
    plt.bar(['US','World'], [41, trav])
    plt.title('Travel History')
    plt.ylabel('Number of Cases')
    plt.show()
