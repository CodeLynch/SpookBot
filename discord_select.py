import discord
from discord.ui import Select
from tmdb_service import TMDBService


def toSelectOption(result):
    return discord.SelectOption(
        label=f"{result['id']}",
        description=f"{result['original_title']} - {result['release_date']}",
    )


class DiscordSelect(Select):
    def __init__(self, movies) -> None:
        super().__init__(options=list(map(toSelectOption, movies["results"])))

    async def callback(self, interaction):
        TMDBSvc = TMDBService()

        res = await TMDBSvc.getMovie(self.values[0])
        await interaction.response.send_message(TMDBSvc.formatMovieDetails(res))
