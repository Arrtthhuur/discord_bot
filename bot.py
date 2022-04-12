# bot.py

# Imports
import os
import random
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Intents enabling
intents = discord.Intents.default()
intents.members = True

# .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# IDs
GENERAL_ID = 962702912117669961
LOG_ID = 962759786783453204
VAGABOND_ID = 963168526733021254
A_ID = 963159344680149022
B_ID = 963159369728557096

# Bot init
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# Badwords
badwords = ['fispute', 'tamere', 'sam']


# BOT EVENTS
# ==========================================================================================

# Bot ready status
@bot.event
async def on_ready():
    print("Ready")


# Link delete
@bot.event
async def on_message(message):
    if ('https://' or "http://") in message.content:
        await message.delete()
        await message.channel.send(f"{message.author.mention} Tiens, ton lien pourri la")
    else:
        await bot.process_commands(message)


# Profanity msg log
@bot.event
async def on_profanity(message, word):
    channel = bot.get_channel(LOG_ID)
    embed = discord.Embed(title="Alerte aux gromo!", description=f"{message.author.name} a dit ||{word}||",
                          color=discord.Color.blurple())
    await channel.send(embed=embed)


# Profanity delete
@bot.event
async def on_message(message):
    for i in badwords:
        if i in message.content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Tsss, ta mere serait fiere de toi...")
            bot.dispatch('profanity', message, i)
            return
    await bot.process_commands(message)


# Join msg
@bot.event
async def on_member_join(member):
    await bot.get_channel(GENERAL_ID).send(f"Bienvenue {member.name}!")
    role = discord.utils.get(member.guild.roles, name="Vagabond")
    await member.add_roles(role)
    await bot.get_channel(GENERAL_ID).send(f"{member.mention}, tu fais maintenant partie des vagabonds, "
                                           f"rejoins la faction A ou B!")


# Remove msg
@bot.event
async def on_member_remove(member):
    await bot.get_channel(GENERAL_ID).send(f"Ciao {member.name}!")


# BOT COMMANDS
# ==========================================================================================

# Hello command
@bot.command(name='couscous', help="Recois le bonjour du bot", description="Salutations")
async def hello(ctx):
    await ctx.send(f"Yeyow {ctx.author.mention}!")


# Random msg command
@bot.command(name='rand', help='Affiche une phrase random', description="Quelques phrases random")
async def rand_msg(ctx):
    rand_messages = [
        'euh bonjour vous allez bien',
        'ah wewe',
        (
                   'Hela le gul, ',
                   'bien ou bien'
        ),
    ]
    response = random.choice(rand_messages)
    await ctx.send(response)


# Give role to author
# If is not already in role
# Or if is not in other role
@bot.command(name='join', help='Rejoins ta faction', description='Faction: A ou B, par defaut: Vagabond')
async def join_role(ctx, faction):
    member = ctx.author
    vagabond = discord.utils.get(member.guild.roles, id=VAGABOND_ID)
    to_apply = discord.utils.find(lambda r: r.name == faction, ctx.guild.roles)
    if not discord.utils.get(ctx.guild.roles, name=faction):
        await ctx.send("Cette faction n'existe pas")
    elif discord.utils.get(ctx.author.roles, name=faction):
        await ctx.send("T'es deja avec les frangins cong de tes mor")
    elif not discord.utils.get(ctx.author.roles, name="Vagabond"):
        await ctx.send("Bien essaye, reste chez toi p'tit gamin")
    else:
        await member.add_roles(to_apply)
        await member.remove_roles(vagabond)
        await ctx.send(f"Hola que tal {ctx.author.mention} bienvenue chez {to_apply.name}")


@bot.command(name='reset', help='Restaure les roles par defaut', description='Vagabond, A ou B')
async def reset_role(ctx):
    member = ctx.author
    vagabond = discord.utils.get(member.guild.roles, id=VAGABOND_ID)
    role_get = discord.utils.get(member.roles)
    if member.roles is None:
        print("Error - User has no role")
    else:
        for role in member.roles:
            try:
                await member.remove_roles(role)
            except:
                print("Error - Cannot delete @everyone")
        await member.add_roles(vagabond)
        await ctx.send(f"{ctx.author.mention} te revoila {vagabond.name}")

# RUN
# ==========================================================================================
bot.run(TOKEN)
