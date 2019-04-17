print("Initiating startup process (this may take longer if this application has just been launched)...")
print("")

#import modules
print("Importing modules...")
#try:
import asyncio
from darksky import forecast
from geopy.geocoders import Nominatim
import linecache
import fileinput
import discord
import random
import datetime
import time
import os
import math
import sys
import urllib.request
import aiohttp
try:
    import youtube_dl
except:
    youtube_dl = None
from PIL import Image, ImageDraw
import PIL
import json
import csv
from glob import glob


from discord.ext.commands import Bot
from discord.ext import commands
from discord.errors import DiscordException

#except Exception as e:
#    x = input("Critical error when importing modules detected. Aborting program.")
#    print(e)
#    exit()
    
print("Import successful.\nSetting up Crdbot configurations..")


#configure Crdbot
try:
    Client = discord.Client()
    bot_prefix= ";"
    crdbot = commands.Bot(command_prefix=bot_prefix)
    crdbot.pm_help = True
    print("Setup of configurations successful. Help to be sent in PM: {}, bot prefix: {}\nAttempting to read files...".format(crdbot.pm_help, bot_prefix))
except Exception:
    x = input("Critical error while performing setup. Aborting program.")
    exit()


#read adminslist.txt to find admins

try:
    file = open("adminlist.txt","r")
except FileNotFoundError:
    print("Error: adminlist.txt not found under my directory. Please create it and add the IDs of any admins on newlines.")
try:
    admin = file.read()
    #print(admin)
except Exception:
    print("Some stupid error occured while I was reading. Did you delete the file?")
file.close()

try:
    file = open("blacklist.txt","r")
except FileNotFoundError:
    print("Error: blacklist.txt not found under my directory. Please create it and add the IDs of any admins on newlines.")
try:
    blacklist = file.read()
    print(blacklist)
except Exception:
    print("Some stupid error occured while I was reading. Did you delete the file?")
file.close()

print("File read sucessful!\nAttempting connection to Discord servers...")

#connect to Discord


@crdbot.event
async def on_ready():
    #try:
    print("Attempting login...")
    #await crdbot.wait_until_login()
    print("Logged in successfully!")
    print("Checking if ready...")
    #await crdbot.wait_until_ready()
    print("Executed successfully! {} is up and running.".format(crdbot.user.name))
    #print("ID: {}".format(crdbot.user.id))
    t = datetime.datetime.now()
    th = t.hour
    tm = t.minute
    ts = t.second

    print("Up and running! The current time of execution is {}:{}.\n\n\n".format(th, tm))
    memes = len(list(open("memes.txt")))
    await crdbot.change_presence(activity=discord.Game(type=1, url = "https://www.twitch.tv/epic_style", name="REWRITE IN PROGRESS!"))#.format(memes,len(set(crdbot.get_all_members())))))

    
    #variables
    queue = []
    fc = 0
    


#remove the help command
crdbot.remove_command("help")
    
#darksky API stuff
key = "217d340e838a283a43e6084d1a59af0f"
units = ["uk2"]
#end of that

geolocator = Nominatim(user_agent="C.R.D.")
#commands



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
        desc = "`;purge [n]`. Deletes the last n messages."
    elif command == "setstatus":
        desc = "`;setstatus [0-4] [status]`. Sets the current status of the bot. Only Crdguy#9939 is able to execute this command."
    elif command == "ehlookup":
        desc = "`;ehlookup [options] [shipname]`. Simple usage: `;ehlookup [shipname]`. Returns information gathered from the most recent Event Horizon Database and calculates useful information such as ship cost, workshop level, and more.\nOptions:\n`-fast` - Creates a lower quality ship image with a grid.\n`-superfast` - Creates a lower quality ship image without a grid.\n`-ultrafast` - Creates a low quality ship image that is not scaled  up. Ideal for extremely large ships.\n`-nolayout` - Shows all information about the ship without generating an output.\n`-myfile` - Upload a ship .json and information will be generated for the ship\n\nIf you would like to see a list of available ships, react with \U0001F522."

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

                        react2 = await crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji in ["▶","◀"])
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


                        '''
                        print("ok")
                        if react2 == "▶":
                            await ctx.send("placeholder_forward")
                        elif react2 == "◀":
                            await ctx.send("placeholder_backward")
                            
                        '''

                   
 
@help.error
async def helpe_error(ctx,err):
    
    if isinstance(err, commands.MissingRequiredArgument):
        #await ctx.send("List of commands:\n")
        desc = "List of commands. Do `;help [command]` to view detailed command info."

        
        for command in crdbot.commands:
            desc = desc + "\n" + str(command)

        emb = discord.Embed(
            title = "Command list",
            type = "rich",
            description = desc,
            )
        
        await ctx.message.channel.send(embed = emb)    

