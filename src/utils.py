import os
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2


def read_data(file: str) -> pd.DataFrame:
    """
    Read a file as a pandas dataframe

    Parameters
    ----------
    file: str
        The name of the file to be read
    Returns
    -------
    pd.DataFrame: The pandas dataframe
    """

    data_dir = os.path.join(os.getcwd(), 'data')
    return pd.read_csv(os.path.join(data_dir, file), encoding='unicode_escape')

def write_data(df: pd.DataFrame, file: str):
    """
    Write the given dataframe to a particular file
    """
    data_dir = os.path.join(os.getcwd(), 'data')
    df.to_csv(os.path.join(data_dir, file), index=False)


def get_continent(col):
    try:
        cn_a2_code =  country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown' 
    try:
        cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    except:
        cn_continent = 'Unknown' 
    return (cn_a2_code, cn_continent)


def geolocate(country):
    geolocator = Nominatim(user_agent='Vis')
    try:
        # Geolocate the center of the country
        loc = geolocator.geocode(country)
        # And return latitude and longitude
        return (loc.latitude, loc.longitude)
    except:
        # Return missing value
        return np.nan

def add_lat_long(df):
    """
    Add the latitude and longitude to the dataset based on the country names
    """
    df['Country-Continent'] = df['Country'].apply(get_continent)
    df['Lat-Long'] = df['Country-Continent'].apply(lambda x: geolocate(x[0]))
    df[['lat', 'lon']] = pd.DataFrame(df['Lat-Long'].to_list(), index=df.index)
    df = df.drop(['Lat-Long'], axis=1)
    return df

def get_highest_cases(df_worldwide_cases: pd.DataFrame, topK: int = 10):

    # Pick the topK countries who has the most cases at the moment
    df_worldwide_cases['Confirmed_Cases'] = df_worldwide_cases['Confirmed_Cases'].astype(int)
    df_worldwide_cases = df_worldwide_cases.sort_values('Confirmed_Cases', ascending=False)
    df_worldwide_cases = df_worldwide_cases.head(topK)

    return df_worldwide_cases["Country"]
