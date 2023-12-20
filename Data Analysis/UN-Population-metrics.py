
import matplotlib.pyplot as plt
import pandas as pd
#import numpy
#import OpenPyXL as pyxl
#import xlrd

excel_file = 'Data_Sources\WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx'
population = pd.read_excel(excel_file)

# population.head()

estimates = pd.read_excel(excel_file, sheetname=0, index_col=3)
estimates.head()


data = pd.read_csv(
    'Data_Sources/Population.csv', index_col='Index')

# Extract year from last 4 characters of each column name
years = data.columns.str.strip('gdpPercap_')
# Convert year values to integers, saving results back to dataframe
data.columns = years.astype(int)

data.loc['Australia'].plot()

