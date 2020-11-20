from discord.ext import commands
import discord
import asyncio
import requests
import time

class MClookup(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot
            
    @commands.command()
    async def mclookup(self, ctx, username):

        info = requests.get("https://mc-heads.net/minecraft/profile/{}".format(username)).json()

        names = ""

        for item in info["name_history"]:
            print(item)
            for x, y in item.items():

                if x == "name":
                    names = names + y
                elif x == "changedToAt":
                    print(int(y))
                    timeObject = time.gmtime(int(y)/1000)
                    #"{0[2]}/{0[1]}/{0[0]} (DD/MM/YYYY) at {0[3]}:{0[4]}"
                    updateTime = "{}/{}/{} (DD/MM/YYYY) at {}:{}".format(timeObject[2],timeObject[1],timeObject[0],timeObject[3],timeObject[4])
                    names = names + " (as of {} GMT+0)\n".format(updateTime)
                print(x)
                print(y)

        #names = 0

        emb = discord.Embed(title = "Direct download", url = "https://mc-heads.net/download/{}".format(username),
        description = "**Name History**:\n\n".format(names),
        type = "rich",
        colour = 0x8cc43d,
        )

        emb.set_thumbnail(url="https://mc-heads.net/head/{}".format(username))
        emb.set_author(name=username)
        emb.set_image(url="https://mc-heads.net/body/{}".format(username))
        emb.set_footer(text="Avatars provided by MCHeads!")
        await ctx.send(embed=emb)

def setup(crdbot):

    crdbot.add_cog(MClookup(crdbot))
