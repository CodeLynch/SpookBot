import sqlite3
from movie import Movie


class MovieSqlite:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("movie.db")

        self.cur = self.conn.cursor()

        self.cur.execute(
            """ CREATE TABLE IF NOT EXISTS movies ( 
            day integer PRIMARY KEY, 
            tmdb_id text NOT NULL, 
            movie_title text NOT NULL, 
            showing_start text NOT NULL, 
            showing_end text NOT NULL, 
            picked_by text NOT NULL)
            """
        )

    def insertMovie(self, movie: Movie):
        print("checking if day already has a pick...")
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM movies WHERE day=?)", movie.day)

        if self.cur.fetchone() is None:
            self.cur.execute(
                "INSERT INTO movies(day, tmdb_id, movie_title, showing_start, showing_end, picked_by) VALUES (?,?,?,?,?,?)",
                (
                    movie.day,
                    movie.tmdb_id,
                    movie.movie_title,
                    movie.showing_start,
                    movie.showing_end,
                    movie.picked_by,
                ),
            )
        else:
            self.cur.execute(
                "UPDATE movies SET tmdb_id=?, movie_title=?, showing_start=?, showing_end=?, picked_by=? WHERE day=?",
                (
                    movie.tmdb_id,
                    movie.movie_title,
                    movie.showing_start,
                    movie.showing_end,
                    movie.picked_by,
                    movie.day,
                ),
            )
        print("committing changes...")
        self.conn.commit()
        print("changes committed, closing connection...")
        self.conn.close()