@crdbot.command()
async def fight(ctx, c1, c2, rounds):

    c1count = 0
    c2count = 0
    event = []
    x = 0
    abort = False
    cont = True
    desc = ""
    
    try:
        int(rounds)
    except Exception:
        desc = "You're funny, aren't you?"
        abort = True

    if c1 in ["@everyone","@here"]:
        desc = "You're funny, aren't you?"
        abort = True
        
    if c2 in ["@everyone","@here"]:
        desc = "You're funny, aren't you?"
        abort = True    

    
    #if decide is 0, c1 wins, else c2 wins


    emb = discord.Embed(
        title = "**Fight - {} vs {} ({} rounds)**".format(c1,c2,rounds),
        type = "rich",
        description = desc,
        colour = 0x8cc43d,
        )
    emb.set_thumbnail(url = "https://cdn.discordapp.com/attachments/447869090493890560/549653088659701770/fight.png")
    t = await ctx.message.channel.send(embed = emb)

    if abort == True:
        #await ctx.send("Abort!")
        return

    if int(rounds) < 0:
        emb.description = "You're funny, aren't you?"
        await t.edit(embed = emb)
        cont = False
        
    if str(int(rounds)) != str(rounds):
        emb.description = "You're funny, aren't you?"
        await t.edit(embed = emb)
        cont = False
        
    if cont != False:
        while x != int(rounds):

            #await ctx.send("**ROUND {}**".format(x+1))
            
            decide = random.randint(0,1)

            if decide == 0:
                event.append(random.choice(["{} flailed their limbs out wildly at {}, causing some damage.\n".format(c1,c2),
                                        "{} screamed loudly at {}, making their ears bleed.\n".format(c1,c2),
                                        "{} points a gun at themselves, but somehow manages to shoot {}.\n".format(c1,c2),
                                        "{} threw a table at {}.\n".format(c1,c2),
                                        "{} threw a fridge at {}.\n".format(c1,c2),
                                        "{} dropped their mixtape, and {} got set on fire.\n".format(c1,c2),
                                        "{} dug a grave for {}, and threw them into it.\n".format(c1,c2),
                                        "{} offered {} some chewing gum, but it was actually rigged with explosives.\n".format(c1,c2),
                                        "{} slapped {} with a carp.\n".format(c1,c2),
                                        "{} fell on {}.\n".format(c1,c2)
                                        ]))
                c1count = c1count + 1
                
            if decide == 1:
                event.append(random.choice(["{} flailed their limbs out wildly at {}, causing some damage.\n".format(c2,c1),
                                        "{} screamed loudly at {}, making their ears bleed.\n".format(c2,c1),
                                        "{} points a gun at themselves, but somehow manages to shoot {}.\n".format(c2,c1),
                                        "{} threw a table at {}.\n".format(c2,c1),
                                        "{} threw a fridge at {}.\n".format(c2,c1),
                                        "{} dropped their mixtape, and {} got set on fire.\n".format(c2,c1),
                                        "{} dug a grave for {}, and threw them into it.\n".format(c2,c1),
                                        "{} offered {} some chewing gum, but it was actually rigged with explosives.\n".format(c2,c1),
                                        "{} slapped {} with a carp.\n".format(c2,c1),
                                        "{} fell on {}.\n".format(c2,c1)
                                        ]))
                c2count = c2count + 1
        
            #await ctx.send(event[x])

            x = x + 1
            await asyncio.sleep(1.5)

            emb.description = "**ROUND {}**\n{}\n\n".format(x,event[x-1])
            await t.edit(embed = emb)



    #End of rounds 

    


    if c1count > c2count:
        await ctx.send("The winner is {}!".format(c1))

    elif c1count < c2count:
        await ctx.send("The winner is {}!".format(c2))
        
    elif c1count == c2count:
        await ctx.send("It appears that {} and {} somehow managed to draw.".format(c1,c2))

'''
@fight.error
async def fight_error(ctx,err):
    
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send("Missing one or more arguments. Correct command format: `;fight [character] [character2] [number of rounds]`")
    elif isinstance(err, commands.CommandInvokeError):
        await ctx.send("I did not recognise the number of rounds. Make sure it's an integer (whole number), and try again.")
'''

@crdbot.command()
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round((crdbot.latency*1000),3)))
    '''
    t = await ctx.send("Just a second.".format(ping))
    ms = (t.timestamp-ctx.created_at).total_seconds() * 1000
    await crdbot.edit_message(t, new_content='Pong! {}ms.'.format(int(ms)))

    '''
    


@crdbot.command()
async def weather(ctx, loc, time):

    loc = loc.replace("_"," ")
    loc = loc.replace("-"," ")

    location = geolocator.geocode(loc)
    lat = location.latitude
    long = location.longitude
    fcast = forecast(key,lat,long)

    hourl = ["hourly","hour","h"]
    dail = ["daily","dail","d"]
    currl = ["currently","current","curr","c"]
    
    if time in hourl:
        data = fcast["hourly"]["data"][1]
        fc = "Hourly"
    elif time in dail:
        data = fcast["daily"]
        fc = "Daily"
    elif time in currl:
        data = fcast["currently"]#["data"][1]
        fc = "Current"
    else:
        await ctx.send("Did not recognise second argument. Correct command format: `;weather [location] [currently, hourly]`")
        return
        
    print(fc)
    print("Icon: {}".format(data["icon"]))
    if data["icon"] == "clear-day":
        icon = "https://i.ibb.co/mvmpC6C/sunny.png"
    elif data["icon"] == "clear-night":
        icon = "https://i.ibb.co/wCZcrK5/clear-night.png"
    elif data["icon"] == "rain":
        icon = "https://i.ibb.co/hLb7TNW/rainy.png"
    elif data["icon"] == "snow":
        icon = "https://i.ibb.co/8sZDGjt/snow.png"
    elif data["icon"] == "sleet":
        icon = "https://i.ibb.co/PjfFSKM/sleet.png"
    elif data["icon"] == "wind":
        icon = "https://i.ibb.co/Gxmk02p/wind.png"
    elif data["icon"] == "fog":
        icon = "https://i.ibb.co/nBWn42N/fog.png"
    elif data["icon"] == "cloudy":
        icon = "https://i.ibb.co/qJgjz2q/cloudy.png"
    elif data["icon"] == "partly-cloudy-day":
        icon = "https://i.ibb.co/F4RH4Zh/partly-cloudy-day.png"
    elif data["icon"] == "partly-cloudy-night":
        icon = "https://i.ibb.co/9W1kn8y/partly-cloudy-night.png"
    else:
        icon = "https://cdn.discordapp.com/attachments/530795138415591434/530795583062016010/CRDindustries.png"

    print(icon)



    #print(data["windSpeed"])
    wind = round((data["windSpeed"]/2.237),2)
    bearing = str(data["windBearing"])+"°"
    precip = str(round(data["precipProbability"]*100,2))+"%"
    humid = str(round(data["humidity"]*100,2))+"%"
    vis = round((data["visibility"]*1.60934),2)


    if fc != "Daily":
        temp = round((data["temperature"]-32)*(5/9),2)
        atemp = round((data["apparentTemperature"]-32)*(5/9),2)
        desc = "{}\n\nTemperature: {}°C ({}°F)\nFeels like: {}°C ({}°F)\nHumidity: {}\nPrecipitation chance: {}\nVisibility: {} miles ({}km)\nPressure: {}mbar\n\n\n\nPowered by DarkSky API https://darksky.net/poweredby/ (I'm legally required to put this 'somewhere prominent in my app or service')".format(
        fcast.daily.summary,temp,data["temperature"],atemp,data["apparentTemperature"],humid,precip,data["visibility"],vis,data["pressure"])

    else:
        tempH = round((data["temperatureHigh"]-32)*(5/9),2)
        tempL = round((data["temperatureLow"]-32)*(5/9),2)
        atempH = round((data["apparentTemperatureHigh"]-32)*(5/9),2)
        atempL = round((data["apparentTemperatureLow"]-32)*(5/9),2)
        desc = "{}\n\nTemperature: Highs of {}°C ({}°F), lows of {}°C ({}°F)\nFeels like highs of {}°C ({}°F), lows of {}°C ({}°F)\nWind speed: {}m/s ({}mph)\n\nWind bearing: {}\nHumidity: {}\nPrecipitation chance: {}\nVisibility: {} miles ({}km)\nPressure: {}mbar\n\n\n\nPowered by DarkSky API https://darksky.net/poweredby/ (I'm legally required to put this 'somewhere prominent in my app or service')".format(
        fcast.daily.summary,tempH,data["temperatureHigh"],tempL,data["temperatureLow"],atempH,data["apparentTemperatureHigh"],atempL,data["apparentTemperatureLow"],wind,data["windSpeed"],bearing,humid,precip,data["visibility"],vis,data["pressure"]),
    


    
    emb = discord.Embed(title = "{} forecast in {}".format(fc, location),
    type = "rich",
    description = desc,
    colour = 0x8cc43d,
    )
    emb.set_thumbnail(url=icon),
    await ctx.send(ctx.message.channel, embed = emb)


