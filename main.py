from src.utils import read_data
from src.visualizations import *


if __name__=="__main__":
    df_worldwide_cases = read_data('Monkey_Pox_Cases_Worldwide_Cleaned.csv')
    df_daily_cases = read_data('Daily_Country_Wise_Confirmed_Cases.csv')
    df_detection_timeline = read_data('Worldwide_Case_Detection_Timeline_Cleaned.csv')
    daily_changes(df_worldwide_cases, df_daily_cases)
