# misc.py

import discord

from discord.ext import commands

o_embed = discord.Embed(color=discord.Color.orange())  # misc
s_embed = discord.Embed(color=discord.Color.green())  # Success

COUNT_CHAN = 964509869724041256


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """
        !hello
        Le bot te dit bonjour.
        """
        await ctx.send(f"Yeyow {ctx.author.mention}! Comment i' va?")


    @commands.command(aliases=["c"])
    async def coffee(self, ctx):
        """
        !coffee / !c
        Le bot te fait un petit kawa.
        """
        o_embed.clear_fields()
        o_embed.set_image(url="https://c.tenor.com/QrDVGQ9cnsMAAAAC/coffee-creamer.gif")
        await ctx.send(f"{ctx.author.mention}", embed=o_embed)


    @commands.command()
    async def refresh(self, ctx):
        """
        !refresh
        Refresh le compteur d'humains.
        """
        print("refresh")
        s_embed.clear_fields()
        s_embed.set_author(name=f"Refresh Human count")
        await ctx.send(f"{ctx.author.mention}", embed=s_embed)
        guild = ctx.guild
        member_count = guild.member_count - 1  # - number of bots on the server
        channel = discord.utils.get(ctx.guild.voice_channels, id=COUNT_CHAN)
        await channel.edit(name="{0} {1}".format("Humans:", member_count))
        s_embed.clear_fields()
        s_embed.set_author(name=f"Done | Humans: {member_count}")
        await ctx.send(f"{ctx.author.mention}", embed=s_embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))