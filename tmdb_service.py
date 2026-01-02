import os
import requests
from discord import Embed


class TMDBService:

    def __init__(self) -> None:
        self.TMDB_TOKEN = os.getenv("TMDB_TOKEN")
        self.TMDB_URL = "https://api.themoviedb.org/3"
        self.TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
        self.headers = {"Authorization": f"Bearer {self.TMDB_TOKEN}"}

    async def search(self, query):
        try:
            query = query.replace(" ", "+")
            url = f"{self.TMDB_URL}/search/movie?query={query}&language=en-US"

            print(f"fetching {url}...")

            r = requests.get(url, headers=self.headers)
            res = r.json()

            print(f"response received, {len(res['results'])} results")

            return res
        except:
            print("TMDBService exception occured!")
            raise Exception("TMDBServiceException")

    async def getMovie(self, id):
        try:
            url = f"{self.TMDB_URL}/movie/{int(id)}?language=en-US"

            print(f"fetching {url}...")

            r = requests.get(url, headers=self.headers)
            res = r.json()

            print(f"response received, sending result...")

            return res
        except:
            print("TMDBService exception occured!")
            raise Exception("TMDBServiceException")

    def formatMovieDetails(self, movie_json):
        embd = Embed(
            title=f"📽 {movie_json['title']}",
            description=f"🔢 **ID**: {movie_json['id']}\n📅  **Date**: {movie_json['release_date']}\n🎬  **Synopsis**: {movie_json['overview']}\n**Runtime**: {movie_json['runtime']} mins",
        )
        embd.set_image(url=f"{self.TMDB_IMAGE_URL}{movie_json['poster_path']}")

        return embd

    def formatDayDetails(
        self,
        day,
        title_w_year,
        stream_start,
        stream_end,
        picker,
        picker_icon_url,
        movie_json,
    ):
        embd = Embed(
            title=f"🎃 **SPOOKTOBER DAY {day}** 🎃",
            description=f"**{title_w_year}**\n {movie_json['overview']} \n🎞 **Runtime**: {movie_json['runtime']} mins \n🍿**Tentative Streaming Time**: {stream_start}-{stream_end}\n",
        )
        embd.set_footer(text=f"Picked by: {picker}", icon_url=f"{picker_icon_url}")
        embd.set_image(url=f"{self.TMDB_IMAGE_URL}{movie_json['poster_path']}")
        return embd

    def formatMovieDetails(self, movie_json):
        embd = Embed(
            title=f"📽 {movie_json['title']}",
            description=f"🔢 **ID**: {movie_json['id']}\n📅  **Date**: {movie_json['release_date']}\n🎬  **Synopsis**: {movie_json['overview']}\n**Runtime**: {movie_json['runtime']} mins",
        )
        embd.set_image(url=f"{self.TMDB_IMAGE_URL}{movie_json['poster_path']}")

        return embd

    def formatDayReviews(
        self,
        day,
        title_w_year,
        stream_start,
        stream_end,
        picker,
        picker_icon_url,
        movie_json,
    ):
        embd = Embed(
            title=f"🎃 **SPOOKTOBER DAY {day}** 🎃",
            description=f"**{title_w_year}**\n {movie_json['overview']} \n🎞 **Runtime**: {movie_json['runtime']} mins \n🍿**Tentative Streaming Time**: {stream_start}-{stream_end}\n",
        )
        embd.set_footer(text=f"Picked by: {picker}", icon_url=f"{picker_icon_url}")
        embd.set_image(url=f"{self.TMDB_IMAGE_URL}{movie_json['poster_path']}")
        return embd
