"""
Python module which contains all the data visualizations
"""
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from src.utils import get_highest_cases, read_data, save_fig, parse_symptoms


@save_fig(name="Total-cases-NA.png")
def cases_NA_map(df_worldwide_cases: pd.DataFrame):

    fig = px.choropleth(df_worldwide_cases,
                        locations='Country',
                        locationmode='country names',
                        color="Confirmed_Cases",
                        scope="north america",
                        color_continuous_scale=px.colors.sequential.Blues_r,
                        title="Cases in North America",
                        labels={"Confirmed_Cases":"Confirmed Cases"})
    return fig

@save_fig(name="Total-cases-SA.png")
def cases_SA_map(df_worldwide_cases: pd.DataFrame):

    fig = px.choropleth(df_worldwide_cases,
                        locations='Country',
                        locationmode='country names',
                        color="Confirmed_Cases",
                        scope="south america",
                        color_continuous_scale=px.colors.sequential.Blues_r,
                        title="Cases in South America",
                        labels={"Confirmed_Cases":"Confirmed Cases"})
    return fig

@save_fig(name="Total-cases-EU.png")
def cases_EU_map(df_worldwide_cases: pd.DataFrame):

    fig = px.choropleth(df_worldwide_cases,
                        locations='Country',
                        locationmode='country names',
                        color="Confirmed_Cases",
                        scope="europe",
                        color_continuous_scale=px.colors.sequential.Blues_r,
                        title="Cases in Europe",
                        labels={"Confirmed_Cases":"Confirmed Cases"})
    return fig

@save_fig(name="Total-cases-AF.png")
def cases_AF_map(df_worldwide_cases: pd.DataFrame):

    fig = px.choropleth(df_worldwide_cases,
                        locations='Country',
                        locationmode='country names',
                        color="Confirmed_Cases",
                        scope="africa",
                        color_continuous_scale=px.colors.sequential.Blues_r,
                        title="Cases in Africa",
                        labels={"Confirmed_Cases":"Confirmed Cases"})
    return fig

@save_fig(name="Total-cases-AS.png")
def cases_AS_map(df_worldwide_cases: pd.DataFrame):

    fig = px.choropleth(df_worldwide_cases,
                        locations='Country',
                        locationmode='country names',
                        color="Confirmed_Cases",
                        scope="asia",
                        color_continuous_scale=px.colors.sequential.Blues_r,
                        title="Cases in Asia",
                        labels={"Confirmed_Cases":"Confirmed Cases"})
    return fig

@save_fig(name='Case-Trends.png')
def case_trends(df_worldwide_cases: pd.DataFrame, df_daily_cases: pd.DataFrame):
    
    # Find the topK countries
    countries = get_highest_cases(df_worldwide_cases)
    df_daily_cases = df_daily_cases[df_daily_cases["Country"].isin(countries)]

    # We need to unpivot the daily cases dataframe to have a date column
    df_daily_cases = df_daily_cases.melt(id_vars='Country', var_name='Date', value_name='Cases')
    df_daily_cases['Total Cases'] = df_daily_cases[['Country', 'Cases']].groupby('Country').cumsum()
    df_daily_cases = df_daily_cases[df_daily_cases['Date']>'2022-05-01']
    fig = px.line(df_daily_cases, x="Date", y="Total Cases", color="Country", title="The total number of cases")
    return fig

@save_fig(name="Daily-Changes.png")
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
    return fig

@save_fig("Cases-in-top-cities.png")
def cases_cities(df_detection_timeline: pd.DataFrame):
    df_cities = df_detection_timeline[['City']]
    df_cities = df_cities.dropna()
    df_cities = df_cities.value_counts(['City']).reset_index(name='Total Cases')

    # Pick the top 10 cities with the highest case counts
    df = df_cities.loc[:10]
    fig = px.bar(df, x='City', y='Total Cases', title='Number of cases in city', color='City', text_auto=True)
    return fig

@save_fig(name="Suspected-cases.png")
def suspected_cases_bar(df_worldwide_cases: pd.DataFrame):
    df = df_worldwide_cases.sort_values(["Suspected_Cases"],ascending=False).head(10)
    fig = px.bar(df,
                 x='Country', 
                 y='Suspected_Cases', 
                 title='Number of suspected cases in the country', 
                 color='Country',
                 text_auto=True
                )
    return fig

@save_fig(name="Hospitalization-Travelled.png")
def hospitalized_and_travelled(df_worldwide_cases: pd.DataFrame):
    # Find the data for countries with the highest cases
    countries = get_highest_cases(df_worldwide_cases)
    df_worldwide_cases = df_worldwide_cases[df_worldwide_cases["Country"].isin(countries)]

    fig = px.bar(df_worldwide_cases,
                 x='Country',
                 y=['Hospitalized', 'Travel_History_Yes'],
                 barmode='group',
                 title="Number of people Hospitalized / Travelled",
                 text_auto=True
                )
    return fig

@save_fig(name="Symptoms-pie.png")
def most_frequent_symptoms(df_detection_timeline: pd.DataFrame, topK=10):
    symptoms: pd.DataFrame = parse_symptoms(df_detection_timeline)
    df = symptoms.head(topK)
    fig = px.bar_polar(df,
                    r='Count',
                    theta='Symptoms',
                    title='Distribution of Symptoms',
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.sequential.Plasma_r
                    )
    return fig

@save_fig(name="Symptoms-WordCloud.png")
def symptoms_word_cloud(df_detection_timeline: pd.DataFrame, topK=10):
    symptoms: pd.DataFrame = parse_symptoms(df_detection_timeline)
    word_cloud = WordCloud(background_color='white').generate(str(symptoms["Symptoms"].values))
    fig = plt.figure()
    plt.imshow(word_cloud)
    plt.axis("off")
    return fig

@save_fig(name="Correlation-Heatmap.png")
def correlation_heatmap(df_worldwide_cases: pd.DataFrame):
    df_worldwide_cases = df_worldwide_cases.drop(columns=['Country', 'Country-Continent', 'lat', 'lon'])
    correlation = df_worldwide_cases.corr()
    fig = px.imshow(correlation,
                    text_auto=True,
                    title="Correlation Heatmap",
                    color_continuous_scale=px.colors.sequential.Blues_r)
    return fig

if __name__=="__main__":
    df_worldwide_cases = read_data('Monkey_Pox_Cases_Worldwide_Cleaned.csv')
    df_daily_cases = read_data('Daily_Country_Wise_Confirmed_Cases.csv')
    df_detection_timeline = read_data('Worldwide_Case_Detection_Timeline_Cleaned.csv')
    correlation_heatmap(df_worldwide_cases)
