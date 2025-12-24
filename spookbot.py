import discord
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Select, View

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TMDB_TOKEN = os.getenv('TMDB_TOKEN')

TMDB_URL='https://api.themoviedb.org/3'
TMDB_IMAGE_URL='https://image.tmdb.org/t/p/w500'

bot = commands.Bot(command_prefix='$pook ', intents=intents)

def toSelectOption(result):
    return discord.SelectOption(label=f'{result['id']}', description=f'{result['original_title']} - {result['release_date']}')

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.command()
async def greet(ctx):
    await ctx.send('the spook says hi!')

@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
async def spook(ctx):
    await ctx.send('some spooky sht here')

@bot.command()
async def search(ctx, *, arg):
    headers = {'Authorization': f'Bearer {TMDB_TOKEN}'}
    query = arg.replace(' ', '+')
    url = (f'{TMDB_URL}/search/movie?query={query}')

    print(f'fetching {url}...')

    r = requests.get(url , headers=headers)
    res = r.json()

    print(f'response received, {len(res['results'])}')
    if len(res['results']) <= 0: 
        await ctx.send('No movie found 😢')
    elif len(res['results']) > 1:
        select = Select(options=list(map(toSelectOption, res['results'])))

        async def onSelect(interaction):
            url = (f'{TMDB_URL}/movie/{int(select.values[0])}')

            print(f'fetching {url}...')

            r = requests.get(url , headers=headers)
            res = r.json()

            print(f'response received, sending result... {res}')
            await ctx.send(f'## 📽 {res['original_title']}\n📅  **Date**: {res['release_date']}\n🎬  **Synopsis**: {res['overview']}\n**Runtime**: {res['runtime']} mins\n [Poster]({TMDB_IMAGE_URL}{res['poster_path']})')

        select.callback = onSelect

        await ctx.send('Multiple movies found, please select from results', view=View().add_item(select))
    else:
        await ctx.send(f'## 📽 {res['results'][0]['original_title']}\n📅  **Date**: {res['results'][0]['release_date']}\n🎬  **Synopsis**: {res['results'][0]['overview']}\n [Poster]({TMDB_IMAGE_URL}{res['results'][0]['poster_path']})')


bot.run(DISCORD_TOKEN or '')

