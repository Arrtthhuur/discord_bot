# bot.py

# Useful Abbreviations
# --------------------
# VC = Voice Channel
#
#
#
#

# Imports
import os
import discord
import asyncio
import datetime


from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime


# Intents enabling
intents = discord.Intents.default()
intents.members = True


# .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# IDs
SERVER_ID = 962702912117669958

BOT_CHAN = 964285664130641960
BOT_ID = 962702131498979400

COUNT_CHAN = 964509869724041256

LOG_ID = 962759786783453204

MSG_LOG_CHAN = 964582976782479462

GENERAL_CHAN = 962702912117669962
GENERAL_TEXT_CHAN = 964287069667086356

ARRIVEE_CHAN = 964288388238831737
DEPART_CHAN = 964288408262443048

WAR_CHAN = 963881045722292224
WAR_ROLE = 963881736016658463

SECRET_CHAN = 964279615541624932
SECRET_ROLE = 964279750975696946

LINKER_ROLE = 963870403628007475
VAGABOND_ROLE = 963168526733021254
A_ROLE = 963159344680149022
B_ROLE = 963159369728557096


# Bot init
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True, help_command=None)
bot.remove_command("help")


# Embed
e_embed = discord.Embed(color=discord.Color.red())  # Error
s_embed = discord.Embed(color=discord.Color.green())  # Success
h_embed = discord.Embed(color=discord.Color.blue())  # Help
w_embed = discord.Embed(color=discord.Color.dark_red())  # War
o_embed = discord.Embed(color=discord.Color.orange())  # misc

# Badwords
badwords = ["fispute", 'tamere', 'sam', 'samuel']


# BOT EVENTS
# ==========================================================================================

# Bot ready status.
@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_message(message):
    """Bot reacts to message.
    Delete links.
    Censures profanity.
    Only reacts to commands when entered in the bot channel.
    """
    role = discord.utils.get(message.author.roles, id=LINKER_ROLE)
    for i in badwords:
        if i in message.content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Tsss, ta mere serait fiere de toi...")
            bot.dispatch('profanity', message, i)
            break
    if 'https://' in message.content or 'http://' in message.content:
        if role is None:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Tiens, ton lien pourri la")
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
    channel = bot.get_channel(MSG_LOG_CHAN)
    m_hour = message.created_at.strftime('%H:%M')
    m_date = message.created_at.strftime('%d/%m/%Y')
    if message.author.id != BOT_ID:
        await channel.send(f"\" ***{message.content}*** \" envoye par **{message.author}**, sur le channel "
                           f"***{message.channel.name}***, a {m_hour} le {m_date}")


@bot.event
async def on_profanity(message, word):
    """Bot displays the profanity in the log channel"""
    channel = bot.get_channel(LOG_ID)
    embed = discord.Embed(title="Alerte aux gromo!", description=f"{message.author.name} a dit ||{word}||",
                          color=discord.Color.blurple())
    await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    """Bot welcomes newcomers"""
    await count_members(member)
    gen_chan = bot.get_channel(ARRIVEE_CHAN)
    role = discord.utils.get(member.guild.roles, name="Vagabond")
    await member.add_roles(role)
    await gen_chan.send(f"Bienvenue {member.mention}, tu fais maintenant "
                                                  f"partie des vagabonds, rejoins la faction A ou B!")


@bot.event
async def on_member_remove(member):
    """Bot farewells"""
    await count_members(member)
    await bot.get_channel(DEPART_CHAN).send(f"Ciao {member.name}!")


async def count_members(member):
    """Count the members, without the bot"""
    guild_id = member.guild.id
    guild = bot.get_guild(guild_id)
    member_count = guild.member_count - 1
    count_chan = bot.get_channel(COUNT_CHAN)
    await count_chan.edit(name="{0} {1}".format("Humans:", member_count))


# BOT COMMANDS
# ==========================================================================================

@bot.command()
async def hello(ctx):
    """
    !hello
    Le bot te dit bonjour.
    """
    await ctx.send(f"Yeyow {ctx.author.mention}! Comment i' va?")


