
# coding: utf-8

# # Python - Grundlagen

# ## Leertasten sind wichtig

# In[75]:


listOfNumbers = [1, 2, 3, 4, 5, 6]

for number in listOfNumbers:
    print(number)
    if (number % 2 == 0):
        print("ist gerade.")
    else:
        print("ist ungerade.")
        
print("Fertig!")


# ## Importieren von Modulen

# In[41]:


import numpy as np

A = np.random.normal(25.0, 5.0, 10)
print(A)


# ## Lists

# In[78]:


x = [1, 2, 3, 4, 5, 6]
print(len(x))


# In[43]:


x[:3]


# In[80]:


x[3:]


# In[45]:


x[-2:]


# In[46]:


x.extend([7,8])
x


# In[47]:


x.append(9)
x


# In[48]:


y = [10, 11, 12]
listOfLists = [x, y]
listOfLists


# In[49]:


y[1]


# In[50]:


z = [3, 2, 1]
z.sort()
z


# In[51]:


z.sort(reverse=True)
z


# ## Tupel

# In[52]:


# Tupel sind unveränderliche Listen. Für ein Tupel wird () statt [] verwendet.
x = (1, 2, 3)
len(x)


# In[53]:


y = (4, 5, 6)
y[2]


# In[54]:


listOfTuples = [x, y]
listOfTuples


# In[83]:


(age, income) = "32,120000".split(',')
print(age)
print(income)


# ## Dictionaries

# In[84]:


# Verhält sich ähnlich wie eine HashMap / Map in anderen Programmiersprachen
# (bzw. ein assoziatives Array in PHP)
captains = {}
captains["Enterprise"] = "Kirk"
captains["Enterprise D"] = "Picard"
captains["Deep Space Nine"] = "Sisko"
captains["Voyager"] = "Janeway"

print(captains)

print(captains["Voyager"])


# In[87]:


print(captains.get("Enterprise"))


# In[58]:


print(captains.get("NX-01"))


# In[59]:


for ship in captains:
    print(ship + ": " + captains[ship])


# ## Funktionen

# In[60]:


def squareIt(x):
    return x * x

print(squareIt(2))


# In[61]:


# Man kann Funktionen als Parameter übergeben
def doSomething(f, x):
    return f(x)

print(doSomething(squareIt, 3))


# In[62]:


# Mit Hilfe von Lambda-Funktionen können Funktionen direkt
# als Parameter übergeben werden
print(doSomething(lambda x: x * x * x, 3))


# ## Bool'sche Ausdrücke

# In[63]:


print(1 == 3)


# In[64]:


print(True or False)


# In[65]:


print(1 is 3)


# In[66]:


if 1 is 3:
    print("Wie kann das sein?")
elif 1 > 3:
    print("Komisch...")
else:
    print("Die Welt ist noch in Ordnung...")


# ## Schleifen

# In[67]:


for x in range(10):
    print(x)


# In[68]:


for x in range(10):
    if (x is 1):
        continue
    if (x > 5):
        break
    print(x)


# In[69]:


x = 0
while (x < 10):
    print(x)
    x += 1


# ## Aufgabe

# Schreibe ein Programm, welches eine Liste von Zahlen erstellt. Gebe dann mit Hilfe einer Schleife nur die geraden Zahlen aus!
