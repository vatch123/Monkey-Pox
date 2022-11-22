from src.utils import *
df_Daily_Country_Wise_Confirmed_Cases=read_data('Daily_Country_Wise_Confirmed_Cases.csv')
df_Monkey_Pox_Cases_WorldWide=read_data('Monkey_Pox_Cases_WorldWide.csv')
df_Worldwide_Case_Detection_Timeline=read_data('Worldwide_Case_Detection_Timeline.csv')

'''Analyzing Shape of datasets in the input'''
# print("World Case Detection Timeline Dataset shape",df_Worldwide_Case_Detection_Timeline.shape)
# print("Monkey Pox Cases Worldwide Dataset shape",df_Monkey_Pox_Cases_WorldWide.shape)
# print("Daily Country Wise confirmed cases Dataset shape",df_Daily_Country_Wise_Confirmed_Cases.shape)

'''Duplicates in World Case Detection Timeline Dataset'''
#print("Number of duplicate entries in the world wide case detection dataset",df_Worldwide_Case_Detection_Timeline.duplicated().sum())
temp_Worldwide_Case_Detection_Timeline=df_Worldwide_Case_Detection_Timeline.drop_duplicates()


'''Info about Worldwide_Case_Detection_Timeline'''
#print(temp_Worldwide_Case_Detection_Timeline.shape)
#print(temp_Worldwide_Case_Detection_Timeline.info())

'''Symptoms for worldwide monkey pox cases'''
#print(temp_Worldwide_Case_Detection_Timeline['Symptoms'].unique())
#print(temp_Worldwide_Case_Detection_Timeline['Symptoms'].mode())
# set_of_symptoms=set()
# for s in temp_Worldwide_Case_Detection_Timeline['Symptoms'].values:
#     set_of_symptoms.add(s)
# print(set_of_symptoms)

'''Case according to the gender'''
#print(temp_Worldwide_Case_Detection_Timeline['Gender'].unique())
temp_Worldwide_Case_Detection_Timeline['Gender']=temp_Worldwide_Case_Detection_Timeline['Gender'].str.lower()
temp_Worldwide_Case_Detection_Timeline['Gender']=temp_Worldwide_Case_Detection_Timeline['Gender'].str.strip()
# print(temp_Worldwide_Case_Detection_Timeline['Gender'].describe())

print(temp_Worldwide_Case_Detection_Timeline.info())
#Confirmed Cases
#print(df_Daily_Country_Wise_Confirmed_Cases.info())


