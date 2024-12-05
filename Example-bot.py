import nextcord
from nextcord import File
from nextcord.ext import tasks, commands
import os
import asyncio
import random
import re
import os.path
from datetime import datetime, timedelta, timezone
import json
from nextcord.ext.commands.help import _HelpCommandImpl
from nextcord.ext import application_checks
import math
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from itertools import cycle
import humanfriendly
from gtts import gTTS 

intents = nextcord.Intents().all()
intents.members = True

bot = commands.Bot(command_prefix = '!', intents=nextcord.Intents.all() , max_messages = 80000)
data = {
    "TOKEN" : "Insert token here",
    "MODERATION_LOG" : 0,
    "TICKET_LOG" : 0,
    "GUILD-ID" : 0
    }

"""
 ____    |\/|       
 \  /\   / ..__.    Discord bot developed by: Bobb3ll1 (AKA: Oiva Huuhtanen.)
  \/  \__\   _/     As of writing i'm a 20yo Furry with a passion for programming. I'm located in Finland :3
   \__   __  \_     This code is not the greatest, but it functions as expected.
      \____\___\    For some of the code i've utilized code from ChatGPT and public sources. Do with this base as you wish.

"""
# I do not take any guarantee that this code works 100% cause some parts have been deleted from it. The code has been ripped from Jackxolotl's Server (Jack's Proot)
# https://discord.gg/PTaWtETmN6

class VotingModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Voting.",
            timeout=None,
        )

        self.topic = nextcord.ui.TextInput(label="Voting Topic.", style=nextcord.TextInputStyle.paragraph, required=True, max_length=2000)
        self.add_item(self.topic)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        ran_char_list = ['a', 'b', 'c', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] # Ahh yes the alphabet :3
        unique_id = f"{interaction.user.id}-{random.choice(ran_char_list)}{random.choice(ran_char_list)}{random.choice(ran_char_list)}{random.choice(ran_char_list)}"
        await asyncio.sleep(2)
        filename = f'voting/{unique_id}.json'
        with open(filename, "w") as file:
            pass

        desc = f"""
        Voting Details:
        ```{self.topic.value}```

        """
        embed = nextcord.Embed(title='`🗳️` New Vote.', description=desc)
        embed.set_footer(text='With ❤️ by: Bobb3ll1')

        with Image.open("äänestys.png") as im:
            fnt = ImageFont.truetype("Open24DisplaySt.ttf", size=100)

            draw = ImageDraw.Draw(im)
            draw.text((687, 50), "0", font=fnt, fill=(255, 255, 255, 255))
            draw.text((687, 159), "0", font=fnt, fill=(255, 255, 255, 255))
            draw.text((687, 264), "0", font=fnt, fill=(255, 255, 255, 255))

            buffer1 = BytesIO()
            im.save(buffer1, format='png')

            buffer1.seek(0)  # Reset the buffer position to the beginning
        message = await interaction.channel.send(f'ID: `{unique_id}`', embed=embed, file=nextcord.File(buffer1, filename="äänestys.png"), view=VotingButtons())

        entry1 = {f'{interaction.user.id}': f'{interaction.user}', 'USER-ID': interaction.user.id, 'STATUS': 'OPEN', 'MESSAGE-ID': f'{message.id}', 'CHANNEL-ID': f'{interaction.channel.id}', 'JAA': 0, 'EI': 0, 'TYHJIÄ': 0, 'DETAILS': f'{self.topic.value}', 'voters': []}
        data = json.dumps(entry1)

        with open(filename, "w") as file:
            file.write(data)
        await interaction.response.send_message(f'Hello <@{interaction.user.id}>! Your vote `{unique_id}` has been started.', ephemeral=True)

class ttsmodal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "TTS settings. (/languages)",
            timeout=None,
        )

        self.kieli = nextcord.ui.TextInput(label = "Language code. (/languages)", style = nextcord.TextInputStyle.short, required = True, max_length=5)
        self.add_item(self.kieli)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        iiidee = f"{interaction.user.id}"
        await asyncio.sleep (2)
        filename = f'user_profiles\{iiidee}.json'
        with open(filename, "w") as file4:
            pass

        entry1 = {f'{interaction.user.id}': f'{interaction.user}', "lang" : f"{self.kieli.value}"}
        dict = json.dumps(entry1)

        with open(filename, "w") as file:
            file.write(dict)
        await interaction.response.send_message (f'<@{interaction.user.id}>! Your settings have been saved.', ephemeral=True)

class BirthdayModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Birthday Notifications",
            timeout=None,
        )

        # Define the TextInput field for the birthday
        self.birthday_input = nextcord.ui.TextInput(
            label="Your birthday (DD-MM)",
            style=nextcord.TextInputStyle.short,
            required=True,
            max_length=5
        )
        self.add_item(self.birthday_input)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        print(f'User {interaction.user} added their birthday as {self.birthday_input.value}')
        # Path to the JSON file
        file_path = r"user_profiles/birthdays.json"

        # Ensure the file exists; if not, create it with an empty dictionary
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump({}, file)

        # Load existing data from the JSON file
        with open(file_path, "r") as file:
            try:
                birthdays = json.load(file)
            except json.JSONDecodeError:
                birthdays = {}

        # Add or update the user's birthday
        user_id = str(interaction.user.id)
        birthdays[user_id] = {
            "username": str(interaction.user),
            "birthday": self.birthday_input.value
        }

        # Save the updated data back to the JSON file
        with open(file_path, "w") as file:
            json.dump(birthdays, file, indent=4)

        # Respond to the user
        await interaction.response.send_message(
            f"Hello <@{interaction.user.id}>! Your birthday ({self.birthday_input.value}) has been noted. A special surprise will happen on your special day!",
            ephemeral=True
        )

class VotingButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Yes.", style=nextcord.ButtonStyle.green, custom_id='vote-yes', disabled=False)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_id = interaction.channel_id
        message_id = interaction.message.id
        voter_id = str(interaction.user.id)

        message = await bot.get_channel(channel_id).fetch_message(message_id)
        user_id_match = re.search(r'\d+', message.content)

        if user_id_match:
            applicant_id = int(user_id_match.group())
            s1 = message.content.replace("ID: `", "")
            s2 = s1.replace("`", "")

        filename = f'voting/{s2}.json'

        try:
            with open(filename, "r") as file:
                applicant_data = json.load(file)

            voters = applicant_data['voters']
            print(voters)

            if f"{voter_id} | JAA" in voters:
                text2 = 'You have already voted for this option.'       # Do not ask why this is not done better, it works.
            elif f"{voter_id} | EI" in voters:                          # I do not feel like fixing this shit.
                applicant_data['voters'].remove(f"{voter_id} | EI")
                applicant_data['EI'] -= 1
                text2 = 'Your vote has been changed.'
                applicant_data['JAA'] += 1
                applicant_data['voters'].append(f"{voter_id} | JAA")

                with open(filename, "w") as file:
                    json.dump(applicant_data, file)

            elif f"{voter_id} | TYHJÄ" in voters:
                applicant_data['voters'].remove(f"{voter_id} | TYHJÄ")
                applicant_data['TYHJIÄ'] -= 1
                text2 = 'Your vote has been changed.'
                applicant_data['JAA'] += 1
                applicant_data['voters'].append(f"{voter_id} | JAA")

                with open(filename, "w") as file:
                    json.dump(applicant_data, file)

            else:
                applicant_data['voters'].append(f"{voter_id} | JAA")
                applicant_data['JAA'] += 1
                text2 = 'Your vote `Yes` has been recorded!'

                entry = {f'{voter_id}': 'JAA'}

            with open(filename, "w") as file:
                json.dump(applicant_data, file)

            jaa = applicant_data['JAA']
            ei = applicant_data['EI']
            tyhjiä = applicant_data['TYHJIÄ']
            with Image.open("äänestys.png") as im:
                fnt = ImageFont.truetype("Open24DisplaySt.ttf", size=100)
                draw = ImageDraw.Draw(im)
                draw.text((687, 50), f"{jaa}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 159), f"{ei}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 264), f"{tyhjiä}", font=fnt, fill=(255, 255, 255, 255))

                buffer1 = BytesIO()
                im.save(buffer1, format='png')
                buffer1.seek(0)

            await message.edit(file=nextcord.File(buffer1, filename="äänestys.png"))
            await interaction.response.send_message(f'{text2}', ephemeral=True)

        except Exception as e:
            print(f"{e}")

    @nextcord.ui.button(label="No.", style=nextcord.ButtonStyle.red, custom_id='vote-no', disabled=False)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_id = interaction.channel_id
        message_id = interaction.message.id
        voter_id = str(interaction.user.id)

        message = await bot.get_channel(channel_id).fetch_message(message_id)
        user_id_match = re.search(r'\d+', message.content)

        if user_id_match:
            applicant_id = int(user_id_match.group())
            s1 = message.content.replace("ID: `", "")
            s2 = s1.replace("`", "")

        filename = f'voting/{s2}.json'

        try:
            with open(filename, "r") as file:
                applicant_data = json.load(file)

            voters = applicant_data['voters']

            if f"{voter_id} | JAA" in voters:
                applicant_data['voters'].remove(f"{voter_id} | JAA")
                applicant_data['JAA'] -= 1
                text = 'Your vote has been changed.'
                applicant_data['EI'] += 1
                applicant_data['voters'].append(f"{voter_id} | EI")

                with open(filename, "w") as file:
                    json.dump(applicant_data, file)

            elif f"{voter_id} | EI" in voters:
                text = "You have already voted for this option."

            elif f"{voter_id} | TYHJÄ" in voters:
                applicant_data['voters'].remove(f"{voter_id} | TYHJÄ")
                applicant_data['TYHJIÄ'] -= 1
                text = 'Your vote has been changed.'
                applicant_data['EI'] += 1
                applicant_data['voters'].append(f"{voter_id} | EI")

                with open(filename, "w") as file:
                    json.dump(applicant_data, file)

            else:
                applicant_data['voters'].append(f"{voter_id} | EI")
                applicant_data['EI'] += 1
                text = 'Your vote `No` has been recorded!'

            with open(filename, "w") as file:
                json.dump(applicant_data, file)

            jaa = applicant_data['JAA']
            ei = applicant_data['EI']
            tyhjiä = applicant_data['TYHJIÄ']
            with Image.open("äänestys.png") as im:
                fnt = ImageFont.truetype("Open24DisplaySt.ttf", size=100)
                draw = ImageDraw.Draw(im)
                draw.text((687, 50), f"{jaa}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 159), f"{ei}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 264), f"{tyhjiä}", font=fnt, fill=(255, 255, 255, 255))

                buffer1 = BytesIO()
                im.save(buffer1, format='png')
                buffer1.seek(0)

            await message.edit(file=nextcord.File(buffer1, filename="äänestys.png"))
            await interaction.response.send_message(f'{text}', ephemeral=True)

        except FileNotFoundError:
            print(f"File {filename} not found")
            pass

    @nextcord.ui.button(label="Abstain.", style=nextcord.ButtonStyle.blurple, custom_id='vote-abstain', disabled=False)
    async def abstain(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_id = interaction.channel_id
        message_id = interaction.message.id
        voter_id = str(interaction.user.id)

        message = await bot.get_channel(channel_id).fetch_message(message_id)
        user_id_match = re.search(r'\d+', message.content)

        if user_id_match:
            applicant_id = int(user_id_match.group())
            s1 = message.content.replace("ID: `", "")
            s2 = s1.replace("`", "")

        filename = f'voting/{s2}.json'

        try:
            with open(filename, "r") as file:
                applicant_data = json.load(file)

            voters = applicant_data['voters']

            if f"{voter_id} | JAA" in voters:
                applicant_data['voters'].remove(f"{voter_id} | JAA")
                applicant_data['JAA'] -= 1
                text = 'Your vote has been changed.'
                applicant_data['TYHJIÄ'] += 1
                applicant_data['voters'].append(f"{voter_id} | TYHJÄ")

                with open(filename, "w") as file:
                    json.dump(applicant_data, file)

            elif f"{voter_id} | EI" in voters:
                applicant_data['voters'].remove(f"{voter_id} | EI")
                applicant_data['EI'] -= 1
                text = 'Your vote has been changed.'
                applicant_data['TYHJIÄ'] += 1
                applicant_data['voters'].append(f"{voter_id} | TYHJÄ")

                with open(filename, "w") as file:
                    json.dump(applicant_data, file)

            elif f"{voter_id} | TYHJÄ" in voters:
                text = "You have already voted for this option."

            else:
                applicant_data['voters'].append(f"{voter_id} | TYHJÄ")
                applicant_data['TYHJIÄ'] += 1
                text = 'Your vote `Abstain` has been recorded!'

            # Save the updated data back to the file
            with open(filename, "w") as file:
                json.dump(applicant_data, file)

            # Update the image
            yes_votes = applicant_data['JAA']
            no_votes = applicant_data['EI']
            abstentions = applicant_data['TYHJIÄ']
            with Image.open("äänestys.png") as im:
                fnt = ImageFont.truetype("Open24DisplaySt.ttf", size=100)
                draw = ImageDraw.Draw(im)
                draw.text((687, 50), f"{yes_votes}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 159), f"{no_votes}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 264), f"{abstentions}", font=fnt, fill=(255, 255, 255, 255))

                buffer1 = BytesIO()
                im.save(buffer1, format='png')
                buffer1.seek(0)  # Reset the buffer position to the beginning
            
            await message.edit(file=nextcord.File(buffer1, filename="äänestys.png"))
            await interaction.response.send_message(f'{text}', ephemeral=True)

        except FileNotFoundError:
            print(f"File {filename} not found")
            pass

    @nextcord.ui.button(label = "End Voting.", style = nextcord.ButtonStyle.gray, custom_id='voting-end', disabled=False)
    async def end_voting(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        guild_id = interaction.guild_id
        guild = nextcord.utils.find(lambda g: g.id == guild_id, bot.guilds)  
        channel_id = interaction.channel_id
        message_id = interaction.message.id

        # Check if the reaction is on an application message
        # Extract user ID from the message content
        message = await bot.get_channel(channel_id).fetch_message(message_id)
        user_id_match = re.search(r'\d+', message.content)
        
        if user_id_match:
            applicant_id = int(user_id_match.group())
            s1 = message.content.replace("ID: `", "")
            s2 = s1.replace("`", "")

            # Open the corresponding JSON file
            filename = f'voting/{s2}.json'
            try:
                with open(filename, "r") as file:
                    applicant_data = json.load(file)
                
                if applicant_data['USER-ID'] == interaction.user.id:

                    await message.edit('The vote has been processed.', view=VoteButtons2())
                    os.remove(filename)
                    
                    await interaction.response.send_message('The vote has been concluded.', ephemeral=True)
                elif applicant_data['USER-ID'] != interaction.user.id:
                    await interaction.response.send_message('You did not start the vote.', ephemeral=True)
            except FileNotFoundError:
                pass

class VoteButtons2(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Yes.", style=nextcord.ButtonStyle.blurple, custom_id='ticket-report2', disabled=True)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label="No.", style=nextcord.ButtonStyle.blurple, custom_id='ticket-general2', disabled=True)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label="Abstain.", style=nextcord.ButtonStyle.blurple, custom_id='ticket-bot2', disabled=True)
    async def abstain(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label="End vote.", style=nextcord.ButtonStyle.blurple, custom_id='ticket-bot3', disabled=True)
    async def end_vote(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

class ticketbuttons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, custom_id='ticket-delete', disabled=False)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        guild_id = interaction.guild_id
        guild = nextcord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        channel_id = interaction.channel_id
        message_id = interaction.message.id
        user = interaction.user
        message = await bot.get_channel(channel_id).fetch_message(message_id)

        if message.channel.category.id == 1278032882148839434:
            
            rooli = nextcord.utils.get(guild.roles, id=1004288428667576400)
            
            if rooli in user.roles:

                s1=interaction.message.content.replace("ID: `","")
                s2=s1.replace("`","")
                s3=s2.replace(" | 🔐","")

                filename = f'Moderation\support_tickets\{s3}.json'
                try:
                    with open(filename, "r") as file:
                        ticket_data = json.load(file)
                except Exception as e:
                    await interaction.response.send_message(f'**Error:** `{e}`')
                
                if ticket_data['STATUS'] == 'LUKITTU':
                    await interaction.response.send_message('This ticket can not be deleted as it is locked.', ephemeral=True)

                elif ticket_data['STATUS'] == 'AUKI':
                    käyttäjä = bot.get_user(ticket_data['KÄYTTÄJÄ-ID'])

                    log = bot.get_channel(data['TICKET_LOG'])
                    desc = f"""
                    **The ticket for user:** {käyttäjä.mention} **has been deleted.**

                    **Deleted by:** `{interaction.user}` ({interaction.user.mention})
                    **Status:** `{ticket_data['STATUS']}`
                    """
                    embed = nextcord.Embed (title = f'`📌` Ticket was deleted.', description = desc)
                    embed.timestamp = datetime.now()
                    embed.set_footer(text='Event logged ')
                    
                    await log.send (embed = embed, file=File(filename))
                    ticket_data['STATUS'] = "POISTETTU"

                    ticket_channel = bot.get_channel(channel_id)
                    await ticket_channel.delete()
                    os.remove(filename)

    @nextcord.ui.button(label="Lock", style=nextcord.ButtonStyle.blurple, custom_id='ticket-lock', disabled=False)
    async def lock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        guild_id = interaction.guild_id
        guild = nextcord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        user = interaction.user
        rooli = nextcord.utils.get(guild.roles, id=1004288428667576400)
        
        if rooli in user.roles:
            s1=interaction.message.content.replace("ID: `","")
            s2=s1.replace("`","")
            s3=s2.replace(" | 🔐","")
            print (s3)
            filename = f'Moderation\support_tickets\{s3}.json'
            print (filename)

            try:
                with open(filename, "r") as file:
                    ticket_data = json.load(file)
            except:
                pass

            if ticket_data['STATUS'] == 'AUKI':
                käyttäjä = bot.get_user(ticket_data['KÄYTTÄJÄ-ID'])

                log = bot.get_channel(data['TICKET_LOG'])
                desc = f"""
                **The ticket for user:** {käyttäjä.mention} **has been locked.**

                **Ticket was locked by:** `{interaction.user}` ({interaction.user.mention})
                """
                embed = nextcord.Embed (title = f'`🔐` Ticket locked.', description = desc)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                
                
                ticket_data['STATUS'] = "LUKITTU"

                with open(filename, "w") as file:
                    json.dump(ticket_data, file)
                
                ticket_channel = bot.get_channel(interaction.channel_id)
                ticket_message = await ticket_channel.fetch_message(ticket_data['VIESTI-ID'])
                ticket_id = ticket_data['TICKET-ID']

                await ticket_message.edit(f'ID: `{ticket_id}` | 🔐')
                await log.send (embed = embed)

            elif ticket_data['STATUS'] == 'LUKITTU':
                käyttäjä = bot.get_user(ticket_data['KÄYTTÄJÄ-ID'])

                log = bot.get_channel(data['TICKET_LOG'])
                desc = f"""
                **The ticket for user:** {käyttäjä.mention} has been unlocked.

                **Ticket was unlocked by:** `{interaction.user}` ({interaction.user.mention})
                """
                embed = nextcord.Embed (title = f'`🔐` Ticket unlocked.', description = desc)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                
                
                ticket_data['STATUS'] = "AUKI"
                
                with open(filename, "w") as file:
                    json.dump(ticket_data, file)

                ticket_channel = interaction.channel
                ticket_message = await ticket_channel.fetch_message(ticket_data['VIESTI-ID'])
                ticket_id = ticket_data['TICKET-ID']

                await ticket_message.edit(f'ID: `{ticket_id}`')
                await log.send (embed = embed)

class ticket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label = "General support", style = nextcord.ButtonStyle.blurple, custom_id='ticket-general', disabled=False)
    async def ilmianna(self, button : nextcord.ui.Button, interaction : nextcord.Interaction):
        try:
            ticket_dir_path = r'Moderation\support_tickets'
            ticket_luku = len([entry for entry in os.listdir(ticket_dir_path) if os.path.isfile(os.path.join(ticket_dir_path, entry))])

            ticket_id = (f'GEN-{ticket_luku}-{interaction.user}')

            guild_id = data['GUILD-ID']               
            guild = bot.get_guild(guild_id)

            category = bot.get_channel(1278032882148839434)

            new_channel = await category.create_text_channel(              # There's also create_voice_channel and create_stage_channel.
                f'{ticket_id}',                                            # channel_name should be "general", not "#general".
                # The rest are optional.
                overwrites={                                               # Used for custom channel permissions and private channels.
                    guild.default_role: nextcord.PermissionOverwrite(
                        view_channel=False                                 # By default, members can't send messages...
                    ),
                    guild.me: nextcord.PermissionOverwrite.from_pair(
                        nextcord.Permissions.all(),                        # But the bot has all permissions enabled...
                        nextcord.Permissions.none()                        # And none disabled!
                    ),
                    interaction.user: nextcord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        attach_files=True
                    ),
                    interaction.guild.get_role(1004288428667576400): nextcord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        attach_files=True
                    )
                },
                reason=f'Ticket | {ticket_id} | {interaction.user}'    # This shows up in the audit logs.
            )  

            filename = f'Moderation\support_tickets\{ticket_id}.json'
            with open(filename, "w") as file4:
                pass

            desc = f"""
            **Ticket created by:** {interaction.user.mention}

            *Please describe your issue now, and a staff member will get back to you shortly.*
            """
            embed = nextcord.Embed (title = f'`📌` General support.', description=desc, color=0x00ff00)
            embed.set_footer(text='With ❤️ by: Bobb3ll1')
            

            viesti = await new_channel.send(f'ID: `{ticket_id}`', embed=embed, view=ticketbuttons())
                
            entry1 = {f'{interaction.user.id}': f'{interaction.user}', 'LIPUKE-MUOTO' : 'General', 'KÄYTTÄJÄ-ID' : interaction.user.id, 'TICKET-ID' : f'{ticket_id}', 'LÄHETETTY': f'{datetime.utcnow()}', 'TICKET-CHANNEL-ID' : f'{new_channel.id}', 'STATUS' : 'AUKI', 'VIESTI-ID' : f'{viesti.id}'}
            dict = json.dumps(entry1)
            
            with open(filename, "w") as file:
                file.write(dict)

            await interaction.response.send_message(f'Hello {interaction.user.mention}! Your support ticket {new_channel.mention} has been created.', ephemeral=True)
        except Exception as e:
            print (e)
