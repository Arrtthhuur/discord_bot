# mute.py

import discord
import asyncio

from discord.ext import commands
from utils.errors import *

s_embed = discord.Embed(color=discord.Color.green())  # Success
w_embed = discord.Embed(color=discord.Color.dark_red())  # War

AUCOIN_CHAN = 964999100074455131


class Mutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["m"], description="Mute un membre.")
    async def mute(self, ctx, member_to_mute=None):
        """
        !mute <membre> || !m <membre>
        """
        if not member_to_mute:
            return await show_help(ctx)
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


    @commands.command(aliases=["u"], description="Un-mute un membre.")
    async def unmute(self, ctx, member_to_unmute=None):
        """
        !unmute <membre> || !u <membre>
        """
        if not member_to_unmute:
            return await show_help(ctx)
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


    @commands.command(aliases=["d"], description="Deafen un membre.")
    async def deafen(self, ctx, member_to_deafen=None):
        """
        !deafen <membre> || !d <membre>
        """
        if not member_to_deafen:
            return await show_help(ctx)
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


    @commands.command(aliases=["ud"], description="Un-deafen un membre.")
    async def undeafen(self, ctx, member_to_undeafen=None):
        """
        !undeafen <membre> || !ud <membre>
        """
        if not member_to_undeafen:
            return await show_help(ctx)
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


    @commands.command(aliases=["a"], description="Mute et deafen tous les membres de ton VC actuel.")
    async def all(self, ctx):
        """
        !all || !a
        """
        author = ctx.author
        if author.voice:  # check if the user is in a voice channel
            if author.guild_permissions.deafen_members and author.guild_permissions.mute_members:  # check if the user has deafen and mute members permission
                for member in author.voice.channel.members:
                    if not member.bot and member != author:
                        await member.edit(mute=True)
                        await member.edit(deafen=True)
                        s_embed.clear_fields()
                        s_embed.set_author(name=f"All ton VC")
                        await ctx.send(f"{ctx.author.mention}", embed=s_embed)
            else:
                await not_muter_error(ctx)
        else:
            await not_in_channel_error(ctx)


    @commands.command(aliases=["ua"], description="Un-mute et un-deafen tous les membres de ton VC actuel.")
    async def unall(self, ctx):
        """
        !unall || !ua
        """
        author = ctx.author
        if author.voice:
            if author.guild_permissions.deafen_members and author.guild_permissions.mute_members:
                for member in author.voice.channel.members:
                    if not member.bot:
                        await member.edit(mute=False)
                        await member.edit(deafen=False)
                        s_embed.clear_fields()
                        s_embed.set_author(name=f"Un-all ton VC")
                        await ctx.send(f"{ctx.author.mention}", embed=s_embed)
            else:
                await not_muter_error(ctx)
        else:
            await not_in_channel_error(ctx)


    @commands.command(aliases=["t"], description="Timeout un membre pour un certain temps, en sec ou min.")
    async def timeout(self, ctx, member_to_timeout=None, duration=0, *, unit=None):
        """
        !timeout <membre> <temps> <unite> || !t <m> <t> <u>
        """
        if not member_to_timeout:
            return await show_help(ctx)
        member = discord.utils.get(ctx.guild.members, name=member_to_timeout)
        if not member:
            return await member_not_found_error(ctx, member_to_timeout)
        if member.voice:
            if ctx.author.guild_permissions.move_members:
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
            else:
                await not_mover_error(ctx)
        else:
            await not_voice_connected_error(ctx, member_to_timeout)


    @commands.command(aliases=["ac"], description="Envoie un membre au coin, qu'il ferme un peu sa gueule.")
    async def aucoin(self, ctx, member_to_move=None):
        """
        !aucoin <membre> || !ac <membre>
        """
        if not member_to_move:
            return await show_help(ctx)
        member = discord.utils.get(ctx.guild.members, name=member_to_move)
        channel = self.bot.get_channel(AUCOIN_CHAN)
        if not member:
            return await member_not_found_error(ctx, member_to_move)
        if member.voice:
            if ctx.author.guild_permissions.move_members:
                await member.move_to(channel)
                await member.edit(mute=True)
                await member.edit(deafen=True)
                s_embed.clear_fields()
                s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
                await ctx.send(f"{ctx.author.mention}", embed=s_embed)
                o_embed.clear_fields()
                o_embed.set_author(name="Au coin!", value="Tais toi un peu")
                await member.send(embed=o_embed)
            else:
                await not_mover_error(ctx)
        else:
            await not_voice_connected_error(ctx, member_to_move)


    @commands.command(aliases=["cb"], description="C'est bon, l'autre con du coin peut revenir.")
    async def cbon(self, ctx, member_to_move=None, channel_dest=None):
        """
        !cbon <membre> <channel_dest> || !cb <membre> <channel_dest>
        """
        if not member_to_move:
            return await show_help(ctx)
        member = discord.utils.get(ctx.guild.members, name=member_to_move)
        channel = discord.utils.get(ctx.guild.voice_channels, name=channel_dest)
        if not member:
            return await member_not_found_error(ctx, member_to_move)
        if not channel:
            return await channel_not_found_error(ctx, channel_dest)
        if member.voice:
            if ctx.author.guild_permissions.move_members:
                await member.move_to(channel)
                await member.edit(mute=False)
                await member.edit(deafen=False)
                s_embed.clear_fields()
                s_embed.set_author(name=f"Moved {member.name} to {channel.name}")
                await ctx.send(f"{ctx.author.mention}", embed=s_embed)
            else:
                await not_mover_error(ctx)
        else:
            await not_voice_connected_error(ctx, member_to_move)


async def setup(bot):
    await bot.add_cog(Mutes(bot))