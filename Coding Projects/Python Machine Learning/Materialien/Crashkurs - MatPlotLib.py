
# coding: utf-8

# # MatPlotLib - Grundlagen

# ## Linie zeichnen

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-3, 3, 0.01)

plt.plot(x, norm.pdf(x))
plt.show()


# In[2]:


plt.plot(x, norm.pdf(x))
plt.plot(x, norm.pdf(x, 1.0, 0.5))
plt.show()


# ## Save it to a File

# In[8]:


plt.plot(x, norm.pdf(x))
plt.plot(x, norm.pdf(x, 1.0, 0.5))
plt.savefig('grafik.png', format='png')


# ## Achsen anpassen

# In[10]:


axes = plt.axes()
axes.set_xlim([-5, 5])
axes.set_ylim([0, 1.0])
axes.set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
plt.plot(x, norm.pdf(x))
plt.plot(x, norm.pdf(x, 1.0, 0.5))
plt.show()


# ## Hilfslinien anpassen

# In[6]:


axes = plt.axes()
axes.set_xlim([-5, 5])
axes.set_ylim([0, 1.0])
axes.set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
axes.grid()
plt.plot(x, norm.pdf(x))
plt.plot(x, norm.pdf(x, 1.0, 0.5))
plt.show()


# ## Change Line Types and Colors

# In[21]:


axes = plt.axes()
axes.set_xlim([-5, 5])
axes.set_ylim([0, 1.0])
axes.set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
axes.grid()
plt.plot(x, norm.pdf(x), 'm-')
plt.plot(x, norm.pdf(x, 1.0, 0.5), 'r-')
plt.show()


# Verfügbare Farben:
# 
# * b: blue
# * g: green
# * r: red
# * c: cyan
# * m: magenta
# * y: yellow
# * k: black
# * w: white

# ## Beschriftungen hinzufügen

# In[26]:


axes = plt.axes()
axes.set_xlim([-5, 5])
axes.set_ylim([0, 1.0])
axes.set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
axes.grid()
plt.xlabel('Anzahl')
plt.ylabel('Wahrscheinlichkeit')
plt.plot(x, norm.pdf(x), 'b-')
plt.plot(x, norm.pdf(x, 1.0, 0.5), 'r:')
plt.legend(['Äpfel', 'Birne'], loc=4)
plt.show()


# ## XKCD Style :)

# In[32]:


plt.xkcd()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xticks([])
plt.yticks([])
ax.set_ylim([-30, 10])

data = np.ones(100)
data[70:] -= np.arange(30)

plt.annotate(
    'DER TAG AN DEM ICH GEMERKT\nHABE, DASS ICH BACON ESSEN\nKANN WANNIMMER ICH WILL',
    xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(5, -10))

plt.plot(data)

plt.xlabel('Zeit')
plt.ylabel('Meine Gesundheit')


# ## Tortendiagramm

# In[55]:


# Remove XKCD mode:
plt.rcdefaults()

values = [12, 55, 4, 32, 14]
colors = ['r', 'g', 'b', 'c', 'm']
explode = [0, 0, 0.2, 0, 0]
labels = ['Österreich', 'Deutschland', 'Schweiz', 'Rest Europa', 'Rest Welt']
plt.pie(values, colors= colors, labels=labels, explode = explode)
plt.title('Herkunft der Teilnehmer')
plt.show()


# ## Balkendiagramm

# In[39]:


values = [12, 55, 4, 32, 14]
colors = ['r', 'g', 'b', 'c', 'm']
plt.bar(range(0,5), values, color= colors)
plt.show()


# ## Punktdiagramm

# In[48]:


from pylab import randn

X = randn(500)
Y = randn(500)
plt.scatter(X,Y)
plt.show()


# ## Histogramm

# In[41]:


incomes = np.random.normal(27000, 15000, 10000)
plt.hist(incomes, 50)
plt.show()


# ## Box & Whisker - Diagramm

# Sehr nützlich um sowohl die Verteilung als auch die Schiefe von Daten zu visualisieren.
# 
# Die rote Linie ist der Median der Daten, die Box drum herum repräsentiert die Grenzen des 1. bzw. 3. Quartil. 
# 
# => Die Hälfte der Daten ist innerhalb der Box.
# 
# Die gepunktetete Linie ("whiskers") stellt den Bereich der Daten da - ausgenommen der Ausreißer, die außerhalb der Linie dargestellt werden. Ausreißer sind weiter weiter als 1,5 mal den Interquartilen Abstand vom Median entfernt.
# 
# In diesem Beispiel werden gleichverteilte Zufallsdaten generiert mit Zahlen zwischen -40 und 60, plus ein paar Ausreißer über 100 bzw. unter -100. 

# In[44]:


uniformSkewed = np.random.rand(100) * 100 - 40
high_outliers = np.random.rand(10) * 50 + 100
low_outliers = np.random.rand(10) * -50 - 100
data = np.concatenate((uniformSkewed, high_outliers, low_outliers))
plt.boxplot(data)
plt.show()


# ## Aufgabe

# Versuche, ein Punktediagramm zu erstellen, auf dem Zufallsdaten von Alter auf der X-Achse und Zeit vor dem Fernseher auf der Y-Achse abgetragen werden. Beschrifte die Achsen.