# >>>

@bot.event
async def on_ready():
    os.system('cls||clear')
    print ("ONLINE")

    change_status.start()
    birthday_check.start()
    cleanup_birthday_roles.start()

    directory = r"voting"
    
    for name in os.listdir(directory):
        print(f'Reactivating {name}')
        try:
            filename = f'voting\{name}'
            with open(filename, "r") as file:
                applicant_data = json.load(file)

            if applicant_data['STATUS'] == "AUKI":
                message_id = int(applicant_data['VIESTI-ID'])       # Persistent buttons.
                channel_id = int(applicant_data['KANAVA-ID'])
                print (f'{message_id}, {channel_id}')
                message = await bot.get_channel(channel_id).fetch_message(message_id)
                await message.edit (view=VotingButtons())
            else:
                pass
        except Exception as e:
            print (f'Reactivation failed :( | E: {e}')

    tuki = await bot.get_channel(1278004089170558976).fetch_message(1278032507329052836) # Channel ID where the support ticket button is, and the message ID. (Message from the bot.)
    await tuki.edit (view=ticket())

    for channel in bot.get_channel(1278032882148839434).channels:
        try:
            if channel.id == 1278034985147957359:
                pass
            else:
                message = await channel.history(limit=None, oldest_first=True).find(lambda m: m.author.id == 1270819691425828916)
                await message.edit (view=ticketbuttons())
        except:
            pass

