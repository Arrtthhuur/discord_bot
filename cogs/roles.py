# roles.py

import discord

from discord.ext import commands
from utils.errors import *

e_embed = discord.Embed(color=discord.Color.red())  # Error
s_embed = discord.Embed(color=discord.Color.green())  # Success

VAGABOND_ROLE = 963168526733021254
A_ROLE = 963159344680149022
B_ROLE = 963159369728557096
C_ROLE = 964943407824896030


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["j"], description="Rejoins une faction.")
    async def join(self, ctx, faction=None):
        """
        !join <faction> || !j <faction>
        """
        if not faction:
            return await show_help(ctx)
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


    @commands.command(aliases=["r"], description="Reset tes roles.")
    async def reset(self, ctx):
        """
        !reset || !r
        """
        vagabond = discord.utils.get(ctx.guild.roles, id=VAGABOND_ROLE)
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
            await ctx.author.add_roles(vagabond)
            s_embed.clear_fields()
            s_embed.set_author(name="Te revoila Vagabond")
            await ctx.send(f"{ctx.author.mention}", embed=s_embed)


async def setup(bot):
    await bot.add_cog(Roles(bot))