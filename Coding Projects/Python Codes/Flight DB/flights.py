import sqlite3
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

conn = sqlite3.connect("flights.db")
cur = conn.cursor()
coords = cur.execute("""
  select cast(longitude as float),
  cast(latitude as float)
  from airports;"""
).fetchall()



m = Basemap(
  projection='merc',
  llcrnrlat=-80,
  urcrnrlat=80,
  llcrnrlon=-180,
  urcrnrlon=180,
  lat_ts=20,
  resolution='c'
)

m.drawcoastlines()
m.drawmapboundary()


x, y = m(
  [l[0] for l in coords],
  [l[1] for l in coords]
)

m.scatter(
  x,
  y,
  1,
  marker='o',
  color='red'
)
