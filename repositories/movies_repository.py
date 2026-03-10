from data.database import read_query, insert_query, update_query
from data.models import Movie

class MovieRepository:

    def create_movie(self, title: str, director: str, release_year: int, rating: float):
        sql = """INSERT INTO movies (title, director, release_year, rating)
                VALUES (?, ?, ?, ?)"""

        return insert_query(sql, (title, director, release_year, rating))

    def get_movies(self, search: str | None, sort: str | None) -> list[Movie]:
        sort_sql = """SELECT id, title, director, release_year, rating 
                        FROM movies
                        ORDER BY rating IS NULL, rating DESC"""

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


    def get_movie_by_id(self, id: int):
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

    def get_movie_by_title(self, title: str):
        sql = """SELECT id
                    FROM movies
                    WHERE title = ?"""

        rows = read_query(sql, (title, ))

        if not rows:
            return None

        return rows[0][0]

    def get_movie_by_title_and_year(self, title: str, release_year: int):
        sql = """SELECT id
                    FROM movies
                    WHERE title = ? AND release_year = ?"""

        rows = read_query(sql, (title, release_year))

        if not rows:
            return None

        return rows[0][0]

    def update_movie(self, movie_id: int, title: str | None, director: str | None, release_year: int | None):
        sql = """UPDATE movies
                    SET title = ?, director = ?, release_year = ?
                    WHERE id = ?"""

        update_query(sql, (title, director, release_year, movie_id))

    def delete_movie(self, movie_id: int):
        sql = """DELETE FROM movies WHERE id = ?"""

        update_query(sql, (movie_id, ))

    def update_movie_rating(self, movie_id, rating):
        sql = """UPDATE movies SET rating = ? WHERE id = ?"""

        update_query(sql, (rating, movie_id))



