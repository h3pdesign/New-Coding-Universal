
# coding: utf-8

# # Standardabweichung und Varianz

# In[10]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

incomes = np.random.normal(100.0, 50.0, 10000)

plt.hist(incomes, 50)
plt.show()


# In[11]:


incomes.std()


# In[12]:


incomes.var()


# ## Aufgabe

# Spiel mit verschiedenen Parametern bei der np.random.normal - Funktion herum, und schaue dir an, welchen Einfluss die verschiedenen Parameter auf die Verteilung haben. Wie verhält sich die Grafik zur neuen Standardabweichung bzw. Varianz?
