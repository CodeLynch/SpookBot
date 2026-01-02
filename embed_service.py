from discord import Embed


class EmbedService:
    def __init__(self) -> None:
        self.TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

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
        poster_url=None,
    ):
        embd = Embed(
            title=f"🎃 **SPOOKTOBER DAY {day}** 🎃",
            description=f"**{title_w_year}**\n {movie_json['overview']} \n🎞 **Runtime**: {movie_json['runtime']} mins \n🍿**Tentative Streaming Time**: {stream_start}-{stream_end}\n",
        )
        embd.set_footer(text=f"Picked by: {picker}", icon_url=f"{picker_icon_url}")
        embd.set_image(
            url=poster_url or f"{self.TMDB_IMAGE_URL}{movie_json['poster_path']}"
        )
        return embd

    def formatDayReviews(
        self,
        day,
        title_w_year,
        reviews,
        picker,
        picker_icon_url,
        movie_json,
        poster_url=None,
    ):
        print(f"movie: {movie_json}")
        embd = Embed(
            title=f"🎃 **SPOOKTOBER DAY {day} RATINGS** 🎃",
            description=f"## {title_w_year}",
        )
        embd.set_thumbnail(
            url=poster_url or f"{self.TMDB_IMAGE_URL}{movie_json['poster_path']}"
        )
        if len(reviews) > 0:
            for review in reviews:
                rating_string = ""
                for _ in range(0, int(review[4])):
                    rating_string = rating_string + "⭐"
                if review[5] is not None:
                    rating_string = rating_string + f" - *{review[5]}*"

                embd.add_field(
                    name=f"{review[2]}'s rating", value=f"{rating_string}", inline=False
                )
        embd.set_footer(
            text=f"Movie picked by: {picker}", icon_url=f"{picker_icon_url}"
        )
        return embd
