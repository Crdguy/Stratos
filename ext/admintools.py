from discord.ext import commands
import discord
import asyncio

class Purge(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot


        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, num):
        if True:#str(ctx.message.author.id) in config["General Settings"]["admins"]:

            user = None
            base = ";purge "+num
            
            if ctx.message.mentions:
                user = ctx.message.mentions[0]

            else:
                try:
                    userid = int(ctx.message.content[len(base)+1:len(ctx.message.content)])
                    user = ctx.message.guild.get_member(userid)
                except ValueError:
                    user = None

            try:
                num = int(num)
                if num < 1:
                    d = await ctx.send("Error, your input was less than 1.")
                    return

                
                if user == None:
                    d = await ctx.message.channel.purge(limit = num+1)
                    await ctx.send("{} messages are now ashes!".format(len(d)-1),delete_after=5)

                else:
                    def is_user(msg):
                        return msg.author == user
                        
                    d = await ctx.message.channel.purge(limit = num+1, check=is_user)
                    await ctx.send("Deleted {} messages by {}.".format(len(d),user),delete_after=5)

                
            except ValueError:
                await ctx.send("Error, your input was not a number.")
            except discord.errors.Forbidden:
                try:
                    await ctx.send("Error, I do not have the permissions to perform this command.")
                except discord.errors.Forbidden:
                    print("Unable to send messages in {0.message.channel.name}, server {0.message.server.name}!".format(ctx))


    @purge.error
    async def purge_error(self, err, ctx):
        
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing an argument. Correct command format: `;purge [x] [optional: user]` where `x` is the number of messages to delete. For further info (especially on the `user` argument) do `;help purge`.")

class Ban(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx):

        #await ctx.send("This is a test. If you are seeing this message, you have the permission to ban users. What? What made you think I would do it?")
        
        base = ";ban "

        if ctx.message.mentions:
            banuser = ctx.message.mentions[0].id

        
        else:
            try:
                banuser = int(ctx.message.content[len(base):len(base)+18])
            except ValueError:
                await ctx.send("Missing one or more arguments. Correct command format: `;ban [user] [reason]`, where `user` is a mentioned user or ID. Do `;help ban` for more information.")
                return

        try:
            reason = ctx.message.content.split(" ")[2]
        except:
            reason = False



        msg = await ctx.message.channel.send("Banning {}. To confirm this action, please react the number of days of {}s messages that should be purged.".format(banuser,banuser))
        await msg.add_reaction("0⃣")
        await msg.add_reaction("1⃣")
        await msg.add_reaction("2⃣")
        await msg.add_reaction("3⃣")
        await msg.add_reaction("4⃣")
        await msg.add_reaction("5⃣")
        await msg.add_reaction("6⃣")
        await msg.add_reaction("7⃣")
        #msg2 = await ctx.fetch_message(msg.id)
        await asyncio.sleep(2)
        #reactsO = msg2.reactions
        while msg:
        #async for y in reactsO[0].users():
        

            react2 = await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji in ["0⃣","1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣"])
            #print("yea react")
            msg2 = await ctx.fetch_message(msg.id)
            
            reacts = msg2.reactions


            async for y in reacts[0].users():
                print(">0<")
                if ctx.message.author == y:
                    #print("delet")
                    delete = 0

            async for y in reacts[1].users():
                print(">1<")
                if ctx.message.author == y:
                    #print("delet")
                    delete = 1

            async for y in reacts[2].users():
                if ctx.message.author == y:
                    delete = 2

            async for y in reacts[3].users():
                if ctx.message.author == y:
                    delete = 3

            async for y in reacts[4].users():
                if ctx.message.author == y:
                    delete = 4

            async for y in reacts[5].users():
                if ctx.message.author == y:
                    delete = 5

            async for y in reacts[6].users():
                if ctx.message.author == y:
                    delete = 6

            async for y in reacts[7].users():
                if ctx.message.author == y:
                    delete = 7

            

            try:
                if reason == False:
                    #print("reason ban")
                    #print(delete)
                    await ctx.guild.ban(discord.Object(id=banuser),reason="Banned using the ;ban command. No reason was specified.",delete_message_days=delete)
                else:
                    #print("no reason ban")
                    #print(delete)
                    await ctx.guild.ban(discord.Object(id=banuser),reason=reason,delete_message_days=delete)
                    
            except discord.errors.Forbidden:
                await ctx.send("Error, I do not have the permissions to perform this command.")
                return
            except discord.errors.NotFound:
                await ctx.send("Error, it does not appear that the ID you specified is a user. Try again.")
                return
            
            await ctx.send("The hammer has been swung on {}. I hope you meant to do that.".format(banuser))

            msg = False
            msg2 = False
    #'''
    '''
    @ban.error
    async def ban_error(self, err,ctx):

        if isinstance(err,commands.CommandInvokeError):
            await ctx.send("h")

    '''
    

def setup(crdbot):

    crdbot.add_cog(Purge(crdbot))
    crdbot.add_cog(Ban(crdbot))