@bot.command(aliases=["j"])
async def join(ctx, faction):
    """
    !join <faction> / !j <faction>
    Rejoins une faction.
    """
    author = ctx.author
    guild_roles = discord.utils.get(ctx.guild.roles, name=faction)
    auth_roles = discord.utils.get(ctx.author.roles, name=faction)
    vaga_role = discord.utils.get(ctx.author.roles, id=VAGABOND_ROLE)
    to_apply = discord.utils.find(lambda r: r.name == faction, ctx.guild.roles)
    vagabond = discord.utils.get(author.guild.roles, id=VAGABOND_ROLE)
    if not guild_roles:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"{faction} n'existe pas")
        await ctx.send(f"{author.mention}", embed=e_embed)
    elif auth_roles:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Tu es deja dans cette faction")
        await ctx.send(f"{author.mention}", embed=e_embed)
    elif not vaga_role:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Tu ne peux pas rejoindre une faction adverse")
        await ctx.send(f"{author.mention}", embed=e_embed)
    else:
        await author.add_roles(to_apply)
        await author.remove_roles(vagabond)
        s_embed.clear_fields()
        s_embed.set_author(name=f"Bienvenue chez {to_apply.name}")
        await ctx.send(f"{author.mention}", embed=s_embed)


@bot.command()
async def move(ctx, member_to_move, channel_dest):
    """
    !move <membre> <channel>
    Deplace un membre vers un channel.
    """
    channel = discord.utils.get(ctx.guild.channels, name=channel_dest)
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    author = ctx.author
    if channel is None and member is None:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"<<{member_to_move}>> et <<{channel_dest}>> n'existent pas")
        await ctx.send(f"{author.mention}", embed=e_embed)
        return
    elif channel is None:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le channel <<{channel_dest}>> n'existe pas")
        await ctx.send(f"{author.mention}", embed=e_embed)
        return
    elif member is None:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<{member_to_move}>> n'existe pas")
        await ctx.send(f"{author.mention}", embed=e_embed)
        return
    elif not author.guild_permissions.move_members:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Tu n'es pas demenageur")
        await ctx.send(f"{author.mention}", embed=e_embed)
        return
    try:
        await member.move_to(channel)
        s_embed.clear_fields()
        s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
        await ctx.send(f"{author.mention}", embed=s_embed)
    except:
        print("Error - Move")


@bot.command(aliases=["w"])
async def war(ctx):
    """
    !war / !w
    Deplace tous les membres War dans le channel War.
    """
    channel = bot.get_channel(WAR_CHAN)
    war_role = discord.utils.get(ctx.guild.roles, id=WAR_ROLE)
    author = ctx.author
    if war_role not in author.roles:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Tu n'es pas demenageur, meme en temps de guerre")
        await ctx.send(f"{author.mention}", embed=e_embed)
        return
    for member in ctx.guild.members:
        if not member.bot:
            if war_role not in member.roles:
                print("Error - " + str(member) + " - missing War role")
            elif member.voice is None:
                print("Error - " + str(member) + " - not Voice connected")
            else:
                try:
                    await member.move_to(channel)
                    w_embed.clear_fields()
                    w_embed.add_field(name="WAR", value=f"Gulyzm appelle a la guerre!")
                    await member.send(embed=w_embed)
                except:
                    print("Error - bigmove")


@bot.command(aliases=["s"])
async def secret(ctx, member_to_move):
    """
    !secret <membre> / !s <membre>
    Deplace un membre vers ton VC secret.
    """
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    secret_role = discord.utils.get(ctx.author.roles, id=SECRET_ROLE)
    channel = bot.get_channel(SECRET_CHAN)
    if not member:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<{member_to_move}>> n'existe pas.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        return
    if ctx.guild:
        if member.voice:
            if author.guild_permissions.move_members and secret_role:
                await member.move_to(channel)
                await member.add_roles(secret_role)
                s_embed.clear_fields()
                s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
                await ctx.send(f"{author.mention}", embed=s_embed)
            else:
                e_embed.clear_fields()
                e_embed.add_field(name="Erreur", value="Tu n'as pas les droits.")
                await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        else:
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"{member_to_move} n'est pas connecte a un VC.")
            await ctx.send(f"{ctx.author.mention}", embed=e_embed)


