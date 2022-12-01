"""
Python module which contains all the data visualizations
"""
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from statistics import mean

from src.utils import get_highest_cases, read_data, save_fig, parse_symptoms


def cases_on_map(df_worldwide_cases: pd.DataFrame, region: str):
    """
    Returns a choropleth plot of number of cases in a given region

    Parameters
    ----------
    df_worldwide_cases: pd.DataFrame
        The DataFrame which contains country-wise data of cases
    region: str
        The region of the world - ["north america", "south america", "europe", "africa", "asia"]
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_worldwide_cases, pd.DataFrame) and isinstance(region, str)
    assert region in ["north america", "south america", "europe", "africa", "asia"]

    @save_fig(name=f"Total_cases_{region.replace( ' ', '_')}.png")
    def get_plot(df_worldwide_cases: pd.DataFrame, region:str):
        fig = px.choropleth(df_worldwide_cases,
                        locations='Country',
                        locationmode='country names',
                        color="Confirmed_Cases",
                        scope=region,
                        color_continuous_scale=px.colors.sequential.Blues_r,
                        title=f"Cases in {region.title()}",
                        labels={"Confirmed_Cases":"Confirmed Cases"})
        return fig
    
    return get_plot(df_worldwide_cases, region)

@save_fig(name='Case-Trends.png')
def case_trends(df_worldwide_cases: pd.DataFrame, df_daily_cases: pd.DataFrame):
    """
    Returns a line chart of total number of cases against the date for top 10 countries
    with the highest number of cases

    Parameters
    ----------
    df_worldwide_cases: pd.DataFrame
        The DataFrame which contains country-wise data of cases
    df_daily_cases: pd.DataFrame
        The dataframe which contains daily country wise number of cases info
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_worldwide_cases, pd.DataFrame) and isinstance(df_daily_cases, pd.DataFrame)
    
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
    """
    Returns a bar chart of number of cases detected on a day against the date for top 5 countries
    with the highest number of cases

    Parameters
    ----------
    df_worldwide_cases: pd.DataFrame
        The DataFrame which contains country-wise data of cases
    df_daily_cases: pd.DataFrame
        The dataframe which contains daily country wise number of cases info
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_worldwide_cases, pd.DataFrame) and isinstance(df_daily_cases, pd.DataFrame)

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
    """
    Returns a bar chart of number of cases detected in a city for top 5 cities
    with the highest number of cases

    Parameters
    ----------
    df_detection_timeline: pd.DataFrame
        The DataFrame which contains the case detection timeline
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_detection_timeline, pd.DataFrame)

    df_cities = df_detection_timeline[['City']]
    df_cities = df_cities.dropna()
    df_cities = df_cities.value_counts(['City']).reset_index(name='Total Cases')

    # Pick the top 10 cities with the highest case counts
    df = df_cities.loc[:10]
    fig = px.bar(df, x='City', y='Total Cases', title='Number of cases in city', color='City', text_auto=True)
    return fig