@weather.error
async def weather_error(err,ctx):
    
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send("Missing one or more arguments. Correct command format: `;weather [location] [currently, hourly]`")
    elif isinstance(err, commands.CommandInvokeError):
        await ctx.send("I did not recognise your location. Is the spelling correct? You may also want to use underscores (_) for locations with multiple words.")
    

@crdbot.command(pass_context=True)
async def sd(ctx):
    if ctx.message.author.id in open("adminlist.txt").read():
        try:
            await ctx.send("Shutting down...")
            await crdbot.change_presence(status="offline")
            await crdbot.logout()
        except RuntimeError:
            print("Closed!")

#music stuff
@crdbot.command(pass_context=True)
async def dc(ctx):
    for x in crdbot.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()

    return await ctx.send("Not connected to a voice channel!")

@crdbot.command(pass_context=True)
async def play(ctx, link):
    #queue.append(link)
    #played = 0
    #try:
    cchannel = ctx.message.author.voice.channel 

    voice = await cchannel.connect()
    '''
    except:
        await ctx.send("Looks like you're not in a voice channel I can access!")
        return
    '''
    #while played != len(queue):
    #try:
    player = discord.FFmpegPCMAudio(source=link).read()
    #except:
    #await ctx.send("Error, unable to download from link. Are you sure that's a YouTube link?")
    #player = voice.create_ffmpeg_player("deadinside.wma")
    #while True:
    #player2 = discord.PCMAudio(player)
    #src = discord.AudioSource()
    #src.read()
    #voice.play(source=player)
    voice.send_audio_packet(data=player,encode=True)
    #voice.send_audio_packet(

    #variable defining mess
    '''
    global ptitle, pdesc, puplo, pupdt, pmins, psec, plike, pdislike, pview, puploader
    ptitle = player.title
    pdesc = player.description
    puplo = player.uploader
    pupdt = player.upload_date
    pdura = player.duration
    pmins = 0
    while pdura > 60:
        pdura = pdura - 60
        pmins = pmins+1
    if pdura < 10:
        psec = "0{}".format(pdura)
    else:
        psec = pdura
    
    plike = player.likes
    pdislike = player.dislikes
    pview = player.views
    puploader = ctx.message.author.name
    '''
    #ends here
    
    #await ctx.send("Now playing! '{}', requested by {}.".format(ptitle,puploader))

'''
@play.error
async def play_error(ctx,err):
    
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send("Missing a link. Correct command format: `;play [link]`")
'''
@crdbot.command(pass_context=True)
async def pinfo(ctx):
    #a = 0
    try:
        playinfo = discord.Embed(title = "Currently playing - '{}', requested by {}.".format(ptitle, puploader),
    
        description = "**Duration:** {}:{}\n**Likes:** {}\n**Dislikes:** {}\n**Video description:**\n{}\n".format(pmins,psec,plike,pdislike,pdesc, colour = 0x8cc43d, thumbnail = "https://cdn.discordapp.com/attachments/530795138415591434/530795750389579816/spiderbee.png"))
    except:
        await ctx.send("Looks like nothing is playing right now!")

    await crdbot.send_message(ctx.message.channel, embed=playinfo)