@bot.command(aliases=["se"])
async def sexit(ctx, member_to_move):
    """
    !sexit <membre> / !s <membre>
    Sors un membre de ton VC secret.
    """
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    channel = bot.get_channel(GENERAL_CHAN)
    secret_role = discord.utils.get(ctx.author.roles, name="Agent Secret")
    if not member:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<{member_to_move}>> n'existe pas.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        return
    if ctx.guild:
        if member.voice:
            if author.guild_permissions.move_members and secret_role:
                await member.move_to(channel)
                await member.remove_roles(secret_role)
            else:
                e_embed.clear_fields()
                e_embed.add_field(name="Erreur", value="Tu n'as pas les droits.")
                await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        else:
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"{member_to_move} n'est pas connecte a un VC.")
            await ctx.send(f"{ctx.author.mention}", embed=e_embed)


@bot.command(aliases=["m"])
async def mute(ctx, member_to_mute):
    """
    !mute <membre> / !m <membre>
    Mute un membre.
    """
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_mute)
    if not member:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<{member_to_mute}>> n'existe pas.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        return
    if ctx.guild:
        if member.voice:
            if author.guild_permissions.mute_members:
                await member.edit(mute=True)
                s_embed.clear_fields()
                s_embed.set_author(name=f"Muted {member.name}")
                await ctx.send(f"{ctx.author.mention}", embed=s_embed)
            else:
                e_embed.clear_fields()
                e_embed.add_field(name="Erreur", value="Tu n'as pas les droits.")
                await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        else:
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"{member_to_mute} n'est pas connecte a un VC.")
            await ctx.send(f"{ctx.author.mention}", embed=e_embed)
    else:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Erreur de chat.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)


@bot.command(aliases=["u"])
async def unmute(ctx, member_to_unmute):
    """
    !unmute <membre> / !u <membre>
    Un-mute un membre.
    """
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_unmute)
    if not member:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<{member_to_unmute}>> n'existe pas.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        return
    if ctx.guild:
        if member.voice:
            if author.guild_permissions.mute_members:
                await member.edit(mute=False)
                s_embed.clear_fields()
                s_embed.set_author(name=f"Un-muted {member.name}")
                await ctx.send(f"{ctx.author.mention}", embed=s_embed)
            else:
                e_embed.clear_fields()
                e_embed.add_field(name="Erreur", value="Tu n'as pas les droits.")
                await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        else:
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"{member_to_unmute} n'est pas connecte a un VC.")
            await ctx.send(f"{ctx.author.mention}", embed=e_embed)
    else:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Erreur de chat.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)


@bot.command(aliases=["d"])
async def deafen(ctx, member_to_deafen):
    """
    !deafen <membre> / !d <membre>
    Deafen un membre.
    """
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_deafen)
    if not member:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<{member_to_deafen}>> n'existe pas.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        return
    if ctx.guild:
        if member.voice:
            if author.guild_permissions.deafen_members:
                await member.edit(deafen=True)
                s_embed.clear_fields()
                s_embed.set_author(name=f"Deafen {member.name}")
                await ctx.send(f"{ctx.author.mention}", embed=s_embed)
            else:
                e_embed.clear_fields()
                e_embed.add_field(name="Erreur", value="Tu n'as pas les droits.")
                await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        else:
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"{member_to_deafen} n'est pas connecte a un VC.")
            await ctx.send(f"{ctx.author.mention}", embed=e_embed)
    else:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Erreur de chat.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)