bot.remove_command('help')

# Birthday notification feature code. <<<
BIRTHDAY_ROLE_ID = 1313956489416933477
GENERAL_CHANNEL_ID = 1004286742829989890
BIRTHDAYS_FILE = r"user_profiles/birthdays.json"

# Load the JSON file
def load_birthdays():
    try:
        with open(BIRTHDAYS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save the JSON file
def save_birthdays(data):
    with open(BIRTHDAYS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Birthday check task
@tasks.loop(time=datetime.strptime("09:00:00", "%H:%M:%S").time())
async def birthday_check():
    guild = bot.guilds[0]
    birthdays = load_birthdays()
    today = datetime.now(timezone.utc).strftime("%d-%m")

    for user_id, details in birthdays.items():
        if details["birthday"] == today and "role_given_at" not in details:
            member = guild.get_member(int(user_id))
            if not member:
                continue  # Skip if the member isn't in the server

            # Assign the birthday role
            role = guild.get_role(BIRTHDAY_ROLE_ID)
            if role and role not in member.roles:
                await member.add_roles(role, reason="It's their birthday!")
                # Update JSON with the time the role was given
                details["role_given_at"] = datetime.now(timezone.utc).isoformat()
                save_birthdays(birthdays)

            # Send a notification in the general channel
            channel = guild.get_channel(GENERAL_CHANNEL_ID)
            if channel:
                embed = nextcord.Embed(
                    title="🎉 Happy Birthday! 🎉",
                    description=f"Today is {member.mention}'s birthday! 🎂\nLet's wish them a happy birthday!",
                    color=nextcord.Color.gold()
                )
                await channel.send(embed=embed)

# Role cleanup task
@tasks.loop(minutes=5)
async def cleanup_birthday_roles():
    guild = bot.guilds[0]
    role = guild.get_role(BIRTHDAY_ROLE_ID)
    if not role:
        return

    birthdays = load_birthdays()
    now = datetime.now(timezone.utc)

    for user_id, details in list(birthdays.items()):
        if "role_given_at" in details:
            role_given_at = datetime.fromisoformat(details["role_given_at"])
            if now - role_given_at >= timedelta(hours=24):
                # Remove the role
                member = guild.get_member(int(user_id))
                if member and role in member.roles:
                    await member.remove_roles(role, reason="Birthday role expired.")
                # Remove the role_given_at field from JSON
                del details["role_given_at"]
                save_birthdays(birthdays)
# >>>

# Custom Status for discord. <<<
äänestys_dir_path = r'voting'
statuses = cycle(['With ❤️ by Bobb3ll1', 'spaghetti code', 'server shenanigans'])

@tasks.loop(seconds=5)
async def change_status():
    global statuses  
    
    current_status = next(statuses)
    
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=current_status))
# >>>

