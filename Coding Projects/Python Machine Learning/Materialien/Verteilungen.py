
# coding: utf-8

# # Beispiele: Verteilung von Daten

# ## Stetige Gleichverteilung (Uniform Distribution)

# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

values = np.random.uniform(-10.0, 10.0, 100000)
plt.hist(values, 50)
plt.show()


# ## Normalverteilung / Gauß-Verteilung

# Grafik zur Wahrscheinlichkeitsdichtefunktion (Englisch: Probability Density Function):

# In[3]:


from scipy.stats import norm
import matplotlib.pyplot as plt

x = np.arange(-3, 3, 0.001)
plt.plot(x, norm.pdf(x))


# Jetzt erzeugen wir ein paar normalverteilte Zufallswerte. "mu" ist der gewünschte Mittelwert, "sigma" die gewünschte Standardabweichung:

# In[11]:


import numpy as np
import matplotlib.pyplot as plt

mu = 5.0
sigma = 2.0
values = np.random.normal(mu, sigma, 10000)
plt.hist(values, 50)
plt.show()


# ## Exponentialverteilung

# In[5]:


from scipy.stats import expon
import matplotlib.pyplot as plt

x = np.arange(0, 10, 0.001)
plt.plot(x, expon.pdf(x))


# ## Binomialverteilung
# 
# Die Binomialverteilung ist eine diskrete Verteilung.
# 
# Also: Wahrscheinlichkeitsfunktion (Englisch: Probability Mass Function)

# In[6]:


from scipy.stats import binom
import matplotlib.pyplot as plt

n, p = 10, 0.5
x = np.arange(0, 10, 0.001)
plt.plot(x, binom.pmf(x, n, p))


# ## Poissonverteilung

# Beispiel: Meine Webseite hat jeden Tag im Schnitt 500 Besucher. Mit welcher Wahrscheinlichkeit besuchen an einem Tag genau 550 Besucher meine Webseite?

# In[7]:


from scipy.stats import poisson
import matplotlib.pyplot as plt

mu = 500
x = np.arange(400, 600, 0.5)
plt.plot(x, poisson.pmf(x, mu))


# ## Kurzes Quiz!

# Im kontinuierlichen verwendet man eine Wahrscheinlichkeitsdichtefunktion. Was verwendet man stattdessen bei diskreten Daten?

# ### Antwort
# Eine Wahrscheinlichtkeitsfunktion
