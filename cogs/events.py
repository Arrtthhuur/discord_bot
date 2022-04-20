# events.py

import discord
import discord.ui

from discord.ext import commands

e_embed = discord.Embed(color=discord.Color.red())  # Error
s_embed = discord.Embed(color=discord.Color.green())  # Success
o_embed = discord.Embed(color=discord.Color.orange())  # misc

BOT_ID = 962702131498979400
BOT_CHAN = 964285664130641960
LOG_ID = 962759786783453204
ARRIVEE_CHAN = 964288388238831737
DEPART_CHAN = 964288408262443048
LINKER_ROLE = 963870403628007475
MSG_LOG_CHAN = 964582976782479462
ATTENTE_FACTION_CHAN = 965290263494926417
COUNT_CHAN = 964509869724041256

# Badwords
badwords = ["fispute", 'tamere', 'sam', 'samuel']


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        print('------')


    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Bot welcomes newcomers and sends them faction join embed.
        """
        print("member joined")
        await faction_join(member)
        await count_members(member)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Bot farewells"""
        print("member remove")
        await self.bot.get_channel(DEPART_CHAN).send(f"Ciao {member}!")
        await count_members(member)


    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Bot reacts to message.
        Delete links.
        Censures profanity.
        Only reacts to commands when entered in the bot channel.
        """
        if message.author.id == BOT_ID:
            return
        await check_badwords(message)
        if await check_links(message) is True:
            return
        if await check_channel(message) is True:
            return
        await log(message)
        # return await bot.process_commands(message)  # not needed inside a cog


async def faction_join(member):
    """
    On member join, bot sends embed to join on of the three factions.
    New member has to chose and will wait for an admin to confirm choice.
    Then adds the corresponding role to new member.
    """
    arrivee_chan = discord.utils.get(member.guild.channels, id=ARRIVEE_CHAN)
    faction_view = Faction()
    embed = discord.Embed(title=f"Rejoins ta faction", color=discord.Color.blurple())
    to_delete0 = await arrivee_chan.send(f"{member.mention}", embed=embed, view=faction_view)
    await faction_view.wait()
    if not faction_view.value:
        print('Timed out...')
        e_embed.clear_fields()
        e_embed.set_author(name=f"Tu n'as pas repondu a temps (180s)")
        await arrivee_chan.send(f"{member.mention}", embed=e_embed)
    attente_chan = discord.utils.get(member.guild.channels, id=ATTENTE_FACTION_CHAN)
    faction_name = faction_view.value
    confirm_view = Confirm()
    embed = discord.Embed(title="Choix de faction",
                          description=f"{member.name} souhaite rejoindre la faction {faction_name}",
                          color=discord.Color.blurple())
    to_delete = await attente_chan.send(embed=embed, view=confirm_view)
    await confirm_view.wait()
    if confirm_view.value is None:
        e_embed.clear_fields()
        e_embed.set_author(name=f"Pas d'admin pour verifier ta demande, reessaye plus tard")
        await member.send(embed=e_embed)
    elif confirm_view.value:
        to_apply = discord.utils.find(lambda r: r.name == faction_name, member.guild.roles)
        await member.add_roles(to_apply)
        s_embed.clear_fields()
        s_embed.set_author(name=f"{member.name} a rejoint la faction {faction_name}")
        await attente_chan.send(embed=s_embed)
        s_embed.clear_fields()
        s_embed.set_author(name=f"Ta demande pour rejoindre la faction {faction_name} a ete acceptee")
        await member.send(embed=s_embed)
    else:
        print('Cancelled...')
        e_embed.clear_fields()
        e_embed.set_author(name=f"Ta demande pour rejoindre la faction {faction_name} a ete refusee")
        await member.send(embed=e_embed)
    await to_delete.delete()
    await to_delete0.delete()


async def count_members(member):
    """
    Count the members, without the bot.
    """
    member_count = member.guild.member_count - 1
    count_chan = discord.utils.get(member.guild.voice_channels, id=COUNT_CHAN)
    await count_chan.edit(name="{0} {1}".format("Humans:", member_count))


async def check_badwords(message):
    """
    Checking if message contains forbidden words.
    """
    for i in badwords:
        if i in message.content:
            await message.delete()
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"Tsss, ta mere serait fiere de toi...")
            await message.channel.send(f"{message.author.mention}", embed=e_embed)
            await manage_profanity(message, i)
            break


async def manage_profanity(message, word):
        """
        Bot displays the profanity in the log channel.
        """
        channel = discord.utils.get(message.guild.channels, id=LOG_ID)
        embed = discord.Embed(title="Alerte aux gromo!", description=f"{message.author.name} a dit ||{word}||",
                              color=discord.Color.blurple())
        await channel.send(embed=embed)


async def check_links(message):
    """
    Checking if message contains links.
    """
    if 'https://' in message.content or 'http://' in message.content:
        role = discord.utils.get(message.guild.roles, id=LINKER_ROLE)
        if role not in message.author.roles:
            await message.delete()
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"Tiens, ton lien du Q.")
            await message.channel.send(f"{message.author.mention}", embed=e_embed)
            return True


async def check_channel(message):
    """
    Checking if command is sent in bot channel.
    """
    if message.content.startswith('!'):
        if message.channel.id != BOT_CHAN:
            await message.delete()
            e_embed.clear_fields()
            e_embed.add_field(name="Erreur", value=f"Entre les commandes dans le channel bot.")
            await message.channel.send(f"{message.author.mention}", embed=e_embed)
            return True


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


async def setup(bot):
    await bot.add_cog(Events(bot))


class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Faction A', description='blabla A', emoji='🟥'),
            discord.SelectOption(label='Faction B', description='blabla B', emoji='🟩'),
            discord.SelectOption(label='Faction C', description='blabla C', emoji='🟦'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choisis ta faction', min_values=1, max_values=1, options=options)
        self.stop()

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Tu es en attente pour rejoindre {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Dropdown())


class Confirm(discord.ui.View):
    """
    Simple View class that gives us a confirmation menu (confirm - cancel).
    """
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


class Faction(discord.ui.View):
    """
    Simple view class that gives the member a choice of factions to join.
    """
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Faction A', style=discord.ButtonStyle.red)
    async def join_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('En attente pour A', ephemeral=True)
        self.value = 'A'
        self.stop()

    @discord.ui.button(label='Faction B', style=discord.ButtonStyle.blurple)
    async def join_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('En attente pour B', ephemeral=True)
        self.value = 'B'
        self.stop()

    @discord.ui.button(label='Faction C', style=discord.ButtonStyle.green)
    async def join_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('En attente pour C', ephemeral=True)
        self.value = 'C'
        self.stop()
