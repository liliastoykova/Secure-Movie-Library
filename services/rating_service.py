import requests

def get_rating(title: str):
    rating = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=dd5c051'+'&t='+title).json()

    movie_rating = rating['imdbRating']

    if movie_rating == "N/A":
        return None

    return float(movie_rating)






