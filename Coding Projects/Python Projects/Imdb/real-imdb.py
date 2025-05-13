import requests
from left_pad import left_pad

# Fetch movie data from The Movie Database API
response = requests.get('https://api.themoviedb.org/3/discover/movie',
    params={'sort_by': 'popularity.desc', 'api_key': '9175af8fa39824d4c6f1264c00a9ec7c'})

movies = response.json()

for movie in movies['results']:
    print(left_pad(movie['title'], 40) + ' ' + '*' * int(movie['popularity'] / 2))

# Note: If pipreqs fails with SyntaxWarning for invalid escape sequences (e.g., \d),
# check for regex patterns in this file that might not use raw strings (r'\d').
