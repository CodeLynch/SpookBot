import discord
import os
from discord_select import DiscordSelect
from movie import Movie
from movie_sqli import MovieSqlite
from tmdb_service import TMDBService
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import View

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TMDBSvc = TMDBService()
MovieSvc = MovieSqlite()

bot = commands.Bot(command_prefix="$pook ", intents=intents)


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")


@bot.command()
async def greet(ctx):
    await ctx.send("the spook says hi!")


@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)


@bot.command()
async def search(ctx, *, arg):
    res = await TMDBSvc.search(arg)

    print(f"response received, {len(res['results'])}")

    if len(res["results"]) <= 0:
        await ctx.send("No movie found 😢")
    elif len(res["results"]) > 0:
        select = DiscordSelect(res)

        await ctx.send(
            "Please Select from query results",
            view=View().add_item(select),
        )


@bot.command()
async def set_day(ctx, day, time, movie_id):
    movie = await TMDBSvc.getMovie(movie_id)

    movieObj = Movie(day, movie["id"], movie["original_title"], time, time, ctx.author)

    await ctx.send(
        f"to insert: {movieObj.movie_title} for day {movieObj.day} at {movieObj.showing_start} as decided by {movieObj.picked_by}"
    )


@bot.command()
async def spook(ctx):
    await ctx.send("some spooky sht here")


bot.run(DISCORD_TOKEN or "")
