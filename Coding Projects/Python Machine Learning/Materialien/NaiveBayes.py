
# coding: utf-8

# # Naive Bayes (mit sklearn.naive_bayes)

# Mit Hilfe der sklearn.naive_bayes - Funktion schreiben wir einen Spamfilter! Ein Großteil des Codes wird nur zum Einlesen / Vorbereiten der Emails benötigt, um die Emails in einem DataFrame vom "pandas" - Paket zu verwenden:

# In[4]:


import os
import io
import numpy
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def readFiles(path):
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root, filename)

            inBody = False
            lines = []
            f = io.open(path, 'r', encoding='latin1')
            for line in f:
                if inBody:
                    lines.append(line)
                elif line == '\n':
                    inBody = True
            f.close()
            message = '\n'.join(lines)
            yield path, message


def dataFrameFromDirectory(path, classification):
    rows = []
    index = []
    for filename, message in readFiles(path):
        rows.append({'message': message, 'class': classification})
        index.append(filename)

    return DataFrame(rows, index=index)

data = DataFrame({'message': [], 'class': []})

data = data.append(dataFrameFromDirectory('./emails/spam', 'spam'))
data = data.append(dataFrameFromDirectory('./emails/ham', 'ham'))


# Anzeigen der ersten paar Zeilen vom DataFrame:

# In[5]:


data.head()


# Mit Hilfe des CountVectorizer können die Nachrichten in eine Liste von Wörtern aufgeteilt werden. Anschließend kann diese Liste mit dem MultinomialNB - Klassifizierer bearbeitet werden. Nach einem Aufruf von fit() ist unser Spamfilter trainiert und wir können ihn verwenden!

# In[8]:


vectorizer = CountVectorizer()
counts = vectorizer.fit_transform(data['message'].values)

classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)


# Probieren wir's mal aus:

# In[9]:


examples = ['Free Viagra now!!!', "Hi Bob, how about a game of golf tomorrow?"]
example_counts = vectorizer.transform(examples)
predictions = classifier.predict(example_counts)
predictions


# ## Aufgabe

# Unsere Spamfilter ist noch nicht wirklich effektiv, da unsere Testdaten sind recht klein sind. Denk dir ein paar weitere Emails aus, erkennt der Filter, ob es sich um eine Spam-Email handelt?
# 
# Was passiert, wenn du eine Email auf Deutsch bewerten lässt, erkennt der Spam-Filter dies eindeutig? Warum / warum nicht? Wie hängt das mit den Trainingsdaten zusammen?
# 
# Wenn du dich herausfordern möchtest, kannst du den Spamfilter mit ein paar Daten trainieren und ihn mit den restlichen Daten testen? Wie gut funktionieren die Vorhersagen? 
