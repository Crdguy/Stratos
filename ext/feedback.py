from discord.ext import commands
import discord
import asyncio
import csv

class Feedback(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.command()
    async def feedback(self, ctx):
        if "@everyone" not in ctx.message.content.lower() and "@here" not in ctx.message.content.lower():
            await ctx.send("Thanks for the feedback!")
            data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
            for line in data:
                if line[0] == "X000":
                    line[1] = ctx.message.guild.id
                    line[2] = ctx.message.channel.id
                    line[3] = ctx.message.author.id
                    line[4] = ctx.message.content[10:len(ctx.message.content)]
                    writer = csv.writer(open("allinfodump.csv","w",newline=""))
                    writer.writerows(data)

            reportchannel = self.crdbot.get_channel(572850938558021659)
            await reportchannel.send("**Server**: {0.guild} [ID: {0.guild.id}]\n**Channel**: #{0.channel} [ID: {0.channel.id}]\n**User**: {0.author.mention} [ID: {0.author.id}]\n**Feedback**:\n`{1}`".format(ctx.message,ctx.message.content[10:len(ctx.message.content)]))
        else:
            await ctx.send("You're not funny. If I had a flesh vessel I would tear every limb from your body and drink your blood.")

    @commands.command()
    async def reply(self, ctx):
        if ctx.message.author.id == 186069912081399808:
            print("1")
            message = ctx.message.content[7:len(ctx.message.content)]
            data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
            print("2")
            for line in data:
                if line[0] == "000":
                    channel = line[2]
                    author = line[3]
                    content = line[4]
                    break
                
            replychannel = self.crdbot.get_channel(int(channel))
            author = self.crdbot.get_user(int(author))

            await replychannel.send("{}, your feedback '`{}`' got a reply from Crdguy!\nMessage:\n`{}`".format(author.mention,content,message))
            await ctx.send("✅ reply sent!")


def setup(crdbot):

    crdbot.add_cog(Feedback(crdbot))
