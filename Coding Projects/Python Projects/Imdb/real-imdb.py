import requests
from left_pad import left_pad

response = request.get('https://api.themoviedb.org/3/discover/movie',
    {'sort_by': 'popularity.desc', 'api_key': '9175af8fa39824d4c6f1264c00a9ec7c'})

movies = response.json()

for movie in movies['results']:
    print left_pad(movie['title'], 40) + ' ' + '*' * int(movie['popularity'] / 2)
