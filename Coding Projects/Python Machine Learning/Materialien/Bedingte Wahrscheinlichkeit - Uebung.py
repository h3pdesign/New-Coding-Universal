
# coding: utf-8

# # Bedingte Wahrscheinlichkeit (inkl. Übung)

# Zuerst erstellen wir ein paar Zufallsdaten über die Anzahl der Einkäufe in einem Online-Shop für Personen in Abhängigkeit zum Alter. 
# 
# Der Code generiert 100.000 zufällige "Personen" und sortiert jede dieser Personen in die Alterskategorie 20-er, 30-er, 40-er, 50-er, 60-er oder 70-er ein.
# 
# Je geringer das Alter, desto geringer ist die Wahrscheinlichkeit, dass diese Person im Online-Shop einkauft. 
# 
# Anschließend wurden zwei Python dictionaries erstellt:
# 
# - "totals": Enthält die Anzahl an Personen pro Altersgruppe
# - "purchases": Enthält die Anzahl der Einkäufe pro Altersgruppe
# 
# Die gesamten Ausgaben über alle Altersgruppen ist in "totalPurchases" gespeichert. Die gesamte Anzahl aller Personen ist festgesetzt auf 100.000. 

# In[33]:


from numpy import random
random.seed(0)

totals = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
purchases = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
totalPurchases = 0
for _ in range(100000):
    ageDecade = random.choice([20, 30, 40, 50, 60, 70])
    purchaseProbability = float(ageDecade) / 100.0
    totals[ageDecade] += 1
    if (random.random() < purchaseProbability):
        totalPurchases += 1
        purchases[ageDecade] += 1


# In[34]:


totals


# In[24]:


purchases


# In[25]:


totalPurchases


# Berechnen der bedingten Wahrscheinlichkeit.
# 
# Berechne P(E|F), E entspricht hierbei dem Einkauf, und F bedeutet, dass die Person in ihren 30-ern ist. Die Wahrscheinlichkeit dass eine einzelne Person in ihren 30-ern etwas kauft entspricht dem Prozentsatz aller Personen in den 30-ern, die etwas gekauft haben:

# In[26]:


PEF = purchases[30] / totals[30]
print("P(purchase | 30s): " + str(PEF))


# P(F) ist die Wahrscheinlichkeit, dass jemand in unserem Datensatz in den 30-ern ist:

# In[27]:


PF = totals[30] / 100000.0
print("P(30's): " + str(PF))


# Und P(E) ist die Wahrscheinlichkeit, dass jemand bei uns etwas kauft, unabhängig vom Alter:

# In[28]:


PE = totalPurchases / 100000.0
print("P(Purchase):" + str(PE))


# Wenn E und F voneinander unabhängig sind, dann würden wir erwarten, dass P(E | F) das Gleiche ist wie P(E). Das ist aber nicht der Fall, P(E) ist 0,45 und P(E | F) ist 0,3. Das bedeutet, dass E und F voneinander abhängig sind (ist in diesem Beispiel klar, weil wir die Zufallsdaten entsprechend generiert haben).
# 
# Was ist P(E)P(F)?
# 

# In[29]:


print("P(30's)P(Purchase)" + str(PE * PF))


# ________
# 
# P(E ∩ F) beschreibt etwas anderes als P(E|F). P(E ∩ F) ist die Wahrscheinlichkeit, dass beides auftritt: Eine Person ist in ihren 30-ern, und kauft etwas bei uns ein. Diese Wahrscheinlichkeit bezieht sich also auf die Gesamtbevölkerung, nicht nur die Anzahl an Personen in den 30-ern: 

# In[30]:


print("P(30's ∩ Purchase)" + str(float(purchases[30]) / 100000.0))


# P(E ∩ F) ist nicht das gleiche wie P(E)P(F), da E und F voneinander abhängig sind! 
# 
# Man kann jetzt auch überprüfen, dass P(E|F) = P(E ∩ F)/P(F) ist. Das ist der Fall:

# In[35]:


print((purchases[30] / 100000.0) / PF)


# __________

# ## Aufgabe

# Passe den Code so an, dass die Wahrscheinlichkeit eines Einkaufs nicht vom Alter abhängt. E und F sind dann unabhängig voneinander. 
# 
# Überprüfe dann, dass P(E|F) ungefähr genauso groß ist wie P(E). Zeige damit, dass die bedingte Wahrscheinlichkeit eines Einkaufes nicht vom Alter des Besuchers abhängig, also davon unabhängig ist.
