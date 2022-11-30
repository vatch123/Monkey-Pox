"""
Created on Thu Nov 27 23:59:59
@author: Abhishek Suryavanshi
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.utils import *


def basic_analysis(df_daily_country_wise_confirmed_cases, df_monkey_pox_cases_worldwide,
                   df_worldwide_case_detection_timeline):
    """
    Does basic analysis over the datasets
    params:df_daily_country_wise_confirmed_cases,df_monkey_pox_cases_worldwide,df_worldwide_case_detection_timeline
    type:pandas.DataFrame,pandas.DataFrame,pandas.DataFrame
    returns None
    """
    """
    This is a docstring explaining function definition
    """
    assert isinstance(df_daily_country_wise_confirmed_cases, pd.DataFrame) and isinstance(df_monkey_pox_cases_worldwide,
                                                                                          pd.DataFrame) and isinstance(
        df_worldwide_case_detection_timeline, pd.DataFrame)
    """Analyzing Shape of datasets in the input"""
    print("World Case Detection Timeline Dataset shape", df_worldwide_case_detection_timeline.shape)
    print("Monkey Pox Cases Worldwide Dataset shape", df_monkey_pox_cases_worldwide.shape)
    print("Daily Country Wise confirmed cases Dataset shape", df_daily_country_wise_confirmed_cases.shape)

    '''Duplicates in World Case Detection Timeline Dataset'''
    print("Number of duplicate entries in the world wide case detection dataset",
          df_worldwide_case_detection_timeline.duplicated().sum())
    temp_Worldwide_Case_Detection_Timeline = df_worldwide_case_detection_timeline.drop_duplicates()

    '''Info about Worldwide_Case_Detection_Timeline'''
    print(temp_Worldwide_Case_Detection_Timeline.shape)
    print(temp_Worldwide_Case_Detection_Timeline.info())

    '''Symptoms for worldwide monkey pox cases'''
    print(temp_Worldwide_Case_Detection_Timeline['Symptoms'].unique())
    print(temp_Worldwide_Case_Detection_Timeline['Symptoms'].mode())

    '''Printing out unique genders in our dataset'''
    print(temp_Worldwide_Case_Detection_Timeline['Gender'].unique())
    '''Dropping off the duplicates from worldwide_case_detection_timeline'''
    temp_Worldwide_Case_Detection_Timeline = df_worldwide_case_detection_timeline.drop_duplicates()
    print(temp_Worldwide_Case_Detection_Timeline.info())
    print(temp_Worldwide_Case_Detection_Timeline.Age.unique())

    temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].str.strip()
    temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].str.lower()
    temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].replace(np.nan,
                                                                                                                'NA')


def clean_worldwide(df_worldwide_case_detection_timeline):
    """
    Drops the duplicates in the worldwide case dataset and identifies unique genders in the dataset
    params:df_worldwide_case_detection_timeline
    type:pandas.DataFrame
    returns a clean worldwide dataset
    """
    """
    This is a docstring explaining function definition
    """
    assert isinstance(df_worldwide_case_detection_timeline, pd.DataFrame)
    temp_Worldwide_Case_Detection_Timeline = df_worldwide_case_detection_timeline.drop_duplicates()
    temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].str.strip()
    temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].str.lower()
    temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].replace(np.nan,
                                                                                                                'NA')
    return temp_Worldwide_Case_Detection_Timeline


def hospitalization_gender(df_worldwide_case_detection_timeline):
    """
    The function plots a graph between Hospitalization vs Gender
    params:df_worldwide_case_detection_timeline
    type:pandas.DataFrame
    returns None
    """
    """
    This is a docstring explaining function definition
    """
    assert isinstance(df_worldwide_case_detection_timeline, pd.DataFrame)
    temp_Worldwide_Case_Detection_Timeline = clean_worldwide(df_worldwide_case_detection_timeline)
    sns.set_style('whitegrid')
    _, axes = plt.subplots(figsize=(12, 8))
    ax = sns.countplot(x='Gender', hue='Hospitalised (Y/N/NA)', data=temp_Worldwide_Case_Detection_Timeline,
                       palette='YlGn')
    ax.tick_params(axis='x', rotation=90)
    for container in ax.containers:
        ax.bar_label(container)
    plt.title('Hospitalized Patients based on Gender')
    plt.show()


def virus_vs_age_group(df_worldwide_case_detection_timeline):
    """
    The function plots a graph  for Virus detected according to diff ages
    params:df_worldwide_case_detection_timeline
    type:pandas.DataFrame
    returns None
    """
    """
    This is a docstring explaining function definition
    """
    assert isinstance(df_worldwide_case_detection_timeline, pd.DataFrame)
    temp_Worldwide_Case_Detection_Timeline = clean_worldwide(df_worldwide_case_detection_timeline)
    temp_Worldwide_Case_Detection_Timeline['Age'] = temp_Worldwide_Case_Detection_Timeline['Age'].fillna('0')
    temp_Worldwide_Case_Detection_Timeline['Age'] = temp_Worldwide_Case_Detection_Timeline['Age'].apply(
        lambda x: np.array(x.split('-'), dtype=int).mean())
    temp_Worldwide_Case_Detection_Timeline['Age'] = np.ceil(temp_Worldwide_Case_Detection_Timeline['Age']).astype(int)

    temp_Worldwide_Case_Detection_Timeline.Age.value_counts().sort_values(ascending=False)
    ages_selected = temp_Worldwide_Case_Detection_Timeline[temp_Worldwide_Case_Detection_Timeline['Age'] > 0]

    figure = sns.histplot(ages_selected, x='Age', bins=25)
    patch_h = [patch.get_height() for patch in figure.patches]
    idx_tallest = np.argmax(patch_h)
    figure.patches[idx_tallest].set_facecolor('#a834a8')
    figure.set_title('Virus detected as per different age groups')
    plt.show()


def hospitalization_vs_age(df_worldwide_case_detection_timeline):
    """
    The function plots a graph  for Hospitalization vs Age
    params:df_worldwide_case_detection_timeline
    type:pandas.DataFrame
    returns None
    """
    """
    This is a docstring explaining function definition
    """
    assert isinstance(df_worldwide_case_detection_timeline, pd.DataFrame)
    temp_Worldwide_Case_Detection_Timeline = clean_worldwide(df_worldwide_case_detection_timeline)
    temp_Worldwide_Case_Detection_Timeline['Age'] = temp_Worldwide_Case_Detection_Timeline['Age'].fillna('0')
    temp_Worldwide_Case_Detection_Timeline['Age'] = temp_Worldwide_Case_Detection_Timeline['Age'].apply(
        lambda x: np.array(x.split('-'), dtype=int).mean())
    temp_Worldwide_Case_Detection_Timeline['Age'] = np.ceil(temp_Worldwide_Case_Detection_Timeline['Age']).astype(int)
    temp_Worldwide_Case_Detection_Timeline.Age.value_counts().sort_values(ascending=False)
    figure = sns.catplot(temp_Worldwide_Case_Detection_Timeline, x='Age', y='Hospitalised (Y/N/NA)')
    plt.title('Hospitalization according to different ages')
    plt.show()


def hospitalization_symptoms(df_worldwide_case_detection_timeline):
    """
    The function plots a graph  for Hospitalization vs Symptoms
    params:df_worldwide_case_detection_timeline
    type:pandas.DataFrame
    returns None
    """
    """
    This is a docstring explaining function definition
    """
    assert isinstance(df_worldwide_case_detection_timeline, pd.DataFrame)
    temp_Worldwide_Case_Detection_Timeline = clean_worldwide(df_worldwide_case_detection_timeline)
    fig = sns.histplot(temp_Worldwide_Case_Detection_Timeline, x='Symptoms', hue='Hospitalised (Y/N/NA)')
    fig.set_title('Hospitalization according to Symptoms')
    _, labels = plt.xticks()
    fig.set_xticklabels(labels, size=4, rotation=90)
    fig.grid(False)
    plt.show()


hospitalization_vs_age(df_worldwide_case_detection_timeline=read_data("Worldwide_Case_Detection_Timeline.csv"))
