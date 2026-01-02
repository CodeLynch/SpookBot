import discord
import os
import re
import random
from datetime import datetime, timedelta
from discord_select import DiscordSelect
from embed_service import EmbedService
from movie import Movie
from review import Review
from sqlite import Sqlite
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
MYSTERY_POSTER_URL = "https://dummyimage.com/500x750/ee5500/000000&text=%3F"
TMDBSvc = TMDBService()
embedSvc = EmbedService()
sqliteSvc = Sqlite()

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
- **Set Day** - `<prefix> set_day [day_number] [stream_start] [movie_tmdb_id] [is_mystery(optional)]` - select a movie for a certain day in October. Overwrites if there is a selected movie for that day. If `is_mystery` is true, `movie_tmdb_id` **argument is ignored** so it doesn't matter what value is inputted for that argument.
- **Get Day** - `<prefix> get_day [day_number]` - displays the movie details for a certain day in October.  
- **Clear Day** - `<prefix> clear_day [day_number]` - clears a certain day in October.  
- **List** - `<prefix> list` - shows the movie list  
- **Clear List** - `<prefix> clear_list` - clears the movie list.  
- **Announce** - `<prefix> announce` - send a message to announce the movie of the current day.  
### ⭐ Movie Ratings \n
- **Rate** - `<prefix> rate [day_number] [rating] [comment(optional)]` - add a rating of a movie for a particular day.  
- **Ratings** - `<prefix> ratings [day_number]` - check ratings of a movie for a particular day.  
- **Delete Rating** - `<prefix> delete_rating [day_number]` - remove your rating of a movie for a particular day.  
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
        result = sqliteSvc.getDay(arg)

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

        ## indicates a mystery movie
        if int(tmdb_id) == -1:
            movie = {
                "runtime": "???",
                "overview": "???",
                "release_date": "???",
                "poster_path": MYSTERY_POSTER_URL,
            }
            embed = embedSvc.formatDayDetails(
                day,
                title_with_year,
                stream_start,
                stream_end,
                picker,
                picker_icon_url,
                movie,
                MYSTERY_POSTER_URL,
            )
        else:
            movie = await TMDBSvc.getMovie(tmdb_id)
            embed = embedSvc.formatDayDetails(
                day,
                title_with_year,
                stream_start,
                stream_end,
                picker,
                picker_icon_url,
                movie,
            )

        await ctx.send(embed=embed)
    except Exception as e:
        print(f"error: {repr(e)}")
        await ctx.send(
            f"❌ Exception occured while retrieving day details, please try again..."
        )


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
    await ctx.send(sqliteSvc.listMovies())


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
    except Exception as e:
        print(f"error: {repr(e)}")
        await ctx.send(f"❌ Exception occured while searching, please try again...")


@bot.command()
async def set_day(ctx, day, start_time, movie_id, is_mystery=False):
    # day argument validations
    if not isNumber(day):
        await send_and_raise_error(ctx, "❌ day argument should be int", TypeError)
    int_day = int(day)
    if int_day < 1 or int_day > 31:
        await send_and_raise_error(
            ctx, "❌ day argument beyond range (1-31 only)", Exception
        )

    # start_time argument validations
    time_regex = re.compile("^([01]\\d|2[0-3]):[0-5]\\d$")

    if time_regex.match(start_time) is None:
        await send_and_raise_error(
            ctx, "❌ start_time argument should follow HH:mm format", Exception
        )
    if is_mystery:
        movie_obj = Movie(
            day,
            -1,
            "???",
            start_time,
            "???",
            str(ctx.author),
            str(ctx.author.display_avatar),
        )

    else:
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

    sqliteSvc.insertMovie(movie_obj)

    await ctx.send(f"✅ Movie selected for day {day}")


