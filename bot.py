import discord
from discord.ext import commands
import sys, traceback

INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    intents=INTENTS,
    command_prefix="<"
)

@bot.event
async def setup_hook() -> None:
    await bot.load_extension("extensions.base")
    await bot.load_extension("extensions.urbex")
    await bot.load_extension("extensions.utility")
    await bot.load_extension("extensions.fun")
    await bot.load_extension("extensions.chatgpt")
    await bot.load_extension("extensions.TDUAS")

bot.run("token")