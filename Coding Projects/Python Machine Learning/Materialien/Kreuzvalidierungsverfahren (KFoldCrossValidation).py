
# coding: utf-8

# # Kreuzvalidierungsverfahren (K-Fold Cross Validation)

# Betrachten wir erneut die Iris - Daten (Schwertlilien):

# In[1]:


import numpy as np
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm

iris = datasets.load_iris()


# Mit der train_test_split - Funktion lassen sich die Daten in train/test - Daten aufteilen.

# In[3]:


# Aufteilen der Iris-Daten in ein train/test - Set, 40% der Daten werden zum Testen verwendet
X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)

# Mit Hilfe des SVC (Support Vector Clustering) wird ein Modell erstellt. Hierfür wird
# der lineare Kernel verwendet
clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)

# Wie genau ist der Algorithmus?
clf.score(X_test, y_test)   


# Um das Kreuzvalidierungsverfahren zu benutzen, kann die Methode cross_val_score benutzt werden. 

# In[5]:


# cross_val_score wird hierfür das Modell übergeben, die gesamten Daten,
# und die "korrekten" Werte. Zudem muss die Anzahl für K übergeben werden.
scores = cross_validation.cross_val_score(clf, iris.data, iris.target, cv=5)

# Wie genau war jedes dieser Modelle?
print(scores)

# Und wie genau wird das resultierende Modell sein?
print(scores.mean())


# Dieses Modell ist nochmal etwas besser! Kann man es noch weiter verbessern? Probieren wir mal einen anderen Kernel aus (poly): 

# In[4]:


clf = svm.SVC(kernel='poly', C=1).fit(X_train, y_train)
scores = cross_validation.cross_val_score(clf, iris.data, iris.target, cv=5)
print scores
print scores.mean()


# Leider nicht! Der polynomiale Kernel führt zu einer geringeren Genauigkeit im Vergleich zum linearen Kernel. Dieser Kernel passt sich also zu stark an die Daten an. Ein einfaches train/test hätte das aber nicht herausgefunden: 

# In[7]:


# Erstelle ein SVC - Modell (Support Vector Clustring), welches den Aufbau
# der Blütenblätter vorhersagt
clf = svm.SVC(kernel='poly', C=1).fit(X_train, y_train)

# Messen der Genauigkeit auf Basis unserer Testdaten
clf.score(X_test, y_test)   


# Gleicher score wie beim train/test mit dem linearen Kernel!

# ## Aufgabe

# Der "poly" - Kernel erlaubt noch einen weiteren, sehr wichtigen Parameter:
#  - Welchen Grad hat das Polynom, was für diesen Kernel verwendet wird? Standardmäßig wird hier die 3 verwendet. 
#  
# Beispiel: `svm.SVC(kernel='poly', degree=3, C=1)` 
# 
# Passt ein Kernel bei dem nur ein Polynom 2. Grades verwendet wird, sich auch zu stark an die Daten an? Probier es aus und vergleiche das Ergebnis mit dem Ergebnis des linearen Kernels.