@bot.command()
async def clear_day(ctx, day):
    try:
        if not isNumber(day):
            await send_and_raise_error(ctx, "❌ day argument should be int", TypeError)
        int_day = int(day)
        if int_day < 1 or int_day > 31:
            await send_and_raise_error(
                ctx, "❌ day argument beyond range (1-31 only)", Exception
            )

        sqliteSvc.deleteDay(day)

        await ctx.send(f"✅ cleared day {day}")
    except Exception as e:
        print(f"error: {repr(e)}")
        await ctx.send(f"❌ Exception occured while clearing day, please try again...")


@bot.command()
async def clear_list(ctx):
    try:
        if str(ctx.author.id) != str(MY_ID):
            await ctx.send(
                f"I'm sorry <@{ctx.author.id}>, I'm afraid I can't let you do that"
            )
            return
        sqliteSvc.deleteAll()

        await ctx.send(f"✅ cleared movie list")
    except Exception as e:
        print(f"error: {repr(e)}")
        await ctx.send(f"❌ Exception occured while clearing list, please try again...")


@bot.command()
async def rate(ctx, day, score, comment=None):
    try:
        # day argument validations
        if not isNumber(day):
            await send_and_raise_error(ctx, "❌ day argument should be int", TypeError)
        int_day = int(day)
        if int_day < 1 or int_day > 31:
            await send_and_raise_error(ctx, "❌ day argument beyond range", Exception)

        # score argument validations
        if not isNumber(score):
            await send_and_raise_error(
                ctx, "❌ score argument should be int", TypeError
            )
        int_score = int(score)
        if int_score < 0 or int_score > 5:
            await send_and_raise_error(
                ctx, "❌ score argument beyond range (0-5 only)", Exception
            )

        # check if movie is picked for day
        if sqliteSvc.getDay(day) is None:
            await ctx.send("❌ No movie picked for that day...")
            return

        review_obj = Review(
            str(ctx.author.id),
            day,
            score,
            str(ctx.author),
            str(ctx.author.display_avatar),
            comment,
        )

        sqliteSvc.insertReview(review_obj)

        await ctx.send(
            f"🌟 **{str(ctx.author)}'s** rating for the movie of day {day}: **{score} stars**"
        )
    except Exception as e:
        print(f"error: {repr(e)}")
        await ctx.send(f"❌ Exception occured while adding rating, please try again...")


@bot.command()
async def ratings(ctx, day):
    try:
        # day argument validations
        if not isNumber(day):
            await send_and_raise_error(ctx, "❌ day argument should be int", TypeError)
        int_day = int(day)
        if int_day < 1 or int_day > 31:
            await send_and_raise_error(ctx, "❌ day argument beyond range", Exception)

        day_details = sqliteSvc.getDay(day)

        if day_details is None:
            await ctx.send("❌ No movie picked for that day...")
            return

        tmdb_id = day_details[1]
        title_with_year = day_details[2]
        picker = day_details[5]
        picker_icon_url = day_details[6]
        overwrite_poster = None

        if int(tmdb_id) == -1:
            movie = {"poster_path": MYSTERY_POSTER_URL}
            overwrite_poster = MYSTERY_POSTER_URL
        else:
            movie = await TMDBSvc.getMovie(tmdb_id)

        reviews = sqliteSvc.getDayReviews(day)
        embedReviews = embedSvc.formatDayReviews(
            day,
            title_with_year,
            reviews,
            picker,
            picker_icon_url,
            movie,
            overwrite_poster,
        )

        await ctx.send(embed=embedReviews)
    except Exception as e:
        print(f"error: {repr(e)}")
        await ctx.send(
            f"❌ Exception occured while retrieving ratings, please try again..."
        )


@bot.command()
async def spook(ctx):
    await ctx.send(random.choice(spookies))


@bot.command()
async def announce(ctx):
    try:
        await ctx.send(f"<@&{ROLE_ID}>")
        await spook(ctx)
        await get_day(ctx, int(datetime.now().day))
    except Exception as e:
        print(f"error: {repr(e)}")
        await ctx.send(
            f"❌ Exception occured while announcing movie, please try again..."
        )


bot.run(DISCORD_TOKEN or "")
