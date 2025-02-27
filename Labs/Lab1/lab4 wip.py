def pick_movie(subgenre=None, min_rating=0):
    # Open and read the JSON file
    with open("romantic_movies.json", "r") as file:
        movie_list = json.load(file)

    # Filter movies based on user input
    matching_movies = []
    for movie in movie_list:
        if subgenre is not None and movie["subgenre"].lower() != subgenre.lower():
            continue
        if movie["rating"] < min_rating:
            continue
        matching_movies.append(movie)

    # Choose a random movie from the filtered list
    if len(matching_movies) == 0:
        return "No movies found with those preferences."
    
    selected_movie = random.choice(matching_movies)
    return selected_movie

# Step 4: Display selected movie details
chosen_movie = pick_movie(subgenre="Drama", min_rating=7.5)
print("\nSelected Movie:")
print(chosen_movie)

# Step 5: Verify JSON file content
with open("romantic_movies.json", "r") as file:
    data = json.load(file)
    print("\nVerifying JSON content:")
    print(json.dumps(data, indent=4))