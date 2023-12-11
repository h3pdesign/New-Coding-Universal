
# coding: utf-8

# ## Momente: Durchschnitt, Varianz, Schiefe (skew), Wölbung (kurtosis)

# 1.: Erstellen von normalverteilten Zufallsdaten

# In[16]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

vals = np.random.normal(0, 0.5, 10000)

plt.hist(vals, 50)
plt.show()


# Das erste, zentrale Moment ist der Durchschnitt. Dieser sollte ungefähr bei 0 liegen:

# In[10]:


np.mean(vals)


# Das zweite, zentrale moment ist die Varianz

# In[11]:


np.var(vals)


# Das dritte, zentrale Moment ist die Schiefe (skewness) des Graphen. Da es sich bei diesem Beispiel um eine Normalvereilung handelt, sollte die Schiefe ungefähr bei 0 liegen:

# In[12]:


import scipy.stats as sp
sp.skew(vals)


# Das vierte, zentrale Moment ist die Wölbung (kurtosis) des Graphen. Da es sich bei diesem Beispiel um eine Normalvereilung handelt, sollte die Wölbung auch bei ungefähr 0 liegen:

# In[15]:


sp.kurtosis(vals)


# ## Aufgabe

# Verstehe die Schiefe: Verändere die Normalverteilung so, dass sie sich um den Wert 10 statt um den Wert 0 verteilt. Welchen Effekt hat das auf die Momente?
# 
# #### Lösung
# 
# Die Schiefe ist weiterhin nahe an der 0, weil die Schiefe die Form der Verteilung beschreibt, und nicht die Position auf der X-Achse.
