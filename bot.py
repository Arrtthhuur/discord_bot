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
ACCEUIL_SECRET_CHAN = 964996079726776400

AUCOIN_CHAN = 964999100074455131

LINKER_ROLE = 963870403628007475
VAGABOND_ROLE = 963168526733021254
A_ROLE = 963159344680149022
B_ROLE = 963159369728557096
C_ROLE = 964943407824896030


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
    print("Bot ready for action")


@bot.event
async def on_message(message):
    """Bot reacts to message.
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
        # role = discord.utils.get(message.author.roles, id=LINKER_ROLE)
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
    channel = bot.get_channel(MSG_LOG_CHAN)
    m_hour = message.created_at.strftime('%H:%M')
    m_date = message.created_at.strftime('%d/%m/%Y')
    if message.author.id != BOT_ID:
        await channel.send(f"\" ***{message.content}*** \" envoye par **{message.author.name}**, sur le channel "
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
    role = discord.utils.get(member.guild.roles, id=VAGABOND_ROLE)
    await member.add_roles(role)
    await gen_chan.send(f"Bienvenue {member.mention}, tu fais maintenant "
                                                  f"partie des vagabonds, rejoins la faction A, B ou C!")


async def count_members(member):
    """Count the members, without the bot"""
    guild_id = member.guild.id
    guild = bot.get_guild(guild_id)
    member_count = guild.member_count - 1
    count_chan = bot.get_channel(COUNT_CHAN)
    await count_chan.edit(name="{0} {1}".format("Humans:", member_count))


@bot.event
async def on_member_remove(member):
    """Bot farewells"""
    await count_members(member)
    await bot.get_channel(DEPART_CHAN).send(f"Ciao {member}!")


# BOT COMMANDS
# ==========================================================================================

@bot.command()
async def hello(ctx):
    """
    !hello
    Le bot te dit bonjour.
    """
    await ctx.send(f"Yeyow {ctx.author.mention}! Comment i' va?")


@bot.command(aliases=["c"])
async def coffee(ctx):
    """
    !coffee / !c
    Le bot te fait un petit kawa.
    """
    o_embed.clear_fields()
    o_embed.set_image(url="https://c.tenor.com/QrDVGQ9cnsMAAAAC/coffee-creamer.gif")
    await ctx.send(f"{ctx.author.mention}", embed=o_embed)


@bot.command(aliases=["j"])
async def join(ctx, faction=None):
    """
    !join <faction> / !j <faction>
    Rejoins une faction.
    """
    if not faction:
        return await show_help(ctx, 'join')
    author = ctx.author
    guild_roles = discord.utils.get(ctx.guild.roles, name=faction)
    auth_roles = discord.utils.get(ctx.author.roles, name=faction)
    vaga_role = discord.utils.get(ctx.author.roles, id=VAGABOND_ROLE)
    to_apply = discord.utils.find(lambda r: r.name == faction, ctx.guild.roles)
    vagabond = discord.utils.get(author.guild.roles, id=VAGABOND_ROLE)
    if not guild_roles:  # check if given faction exists
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value=f"La faction **{faction}** n'existe pas")
        await ctx.send(f"{author.mention}", embed=e_embed)
    elif auth_roles:  # check if author not already in faction
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Tu es deja dans cette faction")
        await ctx.send(f"{author.mention}", embed=e_embed)
    elif not vaga_role:  # check if author still has Vagabond role => no factions yet
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
async def move(ctx, member_to_move=None, channel_dest=None):
    """
    !move <membre> <channel>
    Deplace un membre vers un channel vocal.
    """
    if not member_to_move or not channel_dest:
        return await show_help(ctx, 'move')
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel_dest)
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    author = ctx.author
    if member:
        if channel:
            if member.voice:
                if member.voice.channel != channel:
                    if author.guild_permissions.move_members:
                        await member.move_to(channel)
                        s_embed.clear_fields()
                        s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
                        await ctx.send(f"{author.mention}", embed=s_embed)
                    else:
                        await mover_error(ctx)
                else:
                    await already_in_channel_error(ctx, member_to_move, channel_dest)
            else:
                await not_voice_connected_error(ctx, member_to_move)
        else:
            await channel_not_found_error(ctx, channel_dest)
    elif not channel and not member:
        await cm_not_found_error(ctx, channel_dest, member_to_move)
    else:
        await member_not_found_error(ctx, member_to_move)


@bot.command(aliases=["w"])
async def war(ctx):
    """
    !war / !w
    Deplace tous les membres War dans le channel War.
    """
    channel = bot.get_channel(WAR_CHAN)
    war_role = discord.utils.get(ctx.guild.roles, id=WAR_ROLE)
    author = ctx.author
    if not author.guild_permissions.move_members:
        return await not_mover_error(ctx)
    for member in ctx.guild.members:
        if not member.bot:
            if war_role not in member.roles:
                print("Error - " + str(member) + " - missing War role")
            elif member.voice is None:
                print("Error - " + str(member) + " - not Voice connected")
            else:
                try:
                    await member.move_to(channel)
                    print("Moving - " + str(member))
                    w_embed.clear_fields()
                    w_embed.add_field(name="WAR", value=f"Gulyzm appelle a la guerre!")
                    await member.send(embed=w_embed)
                except:
                    print("Error - bigmove")


@bot.command(aliases=["s"])
async def secret(ctx, member_to_move=None):
    """
    !secret <membre> / !s <membre>
    Deplace un membre vers ton VC secret.
    """
    if not member_to_move:
        return await show_help(ctx, 'secret')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    secret_role = discord.utils.get(ctx.author.roles, id=SECRET_ROLE)
    channel = bot.get_channel(SECRET_CHAN)
    if not member:
        return await member_not_found_error(ctx, member_to_move)
    if member.voice:
        if author.guild_permissions.move_members and secret_role:
            await member.move_to(channel)
            await member.add_roles(secret_role)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
            await ctx.send(f"{author.mention}", embed=s_embed)
        else:
            await not_mover_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_move)


@bot.command(aliases=["se"])
async def sexit(ctx, member_to_move=None):
    """
    !sexit <membre> / !se <membre>
    Sors un membre de ton VC secret.
    """
    if not member_to_move:
        return await show_help(ctx, 'sexit')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    secret_role = discord.utils.get(ctx.author.roles, id=SECRET_ROLE)
    channel = bot.get_channel(ACCEUIL_SECRET_CHAN)
    if not member:
        return await member_not_found_error(ctx, member_to_move)
    if member.voice:
        if author.guild_permissions.move_members and secret_role:
            await member.move_to(channel)
            await member.remove_roles(secret_role)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Removed {member.name} to {channel.name}")
            await ctx.send(f"{author.mention}", embed=s_embed)
        else:
            await not_mover_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_move)


@bot.command(aliases=["m"])
async def mute(ctx, member_to_mute=None):
    """
    !mute <membre> / !m <membre>
    Mute un membre.
    """
    if not member_to_mute:
        return await show_help(ctx, 'mute')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_mute)
    if not member:
        return await member_not_found_error(ctx, member_to_mute)
    if member.voice:
        if author.guild_permissions.mute_members:
            await member.edit(mute=True)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Muted {member.name}")
            await ctx.send(f"{ctx.author.mention}", embed=s_embed)
        else:
            await not_muter_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_mute)


@bot.command(aliases=["u"])
async def unmute(ctx, member_to_unmute=None):
    """
    !unmute <membre> / !u <membre>
    Un-mute un membre.
    """
    if not member_to_unmute:
        return await show_help(ctx, 'unmute')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_unmute)
    if not member:
        return await member_not_found_error(ctx, member_to_unmute)
    if member.voice:
        if author.guild_permissions.mute_members:
            await member.edit(mute=False)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Un-muted {member.name}")
            await ctx.send(f"{ctx.author.mention}", embed=s_embed)
        else:
            await not_muter_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_unmute)


@bot.command(aliases=["d"])
async def deafen(ctx, member_to_deafen=None):
    """
    !deafen <membre> / !d <membre>
    Deafen un membre.
    """
    if not member_to_deafen:
        return await show_help(ctx, 'deafen')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_deafen)
    if not member:
        return await member_not_found_error(ctx, member_to_deafen)
    if member.voice:
        if author.guild_permissions.deafen_members:
            await member.edit(deafen=True)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Deafen {member.name}")
            await ctx.send(f"{ctx.author.mention}", embed=s_embed)
        else:
            await not_muter_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_deafen)


@bot.command(aliases=["ud"])
async def undeafen(ctx, member_to_undeafen=None):
    """
    !undeafen <membre> / !ud <membre>
    Un-deafen un membre.
    """
    if not member_to_undeafen:
        return await show_help(ctx, 'undeafen')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_undeafen)
    if not member:
        return await member_not_found_error(ctx, member_to_undeafen)
    if member.voice:
        if author.guild_permissions.deafen_members:
            await member.edit(deafen=False)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Un-deafen {member.name}")
            await ctx.send(f"{ctx.author.mention}", embed=s_embed)
        else:
            await not_muter_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_undeafen)


@bot.command(aliases=["a"])
async def all(ctx):
    """
    !all / !a
    Mute et deafen tous les membres de ton VC actuel.
    """
    author = ctx.author
    if author.voice:  # check if the user is in a voice channel
        if author.guild_permissions.deafen_members and author.guild_permissions.mute_members: # check if the user has deafen and mute members permission
            for member in author.voice.channel.members:
                if not member.bot and member != author:
                    await member.edit(mute=True)
                    await member.edit(deafen=True)
        else:
            await not_muter_error(ctx)
    else:
        await not_in_channel_error(ctx)



@bot.command(aliases=["ua"])
async def unall(ctx):
    """
    !unall / !ua
    Un-mute et un-deafen tous les membres de ton VC actuel.
    """
    author = ctx.author
    if author.voice:
        if author.guild_permissions.deafen_members and author.guild_permissions.mute_members:
            for member in author.voice.channel.members:
                if not member.bot:
                    await member.edit(mute=False)
                    await member.edit(deafen=False)
        else:
            await not_muter_error(ctx)
    else:
        await not_in_channel_error(ctx)


@bot.command(aliases=["r"])
async def reset(ctx):
    """
    !reset / !r
    Reset tes roles.
    """
    vagabond = discord.utils.get(user.guild.roles, id=VAGABOND_ROLE)
    if ctx.author.roles is None:
        print("Error - " + str(user) + " - no Roles")
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Tu n'as pas de roles")
        await ctx.send(f"{ctx.author.mention}", embed=e_embed)
    else:
        for role in ctx.author.roles:
            try:
                await ctx.author.remove_roles(role)
            except:
                print("Error - " + str(ctx.author.name) + " - Can't delete @everyone")
        await author.add_roles(vagabond)
        s_embed.clear_fields()
        s_embed.set_author(name="Te revoila Vagabond")
        await ctx.send(f"{ctx.author.mention}", embed=s_embed)


@bot.command(aliases=["t"])
async def timeout(ctx, member_to_timeout=None, duration=0, *, unit=None):
    """
    !timeout <membre> <temps> <unite> / !t <membre> <temps> <unite>
    Timeout un membre pour un certain temps, en secondes ou minutes.
    """
    if not member_to_timeout:
        return await show_help(ctx, 'timeout')
    member = discord.utils.get(ctx.guild.members, name=member_to_timeout)
    if not member:
        return await member_not_found_error(ctx, member_to_timeout)
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


@bot.command(aliases=["ac"])
async def aucoin(ctx, member_to_move=None):
    """
    !aucoin <membre>
    Envoie un membre au coin, qu'il ferme un peu sa gueule.
    """
    if not member_to_move:
        return await show_help(ctx, 'aucoin')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    channel = bot.get_channel(AUCOIN_CHAN)
    if not member:
        return await member_not_found_error(ctx, member_to_move)
    if member.voice:
        if author.guild_permissions.move_members:
            await member.move_to(channel)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
            await ctx.send(f"{author.mention}", embed=s_embed)
            o_embed.clear_fields()
            o_embed.add_field(name="Au coin!", value="Tais toi un peu")
            await member.send(embed=o_embed)
        else:
            await not_mover_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_move)


@bot.command(aliases=["cb"])
async def cbon(ctx, member_to_move=None, channel_dest=None):
    """
    !cbon <membre>
    C'est bon, l'autre con du coin peut revenir.
    """
    if not member_to_move:
        return await show_help(ctx, 'cbon')
    author = ctx.author
    member = discord.utils.get(ctx.guild.members, name=member_to_move)
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel_dest)
    if not member:
        return await member_not_found_error(ctx, member_to_move)
    if not channel:
        return await channel_not_found_error(ctx, channel_dest)
    if member.voice:
        if author.guild_permissions.move_members:
            await member.move_to(channel)
            s_embed.clear_fields()
            s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
            await ctx.send(f"{author.mention}", embed=s_embed)
        else:
            await not_mover_error(ctx)
    else:
        await not_voice_connected_error(ctx, member_to_move)


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
    member_count = guild.member_count - 1 # - number of bots on the server
    channel = bot.get_channel(COUNT_CHAN)
    await channel.edit(name="{0} {1}".format("Humans:", member_count))
    s_embed.clear_fields()
    s_embed.set_author(name=f"Done | Humans: {member_count}")
    await ctx.send(f"{ctx.author.mention}", embed=s_embed)


async def not_mover_error(ctx):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value="Tu n'es pas mover")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def not_muter_error(ctx):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value="Tu n'es pas muter")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def member_not_found_error(ctx, member):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value=f"Le membre **{member}** n'existe pas")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def channel_not_found_error(ctx, channel):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value=f"Le channel **{channel}** n'existe pas")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def cm_not_found_error(ctx, channel, member):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value=f"**{member}** et **{channel}** n'existent pas")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def not_voice_connected_error(ctx, member):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value=f"**{member}** n'est pas connecte a un VC")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def already_in_channel_error(ctx, member, channel):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value=f"**{member}** est deja dans **{channel}**")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def not_in_channel_error(ctx):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value=f"Tu dois etre connecte a un channel")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)


async def show_help(ctx, command):
    e_embed.clear_fields()
    e_embed.add_field(name="Erreur", value=f"Mauvais usage de la commande")
    await ctx.send(f"{ctx.author.mention}", embed=e_embed)
    await help(ctx, command)


# HELP
# ==========================================================================================

@bot.command(aliases=["commands", "h"])
async def help(ctx, args=None):
    command_names_list = [x.name for x in bot.commands]
    if not args:
        h_embed.clear_fields()
        h_embed.set_author(name="=============   Commandes Disponibles   =============")
        h_embed.add_field(name="---------------------------------   Misc   ---------------------------------",
                          value="`!...`", inline=False)
        h_embed.add_field(name="`!help <commande>`", value="Plus d'info sur une commande", inline=False)
        h_embed.add_field(name="`!hello`", value="Couscous", inline=True)
        h_embed.add_field(name="`!coffee`", value="Petit cafe?", inline=True)
        h_embed.add_field(name="`!refresh`", value="Refresh le compteur d'humains", inline=False)

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
        h_embed.add_field(name="`!aucoin` <membre> / `!ac <membre>`",
                        value="Envoie un membre au coin", inline=False)
        h_embed.add_field(name="`!cbon` <membre> / `!cb <membre>`",
                        value="L'autre con du coin peut revenir", inline=False)

        h_embed.add_field(name="------------------------------   Roles/Reset   ------------------------------",
                          value="`!...`", inline=False)
        h_embed.add_field(name="`!join <faction>` / `!j <faction>`",
                        value="Rejoins ta faction: A, B ou C", inline=False)
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
        h_embed.add_field(name="`!all` / `!a`", value="Mute et Deafen tous les membres de ton VC",
                        inline=False)
        h_embed.add_field(name="`!unall` / `!ua`", value="Un-mute et Un-deafen tous les membres de ton VC",
                        inline=False)
        h_embed.add_field(name="`!timeout <membre> <temps> <unite>` / `!t <m> <t> <u>`", value="Timeout un membre "
                                                                                        "pour un certain temps",
                        inline=False)
        return await ctx.send(embed=h_embed)
    elif args in command_names_list:
        h_embed.clear_fields()
        h_embed.add_field(name=args, value=bot.get_command(args).help)
        return await ctx.send(embed=h_embed)
    else:
        e_embed.clear_fields()
        e_embed.add_field(name="Erreur", value="Cette commande n'existe pas")
        return await ctx.send(embed=e_embed)


# RUN
# ==========================================================================================
bot.run(TOKEN)
