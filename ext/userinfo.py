from discord.ext import commands
import discord
import asyncio
import datetime
import aiohttp

class Userinfo(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot
        
    @commands.command()
    async def userinfo(self, ctx, *args):
        print(args)

        channel = ctx.message.channel
        user = ctx.message.author

        for arg in args:

            #oarg = arg
            print(arg," input")
            try:
                #identify an argument as a channel (working as of 11/11/2020)
                argchannel = int(arg[2:len(arg)-1])
            except:
                argchannel = None

            try:
            #if True:
                #identify a user by given ID, first checks the guild to see if the user is in the server and then tries an API call if not (not working as of 20/11/2020)
                print("attempting ID")
                try:
                    t_user = ctx.message.guild.get_member(int(arg))
                except:
                    t_user = await self.crdbot.fetch_user(int(arg))


                print("t_user is "+t_user)
                if t_user != None:
                    user = t_user
                print(user)
                
            except:#Exception as e:
                #print(e)
                pass
                
            try:
                #identify a user by mention, first checks the guild to see if the user is in it and then tries an API call if not (not working as of 20/11/2020)
                print("attempting mention")
                argmember = int(arg[3:len(arg)-1])
                print(argmember)

                try:
                    
                    t_user = ctx.message.guild.get_member(argmember)
                    print("got")
                    print(t_user)
                except:
                    
                    t_user = await self.crdbot.fetch_user(argmember)
                    print("got2")
                    
                if isinstance(t_user, discord.User):
                    print("yea")
                    user = t_user

                print(user)
            except:
                pass

                
                #arg1 = False
            #print(arg1)
            #if isinstance(arg1, discord.Member):
                #print(arg1," is a member!")
            #    user = arg1
            print("user is: "+str(user))
            t_channel = self.crdbot.get_channel(argchannel)
            if isinstance(t_channel, discord.TextChannel):
                channel = t_channel

        print("channel:{}".format(channel))
        print("member:{}".format(user))
        
        om1 = False
        #userid = ctx.message.content[10:len(ctx.message.content)]
        '''
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

        '''
        #get activity
        try:
            if om1 == True:
                messages = await channel.history(limit=10000).flatten()#await ctx.message.channel.history(limit=10000).flatten()
            else:
                messages = await channel.history(limit=1000).flatten()#ctx.message.channel.history(limit=1000).flatten()
        except discord.errors.Forbidden:
            await ctx.send("Error, missing permissions to read {}.".format(channel))
            return

        #get history statistics
        
        messageCount = 0
        for message in messages:
            if message.author == user:
                messageCount = messageCount + 1
        if om1 == True:
            activity = messageCount/100
        else:
            activity = messageCount/10
        
        rolestring = "\n"
        not_in_server = False
        
        try:
            for role in user.roles:
                rolestring = rolestring + str(role.mention) + "\n"
        except:
            rolestring = None
            not_in_server = True

        try:
            joindays = str((datetime.datetime.utcnow() - user.joined_at).days)[0:19]
            jointime = str(user.joined_at).replace(" "," at ")[0:19] + " (UTC+0) ({} days ago)".format(joindays)
        except:
            jointime = None
            joindays = None
            
            
        #delta =  
        emb = discord.Embed(title = "{}".format(user),
        type = "rich",
        colour = user.color#0x8cc43d,

        #url = "output.p,
        )

        if not_in_server:
            emb.description = "**Account Creation Date**: {} ({} days ago)\nThis user is not in the server!".format(
            (str(discord.utils.snowflake_time(user.id)).replace(" "," at "))[0:19] + " (UTC+0)",
            str((datetime.datetime.utcnow() - discord.utils.snowflake_time(user.id)).days),
            
            )
            
            
        else:
            emb.description = "**Account Creation Date**: {} ({} days ago)\n**Join Date**: {}\n**Roles**: {}\n**Activity** (your messages per 1000 messages in {}): {}%\n".format(
            (str(discord.utils.snowflake_time(user.id)).replace(" "," at "))[0:19] + " (UTC+0)",
            str((datetime.datetime.utcnow() - discord.utils.snowflake_time(user.id)).days),
            jointime,
            rolestring,
            "#"+str(channel),
            activity
            )   
        '''
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}".format(user)) as r:
                if r.status == 200:
                    file = await r.read()
                    #print(file)
                    with open("input.png", "wb") as f:
                        f.write(file)
        '''
        #print("ok")
        emb.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}".format(user))#"attachment://input.png")
        #f = discord.File("input.png", filename="input.png")
        await ctx.send(embed=emb)#, file=f)
        '''


            emb.set_image(url="attachment://output.png")
            f = discord.File("output.png", filename="output.png")
            endTime = int(round(time.time() * 1000))
            emb.description = "Response time: {}ms\nImage generation time: {}ms".format(endTime-startTime,L2Presponsetime)
            await ctx.send(file=f,embed=emb)
        '''
    '''
    @userinfo.error
    async def userinfo_error(self, ctx, err):

        if isinstance(err, commands.CommandInvokeError):
            await ctx.send("Incorrect command format. See `;help userinfo`.")
    '''

def setup(crdbot):

    crdbot.add_cog(Userinfo(crdbot))
