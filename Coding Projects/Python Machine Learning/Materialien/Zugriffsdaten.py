
# coding: utf-8

# # Daten Bereinigen: Zugriffe auf Webseite

# In diesem Beispiel werden wir echte Zugriffe auf eine Webseite analysieren, und so herausfinden, welches die am häufigsten besuchten Unterseiten sind. Klingt einfach, oder?
# 
# Zuerst definieren wir einen regulären Ausdruck, der uns bei dem Auslesen einer Zeile aus der Log-Datei unterstützt: 

# In[1]:


import re

format_pat= re.compile(
    r"(?P<host>[\d\.]+)\s"
    r"(?P<identity>\S*)\s"
    r"(?P<user>\S*)\s"
    r"\[(?P<time>.*?)\]\s"
    r'"(?P<request>.*?)"\s'
    r"(?P<status>\d+)\s"
    r"(?P<bytes>\S*)\s"
    r'"(?P<referer>.*?)"\s'
    r'"(?P<user_agent>.*?)"\s*'
)


# Der Pfad zur Datei, die wir analysieren wollen. Die Datei liegt im selben Ordner, also brauchen wir hier nichts anzupassen.

# In[18]:


logPath = "access_log.txt"


# Als nächstes schreiben wir ein kleines Script, welches die Datei Zeile für Zeile durchgeht, und die Daten in ein Dictionary schreibt. In diesem Dictionary wird dann als Schlüssel die URL der Seite gepseichert, und als Wert die Anzahl der aufrufe. Was könnte hierbei schief gehen?

# In[23]:


URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            request = access['request']
            # request = "GET /blog/ HTTP/1.1" 
            (action, URL, protocol) = request.split()
            if URL in URLCounts:
                URLCounts[URL] = URLCounts[URL] + 1
            else:
                URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))


# Mhm... Der "request" sollte eigentlich wie folgt aussehen:
# 
# `GET /blog/ HTTP/1.1`
# 
# Zuerst die HTTP-Methode (GET / POST), dann die URL, und dann das Protokoll. Aber das scheint nicht immer zu klappen. Warum nicht?

# In[24]:


URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            request = access['request']
            fields = request.split()
            if (len(fields) != 3):
                print(fields)


# Mhm... Also es gibt einige Einträge, in denen der request einfach nur leer ist, bei einem anderen steht dort einfach nur Müll drinnen. Also passen wir unser Script an, dass diese Fälle abgefangen werden:

# In[25]:


URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            request = access['request']
            fields = request.split()
            if (len(fields) == 3):
                URL = fields[1]
                if URL in URLCounts:
                    URLCounts[URL] = URLCounts[URL] + 1
                else:
                    URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))


# Es hat funktioniert! Aber die Ergebnisse machen keinen Sinn. Was wir ja eigentlich wollten, sind die Seiten die von echten Menschen angeschaut werden. Und was ist diese xmlrpc.php? Wenn man sich dazu die Log-Datei näher anschaut, findet man viele Einträge in folgender Form:
# 
# `46.166.xxx.xxx - - [05/Dec/2015:05:19:35 +0000] "POST /xmlrpc.php HTTP/1.0" 200 370 "-" "Mozilla/4.0 (compatible: MSIE 7.0; Windows NT 6.0)"`
# 
# Was macht dieses Script? Auf jeden Fall wollen wir nur GET - Anfrage betrachten. Warum?
# 
# - `GET`: Anzeigen von irgendwelchen Daten im Internet
# - `POST`: Verändern / Löschen von irgendwelchen Daten, absenden eines Formulares

# In[27]:


URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            request = access['request']
            fields = request.split()
            if (len(fields) == 3):
                (action, URL, protocol) = fields
                if (action == 'GET'):
                    if URL in URLCounts:
                        URLCounts[URL] = URLCounts[URL] + 1
                    else:
                        URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))


# Damit haben wir jetzt alle POST - Anfragen aus den Ergebnissen herausgefiltert. Es sieht schonmal besser aus. Aber bei dieser Seite handelt es sich um eine News-Seite - warum lesen so viele Leute den kleinen Blog? Eigentlich sollten sie eher die News-Artikel lesen... 
# 
# Wie sieht denn ein typischer Eintrag für /blog/ aus?
# 
# 54.165.xxx.xxx - - [05/Dec/2015:09:32:05 +0000] "GET /blog/ HTTP/1.0" 200 31670 "-" "-"
# 
# Mhm... warum ist bei diesem Eintrag der User-Agent leer? Könnte auf einen bösartigen Scraper oder sonst irgendwas komisches hindeuten. 
# 
# Was für User-Agents besuchen eigentlich unserer Webseite?

