from data.database import read_query, insert_query, update_query
from data.models import Movie


def create_movie(title: str, director: str, release_year: int):
    sql = """INSERT INTO movies (title, director, release_year)
            VALUES (?, ?, ?)"""

    return insert_query(sql, (title, director, release_year))

def get_movies(search: str | None, sort: str | None) -> list[Movie]:
    sort_sql = """SELECT id, title, director, release_year, rating 
                    FROM movies
                    ORDER BY rating DESC"""

    search_sql = """SELECT id, title, director, release_year, rating
                    FROM movies
                    WHERE title LIKE ?"""

    sql = """SELECT id, title, director, release_year, rating
                FROM movies"""

    if search:
        rows =  read_query(search_sql, (f"%{search}%",))
    elif sort == 'rating':
        rows = read_query(sort_sql)
    else:
        rows = read_query(sql)

    movies = []

    for row in rows:
        movie = Movie(id=row[0],
              title=row[1],
              director=row[2],
              release_year=row[3],
              rating=row[4]
        )
        movies.append(movie)

    return movies


def get_movie_by_id(id: int):
    sql = """SELECT id, title, director, release_year, rating
                FROM movies
                WHERE id = ?"""

    rows = read_query(sql, (id, ))

    if not rows:
        return None

    row = rows[0]

    movie = Movie(id=row[0],
                title=row[1],
                director=row[2],
                release_year=row[3],
                rating=row[4]
            )

    return movie


def update_movie(movie_id: int, title: str | None, director: str | None, release_year: int | None):
    sql = """UPDATE movies
                SET title = ?, director = ?, release_year = ?
                WHERE id = ?"""

    update_query(sql, (title, director, release_year, movie_id))

def delete_movie(movie_id: int):
    sql = """DELETE FROM movies WHERE id = ?"""

    update_query(sql, (movie_id, ))


