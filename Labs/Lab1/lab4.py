import json
import random

def pick_movie(preferences):
    with open('romantic_movies.json', 'r') as f:
        movies = json.load(f)

    filtered_movies = [movie for movie in movies if all(preference in movie.values() for preference in preferences.values())]
    if filtered_movies:
        return random.choice(filtered_movies)
    else:
        return None
    
def display (movie):
    if movie:
        print(f"Title: {movie['title']}")
        print(f"Year: {movie['year']}")
        print(f"Director: {movie['director']}")
        print(f"Actors: {', '.join(movie['actors'])}")
        print(f"Genres: {', '.join(movie['genres'])}")
    else:
        print("No movie found")

def verify_json_file():
    with open('romantic_movies.json', 'r') as f:
        movies = json.load(f)
    
    for movie in movies:
        print(movie)