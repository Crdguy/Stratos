#Version: 1.0.0.0
#
#Legend: release.major.minor.hotfix

print("Initiating startup process (this may take longer if this application has just been launched)...")
print("Importing modules...")

import asyncio
import discord
import configparser
from glob import glob
from discord.ext.commands import Bot
from discord.ext import commands
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
'''
#import modules
print("Importing modules...")
#try:
import asyncio
#from darksky import forecast
from geopy.geocoders import Nominatim
import linecache
import fileinput
import discord
import random
import datetime
import time
import os
import math
import string
import sys
import urllib.request
import aiohttp
import requests
import configparser
import nacl
#import sys; print(sys.executable)
import numpy
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#google api stuff
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gapi client secret.json', scope)
gcrdbot = gspread.authorize(creds)
gcrdbot.login()

try:
    import youtube_dl
except:
    youtube_dl = None
from PIL import Image, ImageDraw, ImageFont
import PIL
import json
import csv
from glob import glob
from discord.ext.commands import Bot
from discord.ext import commands
from discord.errors import DiscordException

'''
#google api stuff
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gapi client secret.json', scope)
gcrdbot = gspread.authorize(creds)
gcrdbot.login()    
#print("Import successful.\nSetting up Crdbot configurations..")

#open "stratos.ini"
print("Configuring crdbot...")
try:
    config = configparser.ConfigParser()
    config.read('stratos.ini')

except Exception:
    input("Error, something went wrong while parsing 'stratos.ini'. Ensure the file is not corrupt or missing.")
    exit(0)

#configure intents
intents = discord.Intents.default()

#I hate this, but it gives modularity
intents.guilds = True
intents.bans = True
intents.emojis = True
intents.integrations = True
intents.webhooks = True
intents.invites = True
intents.voice_states = False
intents.presences = False
intents.messages = True
intents.guild_messages = True
intents.dm_messages = True
intents.reactions = True
intents.guild_reactions = True
intents.dm_reactions = True
intents.typing = False
intents.guild_typing = False
intents.dm_typing = True


#configure Crdbot
try:
    Client = discord.Client()
    bot_prefix= config["General Settings"]["botPrefix"]
    crdbot = commands.Bot(command_prefix=bot_prefix)
    crdbot.pm_help = True
    print("Setup of configurations successful. Help to be sent in PM: {}, bot prefix: {}\nAttempting to read files...".format(crdbot.pm_help, bot_prefix))
except Exception:
    x = input("Critical error while performing setup. Aborting program.")
    exit(0)


#load extensions
print("Loading all extensions...")
#remove the help command, we already have a command called help
crdbot.remove_command("help")
fstr = ""
for f in glob("ext/*.py"):
    #f is the path to the file, so we can format it to get the module name
    f = str(f).replace("\\" , ".").replace("/",".").replace(".py","")
    crdbot.load_extension(f)
    fstr = fstr + f + ", "
fstr = fstr[0:len(fstr)-2]
print("Loaded the following extensions: {}".format(fstr))




print("Extensions importing successful!\nAttempting connection to Discord servers...")

#connect to Discord


@crdbot.event
async def on_ready():

    print("Logging in...")
    print("Executed successfully! {} is up and running.".format(crdbot.user.name))
    print("Up and running! The current time of execution is {0.hour}:{0.minute}.\n\n\n".format(datetime.datetime.now()))
    await crdbot.change_presence(activity=discord.Game(type=1, url = "https://www.twitch.tv/epic_style", name=";help - {} members".format(len(set(crdbot.get_all_members())))))

    #variables
    queue = []
    fc = 0


    
#darksky API stuff - unused but let's not touch it incase
#units = [config["API Settings"]["darkSkyUnits"]]
#end of that

#geolocator = Nominatim(user_agent="C.R.D.")


#commands

