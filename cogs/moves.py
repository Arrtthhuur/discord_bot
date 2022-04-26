# move.py

import discord

from discord.ext import commands
from utils.errors import *

s_embed = discord.Embed(color=discord.Color.green())  # Success
w_embed = discord.Embed(color=discord.Color.dark_red())  # War

WAR_CHAN = 963881045722292224
WAR_ROLE = 963881736016658463
SECRET_CHAN = 964279615541624932
SECRET_ROLE = 964279750975696946
ACCUEIL_SECRET_CHAN = 964996079726776400


class Moves(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Deplace un membre vers un channel vocal.")
    async def move(self, ctx, member_to_move=None, channel_dest=None):
        """
        !move <membre> <channel>
        """
        if not member_to_move or not channel_dest:
            return await show_help(ctx)
        author = ctx.author
        channel = discord.utils.get(ctx.guild.voice_channels, name=channel_dest)
        member = discord.utils.get(ctx.guild.members, name=member_to_move)
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


    @commands.command(aliases=["w"], description="Deplace tous les membres War dans le channel War.")
    async def war(self, ctx):
        """
        !war || !w
        """
        author = ctx.author
        channel = discord.utils.get(ctx.guild.voice_channels, id=WAR_CHAN)
        war_role = discord.utils.get(ctx.guild.roles, id=WAR_ROLE)
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


    @commands.command(aliases=["s"], description="Deplace un membre vers ton VC secret.")
    async def secret(self, ctx, member_to_move=None):
        """
        !secret <membre> || !s <membre>
        """
        if not member_to_move:
            return await show_help(ctx)
        author = ctx.author
        member = discord.utils.get(ctx.guild.members, name=member_to_move)
        print("", member)
        secret_role = discord.utils.get(ctx.author.roles, id=SECRET_ROLE)
        channel = discord.utils.get(ctx.guild.voice_channels, id=SECRET_CHAN)
        if member is None:
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


    @commands.command(aliases=["se"], description="Sors un membre de ton VC secret.")
    async def sexit(self, ctx, member_to_move=None):
        """
        !sexit <membre> || !se <membre>
        """
        if not member_to_move:
            return await show_help(ctx)
        author = ctx.author
        member = discord.utils.get(ctx.guild.members, name=member_to_move)
        secret_role = discord.utils.get(ctx.author.roles, id=SECRET_ROLE)
        channel = discord.utils.get(ctx.guild.voice_channels, id=ACCUEIL_SECRET_CHAN)
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


async def setup(bot):
    await bot.add_cog(Moves(bot))