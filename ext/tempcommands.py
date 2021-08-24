from discord.ext import commands
import re
import asyncio
import discord
import random
from typing import List

class RandomStars(commands.Cog):
    
    def __init__ (self, crdbot):
        self.crdbot = crdbot

    @commands.command()
    async def minute_timer(self, ctx, minutes):
    #assumes minutes is int
        minutes = int(minutes)

        msg = await ctx.send("Timer started: {} minutes remaining".format(minutes))

        #every minute, the message is edited with how many minutes remain
        while minutes > 0:
            await asyncio.sleep(5) #sleep for 60 seconds, using async so multiple commands can be processed at the same time
            minutes = minutes - 1
            await msg.edit(content="{} minutes remaining".format(minutes))

        await msg.edit(content="Timer's up!")

    '''
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
    '''


class EHComp21(commands.Cog):

    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.command()
    @commands.is_owner()
    async def ehcomp(self, ctx: commands.Context):
        """
        Provided by Eneg()#8410 (190505392504045570)
        """
        channel = ctx.bot.get_channel(294514080272613377)
        assert isinstance(channel, discord.TextChannel)

        emojis = ('<:epix:598275090840551474>', '<:broepix:688682287751364608>', '<:epic:730435572396458014>')

        message = await channel.fetch_message(874633053320917033)

        reactions: List[discord.Reaction] = []

        for reaction in message.reactions:
            if isinstance(reaction.emoji, str):
                continue

            if reaction.emoji.name in {'epix', 'broepix', 'epic'}:
                reactions.append(reaction)

        epix, broepix, epic = reactions
        assert str(epix.emoji) == emojis[0]
        assert str(broepix.emoji) == emojis[1]
        assert str(epic.emoji) == emojis[2]

        epix_users = await epix.users().flatten()
        # everyone can participate so no filters applied
        epix_winner = random.choice(epix_users)

        major_staff_roles_id = {415922791913750530, 294512832190349312, 592028643044229150, 294512708613832704}

        assert ctx.guild is not None

        broepix_members = []

        async for user in broepix.users():
            member = await ctx.guild.fetch_member(user.id)
            print(member)

            if member is not None:
                broepix_members.append(member)

        broepix_winner = random.choice(broepix_members)

        colonel_brig_ids = {565580766285791252, 294512832190349312}

        epic_users = [
            member
            async for user in epic.users()
            if (member := await ctx.guild.fetch_member(user.id)) is not None
            if any(role.id in colonel_brig_ids for role in member.roles)
        ]

        epic_winner = random.choice(epic_users)

        string = (
            f'{epix_winner.mention} won {emojis[0]} lottery'
            f'\n{broepix_winner.mention} won {emojis[1]} lottery'
            f'\n{epic_winner.mention} won {emojis[2]} lottery'
        )

        await ctx.send(string, allowed_mentions=discord.AllowedMentions.none())



class Listener(commands.Cog):

    # listener events

    @commands.Cog.listener()
    @commands.has_permissions(manage_messages=False)
    async def on_message(self, message):

        # temporary - remove messages in cd that are counting (temp feature for EH)

        if message.channel.id == 368110030198800396 or message.channel.id == 750340224973930647:
            if re.match(r"[0-9]{2,9}", message.content):
                await message.delete()

        if message.guild.id == 294511987684147212:
            if re.match(r"(https://media.discordapp.net/attachments/)[0-9]{18}/[0-9]{18}/.+.\.(?:mov|webm|mp4)", message.content):

                link = None
                for match in re.finditer(r"(https://media.discordapp.net/attachments/)[0-9]{18}/[0-9]{18}/.+.\.(?:mov|webm|mp4)", message.content):
                    link = str(message.content)[match.start():match.end()].replace("://media", "://cdn").replace("pp.net/at", "pp.com/at")

                if link:
                    await message.channel.send("Media link detected! Media links only play in a browser. Here is the properly embedded CDN link: " + link, allowed_mentions=discord.AllowedMentions.none())


def setup(crdbot):
    crdbot.add_cog(RandomStars(crdbot))
    crdbot.add_cog(Listener(crdbot))
    crdbot.add_cog(EHComp21(crdbot))