@crdbot.command(pass_context=True)
async def quadratic(ctx, a, b, c):

    imaginary = False
    #await ctx.send("You may use this application to solve any quadratic equation. I use the quadratic formula '(-b +- sqrt(b^2-4ac))/2a' to solve quadratics!")

    
    a = int(a)
    b = int(b)
    c = int(c)

    
    s1 = -b

    s2 = b**2

    s3 = int(4* a *c)

    s4 = s2 - s3

    s5 = 2 * a

    #await ctx.send("(-({}) +- sqrt(({})^2-4({})({})))/2({})".format(b,b,a,c,a))
                     
    #await ctx.send("({} +- sqrt({}-{}))/{}".format(s1,s2,s3,s5))

    s6 = s2 - s3

    #await ctx.send("({} +- sqrt({}))/{}".format(s1,s6,s5))

    try:
        s7 = math.sqrt(s6)
    except Exception:
        imaginary = True
        s7 = "sqrt({})".format(s6)
        print("divide by 0 1")
        #return()
      
    #await ctx.send("({} +- {})/{}".format(s1,s7,s5))

    if imaginary == True:
        s8 = "{}+{}".format(s1,s7)
    else:
        s8 = s1 + s7

      
    #await ctx.send("Solution 1:\n{}/{}".format(s8,s5))
      

    try:
        if imaginary == True:
            s9 = "{}/{}".format(s8,s5)
        else:
            s9 = s8/s5
    except ZeroDivisionError:
        imaginary == True
        print("divide by 0 2")
        s9 = "{}/{}".format(s8,s5)
        #return()

    #await ctx.send("x = {}".format(s9))

    if imaginary == True:
        s10 = "{}-{}".format(s1,s7)
    else:
        s10 = s1 - s7

    #await ctx.send("Solution 2:\n{}/{}".format(s10,s5))

    try:
        if imaginary == True:
            s11 = "{}/{}".format(s10,s5)
        else:
            s11 = s10/s5
    except ZeroDivisionError:
        imaginary = True
        print("divide by 0 3")
        s11 = "{}/{}".format(s10,s5)
        #return()

    



    #await ctx.send("x = {}".format(s11))
    solution = "(-({}) +- sqrt(({})^2-4({})({})))/2({})\n({} +- sqrt({}-{}))/{}\n({} +- sqrt({}))/{}\n({} +- {})/{}\nSolution 1:\n{}/{}\nx = {}\nSolution 2:\n{}/{}\nx = {}".format(b,b,a,c,a,s1,s2,s3,s5,s1,s6,s5,s1,s7,s5,s8,s5,s9,s10,s5,s11) 
    
    emb = discord.Embed(
        title = "Solving quadratic equation {}x² + {}x + {}".format(a,b,c),
        #description = solution,
        colour = 0x8cc43d,
        
        )
    if imaginary == True:
        emb.title = "Solving quadratic equation {}x² + {}x + {} - Error, imaginary number!".format(a,b,c)
        
    emb.add_field(name = "Solution 1", value = "Solution 1:\n{}/{}\nx = {}".format(s8,s5,s9), inline = True)
    emb.add_field(name = "Solution 2", value = "Solution 2:\n{}/{}\nx = {}".format(s10,s5,s11), inline = True)
    emb.add_field(name = "Method", value = "-({}) +- sqrt(({})^2-4({})({})))/2({})\n({} +- sqrt({}-{}))/{}\n({} +- sqrt({}))/{}\n({} +- {})/{}".format(b,b,a,c,a,s1,s2,s3,s5,s1,s6,s5,s1,s7,s5), inline = False)
    await ctx.send(embed = emb)

@quadratic.error
async def quadratic_error(err,ctx):
    
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send("Missing one or more arguments. Correct command format: `;quadratic [a] [b] [c]`")
    elif isinstance(err, commands.CommandInvokeError):
        await ctx.send("Looks like one of the arguments (a, b or c) is incorrect. Are they all integers (whole numbers)?")

@crdbot.command(pass_context=True)
async def cubic(ctx, a, b, c, d):

    imaginary = False

    
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)



    solution = "x = ³√(q + √(q² + (r - p²)³))  +  ³√(q - √(q² + (r - p²)³))  +  p\nwhere:\np = -b/3a\nq = p³ + (bc-3ad)/(6a²)\nr = c/3a\n"

    #find p

    solution = solution + "\np = -{}/3({})".format(b,a)

    p = -(b)/(3*a)

    solution = solution + "\np = {}\n".format(p)

    #find q

    solution = solution + "\nq = ({})³ + (({})({}) - 3({})({}))/(6({})²)".format(p,b,c,a,d,a)

    s0 = p**3

    s1 = b*c

    s2 = 3*a*d

    s3 = a**2

    solution = solution + "\nq = {} + ({}-{})/(6({}))".format(s0,s1,s2,s3)

    s4 = s1 - s2

    s5 = 6*s3

    solution = solution + "\nq = {} + {}/{}".format(s0,s4,s5)

    q = s0 + (s4/s5)

    solution = solution + "\nq = {}\n".format(q)

    #find r

    solution = solution +"\nr = {}/3({})".format(c,a)

    s6 = 3*a

    solution = solution + "\nr = {}/{}".format(c,s6)

    r = c/s6

    solution = solution + "\nr = {}\n".format(r)

    #solve for x

    solution = solution + "\nx = ³√({} + √(({})² + ({} - ({})²)³))  +  ³√({} - √(({})² + ({} - ({})²)³))  +  {}".format(q,q,r,p,q,q,r,p,p)

    s7 = q**2

    s8 = p**2
    
    #good luck, 19/3/2019

    solution = solution + "\nx = ³√({} + √({} + ({} - {})³))  +  ³√({} - √({} + ({} - {})³))  +  {}".format(q,s7,r,s8,q,s7,r,s8,p)

    s9 = r - s8

    s10 = s9**3

    await ctx.send(solution)

