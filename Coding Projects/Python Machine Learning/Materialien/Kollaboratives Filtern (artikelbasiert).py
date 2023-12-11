
# coding: utf-8

# # Artikelbasiertes, kollaboratives Filtern

# Zuerst stellen wir wieder sicher, dass das MovieLens 100k Datenset heruntergeladen ist:

# In[1]:


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


# Anschließend lesen wir diesen Datensatz in ein DataFrame von Pandas ein. Und fügen gleichzeitig noch einen extra Benutzer mit der ID 0 zu den Daten hinzu (extra_data). Den werden wir später noch brauchen:

# In[41]:


import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('./ml-100k/u.data', sep='\t', names=r_cols, usecols=range(3), encoding="ISO-8859-1")

m_cols = ['movie_id', 'title']
movies = pd.read_csv('./ml-100k/u.item', sep='|', names=m_cols, usecols=range(2), encoding="ISO-8859-1")

extra_data = [[0, 172, 5], [0, 133, 1], [0, 50, 5]]
ratings = ratings.append(pd.DataFrame(extra_data, columns=r_cols), ignore_index=True)

ratings = pd.merge(movies, ratings)

ratings.head()


# Auf Basis dieser Tabellen konstruiert man jetzt eine Pivot-Tabelle wo zu jedem Benutzer angeben ist, welche Filme er bewertet hat. NaN bedeutet, dass zu diesem Eintrag keine Daten existieren bzw. der Nutzer den Film nicht angeschaut hat. 

# In[42]:


userRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')
userRatings.head()


# Jetzt wird gezaubert! Mit Hilfe der corr() - Methode wird zu jedem Film ein Korrelationswert zu jedem Spaltenpaar berechnet. Heraus kommt eine Tabelle wo zu jedem Film die Korrelation zu jedem anderen Film berechnet ist, wo also mindestens ein Nutzer beide Filme bewertet hat. 
# 
# Hat kein Nutzer ein Filmepaar bewertet, steht in der Tabelle ein NaN. Cool, dass das so einfach geklappt hat!

# In[46]:


corrMatrix = userRatings.corr()
corrMatrix.head()


# Wenn jetzt aber nur ein Nutzer ein Filmepaar bewertet hat, schleicht sich sehr leicht ein Fehler ein. Daher beschränken wir die Korrelation auf die Filme, die von vielen Personen bewertet wurden. 
# 
# Dadurch bekommen wir einerseits populärere Filme als Ergebnis (weil nur diese von hinreichend vielen Nutzern bewertet wurden), können uns aber auch "sicherer" sein, dass das Ergebnis stimmt. 
# 
# Um dies zu machen, setzen wir den Parameter "min_periods" auf 100, d.h. mindestens 100 Nutzer müssen ein entsprechendes Filmepaar bewertet haben:

# In[49]:


corrMatrix = userRatings.corr(method='pearson', min_periods=100)
corrMatrix.head()


# Erinnerst du dich noch an den Nutzer den wir am Anfang mit in unsere Daten geschrieben haben? Dieser Nutzer hatte die ID 0, und mag Star Wars, sowie The Empire Strikes Back, mochte aber den Film "Gone with the Wind" überhaupt nicht. 
# 
# Schauen wir uns nochmal die Filme an, die dieser Nutzer bewertet hat. Dafür kann die `.loc[0]` - Schreibweise verwendet werden, heraus kommt eine Liste aller Filme mit der jeweiligen Bewertung - oder NaN sollte keine Bewertung existieren. Die NaN - Werte müssen also noch herausgefiltert werden, dies geschieht mit der Methode `dropna()`:

# In[52]:


myRatings = userRatings.loc[0].dropna()
myRatings


# Jetzt gehen wir jeden der 3 bewerteten Filme durch, und erstellen für jeden Film Empfehlungen. Damit diese Empfehlungen möglichst solche Filme enthalten, die ähnlich zu den Filmen sind, die ich gut bewertet habe, wird der Ähnlichkeitswert mit meiner Bewertung multipliziert:

# In[56]:


simCandidates = pd.Series()
for i in range(0, len(myRatings.index)):
    print("Füge Ähnlichkeiten für " + str(myRatings.index[i]) + " hinzu...")
    # Berechne Filme, die ähnlich sind zu den Filmen die ich bewertet habe
    sims = corrMatrix[myRatings.index[i]].dropna()
    # Multipliziere den Ähnlichkeitswert mit meiner Bewertung
    sims = sims.map(lambda x: x * myRatings[i])
    # Und füge diesen Eintrag zur Liste hinzu
    simCandidates = simCandidates.append(sims)
    
#Glance at our results so far:
print("sortieren...")
simCandidates.sort_values(inplace = True, ascending = False)
print(simCandidates.head(10))


# Das sieht doch schonmal gut aus. Jetzt sind aber einige der Filme noch doppelt in unseren Ergebnissen vorhanden. Daher brauchen wir noch eine Gruppierung nach dem Namen des Filmes:

# In[57]:


simCandidates = simCandidates.groupby(simCandidates.index).sum()


# In[58]:


simCandidates.sort_values(inplace = True, ascending = False)
simCandidates.head(10)


# Zu guter Letzt müssen wir noch die Filme entfernen, die ich schon bewertet habe - diese mir erneut vorzuschlagen macht vermutlich keinen Sinn:

# In[59]:


filteredSims = simCandidates.drop(myRatings.index)
filteredSims.head(10)


# Fertig!

# ## Aufgabe

# Wie ließen sich diese Ergebnisse verbessern? Liefert eine andere Methode zur Berechnung der Korrelation oder ein anderer Mindestwert bei `min_periods` bessere Ergebnisse? 
# 
# Es scheinen auch noch ein paar Filme durchgerutscht zu sein, die ähnlich zu "Gone with the Wind" sind, diesen habe ich ja sehr schlecht bewertet. Vielleicht sollten Filme, die ähnlich zum Film "Gone with the Wind" sind, abgestraft werden? 
# 
# Es gibt vermutlich noch einige Ausreißer in unserem Datensatz, einige Benutzer haben vielleicht sehr viele Filme bewertet. Das mag unser Ergebnis verzerrt habe. Schau dir nochmal die vorherigen Lektionen an, und identifiziere diese Ausreißer. Verbessert sich dadurch das Ergebnis weiter? 
# 
# Wenn du noch mehr coden möchtest: Wir berechnen hier ein Ergebnis, aber eigentlich könnten wir auch train/test verwenden, und den Algorithmus mit bekannten Daten überprüfen, z.B. auf Basis der Filme die ein Nutzer bereits angeschaut hat. Aber ob das dann wirklich zu "guten" Ergebnissen führt, darüber kann man natürlich diskutieren ;-) 
