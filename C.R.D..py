# Version: 1.0.0.0
#
#Legend: release.major.minor.hotfix

import datetime
import os
from configparser import ConfigParser

import discord
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

# google api stuff
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'gapi client secret.json', scope)
gcrdbot = gspread.authorize(creds)
gcrdbot.login()

CONFIG = ConfigParser()
CONFIG.read('stratos.ini')

intents = discord.Intents(
    bans=True,
    dm_typing=True,
    emojis=True,
    guilds=True,
    integrations=True,
    invites=True,
    members=True,
    messages=True,
    reactions=True,
    webhooks=True)

bot_prefix = CONFIG["General Settings"]["botPrefix"]
crdbot = commands.Bot(command_prefix=bot_prefix, intents=intents,
                      help_command=None, activity=discord.Game(f'{bot_prefix}help'))
crdbot.pm_help = True

for file in os.listdir("ext"):
    name, ext = os.path.splitext(file)

    if ext == '.py':
        crdbot.load_extension(f'ext.{name}')

@crdbot.event
async def on_ready():
    print(f"Executed successfully! {crdbot.user.name} is up and running.")
    print(f"The current time of execution is {datetime.datetime.now():%H:%M}.\n")

# invite: https://discordapp.com/api/oauth2/authorize?client_id=557309788480864256&permissions=1543957590&scope=bot

crdbot.run(CONFIG["API Keys"]["discordToken"])
