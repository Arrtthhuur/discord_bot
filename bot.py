# bot.py

# Imports
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
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# IDs
BOT_ID = 962702131498979400
BOT_CHAN = 964285664130641960

LOG_ID = 962759786783453204

MSG_LOG_CHAN = 964582976782479462

LINKER_ROLE = 963870403628007475


# Embed
e_embed = discord.Embed(color=discord.Color.red())  # Error


# Badwords
badwords = ["fispute", 'tamere', 'sam', 'samuel']


# BOT INIT
# ==========================================================================================
intents = discord.Intents.all()
# bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True, help_command=None)
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
# bot.remove_command("help")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")



@bot.command()
async def pcog(ctx, cog_name):
    cog = bot.get_cog(cog_name)
    commands = cog.get_commands()
    print([c.name for c in commands])


@bot.event
async def on_message(message):
    """
    Bot reacts to message.
    Delete links.
    Censures profanity.
    Only reacts to commands when entered in the bot channel.
    """
    if message.author.id == BOT_ID:
        return
    for i in badwords:
        if i in message.content:
            await message.delete()
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"Tsss, ta mere serait fiere de toi...")
            await message.channel.send(f"{message.author.mention}", embed=e_embed)
            bot.dispatch('profanity', message, i)
            break
    if 'https://' in message.content or 'http://' in message.content:
        role = discord.utils.get(message.guild.roles, id=LINKER_ROLE)
        if role not in message.author.roles:
            await message.delete()
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"Tiens, ton lien du Q.")
            await message.channel.send(f"{message.author.mention}", embed=e_embed)
            return
    if message.content.startswith('!'):
        if message.channel.id != BOT_CHAN:
            await message.delete()
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"Entre les commandes dans le channel bot.")
            await message.channel.send(f"{message.author.mention}", embed=e_embed)
            return
    await log(message)
    await bot.process_commands(message)


async def log(message):
    """
    Logging messages with content, author, channel, date and time.
    """
    channel = discord.utils.get(message.guild.channels, id=MSG_LOG_CHAN)
    m_hour = message.created_at.strftime('%H:%M')
    m_date = message.created_at.strftime('%d/%m/%Y')
    if message.author.id != BOT_ID:
        await channel.send(f"\" ***{message.content}*** \" envoye par **{message.author.name}**, sur le channel "
                           f"***{message.channel.name}***, a {m_hour} le {m_date}")



# @bot.command(aliases=["commands", "h"])
# async def help(ctx, args=None):
#     command_names_list = [x.name for x in bot.commands]
#     if not args:
#         h_embed.clear_fields()
#         h_embed.set_author(name="=============   Commandes Disponibles   =============")
#         h_embed.add_field(name="---------------------------------   Misc   ---------------------------------",
#                           value="`!...`", inline=False)
#         h_embed.add_field(name="`!help <commande>`", value="Plus d'info sur une commande", inline=False)
#         h_embed.add_field(name="`!hello`", value="Couscous", inline=True)
#         h_embed.add_field(name="`!coffee`", value="Petit cafe?", inline=True)
#         h_embed.add_field(name="`!refresh`", value="Refresh le compteur d'humains", inline=False)
#
#         h_embed.add_field(name="---------------------------------   Move   ---------------------------------",
#                           value="`!...`", inline=False)
#         h_embed.add_field(name="`!move <membre> <voice_channel>`",
#                         value="Deplace un membre vers un Voice Channel", inline=False)
#         h_embed.add_field(name="`!war` / `!w`",
#                         value="Deplace tous les membres du role War vers le VC War", inline=False)
#         h_embed.add_field(name="`!secret` / `!s`",
#                         value="Deplace un membre vers ton VC secret", inline=False)
#         h_embed.add_field(name="`!sexit` / `!se`",
#                         value="Sors un membre de ton VC secret", inline=False)
#         h_embed.add_field(name="`!aucoin` <membre> / `!ac <membre>`",
#                         value="Envoie un membre au coin", inline=False)
#         h_embed.add_field(name="`!cbon` <membre> / `!cb <membre>`",
#                         value="L'autre con du coin peut revenir", inline=False)
#
#         h_embed.add_field(name="------------------------------   Roles/Reset   ------------------------------",
#                           value="`!...`", inline=False)
#         h_embed.add_field(name="`!join <faction>` / `!j <faction>`",
#                         value="Rejoins ta faction: A, B ou C", inline=False)
#         h_embed.add_field(name="`!reset` / `!r`",
#                         value="Restaure toi les roles par defaut", inline=False)
#
#         h_embed.add_field(name="-------------------------------   Sons/Mics   -------------------------------",
#                           value="`!...`", inline=False)
#         h_embed.add_field(name="`!mute <membre>` / `!m <membre>`", value="Mute un membre specifique",
#                         inline=False)
#         h_embed.add_field(name="`!unmute <membre>` / `!u <membre>`", value="Un-mute un membre specifique",
#                         inline=False)
#         h_embed.add_field(name="`!deafen <membre>` / `!d <membre>`", value="Deafen un membre specifique",
#                         inline=False)
#         h_embed.add_field(name="`!undeafen <membre>` / `!ud <membre>`", value="Un-deafen un membre specifique",
#                         inline=False)
#         h_embed.add_field(name="`!all` / `!a`", value="Mute et Deafen tous les membres de ton VC",
#                         inline=False)
#         h_embed.add_field(name="`!unall` / `!ua`", value="Un-mute et Un-deafen tous les membres de ton VC",
#                         inline=False)
#         h_embed.add_field(name="`!timeout <membre> <temps> <unite>` / `!t <m> <t> <u>`", value="Timeout un membre "
#                                                                                         "pour un certain temps",
#                         inline=False)
#         return await ctx.send(embed=h_embed)
#     elif args in command_names_list:
#         h_embed.clear_fields()
#         h_embed.add_field(name=args, value=bot.get_command(args).help)
#         return await ctx.send(embed=h_embed)
#     else:
#         e_embed.clear_fields()
#         e_embed.add_field(name="Erreur", value="Cette commande n'existe pas")
#         return await ctx.send(embed=e_embed)


# RUN
# ==========================================================================================

# bot.run(TOKEN)
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
