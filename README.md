# ECE 143 Project: Monkey Pox Data Analysis

### **Team Members:** *Vatsalya Chaubey, Abhishek Suryavanshi, Raymond Urbina, Shayne Wang*

## Table of Contents:
- [Table of Contents:](#table-of-contents)
- [Directory Structure](#directory-structure)
- [Instructions to run project:](#instructions-to-run-project)
- [Directory Files:](#directory-files)
- [Data Directory:](#data-directory)
- [Plots Directory:](#plots-directory)
- [Project Motivation:](#project-motivation)
- [Presentation Directory:](#presentation-directory)
- [Youtube Presentation Link:](#youtube-presentation-link)

All the plots and analysis is present in the form of an interactive dashboard [here](https://vatch123-monkey-pox-main-eur34g.streamlit.app/).

## Directory Structure 
```
src
|____ __init__.py
|____ analysis.py
|____ clean.py
|____ utils.py
|____ visualizations.py
|
|__ main.py
|__ requirements.txt
|__ EDA_analysis.ipynb
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
pip install -r requirements.txt
```

Run the jupyter notebook `EDA_analysis.ipynb` cell by cell to go through the EDA and the analysis.

You can also run the `main.py` file to see the interactive plots by running the following command
```
streamlit run main.py
```

## Directory Files:
- `init.py`: Indicates that the files in a folder are part of a Python package.
- `analysis.py`: File contains analysis code for how hospitalization is affected by gender, age etc.
- `clean.py`: This cleans the data from the data sets by removing the unwanted nans and replacing them with NA. It also formats the data for the required columns for writing out to the clean data CVS file. 
- `utils.py`: This file contains the methods for reading and writing to Pandas data frames and other utilities.
- `visualizations.py`: This file has all the code to create visualization plots for the project.
- `main.py`: This file builds a `streamlit` app which helps us serve all our visualizations in an interactive way.
- `EDA_analysis.ipynb`: Exploratory Data Analysis file is a Jupyter notebook reads in the clean data sets in terms of dataframes.

## Data Directory:
This folder contains CSV data files that were used for the project, which includes both the raw data and clean data. 

## Plots Directory:
This folders contains all the plots generated for the project. 

## Project Motivation:
In May of 2022 a rare case of Monkeypox was diagnosed in the UK. Soon after, many other cases were reported in other areas of the world. Our motivation was to fulfill the ECE 143 project requirement but also learn about the spread of Monkeypox and predict the future of Monkeypox.


## Presentation Directory:
The presentations slides are in the presentation folder in pdf form. 

## Youtube Presentation Link: 
The link to the presentation video - https://youtu.be/cmSSiGZaN6I