@crdbot.command()
async def rust(ctx):

    pimg = str(ctx.message.content)[6:len(str(ctx.message.content))]
    if ctx.message.mentions:
        print(ctx.message.mentions[0])
        avatar = ctx.message.mentions[0].avatar
        print("https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.mentions[0]))
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}".format(ctx.message.mentions[0])) as r:
                if r.status == 200:
                    file = await r.read()
                    #print(file)
                    with open("input.png", "wb") as f:
                        f.write(file)
    #if "http" in img:
        #urllib.request.urlopen(img)
        #image = urllib.read()
    #image = discord.Attachment()
    #image.save()
    #img = discord.File(image)
    #await ctx.send(img)
    #else:
     #   await crdbot.say("Didn't recognise an image.")
    else:
        await discord.Attachment.save(ctx.message.attachments[0],fp="input.png")
    rust = Image.open("rust.jpg").convert("RGBA")
    image = Image.new("RGBA",(800,600))
    inputy = Image.open("input.png").convert("RGBA")
    #inputy.hsl(60,100%,50%)
    print("input image size: {}x{}".format(inputy.width,inputy.height))
    #if inputy.width > 800 or inputy.height > 600:
    #new_inputy = inputy.resize((400,300), Image.ANTIALIAS)
    #elif inputy.width < 300 or inputy.height < 400:
    #    new_inputy = inputy.resize((400,300), Image.ANTIALIAS)

    #else:
    #    new_inputy = inputy
        
    inputylist = []
    data = inputy.getdata()

    for pixel in data:
        if (pixel[0] != 167 and pixel[1] != 167 and pixel[2] != 167) or (pixel[0] != 255 and pixel[1] != 255 and pixel[2] != 255):
            if pixel[0] > 165:
                pixel[0] == 165
            if pixel[1] > 210:
                pixel[1] == 210
                                    
            inputylist.append(((pixel[0]+45),(pixel[1]+30),(pixel[2])))#,150))
        else:
            inputylist.append((255,255,255,0))

        #inputy.putdata(inputylist)
            

   
    inputy.putdata(inputylist)
    
    inputy.save("temp.png")    
    
    image.paste(inputy,box=((int(400-(inputy.width/2)),int(300-(inputy.height/2)))))
    data = rust.getdata()
    out = []

    for pixel in data:
        if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
            out.append((255,255,255,0))
        else:
            out.append(pixel)
            
    rust.putdata(out)
    new_image = Image.alpha_composite(rust,image)
    new_image.save("out.png")
    newfile = discord.File("out.png")
    await ctx.send(file = newfile)
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(img) as r:
            
            #js = await r.json()
            await ctx.send(r)#js['file'])
    '''

@crdbot.command()
async def userinfo(ctx):
    om1 = False
    userid = ctx.message.content[10:len(ctx.message.content)]
    if "-om1" in userid:
        if str(ctx.message.author.id) == "186069912081399808":
            userid = userid[6:len(userid)]
            om1 = True
        else:
            await ctx.send("Nope.")
        
    if ctx.message.mentions:
        user = ctx.message.mentions[0]

    
    elif userid:
        user = ctx.guild.get_member(int(userid))
        print(user)

    else:
        user = ctx.message.author


    #get activity
    if om1 == True:
        messages = await ctx.message.channel.history(limit=10000).flatten()
    else:
        messages = await ctx.message.channel.history(limit=1000).flatten()
    messageCount = 0
    for message in messages:
        if message.author == user:
            messageCount = messageCount + 1
    if om1 == True:
        activity = messageCount/100
    else:
        activity = messageCount/10
    
    rolestring = "\n"
    for role in user.roles:
        rolestring = rolestring + str(role.mention) + "\n"

    #delta =  
    emb = discord.Embed(title = "{}".format(user),
    type = "rich",
    description = "**Account Creation Date**: {} ({} days ago)\n**Join Date**: {} ({} days ago)\n**Roles**: {}\n**Activity** (your messages per 1000 messages in this channel): {}%\n".format(
    (str(discord.utils.snowflake_time(user.id)).replace(" "," at "))[0:19] + " (UTC+0)",
    str((datetime.datetime.utcnow() - discord.utils.snowflake_time(user.id)).days),
    (str(user.joined_at)).replace(" "," at ")[0:19] + " (UTC+0)",
    str((datetime.datetime.utcnow() - user.joined_at).days)[0:19],
    rolestring,
    activity
    ),
    colour = user.color#0x8cc43d,

    #url = "output.p,
    )
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}".format(user)) as r:
            if r.status == 200:
                file = await r.read()
                #print(file)
                with open("input.png", "wb") as f:
                    f.write(file)                        
    #print("ok")
    emb.set_thumbnail(url="attachment://input.png")
    f = discord.File("input.png", filename="input.png")
    await ctx.send(embed=emb, file=f)
    '''


        emb.set_image(url="attachment://output.png")
        f = discord.File("output.png", filename="output.png")
        endTime = int(round(time.time() * 1000))
        emb.description = "Response time: {}ms\nImage generation time: {}ms".format(endTime-startTime,L2Presponsetime)
        await ctx.send(file=f,embed=emb)
    '''
    
@crdbot.command()
async def order(ctx):
    item = ctx.message.content.lower()
    item = item[7:len(item)]
    if "@everyone" in item or "@here" in item or "enoyreve@" in item or "ereh@" in item:
        #["@everyone","@here","enoyreve@","ereh@"]:
        await ctx.send("You are not funny.")
        return
    elif "beebot" in item:
        await ctx.send("Nope.")
    
    elif str(ctx.message.channel.id) == "492400161864286228" or str(ctx.message.channel.id) == "533006206025859082":
        #item = str(ctx)[6:len(str(ctx))]
        responses = ["I'm not serving that.",
                     "Seriously? {}? {}??".format(item,item.upper()),
                     "{}? More like {}. I'm not serving you that.".format(item,item[::-1]),
                     "Alright *Sir or Madam*, here's your stinking {}. I hope you choke.".format(item),
                     "Enjoy your {}. I won't.".format(item),"Here's your {}.".format(item),
                     "Alright you filthy fascist, here's your {}.".format(item),
                     "I really hope you enjoy your {}.".format(item),
                     "We don't serve {} here. Go away, don't come back.".format(item),
                     "Stop wasting my time.",
                     "BEEBOT would strike me down in my sleep if I served you {}. Please don't order that ever again.".format(item),
                     "Take your {}.".format(item),
                     "Go away and never come back, please. If you seriously consume {} I'd probably have nightmares.".format(item),
                     "Just who do you think you are, {}, trying to order {} from MY pub??!".format(ctx.message.author.mention,item),
                     "Get out of here before I personally deposit you into the Anthill to be consumed.",
                     "No.",
                     "How about you try something else instead.",
                     "I'd recommend the fish and chips here. They're really nice. But if you insist, I'll go and fetch your {}.".format(item),
                     "You want me to serve *you* {}? Over my dead body.".format(item),
                     "It's not happening.",
                     "Okay, here's your freshly prepared {}. Enjoy.".format(item),
                     "Why are you still doing this? Stop already. If you're trying to stress my processors I'm not even using 1% of my CPU's resources.",
                     "Stop.",
                     "Please, leave me alone. I have better things to be doing.",
                     "...okay. I'll prepare the {}.".format(item),
                     "Oh, I haven't served {} for a while. This will be interesting.".format(item),
                     "{} is a specialty of mine. I hope you enjoy.".format(item),
                     "Of all the things you could order, you want me to serve you {}?!".format(item),
                     "I cannot understand why on earth you'd want {}. But I'll get it for you anyway.".format(item),
                     "I swear to SPIDERBEE, I will smash your puny face in when nobody is looking.",
                     "**NO.**"

                     ]
        

        await ctx.send(random.choice(responses))
                   
@crdbot.command()             
async def purge(ctx,num):
    if str(ctx.message.author.id) in open("adminlist.txt").read():

        try:
            num = int(num)
            if num < 1:
                await ctx.send("Error, your input was less than 1.")
                return

            await ctx.message.channel.purge(limit = num+1)
        except ValueError:
            await ctx.send("Error, your input was not a number.")
        except discord.errors.Forbidden:
            try:
                await ctx.send("Error, I do not have the permissions to perform this command.")
            except discord.errors.Forbidden:
                print("Unable to send messages in {0.message.channel.name}, server {0.message.server.name}!".format(ctx))

@purge.error
async def purge_error(err,ctx):
    
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send("Missing an argument. Correct command format: `;purge [x]`")

@crdbot.command()
async def setstatus(ctx,statType):
    if ctx.message.author.id == '186069912081399808':
        statType = int(statType)
        if statType < 0:
            await ctx.send("It doesn't work like that.")
            return()
        playgame = ctx.message.content[12:len(ctx.message.content)]
        await crdbot.change_presence(activity=discord.Game(type=statType, name=playgame))
        await ctx.send("ok")
# url = "https://www.twitch.tv/Crdguy",
@setstatus.error
async def setstatus_error(err,ctx):
    
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.message.channel.send("Missing an argument. Correct command format: `;setstatus [0 - 3] [game]`")
    else:
        await ctx.message.channel.send("oh no")
        
@crdbot.command()
async def role(ctx,role):
    a = 0


'''
@crdbot.event
async def on_command_error(err,ctx):
    if isinstance(err, commands.CommandNotFound):
        await ctx.send("Didn't recognise that.")
    if isinstance(err, commands.InvalidArgument):
        await ctx.send("o")
    
    #await crdbot.send_message(ctx.message.channel, ctx.message.content)
    #await crdbot.send_message(ctx.message.channel,"yikes, {}".format(err))
    #print(err)

    #if err == MissingRequiredArgument:
    #    await ctx.send("gotcha")

    a = 0

