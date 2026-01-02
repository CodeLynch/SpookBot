from datetime import datetime
import sqlite3
from movie import Movie
from review import Review


class Sqlite:
    def connect(self):
        self.conn = sqlite3.connect("spooky.db")

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
            picked_by text NOT NULL,
            picker_avatar text NOT NULL)
            """
        )
        self.cur.execute(
            """ CREATE TABLE IF NOT EXISTS reviews ( 
            day integer NOT NULL, 
            rater_id text NOT NULL, 
            rater_name text NOT NULL, 
            rater_avatar text NOT NULL, 
            score text NOT NULL, 
            comment text,
            PRIMARY KEY (rater_id, day))
            """
        )

        self.conn.close()

    def getDay(self, day):
        self.connect()

        self.cur.execute(
            "SELECT * FROM movies WHERE day=?",
            (day,),
        )

        result = self.cur.fetchone()
        self.cur.close()

        return result

    def getDayReviews(self, day):
        self.connect()

        self.cur.execute(
            "SELECT * FROM reviews LEFT JOIN movies USING(day) WHERE day=?",
            (day,),
        )

        result = self.cur.fetchall()
        self.cur.close()

        return result

    def deleteDay(self, day):
        self.connect()

        self.cur.execute(
            "DELETE FROM movies WHERE day=?",
            (day,),
        )

        print("committing changes...")

        self.conn.commit()

        self.cur.close()

        return

    def deleteReview(self, day, user_id):
        self.connect()

        self.cur.execute(
            "DELETE FROM reviews WHERE day=? AND rater_id = ?",
            (day, user_id),
        )

        print("committing changes...")

        self.conn.commit()

        self.cur.close()

        return

    def deleteAll(self):
        self.connect()

        self.cur.execute(
            "DELETE FROM movies",
        )

        print("committing changes...")

        self.conn.commit()

        self.cur.close()

        return

    def insertMovie(self, movie: Movie):
        self.connect()

        print(f"checking if day {movie.day} already has a pick...")
        self.cur.execute(
            "SELECT * FROM movies WHERE day=?",
            (movie.day,),
        )

        if self.cur.fetchone() is None:
            self.cur.execute(
                "INSERT INTO movies(day, tmdb_id, movie_title, showing_start, showing_end, picked_by, picker_avatar) VALUES (?,?,?,?,?,?,?)",
                (
                    movie.day,
                    movie.tmdb_id,
                    movie.movie_title,
                    movie.showing_start,
                    movie.showing_end,
                    movie.picked_by,
                    movie.picker_avatar,
                ),
            )
            print("day set...")
        else:
            self.cur.execute(
                "UPDATE movies SET tmdb_id=?, movie_title=?, showing_start=?, showing_end=?, picked_by=?, picker_avatar = ? WHERE day=?",
                (
                    movie.tmdb_id,
                    movie.movie_title,
                    movie.showing_start,
                    movie.showing_end,
                    movie.picked_by,
                    movie.picker_avatar,
                    movie.day,
                ),
            )
            print("day updated...")
        print("committing changes...")
        self.conn.commit()
        print("changes committed, closing connection...")
        self.conn.close()

    def insertReview(self, review: Review):
        self.connect()

        print(
            f"checking if {review.rater_name} already has review for day {review.day}..."
        )
        self.cur.execute(
            "SELECT * FROM reviews WHERE day=? AND rater_id=?",
            (
                review.day,
                review.rater_id,
            ),
        )

        if self.cur.fetchone() is None:
            self.cur.execute(
                "INSERT INTO reviews(day, rater_id, rater_name, rater_avatar, score, comment) VALUES (?,?,?,?,?,?)",
                (
                    review.day,
                    review.rater_id,
                    review.rater_name,
                    review.rater_avatar,
                    review.score,
                    review.comment,
                ),
            )
            print("review added...")
        else:
            self.cur.execute(
                "UPDATE reviews SET rater_name=?, rater_avatar=?, score=?, comment=? WHERE day=? AND rater_id=?",
                (
                    review.rater_name,
                    review.rater_avatar,
                    review.score,
                    review.comment,
                    review.day,
                    review.rater_id,
                ),
            )
            print("review updated...")
        print("committing changes...")
        self.conn.commit()
        print("changes committed, closing connection...")
        self.conn.close()

    def listMovies(self):
        self.connect()

        print("listing movies...")

        spook_list = f"# 🎃 SPOOKTOBER {datetime.now().year} MOVIE LIST 🎃\n```"
        self.cur.execute("SELECT day, movie_title FROM movies ORDER BY day DESC")
        res_dict = dict(self.cur.fetchall())
        for i in range(0, 31):
            spook_list = spook_list + f"{i + 1}. {res_dict.get(i+1, "N/A")}\n"
        spook_list = spook_list + "```"
        return spook_list
