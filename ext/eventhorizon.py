from discord.ext import commands
import discord
import asyncio
import csv
import time
import json
import math
from PIL import Image, ImageDraw, ImageFont
import PIL
import configparser
from glob import glob
import gspread
from oauth2client.service_account import ServiceAccountCredentials#
import time
import shutil

#google api stuff
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gapi client secret.json', scope)
gcrdbot = gspread.authorize(creds)
gcrdbot.login()

try:
    config = configparser.ConfigParser()
    config.read('stratos.ini')

except Exception:
    input("Error, something went wrong while parsing 'stratos.ini'. Ensure the file is not corrupt or missing.")
    exit(0)

class StaffTools(commands.Cog):
    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.command()
    async def rslookup(self, ctx, user):
        gcrdbot.login()
        roles = list(ctx.message.author.roles)
        whitelist = [294513095152238592,408368843568971776,294512708613832704,592028643044229150,294512832190349312]

        good = False

        for role in roles:
            for wrole in whitelist:
                #print("is {} == {}".format(str(wrole),str(role.id)))
                if str(wrole) in str(role.id):
                    good = True
                    break

        if good == False:
            await ctx.send("Sorry, you do not have permission to execute this command.")
            return

        database = gcrdbot.open("Event Horizon Administration Log").get_worksheet(0)
        databaseList = database.get_all_values()

        found = False
        instances = []

        for row in databaseList:
            try:
                if str(user) == row[1] or str(user) == row[2]:
                    found = True
                    foo = {

                        "Timestamp": row[0],
                        "User": row[1],
                        "User's ID": row[2],
                        "Restricted By": row[3],
                        "Channel": row[4],
                        "Action": row[5],
                        "Strike": row[6],
                        "Reason": row[7],
                        "Proof": row[8],
                        "Comments": row[9],



                        }
                    instances.append(foo)

            except:
                pass

        if found == False:
            await ctx.send("No entries found in the database for the user you specified.")
            return



        #format data

        for entry in instances:
            maxstrike = 0
            if entry["Strike"] == "No strikes":
                pass
            elif int(entry["Strike"]) > maxstrike:
                maxstrike = int(entry["Strike"])


        emb = discord.Embed(title = user,
        type = "rich",
        description = "{} is currently on strike {}.".format(user,maxstrike),
        colour = 0x8cc43d,
        )

        for entry in instances:
            emb.add_field(name = "Entry on {}".format(entry["Timestamp"]), value =
                          "**Username**:\n{} (**ID**: {})\n\n**Channel**:\n{}\n\n**Action**:\n{}\n\n**Restricted By**:\n{}\n\n**Reason**:\n{}\n\n**Proof**:\n{}\n\n"
                          .format(entry["User"],entry["User's ID"],entry["Channel"],entry["Action"],entry["Restricted By"],entry["Reason"],entry["Proof"]), inline = True)
        await ctx.send(embed = emb)


        print(instances)

    @commands.command()
    async def file(self, ctx, user, channel, action, strike, reason, proof, *comment):
        '''
        1.0.0
        Filing command for Event Horizon staff as an alternative to the form.
        Usage: ;file [user] [channel] [action] [strike] [reason] [proof] (optional: comment - anything after the required arguments will be counted as a comment.
        `user` should be a mentioned user or an ID.
        `channel` should be a mentioned channel.
        `action` should be any of the following: "quarantine", "verbal warning", "purge", "role removal", "kick" or "ban". You can also use "q", "w", "p", "r", "k" or "ban" respectively as shorthand.
        `strike` is the number of strikes the user is now on, from 0 to 4.
        `reason` is a short sentence describing why the user was punished. Please give reasons longer than a sentence in quotations like this: "Spam in #general"
        `proof` should be a url to a screenshot that has evidence of the offending act. Avoid using Discord's CDN here because the links to the image will expire in 2 years. Use Imgur or Gyazo instead, or anything similar.
        '''

        gcrdbot.login()
        roles = list(ctx.message.author.roles)
        whitelist = [294513095152238592,408368843568971776,294512708613832704,592028643044229150,294512832190349312]


        #test inputs to make sure they are correct

        #user - must be mentioned or id


        #start by assuming "user" is a mentioned member
        print(user)
        try:
            user_id = int(user[3:len(user)-1])
            member = await self.crdbot.fetch_user(int(user_id))

        except:
            #await ctx.send("Error, the `user` argument is malformed. Please try again by instead mentioning a user or providing an ID.\nIt is also possible you are trying to file a user that is banned or has left. If this is the case, please instead use the form.")
            #return
            member = None

        #print(member.id)
        #member = ctx.guild.get_member(member_id)
        print(member)
        if member == None:
            #now we know that "user" is not a mentioned user
            member = await self.crdbot.fetch_user(int(user))

            '''
            try:
                member_id = int(user)
                print(member_id)
            except:
                await ctx.send("Error, the `user` argument is malformed. Please try again by instead mentioning a user or providing an ID.\nIt is also possible you are trying to file a user that is banned or has left. If this is the case, please instead use the form.")
                return
            #print(member_id)
            member = ctx.guild.get_member(member_id)
            '''
        try:
            #sanity check for if a discord.Member object has been created
            foo = member.id

        except:
            await ctx.send("Error, the `user` argument is malformed. Please try again by instead mentioning a user or providing an ID.\nIt is also possible you are trying to file a user that is banned or has left. If this is the case, please instead use the form.")
            return

        #channel - must be mentioned, could have added stuff allowing for filing by id but who tf would use that lmao

        channel2_id = int(channel[2:len(channel)-1])
        #print("id:"+str(channel2_id))
        channel2 = self.crdbot.get_channel(channel2_id)
        #print(channel2)
        try:
            if isinstance(channel2, discord.TextChannel):
                channel = channel2
                #print("YEAH")
        except:
            await ctx.send("Error, the `channel` argument is malformed. Please check it is a correctly mentioned channel that I have access to.")
            return
        #print(channel)
        #print(channel.id)

        #action - should be any of these: "quarantine", "warning", "purge", "role removal", "kick" or "ban".

        if action.lower() not in ["quarantine","verbal warning","purge","role removal","kick","ban","q","w","p","r","k","b"]:
            await ctx.send('Error, the `action` argument was not provided correctly. It should be one of the following: "quarantine", "verbal warning", "purge", "role removal", "kick" or "ban". Alternatively, you can also use "q", "w", "p", "r", "k" or "b" respectively as shorthand.')
            return
        if action.lower() == "q":
            action = "quarantine"
        elif action.lower() == "w":
            action = "verbal warning"
        elif action.lower() == "p":
            action = "purge"
        elif action.lower() == "r":
            action = "role removal"
        elif action.lower() == "k":
            action = "kick"
        elif action.lower() == "b":
            action = "ban"

        print(action)


        #strike - should be integer from 0 to 4
        try:
            if int(strike) not in [0,1,2,3,4]:
                await ctx.send("Error, the `strike` argument is malformed. It should be a number from 0 to 4. Be sure to check what strike a user is using ;rslookup or the spreadsheet.")
                return
        except:
            await ctx.send("Error, the `strike` argument is malformed. It should be a number from 0 to 4. Be sure to check what strike a user is using ;rslookup or the spreadsheet.")
            return
        #reason - should be a string.. no need for verification here, we will just assume the user isn't a dumbass which is potentially dangerous

        #proof - should contain a url. blacklist discord urls because they expire after 2 years

        if "cdn.discordapp.com" in proof:
            await ctx.send("Sorry, but Discord CDN links expire after 2 years and are considered unreliable. Use something like Gyazo or Imgur for your proof, and try again.")
            return
        if "http" not in proof:
            await ctx.send("Sorry, but your proof does not look like a valid url. Check it and try again.")
            return

        #comment - see if one exists, if not add a funny thing

        try:
            print(comment[0])
        except:
            comment = ["Filed using Stratos!"]


        #if code gets to this point verification has passed and we can now file the contents to the spreadsheet
        print("A")


        #check they have one of the whitelisted moderator roles

        good = False

        for role in roles:
            for wrole in whitelist:
                if str(wrole) in str(role.id):
                    good = True
                    break

        if ctx.message.author.id == 186069912081399808:
            good = True
            #so I can always run this command
        print("B")
        if good == False:
            await ctx.send("Sorry, you do not have permission to execute this command.")
            return


        database = gcrdbot.open("Event Horizon Administration Log").get_worksheet(0)
        databaseList = database.get_all_values()
        print("C")
        for thing in [
            member,
            member.id,
            ctx.message.author.name,
            "#"+channel.name,
            action.capitalize(),
            strike,
            reason,
            proof,
            comment[0]
            ]:
            print(thing)
        print("BUM")

        msg = await ctx.send("Ready to file the following information to the spreadsheet:\n**Restricted user's name:** {}\n**Restricted user's ID:** {}\n**Your Discord name:** {}\n**What channel did the restriction occur in:** {}\n**Action taken:** {}\n**Strike:** {}\n**Reason:** {}\n**Proof:** {}\n**Comment:** {}\n\nIf this information is correct, please react with <:epic:730435572396458014> to confirm, otherwise wait 30 seconds for this to timeout.".format(member,member.id,ctx.message.author.name,"#"+channel.name,action.capitalize(),strike,reason,proof,comment[0]))
        print("D")
        await msg.add_reaction("<:epic:730435572396458014>")

        def usertest(reaction, reactor):
            return reactor == ctx.message.author and str(reaction.emoji) == "<:epic:730435572396458014>"

        try:
            reaction, reactor = await self.crdbot.wait_for("reaction_add", timeout=60.0, check = usertest)
        except asyncio.TimeoutError:
            await ctx.send("Message timed out.")
            return

        await ctx.send("Confirmed, now filing!")


        #deal with timestamp

        '''
        thetime = list(datetime.datetime.now())
        
        if len(str(thetime.day)) == 1:
            thetime.day = "0"+str(thetime.day)
        if len(str(thetime.month)) == 1:
            thetime.month = "0"+str(thetime.month)
        if len(str(thetime.hour)) == 1:
            thetime.hour = "0"+str(thetime.hour)
        if len(str(thetime.minute)) == 1:
            thetime.minute = "0"+str(thetime.minute)
        if len(str(thetime.second)) == 1:
            thetime.second = "0"+str(thetime.second)
            
        for item in thetime:
            item = str(item)
        '''

        database.insert_row([
            #"{0.day}/{0.month}/{0.year} {0.hour}:{0.minute}:{0.second}".format(thetime),
            time.strftime("%d/%m/%Y %H:%M:%S"),
            str(member),
            str(member.id),
            ctx.message.author.name,
            "#"+channel.name,
            action.capitalize(),
            strike,
            reason,
            proof,
            comment[0]
            ],len(database.get_all_values())+1)

        await ctx.send("Done! You may want to check your entry on the spreadsheet: https://docs.google.com/spreadsheets/d/1jWRRDUrqqpURZEwiFp1Ue64nHOqO6ieRekaIskzUWCc")
    '''
    @file.error
    async def file_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Error, you are missing one of the key arguments. Refer to ;help file for more information.")
        else:
            await ctx.send("OOPSIE WOOPSIE, I MADE A FUCKY WUCKY UWU")
    '''