# In[28]:


UserAgents = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            agent = access['user_agent']
            if agent in UserAgents:
                UserAgents[agent] = UserAgents[agent] + 1
            else:
                UserAgents[agent] = 1

results = sorted(UserAgents, key=lambda i: int(UserAgents[i]), reverse=True)

for result in results:
    print(result + ": " + str(UserAgents[result]))


# Puuhh... Zusätzlich zum User Agent "-" gibt es unglaublich viele verschiedene, automatisierte Scripts die unsere Webseite aufrufen und so unsere Statistik verschmutzen. 
# 
# Jetzt könnten wir diese User-Agents manuell herausfiltern, aber das Einfachste ist jetzt erstmal, einfach alle Einträge zu verwerfen, bei denen der User-Agent "-", "bot", "spider" oder "W3 Total Cache" enthält. 

# In[17]:


URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            agent = access['user_agent']
            if (not('bot' in agent or 'spider' in agent or 
                    'Bot' in agent or 'Spider' in agent or
                    'W3 Total Cache' in agent or agent =='-')):
                request = access['request']
                fields = request.split()
                if (len(fields) == 3):
                    (action, URL, protocol) = fields
                    if (action == 'GET'):
                        if URL in URLCounts:
                            URLCounts[URL] = URLCounts[URL] + 1
                        else:
                            URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))


# Jetzt haben wir ein neues Problem: Wir sehen, dass viele Dateien angefragt werden, Dateien die überhaupt keine Webseiten sind, sondern nur von .html - Dateien eingebunden werden. Diese müssen wir natürlich ignorieren, wir interessieren uns dafür ja nicht.
# 
# Daher entfernen wir im nächsten Schritt alle Adresse, die nicht auf den Schrägstrich "/" enden. Das liegt daran, dass ich weiß, dass all meine Artikel eine URL haben, die auf einen Schrägstrich endet - daher darf ich das tun. Hier verwende ich also weiteres Wissen, welches ich über die Daten habe, um diesen Schritt zu begründen.

# In[29]:


URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            agent = access['user_agent']
            if (not('bot' in agent or 'spider' in agent or 
                    'Bot' in agent or 'Spider' in agent or
                    'W3 Total Cache' in agent or agent =='-')):
                request = access['request']
                fields = request.split()
                if (len(fields) == 3):
                    (action, URL, protocol) = fields
                    if (URL.endswith("/")):
                        if (action == 'GET'):
                            if URL in URLCounts:
                                URLCounts[URL] = URLCounts[URL] + 1
                            else:
                                URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))


# Das sieht jetzt schonmal etwas glaubwürdiger aus. Aber wenn man noch etwas weiter in die Daten hineinschaut sieht man, dass die Seiten mit "/feed/" etwas komisch aussehen, und dass immernoch ein paar Zugriffe von Suchmaschienen nicht herausgefiltert wurden. Dennoch - auf Basis dieser Daten sieht es so aus, dass Orlando News, World News und Comics die am häufigsten aufgerufenen Seiten sind. 
# 
# Das Fazit: Kenn dich mit den Daten aus. Hinterfrag immer was die Ergebnisse sind, und überprüfe die Ergebnisse, bevor du vorschnelle Schlüsse ziehst. Wenn deine Firma wegen einer leichtfertigen Entscheidung nachher richtig Geld verliert, kann das definitiv zu Problemen führen.
# 
# Zudem: Bei jeden Schritt, überlege dir gut, ob du ihn durchführen darfst. Warum darfst du die Daten in jedem Schritt bereinigen? Bereinige die Daten nicht, weil dir das Ergebnis am Ende nicht passt!

# ## Aufgabe

# Dieser Ergebnisse sind noch nicht perfekt, die URL enthalten teilweise noch das Wort "feed", diese werden auch automatisiert abgerufen. Passe den Code so an, dass auch diese Einträge ignoriert werden. Wenn du Lust hast, schau dir das Log-File noch etwas genauer an - was für User-Agents rufen die /feed - Seiten auf? Wo könnten diese herkommen? 
