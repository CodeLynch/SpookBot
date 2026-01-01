import discord
import os
import re
import random
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
ROLE_ID = os.getenv("SPOOKTOBER_ROLE_ID")
MY_ID = os.getenv("MY_ID")
TMDBSvc = TMDBService()
MovieSvc = MovieSqlite()

bot = commands.Bot(command_prefix="$pook ", intents=intents, help_command=None)
spookies = [
    "🎃Spooktober continues...🦇",
    "🌃 'tis a good night for spook 👻",
    "🎃 Another day, another spook 🎃",
    "🕸️🦇🦇 the spook welcomes you to a mysterious night 🦇🦇🕸️",
    "🎃 the spook 🎃 conjures a magical night 🧙",
    "🧡 the spook 🧡 delivers another treat 🍭",
    "🎃 the spook brings a dark night 🌃🧛",
    "🎃 the spook calls for you",
    "🎃 the spook is back 👻",
    "🎃 the spook rises once again 🧟",
    "💀 the spook 👻 beckons you to watch 🌑",
    "🎃 The spook 🎃 is out to get you 🪓 😱",
]
command_guide = """
### 🎦 Movie List \n
- **Search** - `<prefix> search [movie_name]` - search movies in TMDB  
- **Set Day** - `<prefix> set_day [day_number] [stream_start] [movie_tmdb_id] ` - select a movie for a certain day in October. Overwrites if there is a selected movie for that day.  
- **Get Day** - `<prefix> get_day [day_number]` - displays the movie details for a certain day in October.  
- **Clear Day** - `<prefix> clear_day [day_number]` - clears a certain day in October.  
- **List** - `<prefix> list` - shows the movie list  
- **Clear List** - `<prefix> clear_list` - clears the movie list.  
- **Announce** - `<prefix> announce` - send a message to announce the movie of the current day.  
### ⭐ Movie Ratings \n
- (WIP) **Rate** - `<prefix> rate [day_number] [rating]` - add a rating to a movie of a particular day.  
- (WIP) **Ratings** - `<prefix> ratings [day_number]` - check ratings of a movie of a particular day.  
### ⚙️ Misc \n
- **Say** - `<prefix> say [message]` - send a message.  
- **Spook** - `<prefix> spook` - send a random spiel about the spook.  
- **Help** - `<prefix> help`- display commands.  
"""


async def send_and_raise_error(ctx, message, error: type[Exception]):
    await ctx.send(message)
    raise error(message)


def isNumber(num):
    try:
        int(num)
    except ValueError:
        return False
    return True


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_and_raise_error(ctx, "❌ missing required arguments", Exception)
    else:
        raise error


@bot.command()
async def get_day(ctx, arg):
    try:
        if not isNumber(arg):
            await send_and_raise_error(ctx, "❌ day argument should be int", TypeError)
        int_day = int(arg)
        if int_day < 0 or int_day > 31:
            await send_and_raise_error(ctx, "❌ day argument beyond range", Exception)
        result = MovieSvc.getDay(arg)

        if result is None:
            await ctx.send("❌ No movie picked for that day...")
            return

        day = result[0]
        tmdb_id = result[1]
        title_with_year = result[2]
        stream_start = result[3]
        stream_end = result[4]
        picker = result[5]
        picker_icon_url = result[6]

        movie = await TMDBSvc.getMovie(tmdb_id)
        await ctx.send(
            embed=TMDBSvc.formatDayDetails(
                day,
                title_with_year,
                stream_start,
                stream_end,
                picker,
                picker_icon_url,
                movie,
            )
        )
    except:
        await ctx.send(f"❌ Exception occured while searching, please try again...")


@bot.command()
async def greet(ctx):
    await ctx.send("the spook says hi!")


@bot.command()
async def help(ctx):
    embd = discord.Embed(
        title=f"SpookBot Commands",
        description=f"{command_guide}",
    )

    await ctx.send(embed=embd)


@bot.command()
async def list(ctx):
    await ctx.send(MovieSvc.listMovies())


@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)


@bot.command()
async def search(ctx, *, arg):
    try:
        res = await TMDBSvc.search(arg)

        print(f"response received...")

        if len(res["results"]) <= 0:
            await ctx.send("No movie found 😢")
        elif len(res["results"]) > 0:
            select = DiscordSelect(res)

            await ctx.send(
                "Please select from the query results",
                view=View().add_item(select),
            )
    except:
        await ctx.send(f"❌ Exception occured while searching, please try again...")


@bot.command()
async def set_day(ctx, day, start_time, movie_id):
    if not isNumber(day):
        await send_and_raise_error(ctx, "❌ day argument should be int", TypeError)
    int_day = int(day)
    if int_day < 0 or int_day > 31:
        await send_and_raise_error(ctx, "❌ day argument beyond range", Exception)

    time_regex = re.compile("^([01]\\d|2[0-3]):[0-5]\\d$")

    if time_regex.match(start_time) is None:
        await send_and_raise_error(
            ctx, "❌ start_time argument should follow HH:mm format", Exception
        )

    movie = await TMDBSvc.getMovie(movie_id)

    if movie.get("success") != None or movie.get("success") == False:
        await send_and_raise_error(ctx, "❌ Movie not found...", Exception)

    temp_start = datetime(
        100, 1, 1, int(start_time.split(":")[0]), int(start_time.split(":")[1]), 0
    )
    temp_end = temp_start + timedelta(minutes=int(movie["runtime"]))
    end_time = f"{temp_end.hour}:{temp_end.minute}"

    title_with_year = f"{movie["title"]} ({datetime.strptime(movie["release_date"], '%Y-%m-%d').year})"

    movie_obj = Movie(
        day,
        movie["id"],
        title_with_year,
        start_time,
        end_time,
        str(ctx.author),
        str(ctx.author.display_avatar),
    )

    MovieSvc.insertMovie(movie_obj)

    await ctx.send(f"✅ Movie selected for day {day}")


@bot.command()
async def clear_day(ctx, day):
    try:
        if not isNumber(day):
            await send_and_raise_error(ctx, "❌ day argument should be int", TypeError)
        int_day = int(day)
        if int_day < 0 or int_day > 31:
            await send_and_raise_error(ctx, "❌ day argument beyond range", Exception)

        MovieSvc.deleteDay(day)

        await ctx.send(f"✅ cleared day {day}")
    except:
        await ctx.send(f"❌ Exception occured while clearing day, please try again...")


@bot.command()
async def clear_list(ctx):
    try:
        if str(ctx.author.id) != str(MY_ID):
            await ctx.send(
                f"I'm sorry <@{ctx.author.id}>, I'm afraid I can't let you do that"
            )
            return
        MovieSvc.deleteAll()

        await ctx.send(f"✅ cleared movie list")
    except:
        await ctx.send(f"❌ Exception occured while clearing list, please try again...")


@bot.command()
async def spook(ctx):
    await ctx.send(random.choice(spookies))


@bot.command()
async def announce(ctx):
    try:
        await ctx.send(f"<@&{ROLE_ID}>")
        await spook(ctx)
        await get_day(ctx, int(datetime.now().day))
    except:
        await ctx.send(
            f"❌ Exception occured while announcing movie, please try again..."
        )


bot.run(DISCORD_TOKEN or "")