class RustMemeFunny(commands.Cog):
    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.Cog.listener()
    async def on_message(self, message):

        if ";rw" in message.content:
            if True:# message.channel.id in [294514668699910145,304707849055895563,407264987883503618,368110030198800396]:
                emb = discord.Embed(
                title = "**Rusted Warfare**",
                type = "rich",
                description = "Rusted Warfare is an RTS inspired by classic real-time strategy games with modern tech.\n\n-**Built for Large Battles**\n-Over 50 unique units with many upgrades\n-Optimised multi-core engine easily handles battles of 1000's of units.\n-Experimental units for the big late-game battles\n-Infinite zoom to view and issue commands across the whole battlefield\n-Create your own battles and scenarios in the sandbox editor then play them in multiplayer\n\n-**Modern Multiplayer**\n-Host your own game or play on the dedicated servers\n-Reconnect to disconnected multiplayer games\n-Steam friend matchmaking\n-Save and load multiplayer games for the quick lunch time battle\n-Enable shared unit control between allies.\n-Watch recorded multiplayer replays and save at any point to start playing from\n-Full cross-platform multiplayer between the Windows, Linux and Android versions\n\n\n**Get it now!**\nSteam: https://store.steampowered.com/app/647960/\nGoogle Play: https://play.google.com/store/apps/details?id=com.corrodinggames.rts&hl=en_GB",
                colour = 0xc26705,
                )
                emb.set_thumbnail(url="https://steamcdn-a.akamaihd.net/steam/apps/647960/header.jpg")

                await message.channel.send(embed=emb)

    @commands.command()
    async def colossus(self, ctx):
        '''
        Version: 1.0.0
        An embed Estrect made to promote colossus.xxx.
        Takes no arguments.
        '''

        embed=discord.Embed(title="COLOSSUS.XXX installer download", url="https://cdn.discordapp.com/attachments/551002345211691009/714486636855033887/Release.zip", description="YO, ARE YOU LOOKING FOR LEGIT EH HACKS.XXX 200% FREE VIRUS? THEN YOU ARE ON THE RIGHT PLACE, COLOSSUS.XXX HAS ALL THE HACKS AND ALL THE CHEATS TO UP YOUR GAME, DO YOU LACK THE STARS? COLOSSUS.XXX CAN HELP YOU? DO YOU WANT FREE SHIPS.XXX? COLOSSUS.XXX IS JUST FOR YOU, GO AHEAD AND DOWNLOAD IT NOW TO UP YOUR GAME", color=0x00ff00)
        embed.set_author(name="COLOSSUS.XXX")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/551002345211691009/714493661391355995/Zonder_titel814.png")
        embed.set_footer(text="version 1.6.9 (build 1488)")
        await ctx.send(embed=embed)

    @commands.command()
    async def rust(self, ctx):

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

        else:
            await discord.Attachment.save(ctx.message.attachments[0],fp="input.png")
        rust = Image.open("rust.jpg").convert("RGBA")
        image = Image.new("RGBA",(800,600))
        inputy = Image.open("input.png").convert("RGBA")
        print("input image size: {}x{}".format(inputy.width,inputy.height))

        inputylist = []
        imagedata = inputy

        for pixel in imagedata:
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


