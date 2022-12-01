import warnings

import streamlit as st

from src.analysis import *
from src.clean import *
from src.utils import read_data
from src.visualizations import *


if __name__=="__main__":
    warnings.filterwarnings("ignore")

    # This script would first clean the data and then run the visualization suite to generate
    # all the plots
    st.set_page_config(page_title="MonkeyPox Analysis", layout="wide")
    st.title("MonkeyPox: EDA and Analysis")

    # Data Cleaning
    # The code below is commented as cleaned data is already present in the data folder.
    # Uncomment them if you want to see them run
    
    # clean_data("Worldwide_Case_Detection_Timeline.csv")
    # add_geospatial_attributes("Monkey_Pox_Cases_Worldwide.csv")
    
    # Load the cleaned data
    df_worldwide_cases = read_data('Monkey_Pox_Cases_Worldwide_Cleaned.csv')
    df_daily_cases = read_data('Daily_Country_Wise_Confirmed_Cases.csv')
    df_detection_timeline = read_data('Worldwide_Case_Detection_Timeline_Cleaned.csv')

    
    # Generate all plots for the EDA

    st.header("Geographical spread of the disease")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(cases_on_map(df_worldwide_cases, region="north america"))
        st.plotly_chart(cases_on_map(df_worldwide_cases, region="south america"))
        st.plotly_chart(cases_on_map(df_worldwide_cases, region="europe"))
    with col2:
        st.plotly_chart(cases_on_map(df_worldwide_cases, region="asia"))
        st.plotly_chart(cases_on_map(df_worldwide_cases, region="africa"))

    st.header("Case trends and timelines")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(case_trends(df_worldwide_cases, df_daily_cases))
    with col2:
        st.plotly_chart(daily_changes(df_worldwide_cases, df_daily_cases))

    col1, col2 = st.columns(2)

    with col1:
        st.header("Most affected cities")
        st.plotly_chart(cases_cities(df_detection_timeline))
    with col2:
        st.header("Most suspected cases")
        st.plotly_chart(suspected_cases_bar(df_worldwide_cases))

    st.header("Symptoms")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(symptoms_word_cloud(df_detection_timeline))
    with col2:
        st.plotly_chart(symptoms_distribution(df_detection_timeline))
    
    st.header("Correlations - Hospitalization and Travel")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(correlation_heatmap(df_worldwide_cases))
    with col2:
        st.plotly_chart(hospitalized_and_travelled(df_worldwide_cases))

    st.header("Understand effects of gender, age on Hospitalizations")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(hospitalization_gender(df_detection_timeline))
        st.pyplot(hospitalization_vs_age(df_detection_timeline))
    with col2:
        st.pyplot(virus_vs_age_group(df_detection_timeline))
        st.pyplot(hospitalization_symptoms(df_detection_timeline))

    st.header("Comparison of US vs World")
    col1, col2 = st.columns(2)
    conf_fig, hosp_fig, trav_fig = US_world_histogram(df_worldwide_cases)
    with col1:
        st.pyplot(US_world_timeline(df_detection_timeline))
        st.pyplot(conf_fig)
    with col2:
        st.pyplot(hosp_fig)
        st.pyplot(trav_fig)
