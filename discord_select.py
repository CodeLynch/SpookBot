import discord
from discord.ui import Select, View
from tmdb_service import TMDBService


def toSelectOption(result):
    truncated_title = (
        (result["title"][:50] + "..") if len(result["title"]) > 50 else result["title"]
    )

    return discord.SelectOption(
        label=f"{result['id']}",
        description=f"{truncated_title} - {result['release_date']}",
    )


class DiscordSelect(Select):
    def __init__(self, movies) -> None:
        super().__init__(options=list(map(toSelectOption, movies["results"])))

    async def callback(self, interaction):
        TMDBSvc = TMDBService()

        res = await TMDBSvc.getMovie(self.values[0])

        self.disabled = True
        await interaction.response.edit_message(view=View().add_item(self))
        await interaction.followup.send(embed=TMDBSvc.formatMovieDetails(res))