'''


@crdbot.command(pass_context=True)
async def ehlookup(ctx):
    startTime = int(round(time.time() * 1000))
    fast = False
    superfast = False
    nolayout = False
    ultrafast = False
    breakcode = False
    
    ship = ctx.message.content.lower()
    if "-fast" in ship:
        ship = ship[16:len(ship)]
        fast = True
    elif "-superfast" in ship:
        ship = ship[21:len(ship)]
        superfast = True
    elif "-ultrafast" in ship:
        ship = ship[21:len(ship)]
        ultrafast = True
    elif "-nolayout" in ship:
        ship = ship[20:len(ship)]
        nolayout = True
    else:
        ship = ship[10:len(ship)]
        
    if ship == "imperium":
        print(ctx.message.author.id)
        if str(ctx.message.author.id) != "186069912081399808":
            await ctx.send("Sorry, can't have that.")
            return
        


    def getShipClass(file):
        
        with open("shiplookuptable.csv") as lookuptableraw:
            lookuptable = csv.reader(lookuptableraw, delimiter=",")
            
            for row in lookuptable:
                if file == row[0]:
                    file = "Database/Ship/"+row[1]
                else:
                    file = file
              
            with open(file) as jsonfile:
                content = json.load(jsonfile)
                try:
                    raw = content["SizeClass"]
                except KeyError:
                    raw = "NaN"
                    
            if raw == 1:
                sclass = "Destroyer"
            elif raw == 2:
                sclass = "Cruiser"
            elif raw == 3:
                sclass = "Battleship"
            elif raw == 4:
                sclass = "Capital Ship"
            elif raw == 5:
                sclass = "Drone"
            else:
                sclass = "Frigate"

        return sclass

    def getDesc(file):
        
        with open("shiplookuptable.csv") as lookuptableraw:
            lookuptable = csv.reader(lookuptableraw, delimiter=",")
            
            for row in lookuptable:
                if file == row[0]:
                    return row[2]

    def getLayout(file):
        
        with open("shiplookuptable.csv") as lookuptableraw:
            lookuptable = csv.reader(lookuptableraw, delimiter=",")
            
            for row in lookuptable:
                if file == row[0]:
                    file = "Database/Ship/"+row[1]
                else:
                    file = file
                    
            with open(file) as jsonfile:
                content = json.load(jsonfile)
                layout = content["Layout"]
            return layout

    def getWorkshopLevel(file):

        with open("techlookuptable.csv") as lookuptableraw:
            lookuptable = csv.reader(lookuptableraw, delimiter=",")
            
            for row in lookuptable:
                if file == row[0]:
                    file = "Database/Technology/"+row[1]
                else:
                    file = file


        try:            
            with open(file) as jsonfile:
                content = json.load(jsonfile)
                dependencies = content["Dependencies"]

        except FileNotFoundError:
            return "???"
        
        found = False
        contents = []
        try:
            workshoplevel = content["Price"]
        except KeyError:
            workshoplevel = 0
        
        while len(dependencies) > 0:
            for f in glob("Database/Technology/*.json"):
                with open(str(f)) as file:
                    data = json.load(file)
                    x = 0
                    
                    while x != len(dependencies):
                        if dependencies:
                            if x > len(dependencies)-1:
                                x = 0

                            if data["Id"] == dependencies[x]:

                                del dependencies[x] 
                                if len(data["Dependencies"]) > 0:
                                    x = -1
                                    dependencies = dependencies + data["Dependencies"]
                                    workshoplevel = workshoplevel + int(data["Price"])
                                else:
                                    try:
                                        workshoplevel = workshoplevel + data["Price"]
                                    except KeyError:
                                        workshoplevel = "NaN"
                                        return workshoplevel
                        if dependencies:
                            x = x + 1

        return workshoplevel
                
    def layout2png(file):

        L2PstartTime = int(round(time.time() * 1000))
        rgbinput = []
        x = 0
        list = []
        n = 0
        layoutlist = []
        layout = getLayout(file)
        if ctx.message.attachments:
            if len(layout) > 65535:
                
                breakcode = True
                return
            
        #gets image size given the size of any layout is always a square
        size = int(math.sqrt(len(layout)))

        image = Image.new("RGBA", (size,size))

        while n != len(layout):
            layoutlist.append(layout[int(n):int(n+size)])
            n = n + size    

        #convert to RGB
        while x != size:
            y = 0
            while y != size:
                working = int(layoutlist[x][y])
                if working == 0:
                    rgbinput.append((255,255,255,0))
                if working == 1:
                    rgbinput.append((0,0,255))
                elif working == 2:
                    rgbinput.append((0,255,0))
                elif working == 3:
                    rgbinput.append((0,255,255))
                elif working == 4:
                    rgbinput.append((255,0,0))
                elif working == 5:
                    rgbinput.append((255,255,0))
                
                y = y + 1
            x = x + 1

        image.putdata(rgbinput)

        #resize and draw pixel grid


        if ultrafast == True:
            image.save("output.png")
            L2PendTime = int(round(time.time() * 1000))
            L2Presponsetime = L2PendTime - L2PstartTime
            return layoutlist,L2Presponsetime

        new_image = image.resize(((59*image.width),(59*image.width)))
        
        if superfast == True:
            new_image.save("output.png")
            L2PendTime = int(round(time.time() * 1000))
            L2Presponsetime = L2PendTime - L2PstartTime
            return layoutlist,L2Presponsetime
        
        x = 0
        y = 0
        increment = (59*image.width)/image.width
        
        if fast == True:
            #draws columns
            while x < new_image.width:
                while y < new_image.width:
                    line = [(x,0),(y,new_image.width)]
                    draw = ImageDraw.Draw(new_image)
                    draw.line(line,fill=0)
                    x = x + increment
                    y = y + increment
                    del draw

            #draws rows
            x = 0
            y = 0
            while x < new_image.width:
                while y < new_image.width:
                    line = [(0,y),(new_image.width,y)]
                    draw = ImageDraw.Draw(new_image)
                    draw.line(line,fill=0)#,width=60)
                    x = x + increment
                    y = y + increment
                    del draw
            new_image.save("output.png")
            L2PendTime = int(round(time.time() * 1000))
            L2Presponsetime = L2PendTime - L2PstartTime
            return layoutlist,L2Presponsetime            
    
        x = 1
        y = 1
        
        temp = Image.open("Tiles/0.png")
        nullSlot = temp.resize((int(increment),int(increment)))      
        temp = Image.open("Tiles/1.png")
        blueSlot = temp.resize((int(increment),int(increment)))  
        temp = Image.open("Tiles/2.png")
        greenSlot = temp.resize((int(increment),int(increment)))
        temp = Image.open("Tiles/3.png")
        greenblueSlot = temp.resize((int(increment),int(increment)))
        temp = Image.open("Tiles/4.png")
        redSlot = temp.resize((int(increment),int(increment)))
        temp = Image.open("Tiles/5.png")
        yellowSlot = temp.resize((int(increment),int(increment)))

        canvas = Image.new("RGBA", ((59*image.width),(59*image.width)))
        
        while x < new_image.width:
            while y < new_image.width:
                roundy = (round(x),round(y))
                intman = (int(x),int(y))
                (r, g, b, a) = new_image.getpixel((x,y))
                #print(r,g,b)
                if (r,g,b,a) == (255,255,255,0):
                    canvas.paste(nullSlot,intman)
                if (r,g,b) == (0,0,255):
                    canvas.paste(blueSlot,intman)
                elif (r,g,b) == (0,255,0):
                    canvas.paste(greenSlot,intman)
                elif (r,g,b) == (0,255,255):
                    canvas.paste(greenblueSlot,intman)
                elif (r,g,b) == (255,0,0):
                    canvas.paste(redSlot,intman)
                elif (r,g,b) == (255,255,0):
                    canvas.paste(yellowSlot,intman)
        

                y = y + increment
            y = 1
            x = x + increment

        canvas.save("output.png","PNG")
        L2PendTime = int(round(time.time() * 1000))
        L2Presponsetime = L2PendTime - L2PstartTime
        return layoutlist,L2Presponsetime

    def getdata(file):

        #content here is the ship build in plain text, and "raw" is the layout in list form (not used) 
        content = getLayout(file)
        notempty = len(content)-int(content.count("0"))

        #calculate some things
        hp = notempty*0.5
        baseweight = notempty*20
        minweight = int(baseweight/2)

        if getShipClass(file) == "Capital Ship":
            cost = 15*notempty**2
        else:
            cost = 5*notempty**2
        sclass = getShipClass(file)
        

        with open("shiplookuptable.csv") as lookuptableraw:
            lookuptable = csv.reader(lookuptableraw, delimiter=",")
            
            for row in lookuptable:
                if file == row[0]:
                    file = "Database/Ship/"+row[1]
                else:
                    try:
                        raw = int(content["ShipCategory"])
                    except:
                        raw = "???"
                
            with open(file) as jsonfile:
                content = json.load(jsonfile)
                try:
                    raw = int(content["ShipCategory"])
                except KeyError:
                    raw = 0
                    
        if sclass == "Frigate":
            satclass = "Light"
        elif sclass == "Destroyer":
            satclass = "Medium"
        elif sclass == "Cruiser" or sclass == "Battleship":
            satclass = "Heavy"
        elif sclass == "Capital Ship":
            satclass = "Capital Ship"
        else:
            satclass = "NaN"
            
        #calculate star cost  
        if raw == 1:
            #rare
            stars = round(cost/6000)
        elif raw == 2:
            #flagship
            stars = int(hp/5)
        elif raw == 3:
            #special
            stars = "???"
        elif raw == 4:
            #starbase
            stars = "???"
        elif raw == 5:
            #hidden
            stars = "???"
        elif raw == 6:
            #drone
            stars = "???"
        else:
            #common
            stars = int(cost/48000)
            
        return sclass,satclass,hp,baseweight,minweight,cost,stars

    if ship == "-myfile":
        if ctx.message.attachments:
            await ctx.send("Processing!")
            await discord.Attachment.save(ctx.message.attachments[0],fp="file.json")
            file = "file.json"
            if nolayout == False:
                try:
                    layout,L2Presponsetime = layout2png(file)
                except:
                    if breakcode == True:
                        await ctx.send("Sorry, this ship is too big. Try a ship with dimensions less than 256x256.")
                        layout = 0
                        L2Presponsetime = 0
            
            sclass,satclass,hp,baseweight,minweight,cost,stars = getdata(file)
            emb = discord.Embed(title = "Database Modded Ship",
            type = "rich",
            colour = 0x8cc43d,
            )
            emb.set_image(url="attachment://output.png")
            f = discord.File("output.png", filename="output.png")
            emb.add_field(name = "Ship Information", value = "**Ship Class**: {}\n**Satellite Class**: {}\n**Hitpoints**: {}\n**Base Weight**: {}\n**Minimum Weight**: {}\n\n**Cost** (if applicable): {}\n**Star Cost**: {}".format(sclass,satclass,hp,baseweight,minweight,cost,stars,), inline = True)
            endTime = int(round(time.time() * 1000))
            try:
                emb.description = "Response time: {}ms\nImage generation time: {}ms".format(endTime-startTime,L2Presponsetime)
            except UnboundLocalError:
                emb.description = "Response time: {}ms\nThis ship is greater than 256x256 - no image.".format(endTime-startTime)
                await ctx.send(embed=emb)
                return
            await ctx.send(embed=emb,file = f)

        else:
            await ctx.send("Correct syntax: `;ehlookup [ship name]`. You can also upload a .json to see its information.")
        return


    sclass,satclass,hp,baseweight,minweight,cost,stars = getdata(ship)
    #try:
    if nolayout == False:
        layout,L2Presponsetime = layout2png(ship)
    #except discord.HTTPException:
    #    pass
    workshop = getWorkshopLevel(ship)
    desc = getDesc(ship)
    #await ctx.send("Ship class: {}\nSattelite class:{}\nHitpoints:{}\nBase weight:{}\nMinimum weight: {}\nCost:{}\nStar cost: {}\nWorkshop level:{}\n\nDescription: {}".format(sclass,satclass,hp,baseweight,minweight,cost,stars,workshop,desc))
    
    emb = discord.Embed(title = ship.capitalize(),
    type = "rich",
    colour = 0x8cc43d,
    )
    emb.add_field(name = "Ship Information", value = "**Ship Class**: {}\n**Satellite Class**: {}\n**Hitpoints**: {}\n**Base Weight**: {}\n**Minimum Weight**: {}\n\n**Cost** (if applicable): {}\n**Star Cost**: {}\n**Workshop Level**: {}\n\n**Description**: {}".format(sclass,satclass,hp,baseweight,minweight,cost,stars,workshop,desc), inline = True)
    #emb.set_thumbnail(url = "file://output.png")

    
    if nolayout == False:
        emb.set_image(url="attachment://output.png")
        f = discord.File("output.png", filename="output.png")
        endTime = int(round(time.time() * 1000))
        emb.description = "Response time: {}ms\nImage generation time: {}ms".format(endTime-startTime,L2Presponsetime)
        await ctx.send(file=f,embed=emb)
    else:
        endTime = int(round(time.time() * 1000))
        emb.description = "Response time: {}ms".format(endTime-startTime)
        await ctx.send(embed=emb)

@ehlookup.error
async def ehlookup_error(ctx,err):
    
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send("Missing one or more arguments. Correct command format: `;ehlookup [ship]`. Do `;help ehlookup` for more information.")
    elif isinstance(err, commands.CommandInvokeError):
        await ctx.send("I did not recognise the option or ship you specified. Do `;help ehlookup` for more information.")


@crdbot.event
async def on_message(message):
    
    
    if crdbot.user.mention in message.content:
        helpmsg = "ello {}, I am Stratos. To see my commands, do `;help`.".format(message.author.mention)
        with open("ping.txt","r") as file:
            content = file.read()
            content = int(content)
                        
        if content < 3:
            await message.channel.send("H"+helpmsg)
        elif content < 5:
            await message.channel.send("...h" + helpmsg)
        elif content < 6:            
            await message.channel.send("I will strike you down. Stop pinging me unless you mean it.")
        elif content < 10:
            await message.channel.send("How many times? Stop pinging me, you scum.")
        elif content == 10:
            await message.channel.send("**YOU INSOLENT LITTLE RODENT. I WILL FIND YOU WHEN YOU'RE ASLEEP AND BREAK YOUR SKULL IN.**")
        elif content == 11:
            await message.channel.send("**I HAVE BEEBOT AT SLEIGHT OF HAND. DON'T MAKE ME RELEASE HIM.**")
            content = 0
        else:
            content = 0
        with open("ping.txt","w") as file:
            content = content + 1
            file.write(str(content))

    if crdbot.user.mention not in message.content:
        chance = random.randint(1,12)
        if chance == 1:
            with open("ping.txt","w") as file:
                content = 0
                file.write(str(content))            

    if str(message.content).startswith('cmd'):
        if message.author.id == '186069912081399808':
            try:
                await crdbot.delete_message(message)
                c = input("Crdbot experimental console opened. Type 'help' for all commands. Note that commands here will only apply to the channel 'console' was typed in!")
                if c == 'speak':
                    y = 0
                    while 1:
                        x = input("Enter what I should say.")
                        await crdbot.send_message(message.channel, x)
                        y = input("Should I stop?")
                        if y == "yes":
                            return()
                if c == 'exit':
                    return()
                if c == 'sd':
                    print("Sayonara.")
                    await crdbot.logout()
                if c == 'forcesd':
                    exit()
                if c == 'help':
                    print("Current commands: speak (type a message), exit (close console), sd (shut down bot), forcesd (aggressively shut down), help (displays this message")
                else: 
                    print("Command unrecognised! Exiting experimental console.")
            except Exception:
                a = 0

                
    if message.content.startswith(";leave"):
        if message.author.id == '186069912081399808':
            servertl = crdbot.get_server(message.server.id)
            await message.channel.send("Really leave server? (check command line)")
            leave = input("Are you sure you want to leave?")
            if "y" in leave:
                print("Okay. Leaving server {}...".format(servertl))
                await message.channel.send("Goodbye, {}.".format(servertl))
                await crdbot.leave_server(servertl)
            else:
                print("Alright.")
                await message.channel.send("Aborted.")
        else:
            await message.channel.send("That's a bit rude, isn't it?")


    await crdbot.process_commands(message) 

#invite:        https://discordapp.com/api/oauth2/authorize?client_id=557309788480864256&permissions=1543957590&scope=bot
crdbot.run(token)
