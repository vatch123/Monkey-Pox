from src.utils import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_Daily_Country_Wise_Confirmed_Cases = read_data('Daily_Country_Wise_Confirmed_Cases.csv')
df_Monkey_Pox_Cases_WorldWide = read_data('Monkey_Pox_Cases_WorldWide.csv')
df_Worldwide_Case_Detection_Timeline = read_data('Worldwide_Case_Detection_Timeline.csv')

'''Analyzing Shape of datasets in the input'''
print("World Case Detection Timeline Dataset shape", df_Worldwide_Case_Detection_Timeline.shape)
print("Monkey Pox Cases Worldwide Dataset shape", df_Monkey_Pox_Cases_WorldWide.shape)
print("Daily Country Wise confirmed cases Dataset shape", df_Daily_Country_Wise_Confirmed_Cases.shape)

'''Duplicates in World Case Detection Timeline Dataset'''
print("Number of duplicate entries in the world wide case detection dataset",df_Worldwide_Case_Detection_Timeline.duplicated().sum())
temp_Worldwide_Case_Detection_Timeline = df_Worldwide_Case_Detection_Timeline.drop_duplicates()

'''Info about Worldwide_Case_Detection_Timeline'''
print(temp_Worldwide_Case_Detection_Timeline.shape)
print(temp_Worldwide_Case_Detection_Timeline.info())

'''Symptoms for worldwide monkey pox cases'''
print(temp_Worldwide_Case_Detection_Timeline['Symptoms'].unique())
print(temp_Worldwide_Case_Detection_Timeline['Symptoms'].mode())

'''Case according to the gender'''
print(temp_Worldwide_Case_Detection_Timeline['Gender'].unique())
temp_Worldwide_Case_Detection_Timeline = df_Worldwide_Case_Detection_Timeline.drop_duplicates()
# print(temp_Worldwide_Case_Detection_Timeline.info())

temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].str.strip()
temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].str.lower()
temp_Worldwide_Case_Detection_Timeline['Gender'] = temp_Worldwide_Case_Detection_Timeline['Gender'].replace(np.nan,
                                                                                                            'NA')
"""
Hospitalization vs Gender 
"""
sns.set_style('whitegrid')
fig, axes = plt.subplots(figsize=(12, 8))
ax = sns.countplot(x='Gender', hue='Hospitalised (Y/N/NA)', data=temp_Worldwide_Case_Detection_Timeline, palette='YlGn')
ax.tick_params(axis='x', rotation=90)
for container in ax.containers:
    ax.bar_label(container)
plt.title('Hospitalized Patients based on Gender')
plt.show()

print(temp_Worldwide_Case_Detection_Timeline.Age.unique())
"""
Virus detected according to diff ages
"""
temp_Worldwide_Case_Detection_Timeline['Age'] = temp_Worldwide_Case_Detection_Timeline['Age'].fillna('0')
temp_Worldwide_Case_Detection_Timeline['Age'] = temp_Worldwide_Case_Detection_Timeline['Age'].apply(
    lambda x: np.array(x.split('-'), dtype=int).mean())
temp_Worldwide_Case_Detection_Timeline['Age'] = np.ceil(temp_Worldwide_Case_Detection_Timeline['Age']).astype(int)

temp_Worldwide_Case_Detection_Timeline.Age.value_counts().sort_values(ascending=False)
ages_selected = temp_Worldwide_Case_Detection_Timeline[temp_Worldwide_Case_Detection_Timeline['Age'] > 0]

fig = sns.histplot(ages_selected, x='Age', bins=25)
patch_h = [patch.get_height() for patch in fig.patches]
idx_tallest = np.argmax(patch_h)
fig.patches[idx_tallest].set_facecolor('#a834a8')
fig.set_title('Virus detected as per different age groups')
plt.show()

"""
Hospitalization vs Age
"""
fig = sns.catplot(temp_Worldwide_Case_Detection_Timeline, x='Age', y='Hospitalised (Y/N/NA)')
plt.title('Hospitalization according to different ages')
plt.show()

"""
Hospitalization vs Symptoms
"""
fig = sns.histplot(temp_Worldwide_Case_Detection_Timeline, x='Symptoms', hue='Hospitalised (Y/N/NA)')
fig.set_title('Hospitalization according to Symptoms')
_, labels = plt.xticks()
fig.set_xticklabels(labels, size=4, rotation=90)
fig.grid(False)
plt.show()
