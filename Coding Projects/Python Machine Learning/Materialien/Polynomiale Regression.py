
# coding: utf-8

# # Polynomiale Regression

# Was tun, wenn die Daten überhaupt keinen linearen Zusammenhang aufweisen? Betrachtet wir mal etwas realitischere Ladezeit / Einkäufe Daten: 

# In[26]:


get_ipython().run_line_magic('matplotlib', 'inline')
from pylab import *
import numpy as np

np.random.seed(2)
pageSpeeds = np.random.normal(3.0, 1.0, 1000)
purchaseAmount = np.random.normal(50.0, 10.0, 1000) / pageSpeeds

scatter(pageSpeeds, purchaseAmount)


# Das Paket numpy hat hierfür eine praktische polyfit-Funktion, die es uns erlaubt ein Polynom n-ter Ordnung auf Basis der gegebenen Punkte zu berechnen. Dieses Polynom minimiert den quadierten Fehler. Man erstelle ein Polynom 4. Ordnung: 

# In[27]:


x = np.array(pageSpeeds)
y = np.array(purchaseAmount)

p4 = np.poly1d(np.polyfit(x, y, 4))


# Man visualisiere das obigen Punktediagramm, und zeichne da drüber das Polynom für den Bereich zwischen 0-7 Sekunden: 

# In[28]:


import matplotlib.pyplot as plt

xp = np.linspace(0, 7, 100)
plt.scatter(x, y)
plt.plot(xp, p4(xp), c='r')
plt.show()


# Sieht gut aus! Aber was ist r^2? 

# In[22]:


from sklearn.metrics import r2_score

r2 = r2_score(y, p4(x))

print(r2)


# ## Aufgabe

# Spiele etwas mit den verschiedenen Ordnungen herum. Kann man mit einer höheren Ordnung eine bessere Annährung finden? Findest du eine Ordnung, bei der Überanpassung auftritt, obwohl der r-Quadrat - Wert weiterhin gut aussieht?
