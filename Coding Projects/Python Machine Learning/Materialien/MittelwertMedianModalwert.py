
# coding: utf-8

# # Mittelwert, Medianwert, Modalwert: Einführung in NumPy

# ## Mittelwert vs. Median

# Zuerst erstellen wir ein paar Musterdaten zu den Einkommen. Wir verwenden dazu eine Normalverteilung mit einer Standardabweichung von 15.000 sowie 10.000 Datenpunkten. (Wir werden die Fachbegriffe später noch genauer einführen, wenn du dich damit noch nicht auskennst - kein Problem)
# 
# Anschließend berechne den Durchschnitt (auf Englisch: mean) dieser Daten - er sollte ungefähr bei 27.000 liegen:

# In[29]:


import numpy as np

incomes = np.random.normal(27000, 15000, 10000)
np.mean(incomes)


# Wir teilen die Daten dann auf 50 Werte auf, und lassen uns das Histogramm ausgeben:

# In[30]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.hist(incomes, 50)
plt.show()


# Berechne jetzt den Medianwert (median) dieser Daten - da wir eine gleichmäßige Verteilung haben, sollte auch er bei ungefähr 27.000 liegen:

# In[31]:


np.median(incomes)


# Jetzt fügen wir Donald Trup zu den Einkommenswerten hinzu, und nehme hier mal ein recht hohes Einkommen an.

# In[32]:


incomes = np.append(incomes, [1000000000])


# Der Median verändert sich nicht wirklich, aber der Durchschnitt!

# In[33]:


np.median(incomes)


# In[34]:


np.mean(incomes)


# ## Modalwert

# Zuerst generieren wir ein paar zufällige Beispiel - Altersdaten.

# In[35]:


ages = np.random.randint(18, high=90, size=500)
ages


# Und berechnen dann den Modalwert:

# In[36]:


from scipy import stats
stats.mode(ages)

