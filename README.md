<h1> ECE 143 Project: Monkey Pox Data Analysis <h1>

### **Team Members:** *Vatsalya Chaubey, Abhishek Suryavanshi, Raymond Urbina, Shayne Wang*

## Table of Contents:
- [Table of Contents:](#table-of-contents)
- [Directory Structure](#directory-structure)
- [Instructions to run project:](#instructions-to-run-project)
- [Directory Files:](#directory-files)
- [Data Folder Description:](#data-folder-description)
- [Project Motivation:](#project-motivation)
- [Presentation Slides:](#presentation-slides)
- [Youtube Presentation Link:](#youtube-presentation-link)


## Directory Structure 
```
src
|____ __init__.py
|____ utils.py
|____ visualizations.py
|
|__ main.py
|__ clean.py
|__ eda.ipynb
|__ analysis.py
```

## Instructions to run project:

__Usage__

Create a virtual environment
```shell
conda create -n monkey_pox Python=3.6
```

Clone the repository
```
git clone git@github.com:vatch123/Monkey-Pox.git
```

Change the directory
```
cd Monkey-Pox
```

Install all the dependencies
```
conda install --yes --file requirements.txt
```

Run the jupyter notebook `EDA_analysis.ipynb` cell by cell to go through the EDA and the analysis.

## Directory Files:
- init.py: Indicates that the files in a folder are part of a Python package.
- utils.py: This file contains the methods for reading and writing to Pandas data frames.
- visualizations.py: This file has all the code to create visualization plots for the project.
- main.py: This file reads in the clean data CSV files for world wide, daily and timeline and displays a daily changes graph for the 5 countries with the most changes in cases.
- clean.py: This cleans the data from the data sets by removing the unwanted nans and replacing them with NA. It also formats the data for the required columns for writing out to the clean data CVS file. 
- eda.ipynb: Exploratory Data Analysis file is a Jupyter notebook reads in the clean data sets in terms of dataframes.

## Data Folder Description:
This folder contains CSV data files that were used for the project, which includes both the raw data and clean data. 

## Project Motivation:
In May of 2022 a rare case of Monkeypox was diagnosed in the UK. Soon after, many other cases were reported in other areas of the world. Our motivation was to fulfill the ECE 143 project requirement but also learn about the spread of Monkeypox and predict the future of Monkeypox.


## Presentation Slides:
The presentations slides are in the presentation folder in pdf form. 

## Youtube Presentation Link: 
I will post link to presentation video after I record.
