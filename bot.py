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
# bot.remove_command("help")


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


# @bot.command(aliases=["commands", "h"], description="Affiche les commandes.")
# async def help(ctx, args=None):
#     """
#     !help / !h // !help <commande>
#     """
#     command_names_list = [x.name for x in bot.commands]
#     cogs_names_list = [x for x in bot.cogs]
#     if not args:
#         h_embed.clear_fields()
#         h_embed.set_author(name="Commandes Disponibles")
#         misc_cog = bot.get_cog('Misc')
#         misc_cmds = misc_cog.get_commands()
#         h_embed.add_field(name=f"{misc_cog.qualified_name}", value="-----", inline=True)
#         for cmd in misc_cmds:
#             h_embed.add_field(name=f"`{cmd.help}`", value=f"{cmd.description}", inline=False)
#         mute_cog = bot.get_cog('Mutes')
#         mute_cmds = mute_cog.get_commands()
#         h_embed.add_field(name=f"{mute_cog.qualified_name}", value="----", inline=False)
#         for cmd in mute_cmds:
#             h_embed.add_field(name=f"`{cmd.help}`", value=f"{cmd.description}", inline=False)
#         move_cog = bot.get_cog('Moves')
#         move_cmds = move_cog.get_commands()
#         h_embed.add_field(name=f"{move_cog.qualified_name}", value="----", inline=False)
#         for cmd in move_cmds:
#             h_embed.add_field(name=f"{cmd.help}", value=f"{cmd.description}", inline=False)
#         roles_cog = bot.get_cog('Roles')
#         roles_cmds = roles_cog.get_commands()
#         h_embed.add_field(name=f"{roles_cog.qualified_name}", value="----", inline=False)
#         for cmd in roles_cmds:
#             h_embed.add_field(name=f"`{cmd.help}`", value=f"{cmd.description}", inline=False)
#         return await ctx.send(embed=h_embed)
#     elif args in cogs_names_list:
#         cog = bot.get_cog(args)
#         h_embed.clear_fields()
#         h_embed.set_author(name=f"{cog.qualified_name}")
#         cmds = cog.get_commands()
#         for cmd in cmds:
#             h_embed.add_field(name=f"`{cmd.help}`", value=f"{cmd.description}", inline=False)
#         return await ctx.send(embed=h_embed)
#     elif args in command_names_list:
#         h_embed.clear_fields()
#         h_embed.add_field(name=args, value=bot.get_command(args).help)
#         return await ctx.send(embed=h_embed)
#     else:
#         e_embed.clear_fields()
#         e_embed.add_field(name="Erreur", value="Cette commande n'existe pas")
#         return await ctx.send(embed=e_embed)


# @commands.command()
# def help(self, ctx: Context):
#     embed = Embed()
#
#     embed.title = f"Admin commands of  {self.qualified_name}"
#     for command in self.get_commands():
#         name = command.name
#         description = command.description
#         passes_check = True
#         for check in command.checks:
#             if not check(ctx.author):
#                 passes_check = False
#                 break
#         if passes_check:
#             embed.add_field(name=name, value=description, inline=False)
#
#     await ctx.send(embed=embed)

# RUN
# ==========================================================================================
# bot.run(TOKEN)


async def main():
    """
    Main function.
    """
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
