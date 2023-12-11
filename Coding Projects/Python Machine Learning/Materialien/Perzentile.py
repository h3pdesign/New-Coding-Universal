
# coding: utf-8

# # Perzentile

# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

vals = np.random.normal(0, 0.5, 10000)

plt.hist(vals, 50)
plt.show()


# In[4]:


np.percentile(vals, 50)


# In[9]:


np.percentile(vals, 90)


# In[5]:


np.percentile(vals, 20)


# ## Aufgabe

# Probier auch mal andere Werte bei der Generierung der Normalverteilung aus. Wie verändern sich dann die Perzentile? 
