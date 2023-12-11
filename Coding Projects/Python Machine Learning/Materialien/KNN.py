
# coding: utf-8

# # KNN (K-Nearest-Neighbors)

# KNN beschreibt eine einfache Idee: Definiere eine Distanzmetrik zwischen den Punkten, und finde die k nächsten Punkte. Man kann diese Punkte dann verwenden, um die Eigenschaft eines Testobjektes vorherzusagen. 
# 
# In dieser Lektion betrachten wir echte Bewertungen, aus dem MovieLens - Datensatz. 
# 
# Dazu laden wir zuerst das MovieLens Datenset herunter und entpacken die .zip-Datei bei uns. Das erledigt ein kleines Python-Script für uns :-)

# In[30]:


import urllib.request
import zipfile
import io

movieLensData = "http://files.grouplens.org/datasets/movielens/ml-100k.zip"
with urllib.request.urlopen(movieLensData) as f:
    zf = open('ml-100k.zip', 'wb')
    zf.write(f.read())
    zf.close()
    with zipfile.ZipFile('ml-100k.zip') as zipFileObj:
        zipFileObj.extractall(".")


# In[58]:


import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('./ml-100k/u.data', sep='\t', names=r_cols, usecols=range(3))
ratings.head()


# Jetzt gruppieren wir die Daten nach der Film-ID, und berechnen die gesamte Anzahl an Bewertungen sowie den Durchschnitt: 

# In[44]:


import numpy as np

movieProperties = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
movieProperties.head()


# Die Anzahl an Bewertungen ist für die Berechnung einer Distanz nicht sinnvoll, da sie - wenn später weitere Bewertungen hinzugefügt werden - sich leicht verändert.
# 
# Daher erzeugen wir im nächsten Schritt ein neues DataFrame, welches die Anzahl der Bewertungen in normalisierter Form speichert. 0 bedeutet hierbei, dass keiner den Film bewertet hat, 1 bedeutet, dass es der Film mit den meisten Bewertungen ist. 

# In[45]:


movieNumRatings = pd.DataFrame(movieProperties['rating']['size'])
movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
movieNormalizedNumRatings.head()


# Die Informationen zu den jeweiligen Genres dieser Filme sind in der Datei u.item gespeichert, die wir mit der .zip-Datei vorher heruntergeladen haben. In dieser Datei sind 19 verschiedene Genres erfasst, jeder in einer eigenen Spalte.
# 
# Steht in einer Spalte eine 0, bedeutet das, dass der Film diese Genre nicht hat, 1 bedeutet, dass der Film in dieser Genre ist. Alle Filme sind mehr als einer Genre zugeordnet.
# 
# Zuerst werden die Daten eingelesen und in ein Python Dictionary gespeichert. Jeder Eintrag enthält dann den Namen des Filmes, eine Liste der zugehörigen Genres, den normalisierten Beliebtheitswert und die durchschnittliche Bewertung:

# In[51]:


movieDict = {}
with open(r'./ml-100k/u.item', encoding="ISO-8859-1") as f:
    temp = ''
    for line in f:
        fields = line.rstrip('\n').split('|')
        movieID = int(fields[0])
        name = fields[1]
        genres = fields[5:25]
        genres = [int(g) for g in genres]
        movieDict[movieID] = (name, genres, movieNormalizedNumRatings.loc[movieID].get('size'), movieProperties.loc[movieID].rating.get('mean'))


# Beispielsweise ist der Film mit der ID 1 der Film "Toy Story":

# In[53]:


print(movieDict[1])


# Als nächstes müssen wir eine Funktion definieren, die den "Abstand" zwischen 2 Filmen auf Basis der Genres sowie der Popularität berechnet. Das können wir testen, indem wir z.B. den Abstand zwischen Film 2 und 4 berechnen:

# In[54]:


from scipy import spatial

def ComputeDistance(a, b):
    genresA = a[1]
    genresB = b[1]
    genreDistance = spatial.distance.cosine(genresA, genresB)
    popularityA = a[2]
    popularityB = b[2]
    popularityDistance = abs(popularityA - popularityB)
    return genreDistance + popularityDistance
    
ComputeDistance(movieDict[2], movieDict[4])


# Je größer die Distanz, desto unterschiedlicher sind die Filme. Um was für Filme handelt es sich bei Film 2 bzw. Film 4? 

# In[55]:


print(movieDict[2])
print(movieDict[4])


# Als nächstes berechnen wir den Abstand zwischen einem Film den wir testen möchten (hier: Toy Store) und allen anderen Filmen in unserem Datensatz. Wir berechnen also die Distanz, sortieren nach ihr, und geben die K nächstgelegenen Nachbarn aus: 

# In[56]:


import operator

def getNeighbors(movieID, K):
    distances = []
    for movie in movieDict:
        if (movie != movieID):
            dist = ComputeDistance(movieDict[movieID], movieDict[movie])
            distances.append((movie, dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(K):
        neighbors.append(distances[x][0])
    return neighbors

K = 10
avgRating = 0
neighbors = getNeighbors(1, K)
for neighbor in neighbors:
    avgRating += movieDict[neighbor][3]
    print(movieDict[neighbor][0] + " " + str(movieDict[neighbor][3]))
    
avgRating /= K


# Berechnet man die durchschnittliche Bewertung der 10 ähnlichsten Filme zu Toy Story:

# In[37]:


avgRating


# Wie gut trifft das die tatsächliche Bewertung von Toy Story?

# In[57]:


movieDict[1]


# Gar nicht so schlecht...

# ## Aufgabe

# Wir haben bisher einfach K auf den Wert 10 festgesetzt. Ermöglichen andere Werte für K hier bessere Ergebnisse?
# 
# Zudem ist unsere Distanzmetrik etwas ungewöhnlich - wir haben einfach den Cosinus zwischen den Genren gebildet und dazu den normalisierten Beliebtheitswert addiert. Kann man die Distanzmetrik verbessern? Wie?
