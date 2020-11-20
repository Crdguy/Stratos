from discord.ext import commands
import discord
import asyncio
import random
import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gapi client secret.json', scope)
gcrdbot = gspread.authorize(creds)
gcrdbot.login()


class Fight(commands.Cog):
    def __init__(self, crdbot):
        self.crdbot = crdbot
        self.datasheet = gcrdbot.open("Stratos Scrapbox").get_worksheet(0)
        

    @commands.command()
    async def fight(self, ctx, c1, c2, rounds):

        """
        Version: 3.0.0
        A fictional battle between the characters c1 and c2. c1 and c2 take turns (rounds) to battle each other, and a winner is declared at the end.

        1.0.0: Original script coded in VBS.
        2.0.0: Script adapted for Python.
        2.1.0: Script adapted for discord.py. New events added.
        3.0.0: Google Sheets integration allows for "levelling up" which unlocks special moves. A K:D ratio can be found for each player, and a formula involving the wins and losses calculates player level.

        """
        




        

        c1count = 0
        c2count = 0
        event = []
        x = 0
        desc = ""
        print(rounds)
        try:
            int(rounds)
        except Exception:
            desc = "You're funny, aren't you?"
            #print("bad rounds")
            #return
        
        if c1 in ["@everyone","@here"] or c2 in ["@everyone","@here"] or int(rounds) > 333 or int(rounds) < 0 or str(int(rounds)) != str(rounds):
            
            emb = discord.Embed(
                title = "**Nope**".format(c1,c2,rounds),
                type = "rich",
                description = "Wow, you're hilarious. Trying to exploit my code for funny moments, eh? Have you got anything better to be doing right now? Look at yourself, idling, wasting time. You are the bane of society. Go and do something productive.",
                colour = 0xFD0202,
                )
            await ctx.send(embed=emb)            
            return



        #''' #V3.0 content, work on this tomorrow!
        def findData(command):
            #data = gcrdbot.open("Stratos Scrapbox").get_worksheet(0)
            dataList = self.datasheet.get_all_values()
            y = 0
            for row in dataList:
                y = y + 1
                #print(row)

                if command == row[0]:
                    return row, y
                    
        async def findPlayer(rowy, player):
            row = rowy[0]
            y = rowy[1]
            
            x = 0
            for item in row:
                x = x + 1
                #print("row:" + str(row))
                #print("item:" + item)
                try:
                    player = ctx.guild.get_member(int(player[3:len(player)-1]))
                except:
                    pass
                    #at this point we know that whatever was passed as "player" isn't a mentioned user or ID, so we can just skip over it
                print("player: {}".format(str(player)))
                print("player ID: {}".format(str(player.id)))
                print(item.split("`")[0])
                
                try:   
                    if str(player.id) == item.split("`")[0]:
                        #
                        #x is the cell that contains the user's data in the following format: "user`wins`losses`" - "`" is a divider
                        
                        bar = item.split("`") 
                        return player, int(bar[1]), int(bar[2]), x, y
                except:
                    pass
                    #same reason as last try -> except catch

            #print("NOT FOUND, creating!")
            #try:
            foo = player.id
            #we need to see if the player exists but isn't in the database, or if they are not a plyer
            #print("PERSON")
            self.datasheet.update_cell(y,x+1,"{}`{}`{}".format(player.id,0,0))
            await ctx.send("**Welcome, {}, to ranked ;fight!** Battle other members of your server to increase your level (and maybe your K:D ratio!)! Higher levels will unlock special abilities and make you more resilient in combat. **NOTE, THIS ISN'T ADDED YET, BUT YOU CAN STILL GAIN LEVELS AND ALTER YOUR K:D.**\nAlso, note that this match is unranked!".format(player.mention))
            
            #print("YEA DONE")#, SLEEPING FOR 2")

        #print("rounds: " + rounds)      
        if int(rounds) > 11:
            v3 = True
            try:
                c1, wins1, losses1, x1, y1 = await findPlayer(findData("fight"),c1) #here c1 is redefined - if c1 is a mentioned user or a random string, this does nothing, however if a user ID is given it is converted into a user object which is more useful
                print("c1: {} {}:{}".format(c1,wins1,losses1))
            except:
                v3 = False
            try:
                c2, wins2, losses2, x2, y2 = await findPlayer(findData("fight"),c2)
                print("c2: {} {}:{}".format(c2,wins2,losses2))
            except:
                v3 = False

            
            
            
        else:
            x1,y1,x2,y2 = None,None,None,None #at least 12 rounds to slow grinding :)
            v3 = False
            


        #level is calculated using wins and losses, according to this equation: level = int(sqr((wins+(losses/4))/1.11) - this gives level 3 at 10 wins, or 40 losses

        try:
            kdratio1 = round(wins1/losses1,3)
        except:
            kdratio1 = 0

        try:
            level1 = int(math.sqrt(((wins1+1)+((losses1+1)/4)))/1.11)
        except:
            level1 = 0

        try:
            kdratio2 = round(wins2/losses2,3)
        except:
            kdratio2 = 0

        try:
            level2 = int(math.sqrt(((wins2+1)+((losses2+1)/4)))/1.11)
        except:
            level2 = 0

        print("STATS:\nP1:\nLevel: {}\nKD: {}\n\nP2:\nLevel: {}\nKD:{}".format(level1,kdratio1,level2,kdratio2))


        emb = discord.Embed(
            title = "**Fight - {} vs {} ({} rounds)**".format(c1,c2,rounds),
            type = "rich",
            description = desc,
            colour = 0x8cc43d,
            )
        if v3 == True:
            emb.add_field(name="Player Stats", value="**{}**:\n**Level**:{}\n**K/D Ratio**: {}\n\n\n**{}**:\n**Level**:{}\n**K/D Ratio**: {}".format(c1,level1,kdratio1,c2,level2,kdratio2))
        emb.set_thumbnail(url = "https://cdn.discordapp.com/attachments/447869090493890560/549653088659701770/fight.png")
        t = await ctx.send(embed = emb)


        while x != int(rounds):
            
            decide = random.randint(0,1)

            event.append(random.choice(["{} flailed their limbs out wildly at {}, causing some damage.\n",
                                    "{} screamed loudly at {}, making their ears bleed.\n",
                                    "{} points a gun at themselves, but somehow manages to shoot {}.\n",
                                    "{} threw a table at {}.\n",
                                    "{} threw a fridge at {}.\n",
                                    "{} dropped their mixtape, and {} got set on fire.\n",
                                    "{} dug a grave for {}, and threw them into it.\n",
                                    "{} offered {} some chewing gum, but it was actually rigged with explosives.\n",
                                    "{} slapped {} with a carp.\n",
                                    "{} fell on {}.\n",
                                    "{} called an airstrike on {}.\n",
                                    "{} destroyed {}.\n",
                                    "{} butchered {} with a rusty knife.\n",
                                    "{} threw {} into a pit of rotting fish.\n",
                                    "{} beheaded {}.\n",
                                    "{} laid LEGO around the feet of {}.\n",
                                    "{} collapsed {}.\n",
                                    "{} roasted {}.\n",
                                    "{} banned {}.\n",
                                    "{} mortally wounded {} by telling him the secrets of WoofBot's hardware.\n",
                                    ]))
                
            if decide == 1:
                c2count = c2count + 1
            else:
                c1count = c1count + 1
        
            #await ctx.send(event[x])

            x = x + 1
            await asyncio.sleep(2)
            if decide == 1:
                emb.description = "**ROUND {}**\n{}\n\n".format(x,event[x-1].format(c2,c1))
            else:
                emb.description = "**ROUND {}**\n{}\n\n".format(x,event[x-1].format(c1,c2))
            await t.edit(embed = emb)


        #End of rounds 

        


        if c1count > c2count:
            await ctx.send("The winner is {}!".format(c1))
            try:
                self.datasheet.update_cell(y1,x1,"{}`{}`{}".format(c1.id,wins1+1,losses1))
                self.datasheet.update_cell(y2,x2,"{}`{}`{}".format(c2.id,wins2,losses2+1))
            except:
                pass




        elif c1count < c2count:
            await ctx.send("The winner is {}!".format(c2))
            try:
                self.datasheet.update_cell(y2,x2,"{}`{}`{}".format(c2.id,wins2+1,losses2))
                self.datasheet.update_cell(y1,x1,"{}`{}`{}".format(c1.id,wins1,losses1+1))
            except:
                pass
            
        elif c1count == c2count:
            await ctx.send("It appears that {} and {} somehow managed to draw.".format(c1,c2))

    #'''
    @fight.error
    async def fight_error(self,ctx,err):
        
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing one or more arguments. Correct command format: `;fight [character] [character2] [number of rounds]`")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send("I did not recognise the number of rounds. Make sure it's an integer (whole number), and try again.")
    #'''
def setup(crdbot):
    
    crdbot.add_cog(Fight(crdbot))
