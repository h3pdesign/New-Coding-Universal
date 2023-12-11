
# coding: utf-8

# # Hauptkomponentenanalyse (Principal Component Analysis)

# Mit der Hauptkomponentenanalyse (Principal Component Analysis, PCA) kann die Dimensionalität von Daten reduziert werden. Hierbei wird versucht, möglichst viel der Varianz zu erhalten.
# 
# Das braucht man richtig oft. Betrachtet man z.B. ein Schwarz-Weiß-Bild. Dieses Bild kann mit drei Dimensionen beschrieben werden: Jedes Pixel hat eine X-Position, eine Y-Position und eine Helligkeit. Wenn man dieses Bild in nur 2 Dimensionen speichern könnte, würde man massiv Datenvolumen sparen. Die Hauptkomponentenanalyse kann dies tun, und hierbei wird versucht, weiterhin möglichst viel der Varianz zu erhalten.
# 
# Wir werden hier ein einfacheres Beispiel betrachten: Im sklearn-Paket ist der Iris-Datensatz enthalten, den wir in dieser Lektion analysieren werden. Hierbei handelt es sich um verschiedene Messwerte für verschiedene Schwertlilien (Iris), die 2 Arten von Blättern haben, Blütenblätter und Kelchblätter. Jedes Blatt hat eine Länge und eine Breite. Damit haben die Daten insgesamt 4 Dimensionen.

# In[2]:


from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import pylab as pl
from itertools import cycle

iris = load_iris()

numSamples, numFeatures = iris.data.shape
print(numSamples)
print(numFeatures)
print(iris.target_names)


# Unsere Daten bestehen aus 150 Beispielen (verschiedene Blüten), sowie 4 Dimensionen (werden hier Eigenschaft / Feature genannt). Jeder Datensatz ist einer Unterart zugeordnet. 
# 
# 4-dimensionale Daten können wir nicht einfach anzeigen und schlecht visualisieren. Wir führen also eine Hauptkomponentenanalyse durch, und reduzieren die Daten auf 2 Dimensionen. Probieren wir's mal aus:

# In[3]:


X = iris.data
pca = PCA(n_components=2, whiten=True).fit(X)
X_pca = pca.transform(X)


# Damit haben wir jetzt die 4D Daten auf 2 Dimensionen reduziert. Mathematisch gesprochen: Wir haben eine Projektion auf auf den 2-dimensionalen Raum durchgeführt. Für diese Projektion wurden zwei 4-dimensionale Eigenvektoren ermittelt, diese können wir uns ausgeben lassen. Wobei sie jetzt keine direkte, anschauliche Bedeutung haben:

# In[4]:


print(pca.components_)


# Wie viel Varianz haben wir erhalten können?

# In[5]:


print(pca.explained_variance_ratio_)
print(sum(pca.explained_variance_ratio_))


# Wow, wir konnten 97,8% der Varianz erhalten! Und gleichzeitig benötigen wir nur noch 2 statt 4 Dimensionen. Die Hauptkomponentenanalyse hat hierbei die neuen 2 Dimensionen so gewählt, dass möglichst viel Varianz erhalten bleibt.
# 
# In der ersten Dimension konnten bereits 92,5% der Varianz erhalten werden, die 2. Dimension sorgt für weitere 5%, insgesamt sind also weniter als 3% der Varianz verloren gegagngen. Das ist super!
# 
# Jetzt wo wir die 2-Dimensionale Repräsentation ermittelt haben, können wir das natürlich auch anzeigen:

# In[8]:


get_ipython().run_line_magic('matplotlib', 'inline')
from pylab import *

colors = cycle('rgb')
target_ids = range(len(iris.target_names))
pl.figure()
for i, c, label in zip(target_ids, colors, iris.target_names):
    pl.scatter(X_pca[iris.target == i, 0], X_pca[iris.target == i, 1],
        c=c, label=label)
pl.legend()
pl.show()


# Die verschiedenen Typen der Blüten sind relativ gut geclustert.
# 
# Anschaulich gesprochen liegt das vermutlich daran, dass die generelle Größe eines Blütenblattes sehr von der Unterart abhängt, und vermutlich die Länge und die Breite eines Blattes ungefähr um den gleichen Faktor wächst. 
# 
# Die im Graph abgetratenen Zahlen haben keine intuitive Bedeutung, was wir vermutlich sehen ist das normalisierte Verhältnis zwischen der Länge und der Breite der jeweiligen Blätter - wobei die Hauptkomponentenanalyse hierbei automatisch entschieden hat, wie dieses Verhältnis berechnet wird. Wir mussten uns also um nichts kümmern.

# ## Aufgabe

# Man kann die Daten auch auf eine Dimension reduzieren, hierbei werden ja weiterhin 92,5% der Varianz erhalten. Probier es aus: Führe eine Hauptkomponentenanalyse durch, die die Daten auf eine Dimension reduziert, und überprüfe die Ergebnisse!
