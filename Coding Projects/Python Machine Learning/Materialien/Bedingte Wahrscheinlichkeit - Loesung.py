
# coding: utf-8

# # Bedingte Wahrscheinlichkeit - Lösung

# Zuerst wird der Code angepasst, sodass die Personen mit einer festen Wahrscheinlichkeit einem Alter zugeordnet werden (hier: 40%):

# In[14]:


from numpy import random
random.seed(0)

totals = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
purchases = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
totalPurchases = 0
for _ in range(100000):
    ageDecade = random.choice([20, 30, 40, 50, 60, 70])
    purchaseProbability = 0.4
    totals[ageDecade] += 1
    if (random.random() < purchaseProbability):
        totalPurchases += 1
        purchases[ageDecade] += 1


# Als nächstes wird P(E|F) für eine Altersgruppe berechnet:

# In[15]:


PEF = purchases[30] / totals[30]
print("P(purchase | 30s): " + str(PEF))


# Berechnen von P(E):

# In[16]:


PE = totalPurchases / 100000.0
print("P(Purchase):" + str(PE))


# P(E|F) sehr Nah an P(E), sodass P und E höchst Wahrscheinlich voneinander unabhängige Variablen sind.
