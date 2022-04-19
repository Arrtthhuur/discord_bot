# move.py

import discord

from discord.ext import commands

e_embed = discord.Embed(color=discord.Color.red())  # Error


class CmdError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
            try:
                if isinstance(error, commands.CommandNotFound):
                    e_embed.clear_fields()
                    e_embed.add_field(name="Erreur", value=f"Cette commande n'existe pas")
                    return await ctx.send(f"{ctx.author.mention}", embed=e_embed)
            except Exception as error:
                pass


async def setup(bot):
    await bot.add_cog(CmdError(bot))