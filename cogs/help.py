# help.py

import discord

from discord.ext import commands
from utils.errors import *

BOT_CHAN = 964285664130641960

h_embed = discord.Embed(color=discord.Color.blurple())  # Help

VISIBLE_COGS = [ "Misc", "Moves", "Mutes", "Roles" ]

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['h'])
    async def help(self, ctx, args=None):
        # display full command list
        if not args:
            cogs_desc = ''
            cmds_desc = ''
            embed = discord.Embed(title="All Commands")
            # h_embed.clear_fields()
            # h_embed.set_author(name="Commandes Disponibles")
            for cog in self.bot.cogs:
                cogs_desc = ''
                if cog in VISIBLE_COGS:
                    # cogs_desc = ''
                    cog = self.bot.get_cog(cog)
                    cmds = cog.get_commands()
                    cogs_desc = f'\n**{cog.qualified_name}**\t\t\t\t\t ***{len(cmds)} commandes***\n'
                    cmds_desc = ''
                    for cmd in cmds:
                        cmds_desc += f'{cmd.help}\n\t{cmd.description}\n\n'
                    embed.description = f"```yaml\n---\n{cogs_desc}\n{cmds_desc}\n---\n```"
                    print("", cogs_desc)
                    print("", cmds_desc)
            # print("", cmds_desc)
                    # h_embed.add_field(name=cogs_desc, value=cmds_desc, inline=False)
                    # embed.set_footer(
                    #     text=f"Run {self.clean_prefix}{self.invoked_with} [cog] to learn more about a cog and its commands")
            # print("", cogs_desc)

            # h_embed.clear_fields()
            # h_embed.set_author(name="Commandes Disponibles")
            # h_embed.add_field(name=cogs_desc, value=cmds_desc, inline=False)
            # h_embed.add_field(name="Commandes", value=cmds_desc, inline=False)
            # await ctx.send(f"{ctx.author.mention}", embed=h_embed)
            await ctx.send(f"{ctx.author.mention}", embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