@bot.command(aliases=["ud"])
async def undeafen(ctx, member_to_undeafen):
    """
    !undeafen <membre> / !ud <membre>
    Un-deafen un membre.
    """
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_undeafen)
    if not member:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<{member_to_undeafen}>> n'existe pas.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        return
    if ctx.guild:
        if member.voice:
            if author.guild_permissions.deafen_members:
                await member.edit(deafen=False)
                s_embed.clear_fields()
                s_embed.set_author(name=f"Un-deafen {member.name}")
                await ctx.send(f"{ctx.author.mention}", embed=s_embed)
            else:
                e_embed.clear_fields()
                e_embed.add_field(name="Erreur", value="Tu n'as pas les droits.")
                await ctx.send(f"{ctx.author.mention}", embed=e_embed)
        else:
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"{member_to_undeafen} n'est pas connecte a un VC.")
            await ctx.send(f"{ctx.author.mention}", embed=e_embed)
    else:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Erreur de chat.")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)


@bot.command(aliases=["a"])
async def all(ctx):
    """
    !all / !a
    Mute et deafen tous les membres de ton VC actuel.
    """
    author = ctx.author
    if ctx.guild:  # check if the msg was in a server's text channel
        print("", ctx.guild)
        if author.voice:  # check if the user is in a voice channel
            if author.guild_permissions.deafen_members and author.guild_permissions.mute_members: # check if the user has deafen and mute members permission
                for member in author.voice.channel.members:
                    if not member.bot and not author:
                        await member.edit(mute=True)
                        await member.edit(deafen=True)



@bot.command(aliases=["ua"])
async def unall(ctx):
    """
    !unall / !ua
    Un-mute et un-deafen tous les membres de ton VC actuel.
    """
    author = ctx.author
    if ctx.guild:
        if author.voice:
            if author.guild_permissions.deafen_members and author.guild_permissions.mute_members:
                for member in author.voice.channel.members:
                    if not member.bot:
                        await member.edit(mute=False)
                        await member.edit(deafen=False)


@bot.command(aliases=["r"])
async def reset(ctx):
    """
    !reset / !r
    Reset tes roles.
    """
    author = ctx.author
    vagabond = discord.utils.get(user.guild.roles, id=VAGABOND_ROLE)
    if author.roles is None:
        print("Error - " + str(user) + " - no Roles")
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Tu n'as pas de roles")
        await ctx.send(f"{author.mention}", embed=e_embed)
    else:
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                print("Error - " + str(author.name) + " - Can't delete @everyone")
        await author.add_roles(vagabond)
        s_embed.clear_fields()
        s_embed.set_author(name="Te revoila Vagabond")
        await ctx.send(f"{author.mention}", embed=s_embed)


@bot.command(aliases=["t"])
async def timeout(ctx, member_to_timeout, duration=0, *, unit=None):
    """
    !timeout <membre> <temps> <unite> / !t <membre> <temps> <unite>
    Timeout un membre pour un certain temps, en secondes ou minutes.
    """
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_timeout)
    if not member:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"Le membre <<  **{member_to_timeout}**  >> n'existe pas")
        await ctx.send(f"{author.mention}", embed=e_embed)
        return
    s_embed.clear_fields()
    s_embed.set_author(name=f"Timeout {member.name} pour {duration}{unit}")
    await ctx.send(f"{ctx.author.mention}", embed=s_embed)
    await member.edit(mute=True)
    await member.edit(deafen=True)
    if unit == "s":
        wait = 1 * duration
        await asyncio.sleep(wait)
    elif unit == "m":
        wait = 60 * duration
        await asyncio.sleep(wait)
    await member.edit(mute=False)
    await member.edit(deafen=False)
    s_embed.clear_fields()
    s_embed.set_author(name=f"Timeout de {member.name} fini")
    await ctx.send(f"{ctx.author.mention}", embed=s_embed)


