import discord
import os
from datetime import datetime, timedelta
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
async def list(ctx):
    await ctx.send(MovieSvc.listMovies())


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
async def set_day(ctx, day, start_time, movie_id):
    movie = await TMDBSvc.getMovie(movie_id)

    temp_start = datetime(
        100, 1, 1, int(start_time.split(":")[0]), int(start_time.split(":")[1]), 0
    )
    temp_end = temp_start + timedelta(minutes=int(movie["runtime"]))
    end_time = f"{temp_end.hour}:{temp_end.minute}"

    movie_obj = Movie(
        day, movie["id"], movie["original_title"], start_time, end_time, str(ctx.author)
    )

    MovieSvc.insertMovie(movie_obj)

    await ctx.send(f"✅ Movie selected for day {day}")


@bot.command()
async def spook(ctx):
    await ctx.send("some spooky sht here")


bot.run(DISCORD_TOKEN or "")
