import discord
from discord.ext import commands
from discord_components import DiscordComponents
from config.config import config_cogs, get_token
bot = commands.Bot(command_prefix='/')
DiscordComponents(bot)

token = get_token(11)  # old 11 new 13


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Playing Events'))


@bot.command()
async def clear(ctx):
    await ctx.reply('Delete all message successfull..', delete_after=5)
    await ctx.channel.purge()
config_cogs(bot)
bot.run(token)