@bot.command()
async def refresh(ctx):
    """
    !refresh
    Refresh le compteur d'humains.
    """
    s_embed.clear_fields()
    s_embed.set_author(name=f"Refresh Human count")
    await ctx.send(f"{ctx.author.mention}", embed=s_embed)
    guild = ctx.guild
    member_count = guild.member_count - 1
    channel = bot.get_channel(COUNT_CHAN)
    await channel.edit(name="{0} {1}".format("Humans:", member_count))
    s_embed.clear_fields()
    s_embed.set_author(name=f"Done | Humans: {member_count}")
    await ctx.send(f"{ctx.author.mention}", embed=s_embed)


@bot.command(aliases=["c"])
async def coffee(ctx):
    """
    !coffee / !c
    Le bot te fait un petit kawa.
    """
    o_embed.clear_fields()
    o_embed.set_image(url="https://c.tenor.com/QrDVGQ9cnsMAAAAC/coffee-creamer.gif")
    await ctx.send(f"{ctx.author.mention}", embed=o_embed)


# HELP
# ==========================================================================================

@bot.command(aliases=["commands", "h"])
async def help(ctx, args=None):
    command_names_list = [x.name for x in bot.commands]
    if not args:
        h_embed.clear_fields()
        h_embed.set_author(name="=============   Commandes Disponibles   =============")
        h_embed.add_field(name="------------------   ???   -------------------",
                          value="`!...`", inline=False)
        h_embed.add_field(name="`!hello`",
                          value="Recois le bonjour du bot", inline=False)
        h_embed.add_field(name="`!coffee`",
                          value="Petit cafe?", inline=False)

        h_embed.add_field(name="---------------------------------   Move   ---------------------------------",
                          value="`!...`", inline=False)
        h_embed.add_field(name="`!move <membre> <voice_channel>`",
                        value="Deplace un membre vers un Voice Channel", inline=False)
        h_embed.add_field(name="`!war` / `!w`",
                        value="Deplace tous les membres du role War vers le VC War", inline=False)
        h_embed.add_field(name="`!secret` / `!s`",
                        value="Deplace un membre vers ton VC secret", inline=False)
        h_embed.add_field(name="`!sexit` / `!se`",
                        value="Sors un membre de ton VC secret", inline=False)

        h_embed.add_field(name="------------------------------   Roles/Reset   ------------------------------",
                          value="`!...`", inline=False)
        h_embed.add_field(name="`!join <faction>` / `!j <faction>`",
                        value="Rejoins ta faction: A ou B", inline=False)
        h_embed.add_field(name="`!reset` / `!r`",
                        value="Restaure toi les roles par defaut", inline=False)

        h_embed.add_field(name="-------------------------------   Sons/Mics   -------------------------------",
                          value="`!...`", inline=False)
        h_embed.add_field(name="`!mute <membre>` / `!m <membre>`", value="Mute un membre specifique",
                        inline=False)
        h_embed.add_field(name="`!unmute <membre>` / `!u <membre>`", value="Un-mute un membre specifique",
                        inline=False)
        h_embed.add_field(name="`!deafen <membre>` / `!d <membre>`", value="Deafen un membre specifique",
                        inline=False)
        h_embed.add_field(name="`!undeafen <membre>` / `!ud <membre>`", value="Un-deafen un membre specifique",
                        inline=False)
        h_embed.add_field(name="`!undeafenme` / `!udme`", value="Un-deafen toi",
                        inline=False)
        h_embed.add_field(name="`!all` / `!a`", value="Mute et Deafen tous les membres de ton VC",
                        inline=False)
        h_embed.add_field(name="`!unall` / `!ua`", value="Un-mute et Un-deafen tous les membres de ton VC",
                        inline=False)
        h_embed.add_field(name="`!timeout <temps> <unite>` / `!t <temps> <unite>`", value="Timeout un membre "
                                                                                        "pour un certain temps",
                        inline=False)
    elif args in command_names_list:
        h_embed.clear_fields()
        h_embed.add_field(name=args, value=bot.get_command(args).help)
    else:
        h_embed.clear_fields()
        h_embed.add_field(name="Erreur", value="Cette commande n'existe pas")
    await ctx.send(embed=h_embed)


# RUN
# ==========================================================================================
bot.run(TOKEN)
