import pandas as pd

from src.utils import read_data, write_data, add_lat_long

def clean_data(file: str):
    """
    Cleans the Worldwide_Case_Detection_Timeline.csv by removing the nans with
    NA, and performing integration for the required columns

    Writes the saved the data to a Worldwide_Case_Detection_Timeline_Cleaned.csv

    Parameters
    ----------
    file: str
        Name of the file to be cleaned
    """
    assert isinstance(file, str)

    df = read_data(file)

    # All the columns are string so we can replace nans with NA
    df = df.fillna('NA')

    # Replace all values starting with 'm/M' as male and 'f/F' as female
    df['Gender'] = df['Gender'].apply(lambda x: 'M' if (x.startswith('m') or x.startswith('M')) else x)
    df['Gender'] = df['Gender'].apply(lambda x: 'F' if (x.startswith('f') or x.startswith('F')) else x)

    # Replace the spelling mistake in San Francisco's name
    df.replace(to_replace='San Francsico', value='San Francisco', inplace=True)

    # All the other columns either contain a valid string or NAs

    output_file = file.split('.')[0] + "_Cleaned.csv"
    write_data(df, output_file)

def add_geospatial_attributes(file: str):
    """
    Adds the latitude and longitude for each country to the dataset and saves the data to
    a new file suffixed with `_Cleaned`

    Parameters
    ----------
    file: str
        The name of the file to read data from
    """
    assert isinstance(file, str)
    df = read_data(file)
    df = add_lat_long(df)
    output_file = file.split('.')[0] + "_Cleaned.csv"
    write_data(df, output_file)

if __name__=="__main__":
    clean_data("Worldwide_Case_Detection_Timeline.csv")
    add_geospatial_attributes("Monkey_Pox_Cases_Worldwide.csv")
