from discord.ext import commands
import discord
import asyncio
import random
from glob import glob
import math
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gapi client secret.json', scope)
gcrdbot = gspread.authorize(creds)
gcrdbot.login()

class Horizon(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot

    
    @commands.group()
    async def horizon(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a subcommand.\nAvailable subcommands: .\nSee `;help horizon` for more information.")

    @horizon.command()
    async def refreshcreds(self, ctx):
        if ctx.message.author.id == 186069912081399808:
            gcrdbot.login()
            await ctx.send("Logged in successfully!")
            
    @horizon.command()
    @commands.cooldown(rate=1, per=15, type= commands.BucketType.channel)
    async def battle(self, ctx):
        gcrdbot.login()
        
        if ctx.message.mentions:
            p1 = ctx.message.author
            p2 = ctx.message.mentions[0]
            if p1 == p2:
                await ctx.send("You can only battle other people!")
                return
        else:
            await ctx.send("Correct syntax: `;horizon battle [user]`, where `user` is a mentioned user.")
            return

        
        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()

        shipsheet = gcrdbot.open("Stratos Walker").get_worksheet(1)
        shiptable = shipsheet.get_all_values()

        weaponsheet = gcrdbot.open("Stratos Walker").get_worksheet(2)
        weapontable = weaponsheet.get_all_values()

        foundp1 = False
        foundp2 = False
        
        for row in playerFileList:
            try:
                if str(p1.id) == row[1]:
                    p1weapon = row[4]
                    p1ship = row[3]
                    foundp1 = True
                if str(p2.id) == row[1]:
                    p2weapon = row[4]
                    p2ship = row[3]
                    foundp2 = True
                          
            except IndexError:
                pass

        if foundp1 == False:
            await ctx.send("Error, you do not have a Horizon profile. Get one by doing `;horizon start`.")
            return
        elif foundp2 == False:
            await ctx.send("Error, {} does not have a Horizon profile. They can get one by doing `;horizon start`.".format(p2))
            return
            
        #await ctx.send("Fight! P1: Ship: {} Weapon: {}\nP2: Ship: {} Weapon: {}".format(p1ship,p1weapon,p2ship,p2weapon))

        #get ship info



        for row in shiptable:
            try:
                if row[0] == p1ship:
                    p1shipIcon = row[1]
                    p1weaponType = row[2]
                    p1weaponSlot = row[3]
                    p1weaponCount = row[4]
                    p1shipClass = row[5]
                    p1HP = int(row[6])
                    
                if row[0] == p2ship:
                    p2shipIcon = row[1]
                    p2weaponType = row[2]
                    p2weaponSlot = row[3]
                    p2weaponCount = row[4]
                    p2shipClass = row[5]
                    p2HP = int(row[6])
                    
            except IndexError:
                pass


        #get weapon info



        for row in weapontable:

            try:
                if row[0] == p1weapon:
                    p1DPS = row[3]
                    p1EPS = row[4]
                    p1Accuracy = row[5]
                    p1Range = row[6]
                    p1Blast = row[7]
                    p1Cooldown = int(row[8])
                    p1Chargetime = int(row[9])

                if row[0] == p2weapon:
                    p2DPS = row[3]
                    p2EPS = row[4]
                    p2Accuracy = row[5]
                    p2Range = row[6]
                    p2Blast = row[7]
                    p2Cooldown = int(row[8])
                    p2Chargetime = int(row[9])
                    
            except IndexError:
                pass
        
        #calculate
            #ships
        if p1shipClass == "frigate":
            p1dodgeChance = 40
            p1EnergyCap = 40
            p1Recharge = 10
            p1creditsMax = 100
            p1xpMax = 2500

        elif p1shipClass == "destroyer":
            p1dodgeChance = 30
            p1EnergyCap = 60
            p1Recharge = 15
            p1creditsMax = 1000
            p1xpMax = 5000

        elif p1shipClass == "cruiser":
            p1dodgeChance = 20
            p1EnergyCap = 80
            p1Recharge = 20
            p1creditsMax = 2500
            p1xpMax = 7500

        elif p1shipClass == "battleship":
            p1dodgeChance = 10
            p1EnergyCap = 100
            p1Recharge = 25
            p1creditsMax = 5000
            p1xpMax = 10000

        elif p1shipClass == "titan":
            p1dodgeChance = 5
            p1EnergyCap = 480
            p1Recharge = 80
            p1creditsMax = 10000
            p1xpMax = 25000



        if p2shipClass == "frigate":
            p2dodgeChance = 40
            p2EnergyCap = 40
            p2Recharge = 10
            p2creditsMax = 100
            p2xpMax = 2500

        elif p2shipClass == "destroyer":
            p2dodgeChance = 30
            p2EnergyCap = 60
            p2Recharge = 15
            p2creditsMax = 1000
            p2xpMax = 5000

        elif p2shipClass == "cruiser":
            p2dodgeChance = 20
            p2EnergyCap = 80
            p2Recharge = 20
            p2creditsMax = 2500
            p2xpMax = 7500

        elif p2shipClass == "battleship":
            p2dodgeChance = 10
            p2EnergyCap = 100
            p2Recharge = 25
            p2creditsMax = 5000
            p2xpMax = 10000

        elif p2shipClass == "titan":
            p2dodgeChance = 5
            p2EnergyCap = 480
            p2Recharge = 80
            p2creditsMax = 10000
            p2xpMax = 25000


        #data is ready, start the battle!

        p1shotCount = 0
        p2shotCount = 0
        
        p1Username = p1.nick
        if p1Username == None:
            p1Username = str(p1)[0:len(str(p1))-5]
            
        p2Username = p2.nick
        if p2Username == None:
            p2Username = str(p2)[0:len(str(p2))-5]            
        emb = discord.Embed(title = "Horizon - {} vs {}!".format(p1Username, p2Username),
        type = "rich",
        colour = 0x8cc43d,
        )
        turn = 0

        p1shipList = p1ship.split()
        p1ship = " "
        for term in p1shipList:
            p1ship = p1ship + term.capitalize() + " "
            
        p2shipList = p2ship.split()
        p2ship = " "
        for term in p2shipList:
            p2ship = p2ship + term.capitalize() + " "

        p1weaponList = p1weapon.split()
        p1weapon = " "
        for term in p1weaponList:
            p1weapon = p1weapon + term.capitalize() + " "
            
        p2weaponList = p2weapon.split()
        p2weapon = " "
        for term in p2weaponList:
            p2weapon = p2weapon + term.capitalize() + " "
            
        p1Energy = p1EnergyCap
        p2Energy = p2EnergyCap
        
        emb.add_field(name = p1Username, value="**Ship**: {}\n**Weapon**:{}\n**HP**: {}\n**Energy**: {}".format(p1ship,p1weapon,p1HP,p1Energy), inline = True)
        emb.add_field(name = p2Username, value="**Ship**: {}\n**Weapon**:{}\n**HP**: {}\n**Energy**: {}".format(p2ship,p2weapon,p2HP,p2Energy), inline = True)
        startingPlayer = random.randint(0,1)
        
        if startingPlayer == 0:
            startingPlayer = p1Username
        else:
            startingPlayer = p2Username

          

        shiprange = random.randint(30,80)
        damageDealt = 0
        
        emb.add_field(name = "Battle Progress", value = "Game start! {} will fire first.".format(startingPlayer), inline = False)

        #icon = "D:\crdgu\Pictures\Images\STRATOS.png"
        #emb.set_thumbnail(url="attachment://{}".format("STRATOS.png"))
        #f = discord.File(icon, filename="STRATOS.png")

        msg = await ctx.send(embed = emb) 
        while p1HP > 0 and p2HP > 0:

            await asyncio.sleep(2)

            if startingPlayer == p1Username:
                p1shotCount = p1shotCount + 1
                #p1's turn
                
                #icon = "D:/EH Textures 24.4.2019 EXCLUSIVE/Images/Ships/" + p1shipIcon + ".png"
                #print(icon)
                #emb.set_thumbnail(url="attachment://{}".format(p1shipIcon+".png"))
                #f = discord.File(icon, filename=p1shipIcon+".png")
                
                p1Energy = p1Energy - int(p1EPS)*int(p1weaponCount)

                if p1Energy < 0 or shiprange > int(p1Range):# or int(p1EPS) > p1Energy
                    if shiprange > int(p1Range):
                        action = "{} was out of range!".format(p1Username)
                    
                        shiprange = shiprange - random.randint(5,p1dodgeChance)
                        if shiprange <= 0:
                            shiprange = 1
                    else:
                        action = "{} retreated, and recovered energy.".format(p1Username)
                        shiprange = shiprange + 10
                        
                    if p1Energy + int(p1EPS)*int(p1weaponCount) + int(p1EPS) > p1EnergyCap:
                        p1Energy = p1EnergyCap
                    else:
                        p1Energy = p1Energy + int(p1EPS)*int(p1weaponCount)
                        p1Energy = p1Energy + int(p1EPS)
                        
                    if p2Energy + int(p2EPS) > p2EnergyCap:
                        p2Energy = p2EnergyCap
                    else:
                        p2Energy = p2Energy + int(p2EPS)
                        
                    displayHP = p2HP
                    emb.set_field_at(1, name = p2Username, value="**Ship**: {}\n**Weapon**: {}\n**HP**: {} ({})\n**Energy**: {}".format(p2ship,p2weapon,displayHP,damageDealt,p2Energy), inline = True)

                else:
                    
                    chance = random.randint(0,100)
                    if int(int(p1weaponCount)/2) <= 1:
                        place1 = 1
                    else:
                        place1 = random.randint(1,int(int(p1weaponCount)/2))

                    if int(int(p1weaponCount)/2) <= 1:
                        place2 = 1
                    else:
                        place2 = random.randint(int(int(p1weaponCount)/2),int(p1weaponCount))
                    #print("{} and {}".format(place1,place2))
                    if place1 == 1 and place2 == 1:
                        placeholder = 1
                    else:
                        placeholder = random.randint(place1,place2)
                    damageDealt = -1*(random.randint(round(int(p1DPS)/4),int(p1DPS))*placeholder)
                    
                    p2HP = p2HP + damageDealt
                    
                    action = "{} fired their {}, dealing {} damage!".format(p1Username,p1weapon,-1*damageDealt)

                    #print("is {} >= {}?".format(chance,int(p2dodgeChance)))
                    if chance >= int(p2dodgeChance):
                        #print("yeS")
                        dodged = False
                        
                    else:
                        #print("no")
                        dodged = True
                        p2HP = p2HP - damageDealt
                        damagedDealt = "Dodged!"
                        action = "{} fired their {}, but {} dodged the attack!".format(p1Username,p1weapon,p2Username)


                    if p2HP <= 0:
                        displayHP = "Destroyed!"
                        action = "{} was destroyed!".format(p2Username)
                    else:
                        displayHP = p2HP
                        if p2Energy + p2Recharge > p2EnergyCap:
                            p2Energy = p2EnergyCap
                        else:
                            p2Energy = p2Energy + p2Recharge

                    shiprange = shiprange + random.randint(-10,20)
                    if shiprange <= 0:
                        shiprange = 1
                        
                    emb.set_field_at(1, name = p2Username, value="**Ship**: {}\n**Weapon**: {}\n**HP**: {} ({})\n**Energy**: {}".format(p2ship,p2weapon,displayHP,damageDealt,p2Energy), inline = True)
                emb.set_field_at(0, name = p1Username, value="**Ship**: {}\n**Weapon**: {}\n**HP**: {}\n**Energy**: {}".format(p1ship,p1weapon,p1HP,p1Energy), inline = True)

                

            else:
                #p2's turn
                p2shotCount = p2shotCount + 1
                #icon = "D:/EH Textures 24.4.2019 EXCLUSIVE/Images/Ships/" + p2shipIcon + ".png"
                #emb.set_thumbnail(url="attachment://{}".format(p2shipIcon+".png"))
                #f = discord.File(icon, filename=p2shipIcon+".png")

                p2Energy = p2Energy - int(p2EPS)*int(p2weaponCount)
                chance = random.randint(0,100)

                if p2Energy < 0 or int(p2EPS) > p2Energy or shiprange > int(p2Range):
                    if shiprange > int(p2Range):
                        action = "{} was out of range!".format(p2Username)
                    
                        shiprange = shiprange - random.randint(5,p2dodgeChance)
                        if shiprange <= 0:
                            shiprange = 1
                    else:
                        action = "{} retreated, and recovered energy.".format(p2Username)
                        shiprange = shiprange + 10
                        
                    if p2Energy + int(p2EPS)*int(p2weaponCount) > p2EnergyCap:
                        
                        p2Energy = p2EnergyCap
                    else:
                        p2Energy = p2Energy + int(p2EPS)*int(p2weaponCount)
                        p2Energy = p2Energy + int(p2EPS)
                        
                    if p1Energy + int(p1EPS) > p1EnergyCap:
                        p1Energy = p1EnergyCap
                    else:
                        p1Energy = p1Energy + int(p1EPS)
                    
                    displayHP = p1HP
                    emb.set_field_at(1, name = p1Username, value="**Ship**: {}\n**Weapon**: {}**HP**: {}\n**Energy**: {}".format(p1ship,p1weapon,displayHP,p1Energy), inline = True)

                else:
                    if int(int(p2weaponCount)/2) <= 1:
                        place1 = 1
                    else:
                        place1 = random.randint(1,int(int(p2weaponCount)/2))
                        
                    if int(int(p2weaponCount)/2) <= 1:
                        place2 = 1
                    else:
                        place2 = random.randint(int(int(p2weaponCount)/2),int(p2weaponCount))
                    #print("{} and {}".format(place1,place2))
                    #print("{} and {}".format(place1,place2))
                    if place1 == 1 and place2 == 1:
                        placeholder = 1
                    else:
                        placeholder = random.randint(place1,place2)
                    damageDealt = -1*(random.randint(round(int(p2DPS)/4),int(p2DPS))*placeholder)
                    p1HP = p1HP + damageDealt
                    
                    action = "{} fired their {}, dealing {} damage!".format(p2Username,p2weapon,-1*damageDealt)

                    #print("is {} >= {}?".format(chance,int(p1dodgeChance)))
                    if chance >= int(p1dodgeChance):
                        #print("yeS")
                        dodged = False
                        
                    else:
                        #print("no")
                        dodged = True
                        p1HP = p1HP - damageDealt
                        damagedDealt = "Dodged!"
                        action = "{} fired their {}, but {} dodged the attack!".format(p2Username,p2weapon,p1Username)


                    if p1HP <= 0:
                        displayHP = "Destroyed!"
                        action = "{} was destroyed!".format(p1Username)
                    else:
                        displayHP = p1HP          
                        if p1Energy + p1Recharge > p1EnergyCap:
                            p1Energy = p1EnergyCap
                        else:
                            p1Energy = p1Energy + p1Recharge
                            
                    shiprange = shiprange + random.randint(-10,20)
                    if shiprange <= 0:
                        shiprange = 1
                        
                    emb.set_field_at(0, name = p1Username, value="**Ship**: {}\n**Weapon**: {}\n**HP**: {} ({})\n**Energy**: {}".format(p1ship,p1weapon,displayHP,damageDealt,p1Energy), inline = True)
                emb.set_field_at(1, name = p2Username, value="**Ship**: {}\n**Weapon**: {}\n**HP**: {}\n**Energy**: {}".format(p2ship,p2weapon,p2HP,p2Energy), inline = True)

                
                
            emb.set_field_at(2, name = "Battle Progress", value = "**Distance**: {}\n{}".format(shiprange,action), inline = False) 
            await msg.edit(content="",embed = emb)
            
            startingPlayer = random.randint(0,1)
            if startingPlayer == 0:
                startingPlayer = p1Username
            else:
                startingPlayer = p2Username


            turn = turn + 1
            
        if p1HP <= 0 or p1HP == "Destroyed!":
            victor = p2
            multiplier = round(p1creditsMax/p2creditsMax,1)
            creditReward = int(multiplier*random.randint(p1creditsMax/2,p1creditsMax))*random.randint(5,10)
            xpReward = int(multiplier*random.randint(p1creditsMax,p1xpMax))
            print(xpReward)
            general = False
            seasoned = False
            leveledUp = False

            starsReward = random.randint(1,random.randint(5,12))
            if starsReward >= 10:
                starsReward = int(round(random.uniform(1,1.75)))
                append = " and {} <:stars:579008424444952577>.".format(starsReward)
            else:
                append = "."
                


            x = 1
            for row in playerFileList:
                try:
                    
                    print(p2.id)
                    print(row[1])
                    if str(p2.id) == str(row[1]):

                        print("updating {}".format(int(round(int(row[5]) + creditReward))))
                        playerFile.update_cell(x,6,int(round(int(row[5]) + creditReward)))
                        playerFile.update_cell(x,7,int(round(int(row[6]) + starsReward)))
                        playerFile.update_cell(x,8,int(row[7]) + 1)
                        level = int(row[2])

                        try:
                            currentXp = int(row[14])
                        except ValueError:
                            currentXp = 0
                        
                        playerFile.update_cell(x,15,currentXp + (xpReward))
                                               
                        xpForNextLevel = round(100*(math.sqrt(10*(level+1)**3))**4)
                        #print("EXP for next level is {}".format(xpForNextLevel))

                        if int(row[14]) >= xpForNextLevel:
                            playerFile.update_cell(x,15,int(row[14]) + xpReward)
                            playerFile.update_cell(x,3,int(row[2]) + 1)
                            level = row[2]
                            
                            leveledUp = True
                            
                        try:
                            kd = round((int(row[7])/int(row[8])),2)
                        except ZeroDivisionError:
                            try:
                                kd = int(row[7])
                            except ValueError:
                                kd = 0

                        print(kd)
                        if kd > 6:

                            if "general" not in row[12].split("."):
                                general = True
                                playerFile.update_cell(x,13,row[12] + ".general")
                            else:
                                general = False

                        elif kd > 4:

                            if "seasoned captain" not in row[12].split("."):
                                seasoned = True
                                playerFile.update_cell(x,13,row[12] + ".seasoned captain")
                            else:
                                seasoned = False
                        else:
                            seasoned = False
                            general = False
                                                
                    elif str(p1.id) == row[1]:
                        row[8] = int(row[8]) + 1
                except:
                    pass
                x = x + 1
                
        if p2HP <= 0 or p2HP == "Destroyed!":
            victor = p1
            multiplier = round(p2creditsMax/p1creditsMax,1)
            creditReward = int(multiplier*random.randint(p2creditsMax/2,p2creditsMax))*random.randint(5,10)
            xpReward = int(multiplier*random.randint(p2creditsMax,p2xpMax))
            print(xpReward)
            general = False
            seasoned = False
            leveledUp = False

            starsReward = random.randint(1,random.randint(5,12))
            if starsReward >= 10:
                starsReward = int(round(random.uniform(1,1.75)))
                append = " and {} <:stars:579008424444952577>.".format(starsReward)
            else:
                append = "."
                

            x = 1
            for row in playerFileList:
                #try:
                    
                print(p1.id)
                print(row[1])
                if str(p1.id) == str(row[1]):

                    print("updating {}".format(int(round(int(row[5]) + creditReward))))
                    playerFile.update_cell(x,6,int(round(int(row[5]) + creditReward)))
                    playerFile.update_cell(x,7,int(round(int(row[6]) + starsReward)))
                    playerFile.update_cell(x,8,int(row[7]) + 1)
                    level = int(row[2])
                    playerFile.update_cell(x,15,int(row[14]) + (xpReward))
                                           
                    xpForNextLevel = round(100*(math.sqrt(10*(level+1)**3))**4)
                    #print("EXP for next level is {}".format(xpForNextLevel))

                    if int(row[14]) >= xpForNextLevel:
                        playerFile.update_cell(x,15,int(row[14]) + xpReward)
                        playerFile.update_cell(x,3,int(row[2]) + 1)
                        level = row[2]
                        
                        leveledUp = True
                        
                    try:
                        kd = round((int(row[7])/int(row[8])),2)
                    except ZeroDivisionError:
                        try:
                            kd = int(row[7])
                        except ValueError:
                            kd = 0

                    print(kd)
                    if kd > 6:

                        if "general" not in row[12].split("."):
                            general = True
                            playerFile.update_cell(x,13,row[12] + ".general")
                        else:
                            general = False

                    elif kd > 4:

                        if "seasoned captain" not in row[12].split("."):
                            seasoned = True
                            playerFile.update_cell(x,13,row[12] + ".seasoned captain")
                        else:
                            seasoned = False
                    else:
                        seasoned = False
                        general = False
                        
                elif str(p2.id) == row[1]:
                    row[8] = int(row[8]) + 1
                #except:
                #    pass
                x = x + 1
                 

        #emb.set_field_at(2, name = "Battle Progress", value = "{} won the battle, and received <:credits:579008386188705823>{}{}".format(victor,creditReward,append), inline = False)   
        await ctx.send("{} won the battle and received {} experience, and {}<:credits:579008386188705823>{}".format(victor,xpReward,creditReward,append))

        if leveledUp == True:
            await ctx.send("{} leveled up to level {}!".format(victor,level))
        if general == True:
            await ctx.send("Unlocked the **General** title for having a K:D ratio greater than 6!")
        elif seasoned == True:
            await ctx.send("Unlocked the **Seasoned Captain** title for having a K:D ratio greater than 4!")
    '''
    @battle.error
    async def battle_error(self, ctx, err):

        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing an argument. Correct command format: `;horizon battle [player]`, where `player` is a mentioned user. Do `;help horizon` for more information.")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send("Something just went horribly wrong on executing this command. Please contact Crdguy as soon as possible.")
            print("Error!\n{}".format(err))
        elif isinstance(err, commands.CommandOnCooldown):
            await ctx.send("Sorry, `;battle` is on cooldown. Try again after {} seconds.".format(round(err.retry_after,2)))
    '''

    @horizon.command()
    async def start(self, ctx):
        gcrdbot.login()
        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()
        
        for row in playerFileList:
            try:
                if str(ctx.message.author.id) == row[1]:
                    await ctx.send("You already have a profile!")
                    return
            except:
                pass

        #create profile
        

        #writer.writerow([str(len(playerFileList)),str(ctx.message.author.id),1,"scout","pulse cannon m2",0,0,0,0,"scout.raven.spectrum","small pulse cannon","","recruit","recruit"])

        playerFile.insert_row([len(playerFileList),str(ctx.message.author.id),1,"scout","pulse cannon m2",1000,0,0,0,"scout.raven.spectrum","small pulse cannon","","recruit","recruit"],len(playerFileList)+1)

        await ctx.send("Profile created!\nWelcome to **Horizon**! You have been selected as the captain of a small fleet, to lead a rebellion against the chaos and disorder that has befallen this galaxy.\nYou should start by using `;horizon battle` to fight other fleets, and `;horizon mine` to gain free credits.")


    @horizon.command()
    async def title(self, ctx):
        gcrdbot.login()
        title = ctx.message.content[15:len(ctx.message.content)].lower()
        
        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()

        found = False
        
        for row in playerFileList:
            try:
                if str(ctx.message.author.id) == row[1]:
                    found = True
                    titles = row[12].split(".")
                    currentTitle = row[13]

            except:
                pass

        if found == False:
            await ctx.send("It looks like you don't have a Horizon profile. Make one by doing `;horizon start`.")        
            return

        if title == currentTitle:
            await ctx.send("You already have this title active.")
            return
        
        #print("is {} in {}?".format(title,titles))
        if title not in titles:
            await ctx.send("Sorry, you either have not unlocked this title or it does not exist. Do `;horizon profile` to view your unlocked titles.")
        else:
            currentTitle = title

        x = 1
        for row in playerFileList:
            try:
                if str(ctx.message.author.id) == row[1]:

                    titles = row[12].split(".")
                    playerFile.update_cell(x,14,currentTitle)

            except:
                pass
            x = x + 1

        await ctx.send("Success!")
        
    @horizon.command()
    async def weapon(self, ctx):
        gcrdbot.login()
        weapon = ctx.message.content[16:len(ctx.message.content)]
        #print(weapon)

        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()

        shipsheet = gcrdbot.open("Stratos Walker").get_worksheet(1)
        shiptable = shipsheet.get_all_values()

        weaponsheet = gcrdbot.open("Stratos Walker").get_worksheet(2)
        lookuptable = weaponsheet.get_all_values()

        found = False
        for row in playerFileList:
            try:
                if str(ctx.message.author.id) == row[1]:
                    found = True
                    ship = row[3]
            except:
                pass

        if found == False:
            await ctx.send("It looks like you don't have a Horizon profile. Make one by doing `;horizon start`.")        
            return

        
        for row in lookuptable:
            try:
                
                if weapon == row[0]:
                    weaponClass = row[1]
                    weaponSlot = row[2]
            except:
                pass


        match = False

        for row in shiptable:
            try:
                #print("is {} == {} and {} == {}?".format(weaponClass,row[2],weaponSlot,row[3]))
                
                #print("is {} == {}? and {} == {} or {} == *?".format(weaponClass,row[2],weaponSlot,row[3],weaponSlot))
                if row[0] == ship and weaponClass <= row[2] and (weaponSlot == row[3] or weaponSlot == "*"):

                    x = 1
                    for row in playerFileList:
                        try:
                            if str(ctx.message.author.id) == row[1]:

                                #print("new row:\n{}".format(row))
                                playerFile.update_cell(x,5,weapon)
                                await ctx.send("Success!")
                                match = True
                                return
                                      
                        except IndexError:
                            pass
                        x = x + 1

                    

            except IndexError:
                pass
            
            
        if match == False:
            await ctx.send("Sorry, your ship cannot mount this weapon. Try again with a weapon with the same or a smaller platform size and same weapon slot.")
                        #allows empty lines to be passed, makes the .csv a bit more readable
                    
                        
    @horizon.command()
    async def ship(self, ctx):
        gcrdbot.login()

        ship = ctx.message.content[14:len(ctx.message.content)]

        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()

        shipsheet = gcrdbot.open("Stratos Walker").get_worksheet(1)
        lookuptable = shipsheet.get_all_values()
     
        x = 1
        found = False
        found2 = False
        for row in lookuptable:
            try:
                if ship == row[0]:
                    shipClass = row[5]
                    found = True
                    print(1)

                    y = 1
                    for row in playerFileList:
                        print(1.5)
                        try:
                            if str(ctx.message.author.id) == str(row[1]):
                                found2 = True
                                print(2)
                                classMax = []
                                if int(row[2]) > 0:
                                    classMax.append("frigate")
                                if int(row[2]) > 1:
                                    classMax.append("destroyer")
                                if int(row[2]) > 2:
                                    classMax.append("cruiser")
                                if int(row[2]) > 3:
                                    classMax.append("battleship")
                                if int(row[2]) > 4:
                                    classMax.append("titan")

                                if shipClass in classMax:
                                    if ship in row[9]:
                                        print(3)
                                        #print("nice, legal")
                                        
                                        print(y)
                                        playerFile.update_cell(y,4,ship)
                                        playerFile.update_cell(y,5,"small pulse cannon")
                                        await ctx.send("Success! Your ship is now {}.".format(ship.capitalize()))
                                        return
                                    else:
                                        await ctx.send("You have not unlocked this ship yet.")
                                        return
                                else:
                                    await ctx.send("Sorry, your player level is too low to use this ship.")
                                    return
                        except:
                            pass
                        y = y + 1
                    if found2 == False:
                        await ctx.send("It looks like you don't have a Horizon profile. Make one by doing `;horizon start`.")
                        return
            except:
                pass
            
            x = x + 1
                
        if found == False:
            await ctx.send("Sorry, the ship you specified does not exist.")

    @horizon.command()
    async def buy(self, ctx):
        gcrdbot.login()

        user = ctx.message.author
        item = ctx.message.content[13:len(ctx.message.content)].lower()
        
        
        #lootBoxesFile = csv.reader(open("Lootboxes.csv"))
        #lootBoxesList = list(lootBoxesFile)

        lootBoxes = gcrdbot.open("Stratos Walker").get_worksheet(3)
        lootBoxesList = lootBoxes.get_all_values()

        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()

        
        for row in playerFileList:
            try:
                if str(user.id) == str(row[1]):

                    level = int(row[2])
                    credit = int(row[5])
                    stars = int(row[6])
                    unlockedShips = row[9]
                    unlockedShipsList = unlockedShips.split(".")
                    #print(unlockedShipsList)
                    unlockedWeapons = row[10].split(".")
                    unlockedModules = row[11].split(".")
                    break
            except:
                pass


        found = False
        for row in lootBoxesList:
            if item in row:
                boxLevel = int(row[0])
                desc = row[2]
                shipReward = row[3]
                itemReward = row[4]
                price = int(row[5])
                inflateBasedOnLevel = bool(row[6])
                if inflateBasedOnLevel == True:
                    price = round((math.sqrt(price*(level**2)))*level*20)
                found = True
                #print("-1")
            else:
                pass

        if found == False:
            await ctx.send("Sorry, but I have no items in that name. Do `;help horizon buy` for information on what you can buy.")
            return        

        #print("0")
        #print("is {} <= {}".format(price,credit)) 
        if price <= credit:
            credit = credit-price
            allrewards = []
            #print("0.5")

            if shipReward != "0":
                #print(shipReward)
                if shipReward == "all":
                    randomShipClass = random.randint(1,level)
                    if randomShipClass == 1:
                        randomShipClass = "frigate"
                    elif randomShipClass == 2:
                        randomShipClass = "destroyer"
                    elif randomShipClass == 3:
                        randomShipClass = "cruiser"
                    elif randomShipClass == 4:
                        randomShipClass = "battleship"
                    elif randomShipClass == 5:
                        randomShipClass = "titan"
                    #print("1")

                shipsheet = gcrdbot.open("Stratos Walker").get_worksheet(1)
                allships = shipsheet.get_all_values()
                
                ships = []
                
                for ship in allships:

                    if ship[5] == randomShipClass:
                        append = True
                        for playerShip in unlockedShipsList:

                            if playerShip == ship[0]:
                                append = False
                                    
                        if append == True:    
                            ships.append(ship[0])
                            
                x = 1
                for row in playerFileList:
                    try:

                        if str(user.id) == row[1]:

                            row[5] = credit

                            reward = random.choice(ships)
                            allrewards.append(reward)
                            unlockedShips = str(unlockedShips)
                        
                            new = unlockedShips + "." + reward
                            playerFile.update_cell(x,6,credit)
                            playerFile.update_cell(x,10,new)
                        
                            break
                    except IndexError:
                        pass
                    x = x + 1



            if itemReward != "0":

                if itemReward == "weapon":

                    weaponsheet = gcrdbot.open("Stratos Walker").get_worksheet(2)
                    weapontable = weaponsheet.get_all_values()

                    x = 0
                    const = len(weapontable)
                    while x <= const:
                        popped = False

                        try:
                            print("is {} == {}".format(weapontable[x][0].lower(),weapontable[x][0]))
                            if weapontable[x][0].lower() != weapontable[x][0]:
                                print("no")
                                if popped == False:
                                    weapontable.pop(x)
                                popped = True
                                
                            elif weapontable[x][10] == 'IGNORE':

                                if popped == False:
                                    weapontable.pop(x)
                                popped = True
                                
                            elif weapontable[x] == ['', '', '', '', '', '', '', '', '', '', '']:
                                if popped == False:
                                    weapontable.pop(x)
                                    weapontable.pop(x)
                                popped = True                            


                        except IndexError:
                            pass
                    
                        x = x + 1

                    #x = 0
                    #while x != len(weapontable)-1:
                    weapontable.pop(0)
                    print(weapontable)


                    
        else:
            await ctx.send("Looks like you don't have enough money for this box! The box costs <:credits:579008386188705823>{}.".format(price))
            return

        try:    
            await ctx.send("Bought {} for <:credits:579008386188705823>{}!\nRecieved: {}".format(item,price,allrewards))                    
        except UnboundLocalError:
            await ctx.send("Bought {} for <:credits:579008386188705823>{}! There was nothing in the box...".format(item,price))

    @horizon.command()
    async def profile(self, ctx):

        gcrdbot.login()

        '''
        
        <:expbarLE:582696217373310988>
        <:expbarME:582696217553666058>
        <:expbarRE:582696217570705408>

        <:expbarLF:582696217583026176>
        <:expbarMF:582696217553797120>
        <:expbarRF:582696217570705438>

        '''

        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.author

        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()

        shipsheet = gcrdbot.open("Stratos Walker").get_worksheet(1)
        shiptable = shipsheet.get_all_values()

        weaponsheet = gcrdbot.open("Stratos Walker").get_worksheet(2)
        weapontable = weaponsheet.get_all_values()
        
        for row in playerFileList:
            try:
                if str(user.id) == row[1]:

                    level = row[2]
                    ship = row[3]
                    weapon = row[4]
                    credit = row[5]
                    stars = row[6]
                    wins = row[7]
                    losses = row[8]
                    unlockedShips = row[9].split(".")
                    unlockedWeapons = row[10].split(".")
                    unlockedModules = row[11].split(".")
                    titles = row[12].split(".")
                    title = row[13]

                    try:
                        kd = round((int(wins)/int(losses)),2)
                    except ZeroDivisionError:
                        try:
                            kd = wins
                        except ValueError:
                            kd = 0

            except IndexError:
                pass
            

        #get ship info

        print("playerfile table:")
        print(playerFileList)

        for row in shiptable:
            try:
                if row[0] == ship:
                    shipIcon = row[1]
                    weaponType = row[2]
                    weaponSlot = row[3]
                    weaponCount = row[4]
                    shipClass = row[5]
                    HP = int(row[6])
                    
            except IndexError:
                pass
            except UnboundLocalError:
                await ctx.send("It looks like you don't have a Horizon profile. Make one by doing `;horizon start`.")
                return

        #get weapon info

        for row in weapontable:

            try:
                if row[0] == weapon:
                    DPS = row[3]
                    EPS = row[4]
                    Accuracy = row[5]
                    Range = row[6]
                    Blast = row[7]
                    
            except IndexError:
                pass
        
        #calculate
            #ships
        if shipClass == "frigate":
            dodgeChance = 40
            EnergyCap = 40
            Recharge = 10

        elif shipClass == "destroyer":
            dodgeChance = 30
            EnergyCap = 60
            Recharge = 15

        elif shipClass == "cruiser":
            dodgeChance = 20
            EnergyCap = 80
            Recharge = 20

        elif shipClass == "battleship":
            dodgeChance = 10
            EnergyCap = 100
            Recharge = 25

        elif shipClass == "titan":
            dodgeChance = 5
            EnergyCap = 480
            Recharge = 80

        #icon

        icon = "ShipImages/" + shipIcon + ".png"

        titleList = title.split()
        title = ""
        for item in titleList:
            item = item.capitalize()
            title = title + item + " "
            
        userStats = "**Level**: {}\n\n<:credits:579008386188705823> {}  <:stars:579008424444952577> {}\n\n**KD Ratio**: {} (wins: {} losses: {})".format(level,int(float(credit)),int(float(stars)),kd,wins,losses)
        shipStats = "**HP**: {}\n**Weapon Slot**: {}\n**Weapon Size**: {}\n**Gun count**: {}\n**Dodge Chance**: {}\n**Energy**: {}\n**Recharge Rate**: {}\n**Class**: {}\n".format(HP,weaponSlot.capitalize(),weaponType,weaponCount,dodgeChance,EnergyCap,Recharge,shipClass.capitalize())
        if int(weaponCount) > 1:
            weaponStats = "**Damage Per Second**: {} * {}\n**Energy Per Second**: {}\n**Accuracy**: {}\n**Range**: {}\n**Area of Effect**: {}\n".format(DPS,weaponCount,(int(EPS)*int(weaponCount)),Accuracy,Range,Blast)
        else:
            weaponStats = "**Damage Per Second**: {}\n**Energy Per Second**: {}\n**Accuracy**: {}\n**Range**: {}\n**Area of Effect**: {}\n".format(DPS,EPS,Accuracy,Range,Blast)

        emb = discord.Embed(title = "{}{}".format(title,str(user)[0:len(str(user))-5]),
        type = "rich",
        colour = 0x8cc43d,
        )

        emb.set_thumbnail(url="attachment://{}".format(shipIcon+".png"))
        f = discord.File(icon, filename=shipIcon+".png")

        emb.description = userStats

        shipList = ship.split()
        ship = ""
        for item in shipList:
            item = item.capitalize()
            ship = ship + item + " "

        weaponList = weapon.split()
        weapon = ""
        for item in weaponList:
            item = item.capitalize()
            weapon = weapon + item + " "

        shipsString = ""
        x = 0
        for item in unlockedShips:
            item = item.capitalize()
            if x != len(unlockedShips)-1:
                shipsString = shipsString + item + ", "
            else:
                shipsString = shipsString + item
            x = x + 1

        titlesString = ""
        x = 0
        for item in titles:
            item = item.capitalize()
            if x != len(titles)-1:
                titlesString = titlesString + item + ", "
            else:
                titlesString = titlesString + item
            x = x + 1
            
        emb.add_field(name = "Ship - {}".format(ship), value=shipStats, inline = True)
        emb.add_field(name = "Weapon - {}".format(weapon), value=weaponStats, inline = True)
        emb.add_field(name = "Showing {} unlocked ships".format(len(unlockedShips)), value = shipsString, inline = False)
        emb.add_field(name = "Showing {} unlocked titles".format(len(titles)),value = titlesString, inline = False)
        
        await ctx.send(file=f,embed=emb)

    @horizon.command()
    @commands.cooldown(rate=1, per=240, type= commands.BucketType.user)
    async def mine(self, ctx):

        gcrdbot.login()

        user = ctx.message.author
        #"miner" is for the miner title
        miner = False
        
        allAsteroids = glob("Assets/Asteroids/*.png")
        asteroid = random.choice(allAsteroids)
        asteroid = asteroid.replace("\\","/")

        #decide asteroid stuff

        size = random.randint(1,32051939)

        if size > 32051930:
            size = random.uniform(200,1000)
        elif size > 32051900:
            size = random.uniform(100,200)
        elif size > 32051700:
            size = random.uniform(50,100)
        elif size > 32051100:
            size = random.uniform(30,50)
        elif size > 32050000:
            size = random.uniform(10,30)
        elif size > 32040000:
            size = random.uniform(5,10)
        elif size > 31950000:
            size = random.uniform(3,5)
        elif size > 31750000:
            size = random.uniform(1,3)
            miner = True
        elif size > 31000000:
            size = random.uniform(0.5,1)
            miner = True
        elif size > 29000000:
            size = random.uniform(0.3,0.5)
            miner = True
        elif size > 25000000:
            size = random.uniform(0.1,0.3)
            miner = True
        elif size <= 25000000:
            size = random.uniform(0.01,0.1)
            miner = True


        if size < 1:
            size = size*1000
            unit = "m"
        else:
            unit = "km"
        size = round(size,3)


        #composition
        credit = 0
        regolith = 100
        
        iron = round(random.uniform(10,50),3)
        regolith = regolith - iron
        credit = iron*1*size
        nickel = round(random.uniform(5,regolith/2),3)
        regolith = regolith - nickel
        credit = credit + nickel*2.5*size
        cobalt = round(random.uniform(2.5,regolith/2),3)
        regolith = regolith - cobalt
        credit = credit + cobalt*5*size
        copper = round(random.uniform(1.25,regolith/2),3)
        regolith = regolith - copper
        credit = credit + copper*12.5*size
        silver = round(random.uniform(0.625,regolith/2),3)
        regolith = regolith - silver
        credit = credit + silver*20*size
        gold = round(random.uniform(0.3125,regolith/2),3)
        credit = credit + gold*30*size
        credit = round(credit/20)
        #regolith = regolith - gold
        regolith = round(100 - (iron + nickel + cobalt + copper + silver + gold),3)
            
        

        emb = discord.Embed(title = "Asteroid Mining",
        type = "rich",
        description = "**Diameter**: {}{}\n\n**Composition**:\n{}% regolith\n{}% iron\n{}% nickel\n{}% cobalt\n{}% copper\n{}% silver\n{}% gold\n\n**Credits**: {}".format(size,unit,regolith,iron,nickel,cobalt,copper,silver,gold,credit),
        colour = 0x8cc43d,
        )
        #emb.add_field(name = "Module Information", value = "h\n\n\n\h", inline = True)

        #load in player data
        playerFile = gcrdbot.open("Stratos Walker").get_worksheet(0)
        playerFileList = playerFile.get_all_values()

        message = False
        x = 1
        msg = 0
        
        for row in playerFileList:
            #try:
                #print("is {} == {}?".format(user.id,row[1]))
                
            if str(user.id) == row[1]:
                #print("yh")
                playerFile.update_cell(x,6,"{}".format(int(row[5]) + credit))
                #row[5] = int(row[5]) + credit
                print("money")
                if miner == True:
                    if "miner" not in row[12].split("."):
                        message = True

                        playerFile.update_cell(x,13,row[12] + ".miner")
                        

                break
            #except:
            #    pass

            x = x + 1
            
        
        f = discord.File(asteroid, filename="asteroid.png")
        attach = "attachment:/{}".format(asteroid[6:len(asteroid)])
        emb.set_thumbnail(url=attach)

        
        await ctx.send(file = f, embed = emb)
        if size > 10000:
            await ctx.send("Unlocked the **Miner** title for mining an asteroid with a diameter greater than 1km!")
    #'''
    @mine.error
    async def mine_error(self, ctx,err):

        if isinstance(err, commands.CommandOnCooldown):
            await ctx.send("Sorry, `;horizon mine` is on cooldown. Try again after {} seconds.".format(round(err.retry_after,2)))
                   
    #'''
def setup(crdbot):

    crdbot.add_cog(Horizon(crdbot))
