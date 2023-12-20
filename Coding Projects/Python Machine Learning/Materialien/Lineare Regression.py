
# coding: utf-8

# # Lineare Regression

# Zuerst werden ein paar Zufallsdaten generiert, die fast einen linearen Zusammenhang aufweisen:

# In[7]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
from pylab import *

pageSpeeds = np.random.normal(3.0, 1.0, 1000)
purchaseAmount = 100 - (pageSpeeds + np.random.normal(0, 0.1, 1000)) * 3

scatter(pageSpeeds, purchaseAmount)


# Da in diesem Graphen nur 2 Dimensinoen sind (X- und Y-Achse), kann man "stats.linregress" verwenden.

# In[3]:


from scipy import stats

slope, intercept, r_value, p_value, std_err = stats.linregress(pageSpeeds, purchaseAmount)


# Wie zu erwarten, deutet r^2 auf eine ziemlich gute Annäherung hin:

# In[8]:


r_value ** 2


# Was bedeutet slope / intercept? Die Geradengleichung ist f(x) = mx + b:
# 
# - slope: m
# - intercept: b
# 
# Mit diesem Wissen stelle man nun die Geradengleichung auf:

# In[12]:


import matplotlib.pyplot as plt

def predict(x):
    return slope * x + intercept

fitLine = predict(pageSpeeds)

plt.scatter(pageSpeeds, purchaseAmount)
plt.plot(pageSpeeds, fitLine, c='r')
plt.show()


# ## Aufgabe

# Versuche die Zufallsdaten so anzupassen, dass sie nicht mehr ganz so nah an an der roten Linie liegen. Was für einen Effekt hat das auf den Graphen bzw. r-Quadrat?