'''    
@crdbot.command()
async def help(ctx, command):

    if command == "fight":
        desc = "`;fight [character] [character2] [number of rounds]`. Makes two characters 'fight' each other."
    elif command == "ping":
        desc = "`;ping`. Tests the API's response time in milliseconds."
    elif command == "weather":
        desc = "`;weather [location] [currently, hourly]`. Displays the current or hourly forecast for any given location."
    elif command == "sd":
        desc = "`;sd`. Shuts down this bot. Only bot administrators have the permissions to execute this command."
    elif command == "dc":
        desc = "`;dc`. Disconnects the bot from a voice channel."
    elif command == "play":
        desc = "`;play [link]`. Joins the voice channel you're in, and plays a YouTube link."
    elif command == "pinfo":
        desc = "`;pinfo`. Displays info about the current or last played song."
    elif command == "quadratic":
        desc = "`;quadratic [a] [b] [c]`. Solves a quadratic equation using the values a, b and c using the quadratic formula. Also provides full method."
    elif command == "purge":
        desc = "`;purge [x] [optional: user]`. Deletes the last x messages.\n\nIf the `user` argument is passed (either by mentioning that user or adding their user ID) Stratos will look for as many messages that user has sent in the last x messages, and delete them. If you do `;purge 10 557309788480864256` for example, it might not delete 10 messages by Stratos, but rather all messages Stratos has sent in the last 10 messages."
    elif command == "setstatus":
        desc = "`;setstatus [0-4] [status]`. Sets the current status of the bot. Only Crdguy#9939 is able to execute this command."
    elif command == "ehlookup":
        desc = "`;ehlookup [subcommand] [options] [shipname]`. Simple usage: `;ehlookup [subcommand] [shipname]`. Returns information gathered from the most recent Event Horizon Database and calculates useful information such as ship cost, workshop level, and more.\n'subcommand' can be `ship` to find information about a ship, or `module` to return information on any module.\nOptions:\n`-fast` - Creates a lower quality ship image with a grid.\n`-superfast` - Creates a lower quality ship image without a grid.\n`-ultrafast` - Creates a low quality ship image that is not scaled  up. Ideal for extremely large ships.\n`-nolayout` - Shows all information about the ship without generating an output.\n`-myfile` - Upload a ship .json and information will be generated for the ship\n\nIf you would like to see a list of available ships, react with \U0001F522."
    elif command == "rust":
        desc = "`;rust [optional, mention a user]`. Mention a user or upload an image to 'rust' that image.\nThis command serves as a test for image manipulation. It may be removed or changed."
    elif command == "userinfo":
        desc = "`;userinfo [args]`. Simple usage: `;userinfo`. Returns useful information about a user, such as account creation and activity.\n\nArgs:\nYou may use both the `user` and the `channel` arguments in the same command.\n`user` - Mention a user or give their ID to display information about somebody else's account. Only works with users in the server.\n`channel` - Tag a channel to view your activity in that channel instead."
    elif command == "role":
        desc = "Temporary command. Placeholder for role assignment, which will be added at a later date."
    elif command == "feedback":
        desc = "`;feedback [information]`. Use this command to submit bug reports and feedback to the bot developer, Crdguy#9939. Put this information in the [information] field."
    elif command == "support":
        desc = "`;support`. Returns some useful information if you're having some issues or need help with Stratos."
    elif command == "minesweeper":
        desc = "`;minesweeper [args]`. Play a game of Minesweeper and see if you can beat a randomly generated grid up to size 14.\n\nArguments:\n`Difficulty` - pick from `easy`, `normal`, `hard`, `expert` or `death`. Defaults to `normal` if not specifed. Affects the amount of mines on the playing field.\n\n`Size` - pick a number from 1 to 14 to choose the grid size, i.e. picking 4 generates a 4x4 grid. Defaults to 8 if not specified."
    elif command == "ban":
        desc = "`;ban [user] [reason]`, where `user` is a mentioned user or an ID that will be banned, and an optional `reason` to ban them. Bans a user and prompts how many days to ban for, if you have the permissions to ban users. Can be used to ban users not in a server, by ID."
    elif command == "pong":
        desc = "`;pong`. Tests the API's response time in milliseconds."
    elif command == "xkcd":
        desc = "`;xkcd [args]`. Display a random or specified xkcd comic. If no arguments are given, Stratos will display a random comic.\n\nArguments:\n`Number` - if a number is given, Stratos will attempt to retrieve the comic with that number.\n\n`-c`, or `--current` - display the latest comic." 

    msg = await ctx.message.channel.send(desc)
    if command == "ehlookup":
        await msg.add_reaction("\U0001F522")
        passed = False
        while msg:
            await crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U0001F522")
            msg2 = await ctx.fetch_message(msg.id)
            
            reactsO = msg2.reactions

            async for y in reactsO[0].users():
                
                
                if ctx.message.author == y:

                    allships = []
                    with open("shiplookuptable.csv") as lookuptableraw:
                        lookuptable = csv.reader(lookuptableraw, delimiter=",")
                        for line in lookuptable:
                            #if line[0] != "shipname":
                                
                            allships.append(line[0])
                    allships.pop(0)

                    allshiptemp = ""
                    emb = discord.Embed(
                        title = "List of Ships:",
                        type = "rich",
                        )

                    x = 0
                    while x != 20:
                        allshiptemp = allshiptemp + allships[x] + "\n"
                        x = x + 1
                    emb.description = allshiptemp
                    
                    await msg.edit(content="",embed = emb)
                    await msg.add_reaction("◀")
                    await msg.add_reaction("▶")
                    
                    
                    
                    msgc = msg
                    while msg == msgc:

                        react2 = await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji in ["▶","◀"])
                        msg2 = await ctx.fetch_message(msg.id)
                        reacts = msg2.reactions

                        #reacts[1] is ◀,2 is ▶
                        async for y in reacts[1].users():
                            if ctx.message.author == y:
                                z = x
                                allshiptemp = ""
                                while x != z - 20:
                                    try:
                                        allshiptemp = allshiptemp + allships[x] + "\n"
                                    except IndexError:
                                        x = 0
                                        break
                                    x = x - 1

                                emb.description = allshiptemp
                                await msg.edit(content="",embed = emb)
                                
                        async for y in reacts[2].users():
                            if ctx.message.author == y:
                                z = x
                                allshiptemp = ""
                                while x != z + 20:
                                    try:
                                        allshiptemp = allshiptemp + allships[x] + "\n"
                                    except IndexError:
                                        remainder = 17-len(allships)%20
                                        newlines = ""
                                        for a in range(remainder):
                                            newlines = newlines + "\n<:blank:407248051053264900>"
                                        print(newlines)
                                        allshiptemp = allshiptemp + "**END OF LIST!**" + newlines
                                        break
                                        
                                    x = x + 1

                                emb.description = allshiptemp
                                await msg.edit(content="",embed = emb)


                  
 
@help.error
async def helpe_error(ctx,err):
    
    if isinstance(err, commands.MissingRequiredArgument):
        desc = "List of commands. Do `;help [command]` to view detailed command info."
        
        #add any commands that should not be appended to the list of commands 
        forbiddencommands = ["help","order","cubic","horizon","brap","reply"]
        
        for command in crdbot.commands:
            if str(command) not in forbiddencommands:
                desc = desc + "\n" + str(command)
            
        emb = discord.Embed(
            title = "Command list",
            type = "rich",
            description = desc,
            )
        
        await ctx.message.channel.send(embed = emb)

            
'''
#@crdbot.event
#async def on_message(message):





    #await crdbot.process_commands(message) 

#invite:        https://discordapp.com/api/oauth2/authorize?client_id=557309788480864256&permissions=1543957590&scope=bot
crdbot.run(config["API Keys"]["discordToken"])