@bot.slash_command(guild_ids=[data['GUILD-ID']], description="Updates the vote information from the database.")
@commands.has_role(808846863217328139)
async def fix(interaction: nextcord.Interaction, id: str = None):
    if id is not None:
        try:
            filename = f'votes/{id}.json'
            with open(filename, "r") as file:
                applicant_data = json.load(file)

            message_id = applicant_data['MESSAGE-ID']
            message = await interaction.channel.fetch_message(message_id)
            
            text = f"The results of the vote `{id}` have been fetched from the database and updated in the message."
            jaa = applicant_data['YES']
            ei = applicant_data['NO']
            tyhjiä = applicant_data['ABSTAIN']
            with Image.open("vote.png") as im:
                fnt = ImageFont.truetype("Open24DisplaySt.ttf", size=100)
                draw = ImageDraw.Draw(im)
                draw.text((687, 50), f"{jaa}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 159), f"{ei}", font=fnt, fill=(255, 255, 255, 255))
                draw.text((687, 264), f"{tyhjiä}", font=fnt, fill=(255, 255, 255, 255))

                buffer1 = BytesIO()
                im.save(buffer1, format='png')
                buffer1.seek(0)  # Reset the buffer position to the beginning
            
            await message.edit(file=nextcord.File(buffer1, filename="vote.png"))
            print('Hello there')
            await interaction.response.send_message(f'{text}', ephemeral=True)
        except:
            await interaction.response.send_message('I encountered an error, did you execute the command in the same channel where the vote is?', ephemeral=True)
    else:
        await interaction.response.send_message(f"ID is missing | Error: `ID is not specified, cannot read mind.`", ephemeral=True)

@bot.slash_command(guild_ids=[data['GUILD-ID']], description="Set a user on timeout.")
@application_checks.has_permissions(moderate_members=True, administrator=True)
async def timeout(interaction: nextcord.Interaction, user: nextcord.Member, duration: str, *, reason: str = None):
    log = bot.get_channel(data['MODERATION_LOG'])
    try:
        time_seconds = humanfriendly.parse_timespan(duration)
        timeout_duration = nextcord.utils.utcnow() + timedelta(seconds=time_seconds)
        await user.timeout(timeout_duration, reason=reason)
        unix_timestamp = math.trunc(timeout_duration.timestamp())
        
        reason_text = reason if reason else "No reason provided."
        
        log_description = f"""
        **Moderator:** {interaction.user} ({interaction.user.mention})      
        **User:** {user} ({user.mention})
        **Duration:** {duration} (Expires: <t:{unix_timestamp}:R>)
        **Reason:** `{reason_text}`
        """
        log_embed = nextcord.Embed(title="`🤫` Timeout", description=log_description)
        log_embed.timestamp = datetime.now()
        log_embed.set_footer(text="Event logged")
        
        await interaction.response.send_message(f"{user.mention} has been put on timeout! Expires: <t:{unix_timestamp}:R>")
        await log.send(embed=log_embed)
        
        notification_description = f"""
        Hello, you have been placed on a timeout that will expire on <t:{unix_timestamp}:R>.
        **Reason:** `{reason_text}`
        """
        notification_embed = nextcord.Embed(title="`🤫` Timeout Notification", description=notification_description)
        notification_embed.timestamp = datetime.now()

        
        await user.send(embed=notification_embed)
    
    except Exception as e:
        await interaction.response.send_message("An error occurred while trying to set the timeout. Please try again later.", ephemeral=True)
        
        error_description = f"""
        **Moderator:** {interaction.user} ({interaction.user.mention})
        **Attempted to timeout user:** {user} ({user.mention})
        **Reason:** `{reason_text}`
        
        **ERROR:** `{e}`
        """
        error_embed = nextcord.Embed(title="`🤫` Timeout Error", description=error_description, color=0xe0050b)
        error_embed.timestamp = datetime.now()
        error_embed.set_footer(text="An error occurred")
        
        await log.send(embed=error_embed)

@timeout.error
async def on_timeout_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message("Hey, you are not an admin. :angry:", ephemeral=True)
    else:
        raise error

@bot.slash_command(guild_ids=[data['GUILD-ID']], description="TTS for Jackxolotl's Server. The bot speaks for you.")
async def tts(interaction: nextcord.Interaction):
    try:
        voicechannel = bot.get_channel(interaction.user.voice.channel.id)
        if interaction.user.voice.channel.id == interaction.client.voice_clients[0].channel.id:
            await interaction.client.voice_clients[0].disconnect()
            await interaction.response.send_message('I have left the voice channel.', ephemeral=True)

    except Exception as e:
        try:
            voicechannel = bot.get_channel(interaction.user.voice.channel.id)
            await nextcord.VoiceChannel.connect(voicechannel)
            await interaction.response.send_message('I have joined the voice channel.', ephemeral=True)

        except Exception as e:
            await interaction.response.send_message('Something went wrong... Are you in a voice channel? :thinking:', ephemeral=True)

tts_queue = []
is_playing = False

@bot.event
async def on_message(message):
    global is_playing

    ran_char_list = ['a', 'b', 'c', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    iiidee = f"{message.author}-{random.choice(ran_char_list)}{random.choice(ran_char_list)}{random.choice(ran_char_list)}{random.choice(ran_char_list)}" # Do not ask.
    botti = bot.get_user(1270819691425828916)

    if "cute" in message.content.lower() and message.author != botti:
        await message.reply(f"You're cute!") 

    if message.author != botti and message.channel == bot.get_channel(1270848883303649420):
        try:
            filename = f'user_profiles/{message.author.id}.json'
            with open(filename, "r") as file:
                userdata = json.load(file)
            language = userdata["lang"]
        except Exception:
            language = "en"

        tts_text = message.content
        tts_file = f"tts/{iiidee}.mp3"
        myobj = gTTS(text=tts_text, lang=language, slow=False)
        myobj.save(tts_file)

        tts_queue.append((message.author, tts_text, tts_file))
        await process_queue()

async def process_queue():
    global is_playing

    if is_playing:
        return

    while tts_queue:
        is_playing = True
        message_author, tts_text, tts_file = tts_queue.pop(0)
        
        try:
            if message_author.voice.channel.id == bot.voice_clients[0].channel.id:
                voice_client = bot.voice_clients[0]
                audio_source = nextcord.FFmpegPCMAudio(tts_file, executable='ffmpeg.exe')
                
                if not voice_client.is_playing():
                    print (f'TTS | {message_author} --> {tts_text}')
                    voice_client.play(audio_source)
                    while voice_client.is_playing():
                        await asyncio.sleep(1)

                os.remove(tts_file)
        except Exception as e:
            print(e)

    is_playing = False

@bot.slash_command(guild_ids=[data['GUILD-ID']], description = "Tells you the languages that the bot supports.")
async def languages(interaction: nextcord.Interaction):
        viesti = """
```
Afrikaans: af, Arabic: ar
Bulgarian: bg, Bengali: bn
Bosnian: bs, Catalan: ca
Czech: cs, Danish: da
German: de, Greek: el
English: en, Spanish: es
Estonian: et, Finnish: fi
French: fr, Gujarati: gu
Hindi: hi, Croatian: hr
Hungarian: hu, Indonesian: id
Icelandic: is, Italian: it
Hebrew: iw, Japanese: ja
Javanese: jw, Khmer: km
Kannada: kn, Korean: ko
Latin: la, Latvian: lv
Malayalam: ml, Marathi: mr
Malay: ms, Myanmar (Burmese): my
Nepali: ne, Dutch: nl
Norwegian: no, Polish: pl
Portuguese: pt, Romanian: ro
Russian: ru, Sinhala: si
Slovak: sk, Albanian: sq
Serbian: sr, Sundanese: su
Swedish: sv, Swahili: sw
Tamil: ta, Telugu: te
Thai: th, Filipino: tl
Turkish: tr, Ukrainian: uk
Urdu: ur, Vietnamese: vi
Chinese (Simplified): zh-CN, Chinese (Mandarin/Taiwan): zh-TW
Chinese (Mandarin): zh
```
"""

        await interaction.response.send_message(viesti, ephemeral=True)

@bot.slash_command(guild_ids=[data['GUILD-ID']], description="Set the language to use for TTS functionality.")
async def setup(interaction: nextcord.Interaction):
    await interaction.response.send_modal(ttsmodal())

@bot.slash_command(guild_ids=[data['GUILD-ID']], description="Sets a ban for the user")
@application_checks.has_permissions(ban_members=True)
async def ban(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = None):
    log = bot.get_channel(data['MODERATION_LOG'])
    if user.id == interaction.user.id:
        await interaction.response.send_message("Unfortunately, you cannot ban yourself!", ephemeral=True)
    else:
        if reason is None:
            reason = f"Reason not provided by {interaction.user}"
        desc = f"""
        **Successfully issued a ban to `{user}` ({user.mention}).**
        """
        embed = nextcord.Embed(title='`⛔` Ban!', description=desc, color=0xe0050b)
        embed.timestamp = datetime.now()
        embed.set_footer(text='Ban issued ')
        await interaction.response.send_message(embed=embed)

        if reason is None:
            try:
                desc = f"""
                **Administrator:** `{interaction.user}` ({interaction.user.mention})
                **Issued a ban to:** `{user}` ({user.mention}) **ban**
                **ID:** `{user.id}`
                **Reason:** `Reason not provided.`
                """
                embed = nextcord.Embed(title='`⛔` Ban issued', description=desc, color=0xe0050b)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                await log.send(embed=embed)

                desc = f"""
                Hello {user.mention}! You have been banned from Jackxolotl's Server.
                **Reason:** `Reason not provided.`
                """
                embed = nextcord.Embed(title='`⛔` You have been banned.', description=desc, color=0xe0050b)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                await user.send(embed=embed)
                await user.ban(reason=reason)
            except:
                await user.ban(reason=reason)
                desc = f"""
                **Administrator:** `{interaction.user}` ({interaction.user.mention})
                **Issued a ban to:** `{user}` ({user.mention}) **ban**
                **ID:** `{user.id}`
                **Reason:** `Reason not provided.`

                **User has disabled DMs. Notification has not been sent.**
                """
                embed = nextcord.Embed(title='`⛔` Ban issued', description=desc, color=0xe0050b)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                await log.send(embed=embed)
                
        if reason is not None:
            try:
                desc = f"""
                **Administrator:** `{interaction.user}` ({interaction.user.mention})
                **Issued a ban to:** `{user}` ({user.mention}) **ban**
                **ID:** `{user.id}`
                **Reason:** `{reason}`
                """
                embed = nextcord.Embed(title='`⛔` Ban issued', description=desc, color=0xe0050b)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                await log.send(embed=embed)

                desc = f"""
                Hello {user.mention}! You have been banned from Jackxolotl's Server.
                **Reason:** `{reason}`
                """
                embed = nextcord.Embed(title='`⛔` You have been banned.', description=desc, color=0xe0050b)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                await user.send(embed=embed)
                await user.ban(reason=reason)
            except:
                await user.ban(reason=reason)
                desc = f"""
                **Administrator:** `{interaction.user}` ({interaction.user.mention})
                **Issued a ban to:** `{user}` ({user.mention}) **ban**
                **ID:** `{user.id}`
                **Reason:** `{reason}`

                **User has disabled DMs. Notification has not been sent.**
                """
                embed = nextcord.Embed(title='`⛔` Ban issued', description=desc, color=0xe0050b)
                embed.timestamp = datetime.now()
                embed.set_footer(text='Event logged ')
                await log.send(embed=embed)

@ban.error
async def on_ban_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message("You don't have the required permissions do to this! :angry:", ephemeral=True)
    else:
        raise error

@bot.slash_command(guild_ids=[data['GUILD-ID']], description="Starts the process for creating a vote.")
async def vote(interaction: nextcord.Interaction):
    await interaction.response.send_modal(VotingModal())

@bot.slash_command(guild_ids=[data['GUILD-ID']], description="Add your birthday to our database to get a special surprise on your special day.")
async def birthday(interaction: nextcord.Interaction):
    await interaction.response.send_modal(BirthdayModal())

async def update_channel_name(guild):
    channel = guild.get_channel(1279078352577106022)
    if channel and isinstance(channel, nextcord.VoiceChannel):
        member_count = guild.member_count
        new_name = f"Server members: {member_count}"
        await channel.edit(name=new_name)

@bot.event
async def on_member_join(member):
    await update_channel_name(member.guild)
@bot.event
async def on_member_remove(member):
    await update_channel_name(member.guild)

bot.run(data['TOKEN'])