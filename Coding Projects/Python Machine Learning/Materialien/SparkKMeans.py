from pyspark.mllib.clustering import KMeans
from numpy import array, random
from math import sqrt
from pyspark import SparkConf, SparkContext
from sklearn.preprocessing import scale

K = 5

# Spark initialisieren:
conf = SparkConf().setMaster("local").setAppName("SparkKMeans")
sc = SparkContext(conf = conf)

# Zufällige Einkommens- / Alter - Daten erzeugen. Für N Personen, in k Clustern
def createClusteredData(N, k):
    random.seed(10)
    pointsPerCluster = float(N)/k
    X = []
    for i in range (k):
        incomeCentroid = random.uniform(20000.0, 200000.0)
        ageCentroid = random.uniform(20.0, 70.0)
        for j in range(int(pointsPerCluster)):
            X.append([random.normal(incomeCentroid, 10000.0), random.normal(ageCentroid, 2.0)])
    X = array(X)
    return X

# Einlesen und Normalisieren der Daten (scale()).
data = sc.parallelize(scale(createClusteredData(100, K)))

# Modell erstellen
clusters = KMeans.train(data, K, maxIterations=10,
        initializationMode="random")

# Ausgabe der Daten
resultRDD = data.map(lambda point: clusters.predict(point)).cache()

print("Wie viele Eintraege pro Cluster?")
counts = resultRDD.countByValue()
print(counts)

print("Zuordnungen:")
results = resultRDD.collect()
print(results)


# Wie gut hat der Algorithmus funktioniert? Hierfuer wird der Fehler
# als quadrierter Abstand berechnet
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = data.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Quadrierte Abweichung = " + str(WSSSE))

# Ausprobieren:
# - Was passiert zum quadrierten Fehler, wenn K erhoeht / verringert wird? Warum?
# - Was passiert, wenn die Daten nicht normalisiert werden? Warum?