# %%
# Import the pandas library, renamed as pd
import pandas as pd

data_files = "../Data_Sources/"
csv_name = "CountryData.IND.csv"

# Read CountryData.IND into a DataFrame, assigned to df
df = pd.read_csv(f"{data_files}{csv_name}")

# Prints the first 5 rows of a DataFrame as default
df.head()

# Prints no. of rows and columns of a DataFrame
df.shape

# prints first 5 rows and every column which replicates df.head()
df.iloc[0:5, :]
# prints entire rows and columns
df.iloc[:, :]
# prints from 5th rows and first 5 columns
df.iloc[5:, :5]


# %%

# assigning two series to s1 and s2
s1 = pd.Series([1, 2])
s2 = pd.Series(["Ashish", "Sid"])
# framing series objects into data
df = pd.DataFrame([s1, s2])
# show the data frame
df

# data framing in another way
# taking index and column values
dframe = pd.DataFrame(
    [[1, 2], ["Ashish", "Sid"]], index=["r1", "r2"], columns=["c1", "c2"]
)
dframe

# %%

# import the required module
import matplotlib.pyplot as plt

# plot a histogram
df["Observation Value"].hist(bins=10)

# shows presence of a lot of outliers/extreme values
df.boxplot(column="Observation Value", by="Time period")

# plotting points as a scatter plot
x = df["Observation Value"]
y = df["Time period"]
plt.scatter(x, y, label="stars", color="m", marker="*", s=30)
# x-axis label
plt.xlabel("Observation Value")
# frequency label
plt.ylabel("Time period")
# function to show the plot
plt.show()

# %%

# import the required module
import matplotlib.pyplot as plt

# plot a histogram
df["Observation Value"].hist(bins=10)

# shows presence of a lot of outliers/extreme values
df.boxplot(column="Observation Value", by="Time period")

# plotting points as a scatter plot
x = df["Observation Value"]
y = df["Time period"]
plt.scatter(x, y, label="stars", color="m", marker="*", s=30)
# x-axis label
plt.xlabel("Observation Value")
# frequency label
plt.ylabel("Time period")
# function to show the plot
plt.show()

# %%
import pandas as pd

# Create a DataFrame
dframe = pd.DataFrame(
    {"Geeks": [23, 24, 22], "For": [10, 12, np.nan], "geeks": [0, np.nan, np.nan]},
    columns=["Geeks", "For", "geeks"],
)

# This will remove all the
# rows with NAN values

# If axis is not defined then
# it is along rows i.e. axis = 0
dframe.dropna(inplace=True)
print(dframe)

# if axis is equal to 1
dframe.dropna(axis=1, inplace=True)

print(dframe)

# %%
import numpy as np
import pandas as pd

# Create a DataFrame
dframe = pd.DataFrame(
    {"Geeks": [23, 24, 22], "For": [10, 12, np.nan], "geeks": [0, np.nan, np.nan]},
    columns=["Geeks", "For", "geeks"],
)

# Use fillna of complete Dataframe

# value function will be applied on every column
dframe.fillna(value=dframe.mean(), inplace=True)
print(dframe)

# filling value of one column
dframe["For"].fillna(value=dframe["For"].mean(), inplace=True)
print(dframe)

# %%
import pandas as pd
import numpy as np

# create DataFrame
dframe = pd.DataFrame(
    {
        "Geeks": [23, 24, 22, 22, 23, 24],
        "For": [10, 12, 13, 14, 15, 16],
        "geeks": [122, 142, 112, 122, 114, 112],
    },
    columns=["Geeks", "For", "geeks"],
)

# Apply groupby and aggregate function
# max to find max value of column

# &quot;For&quot; and column &quot;geeks&quot; for every
# different value of column &quot;Geeks&quot;.

print(dframe.groupby(["Geeks"]).max())


# %%
