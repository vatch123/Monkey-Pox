import os
import re
import pandas as pd
import numpy as np
import matplotlib
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

def parse_symptoms(df_detection_timeline: pd.DataFrame):
    symptoms: pd.DataFrame = df_detection_timeline[["Symptoms"]]
    symptoms["Symptoms"].replace(np.nan,"NA",inplace = True)
    symptoms = symptoms[symptoms["Symptoms"].isin(["NA"]) == False]
    symptoms["Symptoms"] = symptoms["Symptoms"].str.split(", | , | ,|;")
    symptoms = symptoms.explode("Symptoms")

    # Replace similar symptoms with a single
    symptoms.replace(regex=re.compile(r".*rash.*", flags=re.IGNORECASE), value="Rash", inplace=True)
    symptoms.replace(regex=re.compile(r".*headache.*", flags=re.IGNORECASE), value = "Headache", inplace=True)
    symptoms.replace(regex=re.compile(r".*pain.*", flags=re.IGNORECASE), value = "Muscle Pain", inplace=True)
    symptoms.replace(to_replace = ["Swelling","swelling of lymph nodes","enlarged lymph nodes","Slight swallowing difficulties and an elevated temperature"], value = "swollen lymph nodes", inplace=True)
    symptoms.replace(to_replace = ["lesions","skin manifestations","isolated skin lesions","lower abdomen skin lesions","Spots on skin","Three lesions typical of monkeypox"], value = "skin lesions", inplace=True)
    symptoms.replace(regex=re.compile(r".*fever.*", flags=re.IGNORECASE), value = "Fever", inplace=True)
    symptoms.replace(regex=re.compile(r".*algia.*", flags=re.IGNORECASE), value = "Myalgia", inplace=True)
    symptoms["Symptoms"] = symptoms["Symptoms"].str.title()

    return symptoms.groupby('Symptoms').size().reset_index(name='Count').sort_values('Count', ascending=False)

def save_fig(name):
    def show_and_save_plots(func):
        def plot(*args, **kwargs):
            # Get the figure
            fig = func(*args, **kwargs)
            # Save and show the plots
            plot_path = os.path.join(os.getcwd(), f'plots/{name}')
            if isinstance(fig, matplotlib.figure.Figure):
                fig.savefig(plot_path)
            else:
                fig.write_image(plot_path)
            return fig
        return plot
    return show_and_save_plots
