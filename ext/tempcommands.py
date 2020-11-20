from discord.ext import commands
import discord
import random

class RandomStars(commands.Cog):
    
    def __init__ (self, crdbot):
        self.crdbot = crdbot

    @commands.Cog.listener()
    async def on_message(self, message):
        odds = random.randint(1,750)
        if odds == 42:
           # print("YTEAH")
            #print(message.author)
            channellist = [294511987684147212,294513542076432394,671045376115081226,297653682965839873]
            #channellist = [533006206025859082]
            
            
            
            def thecheck():
                good = False
                for channel in channellist:
                    print(channel)
                    if message.channel.id == channel:
                        #print("yess")
                        return True
                return False

            epic = thecheck()
            if epic == False:
                return
            #print("epic is {}".format(epic))
            
            #str(message.author.id) == "186069912081399808":
            #    print("thing happened")
            if message.author.dm_channel == None:
                message.author.dm_channel = await message.author.create_dm()

            with open("10starcodes.txt", "r") as codesfile:
                codeslist = list(codesfile)
                code = codeslist.pop()
                #print(code)

            with open("10starcodes.txt", "w") as codesfile:
                for item in codeslist:
                    #print(item)
                    codesfile.write("{}".format(item))
            
            if "\n" in code:
                code = code[0:len(code)-1]
                
            await message.author.dm_channel.send("Congratulations! As part of the 2000 update on the Event Horizon Server there is a small chance that talking in any on-topic channel will give you a 10 star code.\nYou have won a 10<:stars:579008424444952577> code, which can be redeemed in Event Horizon. Your code is **{}**! Happy spending.\n\nTo redeem your code, open up Event Horizon, and tap the top left of the screen until a keypad appears. Enter your code into the keypad and your current save will get 10 stars.\n\nYes, this is legit. You can contact my developer Crdguy#9939 if you have any questions.".format(code))
            print("sent  a code")

def setup(crdbot):
    crdbot.add_cog(RandomStars(crdbot))
