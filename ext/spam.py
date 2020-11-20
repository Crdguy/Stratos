from discord.ext import commands
import discord
import asyncio
import requests
import time
import configparser

#open "stratos.ini"
try:
    config = configparser.ConfigParser()
    config.read('stratos.ini')

except Exception:
    input("Error, something went wrong while parsing 'stratos.ini'. Ensure the file is not corrupt or missing.")
    exit(0)

class Spam(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def brap(self, ctx, n):
        
        n = int(n)
        x = 0
        while x != n:
            await ctx.send(open("brap.txt","r").read())
            x = x + 1


    @commands.Cog.listener()
    async def on_message(self, message):
        if "destroy their religion" in message.content:
            await message.channel.send("As you wish, Captain. All ye of little faith, succumb to the eternal darkness of P U R G E. Only in the darkest abyss will you see the light of Rusted Warfare.")

        '''
        if message.content.startswith(";b "):
            if message.channel.id == 368110030198800396:
                try:
                    num = int(message.content[2:len(message.content)])
                except:
                    await message.channel.send("Incorrect syntax. Correct command format: `;b [beats]`.")
                    return

                beatmessage = "bum "
                for x in range(num-1):
                    beatmessage = beatmessage + "bum "
                try:
                    
                    x = 0
                    while x != 19:
                        await asyncio.sleep(8)
                        await message.channel.send(beatmessage)
                        x = x + 1
                except discord.errors.HTTPException:

                    await message.channel.send("Nope. Max length is 500.")
        '''

        '''
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

        '''

def setup(crdbot):

    crdbot.add_cog(Spam(crdbot))