class EHlookup(commands.Cog):

    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.group()
    async def ehlookup(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a subcommand.\nAvailable subcommands: `ship`, `module`.\n See `;help ehlookup` for more information.")



    @ehlookup.command()
    async def module(self, ctx):

        module = None
        modname = "Vanilla"
        fast = False
        superfast = False
        nolayout = False
        ultrafast = False

        args = ctx.message.content.lower().split(" ")
        arg_index = 0

        for arg in args:

            if arg == "-fast" or arg == "-f":
                fast = True

            elif arg == "-superfast" or arg == "-s":
                superfast = True

            elif arg == "-ultrafast" or arg == "-u":
                ultrafast = True

            elif arg == "-nolayout" or arg == "-n":
                nolayout = True

            # mod support

            elif arg == "-mod" or arg == "-m":
                if args[arg_index+1] == "end of paradox" or args[arg_index+1] == "eop":
                    modname = "End of Paradox"

            elif arg == "-input" or arg == "-i":
                module = args[arg_index+1]
                if '"' in module:
                    module = ctx.message.content.lower().split('"')[1]

            arg_index += 1

        if not module:

            module = ctx.message.content.lower()[17:len(ctx.message.content)]

        #I don't like this line
        weaponvelocity=hp=damageType=damage=energyCost=firerate=weaponrange=velocity=impulse=recharge=energy=droneCapacity=droneRange=droneWeapon=weight=armourPoints=armourRepairRate=hullPoints=hullRepairRate=hullRepairCooldownMod=energy=recharge=energyRechargeCooldownMod=shieldHP=shieldRechargeRate=weight=ramDamage=energyAbsorption=kineticRes=energyRes=thermalRes=velocity=turnRate=droneRangeMod=droneDamage=droneDefenceMod=droneSpeedMod=dronesBPS=droneBuildTimeMod=weaponFirerateMod=weaponDamageMod=weaponRangeMod=weaponEnergyCostMod=faction = None

        def getComponent(file):
            with open("Databases/" + modname + "/modulelookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")

                for row in lookuptable:
                    try:
                        if module == row[0]:
                            file = "Databases/" + modname + "/Database/Component/"+row[1]
                            break
                        elif row == "BREAK":
                            break
                    except IndexError:
                        pass

                with open(file) as jsonfile:
                    content = json.load(jsonfile)

                    #get availability
                    try:
                        if content["Availability"] == 0:
                            #None
                            available = "Unobtainable"
                        elif content["Availability"] == 1:
                            available = "Common"
                        elif content["Availability"] == 2:
                            available = "Rare"
                        elif content["Availability"] == 3:
                            available = "Special"
                        elif content["Availability"] == 4:
                            available = "Hidden"
                        else:
                            available = "???"
                    except KeyError:
                        available = "None"

                    try:
                        workshopLevel = content["Level"]
                    except KeyError:
                        workshopLevel = "None"

                    #get modifications
                    allMods = []
                    #print("getting mods")
                    with open("Databases/" + modname + "/modificationlookuptable.csv") as lookuptableraw:
                        lookuptable = csv.reader(lookuptableraw, delimiter=",")
                        for row in lookuptable:
                            x = 0

                            while x != len(content["PossibleModifications"]):
                                try:
                                    if str(content["PossibleModifications"][x]) == row[0]:
                                        allMods.append(row[2])
                                except IndexError:
                                    pass

                                x = x + 1

                    icon = "Components/{}.png".format(content["Icon"])

                    try:
                        if content["WeaponSlotType"] != "":
                            redSlot = Image.open("Tiles/4.png")
                            font = ImageFont.truetype("Fonts/bicubik.ttf", 30, encoding="unic")
                            temp = Image.open("Tiles/4.png")
                            draw = ImageDraw.Draw(temp)
                            draw.text((19/len(content["WeaponSlotType"]),18),content["WeaponSlotType"],font=font,fill=(247,247,123))
                            temp.save("currentRedSlot.png","PNG")

                        else:
                            temp = Image.open("Tiles/4.png")
                            temp.save("currentRedSlot.png","PNG")
                    except:
                        pass

                    try:
                        weaponSlotType = content["WeaponSlotType"]
                    except:
                        weaponSlotType = "None"
                    try:
                        ammunitionID = content["AmmunitionId"]
                    except:
                        ammunitionID = "None"
                    try:
                        weaponID = content["WeaponId"]
                    except:
                        weaponID = "None"


                    try:
                        statsID = content["ComponentStatsId"]
                    except:
                        statsID = "None"
                print("Available:{}\nWorkshop:{}\nFac:{}\nMods:{}\nIcon:{}\nSlottype:{}\nWeapoNID:{}\nAmmOID:{}\nStats:{}".format(available, workshopLevel, faction, allMods, icon, weaponSlotType, weaponID, ammunitionID, statsID))
                return available, workshopLevel, allMods, icon, weaponSlotType, weaponID, ammunitionID, statsID


        def getAmmunition(ammoID):

            if config[";ehlookup Settings"]["generateWorkshopLevels"] == "True":
                WorkshopstartTime = int(round(time.time() * 1000))

                for f in glob("Databases/" + modname + "/Database/Ammunition/Obsolete/*.json"):
                    # check obsolete first
                    with open(str(f)) as file:
                        data = json.load(file)
                        x = 0

                        if data["Id"] == ammoID:
                            ammo = data
                            break

                for f in glob("Databases/" + modname + "/Database/Ammunition/*.json"):
                    with open(str(f)) as file:
                        data = json.load(file)
                        x = 0

                        if data["Id"] == ammoID:
                            ammo = data
                            break

                WorkshopendTime = int(round(time.time() * 1000))
                WorkshopResponseTime = WorkshopendTime - WorkshopstartTime

                # do stuff with "data":

                # find damage type
                try:
                    if ammo["DamageType"] == 0:
                        damageType = "Kinetic"
                    elif ammo["DamageType"] == 1:
                        damageType = "Energy"
                    elif ammo["DamageType"] == 2:
                        damageType = "Heat"
                    elif ammo["DamageType"] == 3:
                        damageType = "Direct"
                    else:
                        damageType = "Undefined"
                except KeyError:
                    damageType = "Kinetic"
                try:
                    weaponRange = ammo["Range"]
                except:
                    weaponRange = "None"

                try:
                    velocity = ammo["Velocity"]
                except:
                    velocity = "None"

                try:
                    impulse = ammo["Impulse"]
                except:
                    impulse = "None"

                try:
                    energycost = ammo["EnergyCost"]
                except:
                    energycost = "None"
                try:
                    damage = ammo["Damage"]
                except:
                    damage = "None"

                return damageType,damage,weaponRange,velocity,energycost,impulse
            else:
                return "Feature disabled!"


        def getWeapon(weaponID):

            if config[";ehlookup Settings"]["generateWorkshopLevels"] == "True":
                WorkshopstartTime = int(round(time.time() * 1000))

                for f in glob("Databases/" + modname + "/Database/Weapon/Obsolete/*.json"):
                    # check old ammo first
                    with open(str(f)) as file:
                        data = json.load(file)
                        x = 0
                        if data["Id"] == weaponID:
                            weapon = data
                            break

                for f in glob("Databases/" + modname + "/Database/Weapon/*.json"):
                    # check new ammo (what will happen?)
                    with open(str(f)) as file:
                        data = json.load(file)
                        x = 0
                        if data["Id"] == weaponID:
                            weapon = data
                            break



                WorkshopendTime = int(round(time.time() * 1000))
                WorkshopResponseTime = WorkshopendTime - WorkshopstartTime
                #print("response time weapon: {}".format(WorkshopResponseTime))
                #do stuff with data
                try:
                    fireRate = weapon["FireRate"]
                except:
                    fireRate = "None"

                try:
                    magazine = weapon["Magazine"]
                except:
                    magazine = "None"
                try:
                    spread = weapon["Spread"]
                except:
                    spread = "None"

                return fireRate,spread,magazine

        def getStats(statsID,platformSize):

            if config[";ehlookup Settings"]["generateWorkshopLevels"] == "True":
                StatsstartTime = int(round(time.time() * 1000))

                for f in glob("Databases/" + modname + "/Database/Component/Stats/*.json"):
                    with open(str(f)) as file:
                        data = json.load(file)
                        x = 0
                        if data["Id"] == statsID:
                            break


                StatsendTime = int(round(time.time() * 1000))
                StatsResponseTime = StatsendTime - StatsstartTime
                #print("response time stats: {}".format(StatsResponseTime))
                #do stuff with data

                try:
                    if data["Type"]:
                        modifier = platformSize
                    else:
                        modifier = 1
                except KeyError:
                    modifier = 1
                try:
                    armourPointsR = data["ArmorPoints"]*modifier
                except:
                    armourPointsR = "None"
                try:
                    armourRepairRateR = data["ArmorRepairRate"]*modifier
                except:
                    armourRepairRateR = "None"
                try:
                    hullPointsR = data["HullPoints"]*modifier
                except:
                    hullPointsR = "None"
                try:
                    hullRepairRateR = data["HullRepairRate"]*modifier
                except:
                    hullRepairRateR = "None"
                try:
                    hullRepairCooldownMod = data["HullRepairCooldownModifier"]*modifier
                except:
                    hullRepairCooldownMod = "None"
                try:
                    energyR = data["EnergyPoints"]*modifier
                except:
                    energyR = "None"
                try:
                    rechargeRateR = data["EnergyRechargeRate"]*modifier
                except:
                    rechargeRateR = "None"
                try:
                    energyRechargeCooldownMod = data["EnergyRechargeCooldownModifier"]*modifier
                except:
                    energyRechargeCooldownMod = "None"
                try:
                    shieldHPR = data["ShieldPoints"]*modifier
                except:
                    shieldHPR = "None"
                try:
                    shieldRechargeRateR = data["ShieldRechargeRate"]*modifier
                except:
                    shieldRechargeRateR = "None"
                try:
                    weightR = data["Weight"]*modifier
                except:
                    weightR = "None"

                try:
                    ramDamageR = data["RammingDamage"]*modifier
                except:
                    ramDamageR = "None"
                try:
                    energyAbsorptionR = data["EnergyAbsorption"]*modifier
                except:
                    energyAbsorptionR = "None"
                try:
                    kineticResR = data["KineticResistance"]*modifier
                except:
                    kineticResR = "None"
                try:
                    energyResR = data["EnergyResistance"]*modifier
                except:
                    energyResR = "None"
                try:
                    thermalResR = data["ThermalResistance"]*modifier
                except:
                    thermalResR = "None"

                try:
                    velocityR = data["EnginePower"]*modifier
                except:
                    velocityR = "None"
                try:
                    turnRateR = data["TurnRate"]*modifier
                except:
                    turnRateR = "None"

                try:
                    droneRangeMod = str(round(data["DroneRangeModifier"]*modifer*100))+"%"
                except:
                    droneRangeMod = "None"
                try:
                    droneDamageMod = str(round(data["DroneDamageModifier"]*modifier*100))+"%"
                except:
                    droneDamageMod = "None"
                try:
                    droneDefenceMod = str(round(data["DroneDefenseModifier"]*modifier*100))+"%"
                except:
                    droneDefenceMod = "None"
                try:
                    droneSpeedMod = str(round(data["DroneSpeedModifier"]*modifier*100))+"%"
                except:
                    droneSpeedMod = "None"
                try:
                    dronesBPS = str(round(data["DronesBuiltPerSecond"]*modifier*100))+"%"
                except:
                    dronesBPS = "None"
                try:
                    droneBuildTimeMod = str(round(data["DroneBuildTimeModifier"]*modifier*100))+"%"
                except:
                    droneBuildTimeMod = "None"

                try:
                    weaponFirerateMod = str(round(data["WeaponFireRateModifier"]*modifier*100))+"%"
                except:
                    weaponFirerateMod = "None"
                try:
                    weaponDamageMod = str(round(data["WeaponDamageModifer"]*modifier*100))+"%"
                except:
                    weaponDamageMod = "None"
                try:
                    weaponRangeMod = str(round(data["WeaponRangeModifier"]*modifier*100))+"%"
                except:
                    weaponRangeMod = "None"
                try:
                    weaponEnergyCostMod = str(round(data["WeaponEnergyCostModifier"]*modifier*100))+"%"
                except:
                    weaponEnergyCostMod = "None"

                return armourPointsR,armourRepairRateR,hullPointsR,hullRepairRateR, hullRepairCooldownMod, energyR, rechargeRateR, energyRechargeCooldownMod, shieldHPR, shieldRechargeRateR, weightR, ramDamageR, energyAbsorptionR, kineticResR, energyResR, thermalResR, velocityR, turnRateR, droneRangeMod, droneDamage, droneDefenceMod, droneSpeedMod, dronesBPS, droneBuildTimeMod, weaponFirerateMod, weaponDamageMod, weaponRangeMod,weaponEnergyCostMod


        def getWorkshopLevel(file):

            if config[";ehlookup Settings"]["generateWorkshopLevels"] == "True":
                WorkshopstartTime = int(round(time.time() * 1000))
                with open("Databases/" + modname + "/techlookuptable.csv") as lookuptableraw:
                    lookuptable = csv.reader(lookuptableraw, delimiter=",")

                    for row in lookuptable:
                        try:
                            if file == row[0]:
                                file = "Databases/" + modname + "/Database/Technology/"+row[1]

                            elif row == "":
                                pass

                            elif row == "BREAK":
                                break
                        except:
                            pass

                try:
                    with open(file) as jsonfile:
                        content = json.load(jsonfile)
                        try:
                            dependencies = content["Dependencies"]
                        except KeyError:
                            return "???"

                except FileNotFoundError:
                    return "???"

                found = False
                contents = []
                try:
                    workshoplevel = content["Price"]
                except KeyError:
                    workshoplevel = 0

                try:
                    while len(dependencies) > 0:
                        for f in glob("Databases/" + modname + "/Database/Technology/*.json"):
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

                                                    return "None"
                                    if dependencies:
                                        x = x + 1
                except:
                    return "None"

                WorkshopendTime = int(round(time.time() * 1000))
                WorkshopResponseTime = WorkshopendTime - WorkshopstartTime
                print("response time for workshop level: {}".format(WorkshopResponseTime))
                return workshoplevel
            else:
                return "Feature disabled!"


        def getTech(file):

            with open("Databases/" + modname + "/modulelookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")
                faction = None
                for row in lookuptable:
                    try:
                        if file == row[0]:
                            file = "Databases/" + modname + "/Database/Technology/"+row[1]
                            break

                        elif row == "BREAK":
                            break
                    except IndexError:
                        pass
                try:
                    with open(file) as jsonfile:
                        content = json.load(jsonfile)
                except:
                    return "???"

                    #get faction

                try:
                    with open("Databases/" + modname + "/factionlookuptable.csv") as lookuptableraw:
                        lookuptable = csv.reader(lookuptableraw, delimiter=",")
                        for row in lookuptable:
                            try:
                                if str(content["Faction"]) == row[0]:
                                    faction = row[1]
                                    break

                                elif row == "BREAK":
                                    break

                                else:
                                    faction = "Free Stars"
                            except IndexError:
                                pass

                except KeyError:
                    faction = "None"

            return faction

        def getLayout(file):

            # return of the king
            # file = file.split("/")[::-1][0]
            with open("Databases/" + modname + "/modulelookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")

                for row in lookuptable:
                    try:
                        if file == row[0]:
                            file = "Databases/" + modname + "/Database/Component/"+row[1]
                            break
                        elif row == "BREAK":
                            break
                    except IndexError:
                        pass

                with open(file) as jsonfile:
                    content = json.load(jsonfile)
                    layout = content["Layout"]
                return layout

        def layout2png(file):

            L2PstartTime = int(round(time.time() * 1000))
            rgbinput = []
            x = 0
            n = 0
            layoutlist = []

            with open("Databases/" + modname + "/modulelookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")
                for row in lookuptable:
                    try:
                        if module == row[0]:
                            file = "Databases/" + modname + "/Database/Component/"+row[1]
                            break
                        elif row == "BREAK":
                            break
                    except IndexError:
                        pass

            layout = getLayout(file)
            #print(layout)

            #if ctx.message.attachments:
                #W.I.P. database module support
            #print("is {} > {}".format(len(layout),int(config[";ehlookup Settings"]["maxShipSize"])))
            if len(layout) > int(config[";ehlookup Settings"]["maxShipSize"]):

                breakcode = True
                return

            #gets image size given the size of any layout is always a square
            size = int(math.sqrt(len(layout)))

            image = Image.new("RGBA", (size,size))

            while n != len(layout):
                layoutlist.append(layout[int(n):int(n+size)])
                n = n + size


            with open(file) as jsonfile:
                content = json.load(jsonfile)
                platformSize = 0
                print(content)
                #convert to RGB
                while x != size:
                    y = 0
                    while y != size:
                        working = int(layoutlist[x][y])

                        if working == 0:
                            rgbinput.append((255,255,255,0))
                        elif working == 1:
                            try:

                                if content["CellType"] == "1":
                                    rgbinput.append((0,0,255))
                                elif content["CellType"] == "2":
                                    rgbinput.append((0,255,0))
                                elif content["CellType"] == "3":
                                    rgbinput.append((0,255,255))
                                elif content["CellType"] == "4":
                                    rgbinput.append((255,0,0))
                                elif content["CellType"] == "5":
                                    rgbinput.append((255,255,0))
                                elif content["CellType"] == "":
                                    rgbinput.append((222,222,222))
                                else:
                                    print("YIKES")
                                platformSize = platformSize + 1
                            except KeyError:
                                rgbinput.append((222,222,222))

                        y = y + 1
                    x = x + 1

            image.putdata(rgbinput)

            #resize and draw pixel grid


            if ultrafast == True:
                image.save("output.png")
                L2PendTime = int(round(time.time() * 1000))
                L2Presponsetime = L2PendTime - L2PstartTime
                return layoutlist,L2Presponsetime

            new_image = image.resize(((59*image.width),(59*image.width)), resample = PIL.Image.NEAREST)

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
                return layoutlist,L2Presponsetime,platformSize

            x = 1
            y = 1

            temp = Image.open("Tiles/0.png")
            nullSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
            temp = Image.open("Tiles/1.png")
            blueSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
            temp = Image.open("Tiles/2.png")
            greenSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
            temp = Image.open("Tiles/3.png")
            greenblueSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
            temp = Image.open("currentRedSlot.png")
            redSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
            temp = Image.open("Tiles/5.png")
            yellowSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
            temp = Image.open("Tiles/X.png")
            allSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)

            canvas = Image.new("RGBA", (59*image.width,59*image.width))

            while x < new_image.width:
                while y < new_image.width:
                    roundy = (round(x),round(y))
                    intman = (int(x),int(y))
                    (r, g, b, a) = new_image.getpixel((x,y))
                    #print(r,g,b)
                    if (r,g,b,a) == (255,255,255,0):
                        canvas.paste(nullSlot,intman)
                    elif (r,g,b) == (0,0,255):
                        canvas.paste(blueSlot,intman)
                    elif (r,g,b) == (0,255,0):
                        canvas.paste(greenSlot,intman)
                    elif (r,g,b) == (0,255,255):
                        canvas.paste(greenblueSlot,intman)
                    elif (r,g,b) == (255,0,0):
                        canvas.paste(redSlot,intman)
                    elif (r,g,b) == (255,255,0):
                        canvas.paste(yellowSlot,intman)
                    elif (r,g,b) == (222,222,222):
                        canvas.paste(allSlot,intman)

                    y = y + increment
                y = 1
                x = x + increment

            canvas.save("output.png","PNG")
            L2PendTime = int(round(time.time() * 1000))
            L2Presponsetime = L2PendTime - L2PstartTime
            return layoutlist,L2Presponsetime,platformSize




        weapon = False
        desc = ""
        faction = getTech(module)
        available, price, allMods, icon, weaponSlotType, weaponID, ammoID, statsID = getComponent(module)
        workshopLevel = getWorkshopLevel(module)
        try:
            price = 50 + int(price) * 20
        except:
            price = 50
        #try:
        #print("Ammo ID: {}\nWeapon ID: {}".format(ammoID,weaponID))
        if ammoID != "None":
            damageType, damage, weaponrange, weaponvelocity, energyCost, impulse = getAmmunition(ammoID)
            try:
                impulse = impulse * 1000
            except:
                impulse = "None"
        if weaponID != "None":
            firerate, spread, magazine = getWeapon(weaponID)
            try:
                firerate = round((1/float(firerate)),2)
            except:
                firerate = "None"

        layout,responseTimeL2PNG,platformSize = layout2png(module)

        armourPoints,armourRepairRate,hullPoints,hullRepairRate, hullRepairCooldownMod, energy, recharge, energyRechargeCooldownMod, shieldHP, shieldRechargeRate, weight, ramDamage, energyAbsorption, kineticRes, energyRes, thermalRes, velocity, turnRate, droneRangeMod, droneDamage, droneDefenceMod, droneSpeedMod, dronesBPS, droneBuildTimeMod, weaponFirerateMod, weaponDamageMod, weaponRangeMod,weaponEnergyCostMod = getStats(statsID,platformSize)


        weapon = True
        listOfAllStats = ["**Hit Points**: {}\n".format(armourPoints),"**Energy**: {}\n".format(energy),"**Shield Points**: {}\n".format(shieldHP),
                          "**Shield Recharge Rate**: {}\n".format(shieldRechargeRate),"**Ramming Damage**: {}\n".format(ramDamage), "**Energy Absorption**: {}\n".format(energyAbsorption),
                          "**Kinetic Resistance**: {}\n".format(kineticRes),"**Thermal Resistance**: {}\n".format(thermalRes),"**Energy Resistance**: {}\n".format(energyRes),
                          "**Velocity**: {}\n".format(velocity),"**Turn Rate**: {}\n".format(turnRate), "**Drone Range Modifier**: {}\n".format(droneRangeMod),
                          "**Drone Damage Modifier**: {}\n".format(droneDamage),"**Drone Defence Modifier**: {}\n".format(droneDefenceMod),"**Drone Speed Mod**: {}\n".format(droneSpeedMod),
                          "**Drone Build Time**: {}\n".format(droneBuildTimeMod), "**Weapon Fire Rate Modifier**: {}\n".format(weaponFirerateMod), "**Weapon Damage Modifier**: {}\n".format(weaponDamageMod),
                          "**Weapon Range Modifier**: {}\n".format(weaponRangeMod),"**Weapon Energy Cost Modifier**: {}\n".format(weaponEnergyCostMod),
                          "**Damage Type**: {}\n".format(damageType),"**Damage**: {}\n".format(damage),"**Energy Consumption**: {}\n".format(energyCost),
                          "**Reload Time**: {}\n".format(firerate),"**Range**: {}\n".format(weaponrange),"**Velocity**: {}\n".format(weaponvelocity),
                          "**Impulse**: {}\n".format(impulse),"**Recharge Rate**: {}\n".format(recharge),
                          "**Capacicty**: {}\n".format(droneCapacity),"**Drone Range**: {}\n".format(droneRange),"**Weapon**: {}\n".format(droneWeapon),
                          "**Weight**: {}\n\n".format(weight),"**Workshop Level**: {}\n".format(workshopLevel),"**Cost**: {}\n".format(price),
                          "**Faction**: {}\n".format(faction),"**Rarity**: {}\n".format(available)
                          ]

        for stat in listOfAllStats:
            try:
                if "none" not in stat.lower():
                    desc = desc + stat
            except NameError:
                pass


        title = module.split()
        newTitle = ""

        for word in title:
            newWord = word.capitalize() + " "
            newTitle = newTitle + newWord

        if modname != "Vanilla":
            newTitle = newTitle + " (" + modname + ")"

        allMods2 = ""
        for word in allMods:
            newWord = word + ", "#word.capitalize() + ", "
            allMods2 = allMods2 + newWord# + ","

        allMods2 = allMods2[0:len(allMods2)-2]

        emb = discord.Embed(title = newTitle,
        type = "rich",
        colour = 0x8cc43d,
        )
        emb.add_field(name = "Module Information", value = desc, inline = True)
        emb.add_field(name = "Possible Modifications", value = allMods2, inline = True)
        #emb.set_thumbnail(url = "file://output.png")


        if nolayout == False:
            emb.set_image(url="attachment://output.png")
            f = discord.File("output.png", filename="output.png")
            endTime = int(round(time.time() * 1000))
            #emb.description = "hehe"
            #emb.description = "Response time: {}ms\nImage generation time: {}ms".format(endTime-startTime,L2Presponsetime)
            await ctx.send(file=f,embed=emb)
        else:
            endTime = int(round(time.time() * 1000))
            emb.description = "Response time: {}ms".format(endTime-startTime)
            await ctx.send(embed=emb)

    '''
    # example of calling function.. simpler than expected
    @ehlookup.command()
    async def test(self, ctx):
        await EHlookup.module(EHlookup, ctx)
    '''

    @ehlookup.command()
    async def ship(self, ctx):

        startTime = int(round(time.time() * 1000))
        fast = False
        superfast = False
        nolayout = False
        ultrafast = False
        breakcode = False
        modname = "Vanilla"
        ship = None

        args = ctx.message.content.lower().split(" ")
        arg_index = 0

        for arg in args:
            if arg == "-fast" or arg == "-f":
                fast = True

            elif arg == "-superfast" or arg == "-s":
                superfast = True

            elif arg == "-ultrafast" or arg == "-u":
                ultrafast = True

            elif arg == "-nolayout" or arg == "-n":
                nolayout = True

            elif arg == "-mod" or arg == "-m":
                if args[arg_index+1] == "end of paradox" or args[arg_index+1] == "eop":
                    modname = "End of Paradox"

            elif arg == "-input" or arg == "-i":
                ship = args[arg_index+1]
                if '"' in ship:
                    ship = ctx.message.content.lower().split('"')[1]


            arg_index += 1

        if ship is None:

            # this will allow people to still use the old format if they are accustomed to it, although this may be
            # made redundant

            ship = ctx.message.content.lower()[5:len(ctx.message.content)]

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
                if ctx.message.author.id != 186069912081399808 or ctx.message.author.id != 399410993618223115:
                    if ultrafast == False:
                        msg = await ctx.send("Are you sure? **WARNING: This will lag me (and my server) quite a bit!** React with \U00002611 to confirm. Otherwise, ignore this message and it will automatically delete.",delete_after=60)

                        await msg.add_reaction("\U00002611")
                        passed = False
                        while msg:
                            await wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U00002611")


                            msg2 = await ctx.fetch_message(msg.id)

                            reactsO = msg2.reactions

                            async for y in reactsO[0].users():


                                if ctx.message.author == y:

                                    await ctx.send("Understood. Processing!")
                                    await msg.delete()




        def getShipClass(file):

            with open("Databases/" + modname + "/shiplookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")


                for row in lookuptable:

                    try:
                        if file == row[0]:
                            file = "Databases/" + modname + "/Database/Ship/"+row[1]
                            break

                        elif row == "BREAK":
                            break
                    except IndexError:
                        pass

                with open(file) as jsonfile:
                    content = json.load(jsonfile)
                    try:
                        raw = content["SizeClass"]
                    except KeyError:
                        raw = "None"

                    shipId = content["Id"]

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

            return sclass, shipId

        def getDesc(file):

            with open("Databases/" + modname + "/shiplookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")

                for row in lookuptable:
                    try:
                        if file == row[0]:
                            try:
                                return row[2]
                            except:
                                return "No ship description provided."

                        elif row == "":
                            pass

                        elif row == "BREAK":
                            break

                    except IndexError:
                        pass

        def getImage(file):

            with open("Databases/" + modname + "/shiplookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")


                for row in lookuptable:
                    try:
                        if file == row[0]:
                            try:
                                return "Databases/" + modname + "/ShipImages/" + row[3]
                            except:
                                return None

                        elif row == "BREAK":
                            break
                    except IndexError:
                        pass


        def getLayout(file):

            with open("Databases/" + modname + "/shiplookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")

                for row in lookuptable:
                    try:
                        if file == row[0]:
                            file = "Databases/" + modname + "/Database/Ship/"+row[1]
                            break
                        elif row == "":
                            pass
                        elif row == "BREAK":
                            break

                    except IndexError:
                        pass


                with open(file) as jsonfile:
                    content = json.load(jsonfile)
                    layout = content["Layout"]
                return layout

        def getWorkshopLevel(file):

            if config[";ehlookup Settings"]["generateWorkshopLevels"] == "True":
                WorkshopstartTime = int(round(time.time() * 1000))
                with open("Databases/" + modname + "/techlookuptable.csv") as lookuptableraw:
                    lookuptable = csv.reader(lookuptableraw, delimiter=",")

                    for row in lookuptable:
                        try:
                            if file == row[0]:
                                file = "Databases/" + modname + "/Database/Technology/"+row[1]

                            elif row == "BREAK":

                                raise FileNotFoundError#commands.CommandInvokeError("Ship not found")

                            else:
                                pass
                        except IndexError:
                            # this allows for empty lines for better organisation
                            pass
                try:
                    with open(file) as jsonfile:
                        content = json.load(jsonfile)
                        try:

                            dependencies = content["Dependencies"]

                        except KeyError:
                            # this surely means the tech is the first item in the tree
                            dependencies = []



                except FileNotFoundError:
                    return "???"

                found = False
                contents = []
                try:
                    workshoplevel = content["Price"]
                except KeyError:
                    workshoplevel = 0

                e = 0
                while len(dependencies) > 0:
                    start = glob("Databases/" + modname + "/Database/Technology/*.json")[0]
                    #print("looking for ")
                    for f in glob("Databases/" + modname + "/Database/Technology/*.json"):

                        if f == start:
                            e = e + 1


                            if e == 2:

                                return "???"


                        with open(str(f)) as file:
                            data = json.load(file)
                            x = 0

                            while x != len(dependencies):
                                if dependencies:

                                    if x > len(dependencies)-1:
                                        x = 0

                                    if data["Id"] == dependencies[x]:

                                        del dependencies[x]

                                        try:
                                            if len(data["Dependencies"]) > 0:
                                                x = -1
                                                dependencies = dependencies + data["Dependencies"]
                                                workshoplevel = workshoplevel + int(data["Price"])
                                            else:
                                                try:
                                                    workshoplevel = workshoplevel + data["Price"]
                                                except KeyError:

                                                    return "None"
                                        except KeyError:
                                            try:
                                                workshoplevel = workshoplevel + data["Price"]
                                            except KeyError:
                                                return "None"
                                if dependencies:
                                    x = x + 1




                WorkshopendTime = int(round(time.time() * 1000))
                WorkshopResponseTime = WorkshopendTime - WorkshopstartTime
                print("response time for workshop level: {}".format(WorkshopResponseTime))
                return workshoplevel
            else:
                return "Feature disabled!"

        def layout2png(file):

            L2PstartTime = int(round(time.time() * 1000))
            rgbinput = []
            x = 0
            layoutlist = []
            layout = getLayout(file)
            n = 0
            # gets image size given the size of any layout is always a square
            size = int(math.sqrt(len(layout)))

            while n != len(layout):
                layoutlist.append(layout[int(n):int(n+size)])
                n = n + size

            # first check for a cached image, this will dramatically speed up response time
            try:

                # a simple copy operation is an extremely time efficient alternative to generating the image
                shutil.copy("Databases/" + modname + "/LayoutCache/" + ship + ".png", "output.png")

                L2PendTime = int(round(time.time() * 1000))
                L2Presponsetime = str(L2PendTime - L2PstartTime) + "ms (cached)"

                return layoutlist,L2Presponsetime

            except FileNotFoundError:

                print("first time generation")
                if ctx.message.attachments:
                    if len(layout) > int(config[";ehlookup Settings"]["maxShipSize"]):

                        breakcode = True
                        return



                image = Image.new("RGBA", (size,size))



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

                new_image = image.resize(((59*image.width),(59*image.width)), resample = PIL.Image.NEAREST)

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
                nullSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
                temp = Image.open("Tiles/1.png")
                blueSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
                temp = Image.open("Tiles/2.png")
                greenSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
                temp = Image.open("Tiles/3.png")
                greenblueSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
                temp = Image.open("Tiles/4.png")
                redSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
                #temp = Image.open("Tiles/4P.png")
                #redSlotP = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)
                temp = Image.open("Tiles/5.png")
                yellowSlot = temp.resize((int(increment),int(increment)), resample = PIL.Image.NEAREST)

                canvas = Image.new("RGBA", ((59*image.width),(59*image.width)))

                def addWeaponLabels(canvas,intman,x,y,increment):
                    tempx = intman[0]
                    tempy = intman[1]

                    redNearby = True

                    while redNearby == True:
                        tempPixel_up = new_image.getpixel(x,y+increment)
                        tempPixel_right = new_image.getpixel(x+increment,y)
                        tempPixel_down = new_image.getpixel(x,y-increment)
                        tempPixel_left = new_image.getpixel(x-increment,y)

                        tempPixel_up_RGB = "a"





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
                canvas.save("Databases/" + modname + "/LayoutCache/" + ship + ".png")
                L2PendTime = int(round(time.time() * 1000))
                L2Presponsetime = str(L2PendTime - L2PstartTime) + "ms"
                return layoutlist,L2Presponsetime

        def getdata(file):

            def getAllShipData(file):
                with open("Databases/" + modname + "/shiplookuptable.csv") as lookuptableraw:
                    lookuptable = csv.reader(lookuptableraw, delimiter=",")
                    for row in lookuptable:

                        try:

                            if file == row[0]:
                                file = "Databases/" + modname + "/Database/Ship/" + row[1]
                                break

                            elif row == "BREAK":
                                break

                            else:
                                pass

                        except IndexError:
                            pass



                    with open(file) as jsonfile:
                        return json.load(jsonfile)


            shipdata = getAllShipData(file)

            #content here is the ship build in plain text, and "raw" is the layout in list form (not used)
            content = getLayout(file)
            notempty = len(content)-int(content.count("0"))

            try:
                weightmod = shipdata["BaseWeightModifier"]
            except:
                weightmod = 0

            #print("weightmod: {}".format(weightmod))
            tileweight = (20) * (1+weightmod)

            #calculate some things
            hp = notempty*0.5
            baseweight = notempty*tileweight
            minweight = int(baseweight/2)

            #does the ship have any resistances?
            try:
                kineticresistance = int(-(100/((shipdata["KineticResistance"])+1))+100)
                #print(kineticresistance)
            except:
                kineticresistance = "none"
            try:
                thermalresistance = int(-(100/((shipdata["HeatResistance"])+1))+100)
                #print(thermalresistance)
            except:
                thermalresistance = "none"
            try:
                energyresistance = int(-(100/((shipdata["EnergyResistance"])+1))+100)
                #print(energyresistance)
            except:
                energyresistance = "none"

            #living ship?
            try:
                if shipdata["Regeneration"] == True:
                    regen = True

            except:
                regen = False

            sclass, shipId = getShipClass(file)

            if getShipClass(file) == sclass:
                cost = 15*notempty**2
            else:
                cost = 5*notempty**2

            with open("Databases/" + modname + "/shiplookuptable.csv") as lookuptableraw:
                lookuptable = csv.reader(lookuptableraw, delimiter=",")

                for row in lookuptable:
                    try:
                        if row[0] == "MODDED SHIPS BELOW THIS LINE" and config[";ehlookup Settings"]["databaseSupport"] != "True":
                            breakcode = True
                            return "None","None","None","None","None","None","None"
                        if file == row[0]:
                            file = "Databases/" + modname + "/Database/Ship/" + row[1]
                            break

                        elif row == "BREAK":
                            break

                        else:
                            try:
                                raw = int(content["ShipCategory"])
                            except:
                                raw = "???"
                    except IndexError:
                        pass

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
                satclass = "None"

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

            return sclass,satclass,hp,baseweight,minweight,cost,stars,kineticresistance,thermalresistance,energyresistance,regen, shipId


        # below is new 2021 functions that read build information

        class Build:

            def __init__(self, veteran, available, modules):

                self.veteran = veteran
                self.available = available
                self.modules = modules

            def get_modules(self):
                return self.modules

        def find_builds(ship, shipId):

            print("finding builds")

            builds = []
            '''
            # first we need to find the file name we are looking for, e.g. f1s1_mk2.json

            def get_filename(ship, shipId):
                with open("Databases/" + modname + "/shiplookuptable.csv") as lookuptableraw:
                    lookuptable = csv.reader(lookuptableraw, delimiter=",")
                    for row in lookuptable:

                        try:
                            filename = ""
                            if ship == row[0]:

                                # complement name search with id check to make sure we do not confuse similarly-named ships, or
                                # mk2 versions
                                with open(str("Databases/" + modname + "/Database/Ship/" + row[1])) as file:
                                    data = json.load(file)
                                    if data["ShipId"] == shipId:

                                        filename = row[1][0:len(row[1])-5]
                                        # special case for weird fucking EOP formatting
                                        if "_ship" in filename:
                                            return filename.split("_ship")[0][0:len(filename.split("_build")[0]) - 1]

                                        return filename

                            elif row == "BREAK":
                                break

                        except IndexError:
                            pass

            filename = get_filename(ship, shipId)
            print(filename)
            '''
            for f in glob("Databases/" + modname + "/Database/Ship/Builds/*.json"):
                with open(str(f)) as file:
                    data = json.load(file)
                    if data["ShipId"] == shipId:
                        builds.append(str(f))

            buildslist = []
            for build in builds:
                buildjson = json.load(open(str(build)))
                # print(buildjson)

                # identify what veteran level this build is
                try:
                    if buildjson["DifficultyClass"] == 0:
                        veteran = 0

                    elif buildjson["DifficultyClass"] == 1:
                        veteran = 1

                    elif buildjson["DifficultyClass"] == 2:
                        veteran = 2

                    elif buildjson["DifficultyClass"] == 3:
                        veteran = 3

                except KeyError:
                    veteran = 0

                # see if this build is actually in the game
                try:
                    if buildjson["NotAvailableInGame"] == False or not buildjson["NotAvailableInGame"]:
                        available = True

                    else:
                        available = False

                except KeyError:
                    available = True

                buildslist.append(Build(veteran, available, buildjson["Components"]))
            return buildslist

        def getComponents(build: Build):
            """
            Returns a dictionary of components with their modifications, given a build.
            """

            modules = {}

            for component in build.modules:
                # first we determine what component it is by looking up the id - this is a very time-inefficient
                # algorithm but there is little that can be done about that

                for f in glob("Databases/" + modname + "/Database/Component/*.json"):
                    with open(str(f)) as file:
                        data = json.load(file)
                        x = 0
                        #print(data)
                        try:
                            assert data["Id"]
                            componentid = data["Id"]
                        except KeyError:
                            componentid = 0

                    if componentid == component["ComponentId"]:

                        # very nice line right here
                        filename = f.split("\\")[::-1][0]
                        modulename = "None"
                        quality_effect = ""

                        with open("Databases/" + modname + "/modulelookuptable.csv") as lookuptableraw:
                            lookuptable = csv.reader(lookuptableraw, delimiter=",")

                            for row in lookuptable:
                                try:
                                    if filename == row[1]:
                                        modulename = row[0]
                                        break
                                    elif row == "BREAK":
                                        break

                                except IndexError:
                                    pass

                        # determine if the module is normal or modified

                        try:
                            # necessary to make sure we actually have these variables
                            modification = component["Modification"]
                            quality = component["Quality"]

                        except KeyError:
                            modification = None
                            quality = None


                        if quality:

                            # now to determine what the quality does - some pavelparsing

                            if modification == 1:
                                if quality == 0:
                                    quality_effect = "+100% weight"
                                elif quality == 1:
                                    quality_effect = "+50% weight"
                                elif quality == 2:
                                    quality_effect = "+20% weight"
                                elif quality == 3:
                                    quality_effect = "-20% weight"
                                elif quality == 4:
                                    quality_effect = "-40% weight"
                                elif quality == 5:
                                    quality_effect = "-50% weight"

                            elif modification == 2:
                                if quality == 0:
                                    quality_effect = "+100% energy cost"
                                elif quality == 1:
                                    quality_effect = "+50% energy cost"
                                elif quality == 2:
                                    quality_effect = "+20% energy cost"
                                elif quality == 3:
                                    quality_effect = "-10% energy cost"
                                elif quality == 4:
                                    quality_effect = "-25% energy cost"
                                elif quality == 5:
                                    quality_effect = "-50% energy cost"

                            elif modification == 3:
                                if quality == 0:
                                    quality_effect = "-50% defense"
                                elif quality == 1:
                                    quality_effect = "-30% defense"
                                elif quality == 2:
                                    quality_effect = "-20% defense"
                                elif quality == 3:
                                    quality_effect = "+20% defense"
                                elif quality == 4:
                                    quality_effect = "+50% defense"
                                elif quality == 5:
                                    quality_effect = "+100% defense"

                            elif modification == 4:
                                if quality == 0:
                                    quality_effect = "-3 hit points"
                                elif quality == 1:
                                    quality_effect = "-2 hit points"
                                elif quality == 2:
                                    quality_effect = "-1 hit point"
                                elif quality == 3:
                                    quality_effect = "+1 hit point"
                                elif quality == 4:
                                    quality_effect = "+3 hit points"
                                elif quality == 5:
                                    quality_effect = "+5 hit points"

                            elif modification == 5:
                                if quality == 0:
                                    quality_effect = "-50% damage"
                                elif quality == 1:
                                    quality_effect = "-30% damage"
                                elif quality == 2:
                                    quality_effect = "-20% damage"
                                elif quality == 3:
                                    quality_effect = "+20% damage"
                                elif quality == 4:
                                    quality_effect = "+50% damage"
                                elif quality == 5:
                                    quality_effect = "+100% damage"

                            elif modification == 6:
                                if quality == 0:
                                    quality_effect = "+100% cooldown time"
                                elif quality == 1:
                                    quality_effect = "+50% cooldown time"
                                elif quality == 2:
                                    quality_effect = "+20% cooldown time"
                                elif quality == 3:
                                    quality_effect = "-10% cooldown time"
                                elif quality == 4:
                                    quality_effect = "-25% cooldown time"
                                elif quality == 5:
                                    quality_effect = "-50% cooldown time"

                            elif modification == 7:
                                if quality == 0:
                                    quality_effect = "-50% range"
                                elif quality == 1:
                                    quality_effect = "-30% range"
                                elif quality == 2:
                                    quality_effect = "-20% range"
                                elif quality == 3:
                                    quality_effect = "+10% range"
                                elif quality == 4:
                                    quality_effect = "+25% range"
                                elif quality == 5:
                                    quality_effect = "+50% range"

                            elif modification == 8:
                                if quality == 0:
                                    quality_effect = "-50% projectile speed"
                                elif quality == 1:
                                    quality_effect = "-30% projectile speed"
                                elif quality == 2:
                                    quality_effect = "-20% projectile speed"
                                elif quality == 3:
                                    quality_effect = "+10% projectile speed"
                                elif quality == 4:
                                    quality_effect = "+25% projectile speed"
                                elif quality == 5:
                                    quality_effect = "+50% projectile speed"

                            elif modification == 9:
                                if quality == 0:
                                    quality_effect = "-50% energy capacity"
                                elif quality == 1:
                                    quality_effect = "-30% energy capacity"
                                elif quality == 2:
                                    quality_effect = "-20% energy capacity"
                                elif quality == 3:
                                    quality_effect = "+20% energy capacity"
                                elif quality == 4:
                                    quality_effect = "+50% energy capacity"
                                elif quality == 5:
                                    quality_effect = "+100% energy capacity"

                            elif modification == 10:
                                if quality == 0:
                                    quality_effect = "-50% repair rate"
                                elif quality == 1:
                                    quality_effect = "-30% repair rate"
                                elif quality == 2:
                                    quality_effect = "-20% repair rate"
                                elif quality == 3:
                                    quality_effect = "+10% repair rate"
                                elif quality == 4:
                                    quality_effect = "+25% repair rate"
                                elif quality == 5:
                                    quality_effect = "+50% repair rate"

                            elif modification == 11:
                                if quality == 0:
                                    quality_effect = "-50% engine power"
                                elif quality == 1:
                                    quality_effect = "-30% engine power"
                                elif quality == 2:
                                    quality_effect = "-20% engine power"
                                elif quality == 3:
                                    quality_effect = "+10% engine power"
                                elif quality == 4:
                                    quality_effect = "+25% engine power"
                                elif quality == 5:
                                    quality_effect = "+50% engine power"

                            elif modification == 12:
                                if quality == 0:
                                    quality_effect = "-50% recharge rate"
                                elif quality == 1:
                                    quality_effect = "-30% recharge rate"
                                elif quality == 2:
                                    quality_effect = "-20% recharge rate"
                                elif quality == 3:
                                    quality_effect = "+10% recharge rate"
                                elif quality == 4:
                                    quality_effect = "+25% recharge rate"
                                elif quality == 5:
                                    quality_effect = "+50% recharge rate"

                            elif modification == 13:
                                if quality == 0:
                                    quality_effect = "-30% projectile speed, -20% damage"
                                elif quality == 1:
                                    quality_effect = "-20% projectile speed, -15% damage"
                                elif quality == 2:
                                    quality_effect = "-10% projectile speed, -10% damage"
                                elif quality == 3:
                                    quality_effect = "+20% projectile speed, -10% damage"
                                elif quality == 4:
                                    quality_effect = "+50% projectile speed, -20% damage"
                                elif quality == 5:
                                    quality_effect = "+100% projectile speed, -25% damage"

                            elif modification == 14:
                                if quality == 0:
                                    quality_effect = "-50% area of effect"
                                elif quality == 1:
                                    quality_effect = "-30% area of effect"
                                elif quality == 2:
                                    quality_effect = "-20% area of effect"
                                elif quality == 3:
                                    quality_effect = "+25% area of effect"
                                elif quality == 4:
                                    quality_effect = "+60% area of effect"
                                elif quality == 5:
                                    quality_effect = "+100% area of effect"

                            elif modification == 15:
                                if quality == 0:
                                    quality_effect = "-50% shield power"
                                elif quality == 1:
                                    quality_effect = "-30% shield power"
                                elif quality == 2:
                                    quality_effect = "-20% shield power"
                                elif quality == 3:
                                    quality_effect = "+10% shield power"
                                elif quality == 4:
                                    quality_effect = "+25% shield power"
                                elif quality == 5:
                                    quality_effect = "+50% shield power"

                            elif modification == 16:
                                if quality == 0:
                                    quality_effect = "-60% damage, -30% cooldown time"
                                elif quality == 1:
                                    quality_effect = "-40% damage, -20% cooldown time"
                                elif quality == 2:
                                    quality_effect = "-15% damage, -10% cooldown time"
                                elif quality == 3:
                                    quality_effect = "+40% damage, +10% cooldown time"
                                elif quality == 4:
                                    quality_effect = "+100% damage, +25% cooldown time"
                                elif quality == 5:
                                    quality_effect = "+200% damage, +50% cooldown time"

                            elif modification == 17:
                                #drone damage
                                if quality == 0:
                                    quality_effect = "-50% damage"
                                elif quality == 1:
                                    quality_effect = "-30% damage"
                                elif quality == 2:
                                    quality_effect = "-20% damage"
                                elif quality == 3:
                                    quality_effect = "+30% damage"
                                elif quality == 4:
                                    quality_effect = "+80% damage"
                                elif quality == 5:
                                    quality_effect = "+150% damage"

                            elif modification == 18:
                                #drone defence
                                if quality == 0:
                                    quality_effect = "-50% defense"
                                elif quality == 1:
                                    quality_effect = "-30% defense"
                                elif quality == 2:
                                    quality_effect = "-20% defense"
                                elif quality == 3:
                                    quality_effect = "+30% defense"
                                elif quality == 4:
                                    quality_effect = "+80% defense"
                                elif quality == 5:
                                    quality_effect = "+150% defense"

                            elif modification == 19:
                                #drone speed
                                if quality == 0:
                                    quality_effect = "-50% drones speed"
                                elif quality == 1:
                                    quality_effect = "-30% drones speed"
                                elif quality == 2:
                                    quality_effect = "-20% drones speed"
                                elif quality == 3:
                                    quality_effect = "+20% drones speed"
                                elif quality == 4:
                                    quality_effect = "+50% drones speed"
                                elif quality == 5:
                                    quality_effect = "+80% drones speed"

                            elif modification == 20:
                                #drone range
                                if quality == 0:
                                    quality_effect = "-50% range"
                                elif quality == 1:
                                    quality_effect = "-30% range"
                                elif quality == 2:
                                    quality_effect = "-20% range"
                                elif quality == 3:
                                    quality_effect = "+20% range"
                                elif quality == 4:
                                    quality_effect = "+50% range"
                                elif quality == 5:
                                    quality_effect = "+80% range"

                            elif modification == 21:
                                if quality == 0:
                                    quality_effect = "+150% projectile weight"
                                elif quality == 1:
                                    quality_effect = "+100% projectile weight"
                                elif quality == 2:
                                    quality_effect = "+50% projectile weight"
                                elif quality == 3:
                                    quality_effect = "-20% projectile weight"
                                elif quality == 4:
                                    quality_effect = "-50% projectile weight"
                                elif quality == 5:
                                    quality_effect = "-80% projectile weight"

                        quality_effect = " " + quality_effect
                        if quality_effect == " ":
                            quality_effect = ""

                        if modulename + quality_effect in modules:
                            count = modules.get(modulename + quality_effect)
                            modules.update({modulename +  quality_effect: count+1})
                        else:
                            modules.update({modulename + quality_effect: 1})

                        break

            return modules


        if ship == "-myfile":

            if ctx.message.attachments:
                await ctx.send("Processing!")
                await discord.Attachment.save(ctx.message.attachments[0],fp="file.json")
                file = "file.json"
                if nolayout == False:
                    try:
                        layout, L2Presponsetime = layout2png(file)
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
                    emb.description = "Response time: {}ms\nImage generation time: {}".format(endTime-startTime,L2Presponsetime)
                except UnboundLocalError:
                    emb.description = "Response time: {}ms\nThis ship's size is greater than {}x{} - no image.".format(endTime-startTime,int(math.sqrt(int(config[";ehlookup Settings"]["maxShipSize"]))),int(math.sqrt(int(config[";ehlookup Settings"]["maxShipSize"]))))
                    await ctx.send(embed=emb)
                    return
                await ctx.send(embed=emb,file = f)

            else:
                await ctx.send("Correct syntax: `;ehlookup [ship name]`. You can also upload a .json to see its information.")
            return

        sclass,satclass,hp,baseweight,minweight,cost,stars,kineticresistance,thermalresistance,energyresistance,living, shipId = getdata(ship)
        if sclass == "None":
            await ctx.send("Sorry, but I currently have database ships disabled.")
            layout = 0
            return





        listOfAdditionalStats = ["**Kinetic Resistance**: {}%\n".format(kineticresistance),"**Thermal Resistance**: {}%\n".format(thermalresistance),"**Energy Resistance**: {}%\n".format(energyresistance)]

        if living == True:
            listOfAdditionalStats.append("**Living ship** (this ship regenerates its own HP)\n")

        #desc = "**Damage Type**: {}\n**Damage**: {}\n**Energy Consumption**: {}\n**Reload Time**: {}\n**Range**: {}\n**Velocity**: {}\n**Impulse**: {}\n".format(damageType,damage,energyCost,firerate,weaponrange,velocity,impulse)
        #except:
        #    weapon = False
        adddesc = ""
        for stat in listOfAdditionalStats:
            try:
                if "none" not in stat.lower():
                    adddesc = adddesc + stat
            except NameError:
                pass





        if nolayout == False:
            layout,L2Presponsetime = layout2png(ship)
        #except discord.HTTPException:
        #    pass
        workshop = getWorkshopLevel(ship)
        desc = getDesc(ship)
        shipIcon = getImage(ship)

        builds = find_builds(ship, shipId)

        #await ctx.send("Ship class: {}\nSattelite class:{}\nHitpoints:{}\nBase weight:{}\nMinimum weight: {}\nCost:{}\nStar cost: {}\nWorkshop level:{}\n\nDescription: {}".format(sclass,satclass,hp,baseweight,minweight,cost,stars,workshop,desc))

        if modname != "Vanilla":
            title = ship.capitalize() + " ({})".format(modname)

        else:
            title = ship.capitalize()

        emb = discord.Embed(title = title,
        type = "rich",
        colour = 0x8cc43d,
        )
        emb.add_field(name = "Ship Information", value = "**Ship Class**: {}\n**Satellite Class**: {}\n**Hitpoints**: {}\n**Base Weight**: {}\n**Minimum Weight**: {}\n{}\n**Cost** (if applicable): {}\n**Star Cost**: {}\n**Workshop Level**: {}\n\n**Description**: {}".format(sclass,satclass,hp,baseweight,minweight,adddesc,cost,stars,workshop,desc), inline = True)
        #emb.set_thumbnail(url = "file://output.png")

        # new field for build info
        buildstring = ""
        buildlist = [[], [], [], []]
        for build in builds:

            if build.veteran == 0:
                buildstring = buildstring + "Non-veteran - :zero:\n"
                buildlist[0].append(build)
            elif build.veteran == 1:
                buildstring = buildstring + "Veteran - :one:\n"
                buildlist[1].append(build)
            elif build.veteran == 2:
                buildstring = buildstring + "Double veteran - :two:\n"
                buildlist[2].append(build)
            elif build.veteran == 3:
                buildstring = buildstring + "Triple veteran - :three:\n"
                buildlist[3].append(build)


        if buildstring == "":
            buildstring = "Builds not found!"
        emb.add_field(name = "Ship Builds - react to see information (after reacting, wait a few seconds, API is slow!)", value = buildstring, inline = False)
        f = discord.File("output.png", filename="output.png")
        f2 = discord.File(shipIcon, filename="ship.png")
        emb.set_thumbnail(url="attachment://ship.png")#{}".format(shipIcon))
        print(shipIcon)

        if nolayout == False:
            emb.set_image(url="attachment://output.png")
            endTime = int(round(time.time() * 1000))
            emb.description = "Response time: {}ms\nImage generation time: {}".format(endTime-startTime,L2Presponsetime)
            msg = await ctx.send(files=[f,f2],embed=emb)

        else:
            endTime = int(round(time.time() * 1000))
            emb.description = "Response time: {}ms".format(endTime-startTime)
            msg = await ctx.send(embed=emb,files = [f,f2])

        for build in builds:
            if build.veteran == 0:
                await msg.add_reaction("0⃣")
            elif build.veteran == 1:
                await msg.add_reaction("1⃣")
            elif build.veteran == 2:
                await msg.add_reaction("2⃣")
            elif build.veteran == 3:
                await msg.add_reaction("3⃣")

        nv_index = 0
        v_index = 0
        dv_index = 0
        tv_index = 0

        while msg:
            # async for y in reactsO[0].users():

            await self.crdbot.wait_for("reaction_add", check=lambda reaction, user: reaction.emoji in ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣"])
            msg2 = await ctx.fetch_message(msg.id)

            reacts = msg2.reactions

            # certain ships have multiple veteran builds f.e. so unfortunately this is necessary
            newtitle = "Ship Builds - react to see information (after reacting, wait a few seconds, API is slow!)"
            newdesc = buildstring

            async for y in reacts[0].users():
                if ctx.message.author == y:
                    modules = getComponents(buildlist[0][nv_index])
                    newtitle = "Non-Veteran Information ({} of {})".format(nv_index+1, len(buildlist[0]))
                    newdesc = ""

                    for item in modules:
                        newdesc = newdesc + item.capitalize() + ": " + str(modules.get(item)) + "\n"

                    nv_index += 1
                    if nv_index == len(buildlist[0]):
                        nv_index = 0
                    print("index: " + str(nv_index))


            try:
                async for y in reacts[1].users():
                    if ctx.message.author == y:
                        modules = getComponents(buildlist[1][v_index])
                        newtitle = "Veteran Information ({} of {})".format(v_index + 1, len(buildlist[1]))
                        newdesc = ""

                        for item in modules:
                            newdesc = newdesc + item.capitalize() + ": " + str(modules.get(item)) + "\n"
                        v_index += 1
                        if v_index == len(buildlist[1]):
                            v_index = 0
                        print("index: " + str(v_index))

            except IndexError:
                pass

            try:
                async for y in reacts[2].users():
                    if ctx.message.author == y:
                        modules = getComponents(buildlist[2][dv_index])
                        newtitle = "Double Veteran Information ({} of {})".format(dv_index + 1, len(buildlist[2]))
                        newdesc = ""

                        for item in modules:
                            newdesc = newdesc + item.capitalize() + ": " + str(modules.get(item)) + "\n"
                        dv_index += 1
                        if dv_index == len(buildlist[2]):
                            dv_index = 0

            except IndexError:
                pass

            try:
                async for y in reacts[3].users():
                    if ctx.message.author == y:
                        modules = getComponents(buildlist[3][tv_index])
                        newtitle = "Triple Veteran Information ({} of {})".format(tv_index + 1, len(buildlist[3]))
                        newdesc = ""

                        for item in modules:
                            newdesc = newdesc + item.capitalize() + ": " + str(modules.get(item)) + "\n"

                        tv_index += 1
                        if tv_index == len(buildlist[3]):
                            tv_index = 0

            except IndexError:
                pass

            emb.set_field_at(index=1, name=newtitle, value=newdesc, inline=False)
            await msg.edit(embed=emb)
            await asyncio.sleep(1)
    '''
    @ship.error
    async def ship_error(ctx,ctx2,err):
        print(ctx2)
        print(err)
        # I don't fucking know why there are two ctxs, horrors of error handling


        if isinstance(err, commands.MissingRequiredArgument):
            await ctx2.send("Missing one or more arguments. Correct command format: `;ehlookup [ship]`. Do `;help ehlookup` for more information.")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx2.send("I did not recognise the option or ship you specified. Do `;help ehlookup` for more information.")

    '''

def setup(crdbot):

    crdbot.add_cog(EHlookup(crdbot))
    crdbot.add_cog(RustMemeFunny(crdbot))
    crdbot.add_cog(StaffTools(crdbot))