@save_fig(name="Suspected-cases.png")
def suspected_cases_bar(df_worldwide_cases: pd.DataFrame):
    """
    Returns a bar chart of number of suspected cases for top 10 countries with the
    highest number of suspected cases

    Parameters
    ----------
    df_worldwide_cases: pd.DataFrame
        The DataFrame which contains country-wise data of cases
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_worldwide_cases, pd.DataFrame)

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
    """
    Returns a grouped bar chart of number of confirmed cases where people have been
    hospitalized or who have a travel history for top 10 countries with the
    highest number of cases

    Parameters
    ----------
    df_worldwide_cases: pd.DataFrame
        The DataFrame which contains country-wise data of cases
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_worldwide_cases, pd.DataFrame)

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
def symptoms_distribution(df_detection_timeline: pd.DataFrame, topK=10):
    """
    Returns a polar bar chart of number of cases having a particular symptom for the topK
    most common symptoms

    Parameters
    ----------
    df_detection_timeline: pd.DataFrame
        The DataFrame which contains the case detection timeline
    topK: int
        The number of symptoms to choose
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_detection_timeline, pd.DataFrame) and isinstance(topK, int)

    symptoms: pd.DataFrame = parse_symptoms(df_detection_timeline)
    df = symptoms.head(topK)
    fig = px.bar_polar(df,
                    r='Count',
                    theta='Symptoms',
                    title='Distribution of Symptoms',
                    template="plotly_white",
                    color_discrete_sequence=px.colors.sequential.Plasma_r
                    )
    return fig

@save_fig(name="Symptoms-WordCloud.png")
def symptoms_word_cloud(df_detection_timeline: pd.DataFrame):
    """
    Returns a word cloud of all the symptoms

    Parameters
    ----------
    df_detection_timeline: pd.DataFrame
        The DataFrame which contains the case detection timeline
    Returns
    -------
        A matplotlib figure
    """
    assert isinstance(df_detection_timeline, pd.DataFrame)

    symptoms: pd.DataFrame = parse_symptoms(df_detection_timeline)
    word_cloud = WordCloud(background_color='white').generate(str(symptoms["Symptoms"].values))
    fig = plt.figure()
    plt.imshow(word_cloud)
    plt.axis("off")
    return fig

@save_fig(name="Correlation-Heatmap.png")
def correlation_heatmap(df_worldwide_cases: pd.DataFrame):
    """
    Returns a correlation heatmap between the various columns in the dataset

    Parameters
    ----------
    df_worldwide_cases: pd.DataFrame
        The DataFrame which contains country-wise data of cases
    Returns
    -------
        A plotly figure
    """
    assert isinstance(df_worldwide_cases, pd.DataFrame)

    df_worldwide_cases = df_worldwide_cases.drop(columns=['Country', 'Country-Continent', 'lat', 'lon', 'Suspected_Cases'])
    correlation = df_worldwide_cases.corr()
    fig = px.imshow(correlation,
                    text_auto=True,
                    title="Correlation Heatmap",
                    color_continuous_scale=px.colors.sequential.Blues_r)
    return fig

@save_fig(name="Timeline.png")
def US_world_timeline(df_detection_timeline: pd.DataFrame):
    """
    Returns a line chart of number of confirmed cases in US and the world.
    
    Parameters
    ----------
    df_detection_timeline: pd.DataFrame
        The DataFrame which contains the case detection timeline.
    Returns
    -------
        A matplotlib figure.
    """
    df = df_detection_timeline.copy()
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

    fig= plt.figure()
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

    return fig

def US_world_histogram(df_worldwide_cases: pd.DataFrame):
    """
    Returns a set of histograms compare the number of confirmed cases, 
    hospitalized cases, and travel history between US and the world.

    Parameters
    ----------
    df_worldwide_cases: pd.DataFrame
        The DataFrame which contains country-wise data of cases.
    Returns
    -------
        Three matplotlib figures.
    """
    df = df_worldwide_cases.copy()
    conf = mean(df['Confirmed_Cases'].tolist())
    hosp = mean(df['Hospitalized'].tolist())
    trav = mean(df['Travel_History_Yes'].tolist())

    conf_fig = plt.figure()
    plt.bar(['US','World'], [24403, conf])
    plt.title('Confirmed')
    plt.ylabel('Number of Cases')

    hosp_fig = plt.figure()
    plt.bar(['US','World'], [4, hosp])
    plt.title('Hospitalized')
    plt.ylabel('Number of Cases')

    trav_fig = plt.figure()
    plt.bar(['US','World'], [41, trav])
    plt.title('Travel History')
    plt.ylabel('Number of Cases')

    return (conf_fig, hosp_fig, trav_fig)

if __name__=="__main__":
    df_worldwide_cases = read_data('Monkey_Pox_Cases_Worldwide_Cleaned.csv')
    df_daily_cases = read_data('Daily_Country_Wise_Confirmed_Cases.csv')
    df_detection_timeline = read_data('Worldwide_Case_Detection_Timeline_Cleaned.csv')
    US_world_timeline(df_detection_timeline)
