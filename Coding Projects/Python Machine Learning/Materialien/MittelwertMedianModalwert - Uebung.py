
# coding: utf-8

# # Übung: Mittel- und Medianwert, Kaufverhalten von Kunden

# Zuerst generieren wir ein paar zufällige Daten mit denen wir später arbeiten können. Das erzeugt einfach ein Array mit dem Gesamtbetrag pro Einkauf. Klicke auf die Box und drücke die "play" - Taste um den Code auszuführen: 

# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

incomes = np.random.normal(100.0, 20.0, 10000)

plt.hist(incomes, 50)
plt.show()


# Ermittle jetzt den Durchschnitt und den Median von diesen Daten. Schreibe deinen Code in den Codeblock hier drunter, und überlege, ob dein Ergebnis Sinn machen könnte:

# Das ist jetzt eine sehr einfache Aufgabe, aber darum geht es nicht - es geht primär darum, etwas in iPython einzusteigen und numpy kennenzulernen. 
# 
# Versuch aber auf jeden Fall, noch etwas mit der Verteilung herumzuspielen, oder Außreißer zu den Daten hinzuzufügen. Wie beeinflusst das den Mittelwert / Medianwert / Graph?
