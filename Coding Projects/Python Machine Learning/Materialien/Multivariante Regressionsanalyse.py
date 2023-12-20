
# coding: utf-8

# # Multivariante Regressionsanalyse

# Zuerst lese man eine Datei mit Beispieldaten ein. Hier z.B. über tatsächliche Verkaufspreise von Autos (in den USA):

# In[2]:


import pandas as pd

df = pd.read_excel('http://cdn.sundog-soft.com/Udemy/DataScience/cars.xls')


# df.head() zeigt den Tabellenkopf sowie die ersten paar Zeilen an:

# In[3]:


df.head()


# Man kann jetzt mit Hilfe von Panda die Matrix in für uns relevante Attributvektoren zerlegen. X sind hierbei die Ausgangsdaten, Y das was wir versuchen vorherzusagen. 
# 
# Hierbei ist es wichtig, dass alle Daten einer Zahl zugeordnet werden. Das ist bei dem Attribut "Model" nicht der Fall, daher wird dieses Attribut mit Hilfe pandas.Categorical() in eine ordinale Zahl umgewandelt.

# In[3]:


import statsmodels.api as sm

df['Model_ord'] = pd.Categorical(df.Model).codes
X = df[['Mileage', 'Model_ord', 'Doors']]
y = df[['Price']]

X1 = sm.add_constant(X)
est = sm.OLS(y, X1).fit()

est.summary()


# In der mittleren Tabelle werden in der Spalte der Koeffizienten die Werte für folgende Formel angegeben:
# 
# >B0 + B1 \* Mileage + B2 \* model_ord + B3 \* doors
# 
# Achtung! Die Koeffizienten geben nur bei normalisierten Daten an ob eine Spalte relevant ist oder nicht. Daher hier: Standardabweichung betrachten. 
# 
# In diesem Beispiel wird sehr deutlich, dass der Kilometerstand (Mileage) einen entscheidenen Einfluss auf den Verkaufspreis hat (die Spalte mit der Standardabweichung ist relativ gering).
# 
# Aber hätte man das nicht schneller herausfinden können?

# In[9]:


y.groupby(df.Doors).mean()


# Mehr Türen = Gerinerer Verkaufspreis. Die Anzahl der Türen ist also - zumindest für dieses Beispiel - vermutlich ein recht nutzloser Schätzer für den tatsächlichen Verkaufspreis. Allerdings betrachten wir nur eine relativ kleine Menge an Daten, könnte sich auch einfach um ein paar Ausreißer handeln, die die Statistik beeinflussen.  

# ## Aufgabe

# Spiel mit den Daten herum. Kannst du andere Faktoren finden, die den Verkaufspreis beeinflussen? Lade dir die Excel-Datei herunter, füge noch ein paar Einträge hinzu. Wie verändern sich dann die Daten?
