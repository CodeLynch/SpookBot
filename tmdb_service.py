import os
import requests


class TMDBService:

    def __init__(self) -> None:
        self.TMDB_TOKEN = os.getenv("TMDB_TOKEN")
        self.TMDB_URL = "https://api.themoviedb.org/3"
        self.TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
        self.headers = {"Authorization": f"Bearer {self.TMDB_TOKEN}"}

    async def search(self, query):
        query = query.replace(" ", "+")
        url = f"{self.TMDB_URL}/search/movie?query={query}"

        print(f"fetching {url}...")

        r = requests.get(url, headers=self.headers)
        res = r.json()

        print(f"response received, {len(res['results'])} results")

        return res

    async def getMovie(self, id):
        url = f"{self.TMDB_URL}/movie/{int(id)}"

        print(f"fetching {url}...")

        r = requests.get(url, headers=self.headers)
        res = r.json()

        print(f"response received, sending result...")

        return res

    def formatMovieDetails(self, movie_json):
        return f"## 📽 {movie_json['original_title']}\n🔢 **ID**: {movie_json['id']}\n📅  **Date**: {movie_json['release_date']}\n🎬  **Synopsis**: {movie_json['overview']}\n**Runtime**: {movie_json['runtime']} mins\n [Poster]({self.TMDB_IMAGE_URL}{movie_json['poster_path']})"
