from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF

# Spark initialisieren:
conf = SparkConf().setMaster("local").setAppName("SparkTFIDF")
sc = SparkContext(conf = conf)

# Einlesen der Dokumente (ein Dokuement pro Zeile).
rawData = sc.textFile("C:/DataScience/subset-small.tsv")
fields = rawData.map(lambda x: x.split("\t"))
documents = fields.map(lambda x: x[3].split(" "))

# Zwischenspeichern der Dateinamen
documentNames = fields.map(lambda x: x[1])

# Wandle jedes Dokument in einen SparseVektor um, mit dem gehashten Wort (als int)
# zu der Häufigkeit dieses Wortes in diesem Dokument
hashingTF = HashingTF(100000)  #100K "buckets", dies spart Arbeitsspeicher
tf = hashingTF.transform(documents)

# Ergebnis: RDD, bestehend aus vielen SparseVectorn, die zu jedem
# Wort die Häufigkeit in diesem Dokument angeben

# Jetzt wird TF*IDF für jedes Wort berechnet:
tf.cache()
idf = IDF(minDocFreq=2).fit(tf)
tfidf = idf.transform(tf)

# Ergebnis: Ein RDD, welches aus vielen SparseVectoren besteht. Jeder
# SparseVector gibt zu jedem Wort(-Hash) den entsprechenden TFxIDF - Wert
# an.

# Ich weiß, dass in den Daten der Artikel für "Abraham Lincoln" im Datensatz
# enthalten ist. Was ist das Ergebnis bei der Suche nach "Gettysburg"? 
# (Lincoln hat dort eine Rede gehalten):

# Zuerst müssen wir den hash-Wert für "Gettysburg" ermitteln. Dazu verwenden
# wir die HashingTF:
gettysburgTF = hashingTF.transform(["Gettysburg"])
gettysburgHashValue = int(gettysburgTF.indices[0])

# Jetzt laden wir den TF*IDF - Wert für den Worthash für Gettysburg 
# in ein neues RDD:
gettysburgRelevance = tfidf.map(lambda x: x[gettysburgHashValue])

# Dieses Ergebnis wird jetzt mit dem Namen des Dokumentes kombiniert
zippedResults = gettysburgRelevance.zip(documentNames)

# Und das Dokument mit dem höchsten TF*IDF - Wert wird ausgegeben:
print("Das beste Dokument für den Suchbegriff 'Gettysburg' ist:")
print(zippedResults.max())  
