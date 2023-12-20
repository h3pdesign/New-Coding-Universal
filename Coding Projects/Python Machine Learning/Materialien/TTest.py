
# coding: utf-8

# # T-Test, P-Werte...

# Angenommen, man führt einen A/B - Test durch. Zuerst erstellen wir ein paar Zufallsdaten mit Umsätzen von Kunden in 2 Gruppen, A und B. B hat hierbei einen etwas höheren Umsatz:

# In[60]:


import numpy as np
from scipy import stats

A = np.random.normal(25.0, 5.0, 10000)
B = np.random.normal(26.0, 5.0, 10000)

stats.ttest_ind(A, B)


# Der T-Wert (*statistic*) ist die Maszahl zwischen den 2 Gruppen, ausgedrückt in Einheiten vom Standardfehler. Das bedeutet, dass dieser Test die Größe des Unterschiedes der 2 Gruppen, relativ zur Varianz in den Daten ausgibt.
# 
# Ein Hoher Wert für t bedeutet also, dass es einen echten Unterschied zwischen den 2 Datensätzen gibt, der Unterschied ist dann "signifikant".
# 
# Der P-Wert gibt an, mit welcher Wahrscheinlichkeit beide Gruppen identisch sind. Es könnte ja auch sein, dass wir aus einer der Gruppen nur etwas "extremere" Randwerte gemessen haben, die Gruppen aber grundsätzlich immernoch identisch sind. Ein niedriger Wert für P bedeutet also, dass das Ergebnis statistisch signifikant ist. 
# 
# Gesucht:
#  - Niedriger Wert für P
#  - Hoher Wert für T
# 
# Normalerweise ist der P-Wert wichtiger als der T-Wert, weil er einfacher vorzustellen ist. 
# 
# Passen wir nun mal die Gruppe A und B so an, dass sie beide die gleiche Verteilung haben. Es gibt also keinen "echten" Unterschied zwischen den Gruppen:

# In[61]:


B = np.random.normal(25.0, 5.0, 10000)

stats.ttest_ind(A, B)


# Jetzt ist der T-Wert (*statistic*) sehr viel geringer, und der P-Wert recht hoch. Diese Ergebnisse unterstützen die Nullhypothese: Dass es keinen Unterschied zwischen den 2 Gruppen gibt. 
# 
# Aber macht die Größe unserer Stichprobe einen Unterschied? Führen wir das Gleiche nochmal aus, also generieren 2 Gruppen die die gleiche Verteilung haben, aber mit 10X so vielen Messungen:

# In[62]:


A = np.random.normal(25.0, 5.0, 100000)
B = np.random.normal(25.0, 5.0, 100000)

stats.ttest_ind(A, B)


# Der P-Wert wird jetzt etwas geringer, der T-Wert etwas größer, aber nur unmerklich, man kann kaum einen Unterschied erkennen (insbesondere kann es passieren, dass der Wert aufgrund von Zufall doch größer geworden ist...)
# 
# Auch eine 1 Millionen Messungen reichen nicht aus, einen P-Wert von 1 und einen T-Wert von 0 zu bekommen:

# In[70]:


A = np.random.normal(25.0, 5.0, 1000000)
B = np.random.normal(25.0, 5.0, 1000000)

stats.ttest_ind(A, B)


# Nur wenn man die Gruppe mit sich selbst vergleicht, bekommt man - analog der Definition - einen T-Wert von 0 und einen P-Wert von 1:

# In[71]:


stats.ttest_ind(A, A)


# Man muss entscheiden, mit welcher Signifikanz, also was für einem Wert von P man sich zufrieden geben möchte. Man kann nie mit 100%-iger Wahrscheinlichkeit sagen, dass die Ergebnisse eines Experimentes "signifikant" sind. Aber immerhin, mit Hilfe des T-Tests bzw. dem P-Wert kann man eine Maßzahl für die Signifikanz bestimmen, und so ggf. feststellen, ob es Sinn macht, ein Experiment länger laufen zu lassen oder nicht. 

# ## Aufgabe

# Probier auch noch andere Verteilungen für A und B aus. Was für einen Einfluss hat dies auf die T-statistics bzw. den P-Wert?
