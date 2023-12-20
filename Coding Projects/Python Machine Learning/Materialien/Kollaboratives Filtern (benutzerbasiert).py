
# coding: utf-8

# # Benutzerbasiertes, kollaboratives Filtern
# 
# ### Berechnen der Ähnlichkeit von Filmen

# Zuerst laden wir die Daten herunter, die wir später für die Berechnungen benötigen werden:

# In[3]:


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


# Diese Daten lesen wir in ein DataFrame von Pandas ein, und kombinieren die u.data mit der u.item - Datei. Dadurch können wir mit den Namen des Filmes verwenden und müssen nicht die ID zum Identifizieren verwenden. 
# 
# (Im "echten Leben" würde man natürlich weiterhin die ID verwenden, um Arbeitsspeicher zu sparen)

# In[4]:


import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('./ml-100k/u.data', sep='\t', names=r_cols, usecols=range(3), encoding="ISO-8859-1")

m_cols = ['movie_id', 'title']
movies = pd.read_csv('./ml-100k/u.item', sep='|', names=m_cols, usecols=range(2), encoding="ISO-8859-1")

ratings = pd.merge(movies, ratings)


# In[5]:


ratings.head()


# Mit Hilfe der `pivot_table` - Funktion wird eine Tabelle erstellt, wo zu jedem Nutzer die entsprechenden Bewertungen der Filme definiert sind. NaN steht hierfür für fehlende Daten - also dass ein Nutzer diesen Film nicht bewertet hat. 

# In[6]:


movieRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')
movieRatings.head()


# Welche Nutzer haben Star Wars bewertet?

# In[7]:


starWarsRatings = movieRatings['Star Wars (1977)']
starWarsRatings.head()


# Mit Hilfe der `corrwith` - Funktion von Pandas kann Korrelation von jedem Nutzer der Star Wars bewertet hat zu den anderen Filmen berechnet werden. 
# 
# Anschließend werden alle Einträge verworfen bei denen keine Werte definiert sind, und aus dem Ergebnis wird ein neues DataFrame erstellt, dieses enthält dann die Korrelation (Ähnlichkeit) zum Star Wars - Film: 

# In[13]:


similarMovies = movieRatings.corrwith(starWarsRatings)
similarMovies = similarMovies.dropna()
df = pd.DataFrame(similarMovies)
df.head(10)


# (Die Warnmeldung kann problemlos ignoriert werden)
# 
# Wenn man jetzt die Ergebnisse nach Ähnlichkeitswert sortiert, sollten oben die Filme stehen, die ähnlich zu Star Wars sind. Wobei... Irgendwie machen diese Ergebnisse keinen Sinn! Wir haben vermutlich irgendwas übersehen...

# In[15]:


similarMovies.sort_values(ascending=False)


# Unsere Ergebnisse werden vermutlich durch ein paar Filme, die nur von ganz wenigen Nutzern geschaut wurden beeinflusst. Also ein paar Ausreißer, die unsere Daten massiv beeinflussen. 
# 
# Diese gilt es also zu entfernen. Wir erstellen daher ein neues DataFrame, welches zu jedem Film die Anzahl speichert, wie oft dieser Film bewertet wurde, und was die durchschnittliche Bewertung war. Das könnte später nützlich sein:

# In[17]:


import numpy as np
movieStats = ratings.groupby('title').agg({'rating': [np.size, np.mean]})
movieStats.head()


# Jetzt entfernen wir alle Filme, die von weniger als 100 Personen bewertet wurden, und schauen uns die übrig gebliebenen an:

# In[25]:


popularMovies = movieStats['rating']['size'] >= 100
movieStats[popularMovies].sort_values([('rating', 'mean')], ascending=False)[:15]


# Diese Ergebnisse sehen schon sehr viel besser aus, auch wenn 100 in der Praxis immer noch etwas gering sein mag. Dennoch, bleiben wir erstmal bei 100, und kombinieren diese Daten mit den Ähnlichkeitswerten zum Film "Star Wars":

# In[19]:


df = movieStats[popularMovies].join(pd.DataFrame(similarMovies, columns=['similarity']))


# In[20]:


df.head()


# Diese Ergebnisse sortieren wir dann nach dem Ähnlichkeitswert. Das kommt schon eher hin!

# In[23]:


df.sort_values(['similarity'], ascending=False)[:15]


# Natürlich würde man jetzt noch den Film aus den Daten herausfiltern, mit dem wir angefangen haben - natürlich ist Star Wars zu 100% identisch mit sich selbst. Aber ansonsten - die Ergebnisse sind schon recht gut!

# ## Aufgabe

# Die Zahl 100 haben wir zufällig gewählt. Probier mal andere Werte aus, funktionieren kleinere / größere Werte besser? Könnte man die Ergebnisse weiter verbessern, indem man nicht nur nach der Ähnlichkeit sortiert, sondern auch die Anzahl oder den Durchschnitt der Bewertungen mit in die Ähnlichkeit mit einfließen lässt?
