# bot.py

# Imports
# ==========================================================================================
import os
import discord
import asyncio
import datetime
import discord.ui

from discord.ext import commands
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument
from dotenv import load_dotenv
from datetime import datetime


# .env
# ==========================================================================================
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


h_embed = discord.Embed(color=discord.Color.blurple())  # Help
e_embed = discord.Embed(color=discord.Color.red())  # Error


# BOT INIT
# ==========================================================================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True, help_command=None)
# bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
bot.remove_command("help")


# Code
# ==========================================================================================
@bot.command(description="test")
async def pcog(ctx, cog_name):
    """
    Testing cod.
    """
    cog = bot.get_cog(cog_name)
    commands = cog.get_commands()
    print([c.name for c in commands])


async def load_extensions():
    """
    Load needed extensions (i.e. Cogs).
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # print ("", filename)
            await bot.load_extension(f"cogs.{filename[:-3]}")


# RUN
# ==========================================================================================
async def main():
    """
    Main function.
    """
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
