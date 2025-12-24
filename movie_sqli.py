from datetime import datetime
import sqlite3
from movie import Movie


class MovieSqlite:
    def connect(self):
        self.conn = sqlite3.connect("movie.db")

        self.cur = self.conn.cursor()

    def __init__(self) -> None:
        self.connect()

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

        self.conn.close()

    def insertMovie(self, movie: Movie):
        self.connect()

        print(f"checking if day {movie.day} already has a pick...")
        self.cur.execute(
            "SELECT * FROM movies WHERE day=?",
            (movie.day,),
        )

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
            print("day set...")
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
            print("day updated...")
        print("committing changes...")
        self.conn.commit()
        print("changes committed, closing connection...")
        self.conn.close()

    def listMovies(self):
        self.connect()

        print("listing movies...")

        spook_list = f"# 🎃 SPOOKTOBER {datetime.now().year} MOVIE LIST 🎃\n"
        self.cur.execute("SELECT day, movie_title FROM movies ORDER BY day DESC")
        res_dict = dict(self.cur.fetchall())
        for i in range(0, 31):
            spook_list = spook_list + f"{i + 1}. {res_dict.get(i+1, "N/A")}\n"
        return spook_list
