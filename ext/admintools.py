from discord.ext import commands
import discord
import asyncio
import csv

class Purge(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot


        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, num=None, user=None, before_message_id=None):

        
        if user:
            if ctx.message.mentions:
                user = ctx.message.mentions[0]
            else:
                user = ctx.message.guild.get_member(int(user))

        if num == None:
            if before_message_id:
                before = fetch_message(int(before_message_id))
            else:
                await ctx.send("Missing an argument. Correct command format: `;purge [x] [optional: user]` where `x` is the number of messages to delete. For further info (especially on the `user` argument) do `;help purge`.")
                return
            
        else:
            #a number is specified
            before = None
            
            if int(num) > 50:
                msg = await ctx.send("You are about to purge {} messages. React with ✅ to confirm and purge. Otherwise, wait 60 seconds for this message to time out.".format(num))
                await msg.add_reaction("✅")
                def usertest(reaction, reactor):
                    return reactor == ctx.message.author and str(reaction.emoji) == "✅" 

                try:
                    reaction, reactor = await self.crdbot.wait_for("reaction_add", timeout=60.0, check = usertest)
                    
                except asyncio.TimeoutError:
                    await ctx.send("Message timed out.")
                    return

                
            
        
            
        try:
            num = int(num)
            if num < 1:
                await ctx.send("Error, your input was less than 1.")
                return

            '''          
            if user == None:
                messages = await ctx.message.channel.purge(limit = num+1)
                await ctx.send("{} messages are now ashes!".format(len(messages)-1),delete_after=5)

            if user == True:
            '''
            def is_user(msg):
                if user:
                    return msg.author == user
                else:
                    return True
                
            messages = await ctx.message.channel.purge(limit = num+1, check=is_user, before=before)

            if user:
                await ctx.send("Deleted {} messages by {}.".format(len(messages),user),delete_after=5)
            else:
                await ctx.send("{} messages are now ashes!".format(len(messages)-1),delete_after=5)

            
        except ValueError:
            await ctx.send("Error, your input was not a number.")
        except discord.errors.Forbidden:
            try:
                await ctx.send("Error, I do not have the permissions to perform this command.")
            except discord.errors.Forbidden:
                print("Unable to send messages in {0.message.channel.name}, server {0.message.server.name}!".format(ctx))

    '''
    @purge.error
    async def purge_error(self, err, ctx):
        
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing an argument. Correct command format: `;purge [x] [optional: user]` where `x` is the number of messages to delete. For further info (especially on the `user` argument) do `;help purge`.")
    '''

class Filter(commands.Cog):

    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.group()
    async def filter(self, ctx):
         if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a subcommand.\nAvailable subcommands: `check`, `add`, `remove`.\n See `;help filter` for more information.")    


    @filter.command()
    @commands.has_permissions(manage_messages=True)
    async def check(self, ctx):
        #filters are assigned line 3 of the allinfodump.csv file: that is, X002
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))

        guild_id = None
        
        for line in data:
            if line[0] == "X002":
                for item in line:
                    if item.split("~")[0] == str(ctx.guild.id):
                        guild_id, block_content = item.split("~") 
                        block_content = block_content.split("+")
        #syntax example: X002,530780654133051453:Text - foo+Text - bar+User - foobar,
        if guild_id == None:
            await ctx.send("No filters are active for this server. You can configure them with ;filter add. See ;help filter for more information.")

        else:
            await ctx.send("There are currently {} filters active in this server: {}".format(len(block_content), block_content))

    @filter.group()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a subcommand.\nAvailable subcommands: `text`, `user`.\n See `;help filter` for more information.") 

    @add.command()
    @commands.has_permissions(manage_messages=True)
    async def text(ctx):

        new_filter = "Text - " + ctx.message.content.lower()[17:len(ctx.message.content)]
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
        guild_id = None
        lineno = -1
        itemno = -1
        
        for line in data:
            #X000,294511987684147212,294514668699910145,443414082750775298,ck I ate all the piss earlier
            #X001,530780654133051453:750360059694809171,697060463497969674:697060465695522840,294511987684147212:750843146115743846
            #X002,530780654133051453:Text - foo
            lineno += 1
            
            if line[0] == "X002":
                #X002,530780654133051453:Text - foo
                
                for item in line:
                    itemno += 1
                    #X002
                    #530780654133051453:Text - foo
                    
                    if item.split("~")[0] == str(ctx.guild.id):
                        #530780654133051453:Text - foo
                        guild_id, block_content = item.split("~") 
                        block_content_list = block_content.split("+")

                        if new_filter not in block_content_list:
                            block_content = block_content + "+" + new_filter

                        else:
                            await ctx.send("This filter has already been added! You can remove it with ;filter remove text.")
                            return

                        item = guild_id + "~" + block_content
                        data[lineno][itemno] = item
                        writer = csv.writer(open("allinfodump.csv","w",newline=""))
                        writer.writerows(data)

                        await ctx.send("Filter added successfully!")
                        return
                    
                line.append(str(ctx.guild.id) + "~" + new_filter)
                writer = csv.writer(open("allinfodump.csv","w",newline=""))
                writer.writerows(data)
                await ctx.send("Filter created successfully!")
                
                                                
    @add.command()
    @commands.has_permissions(manage_messages=True)
    async def user(ctx):

        new_filter = "User - " + ctx.message.content.lower()[17:len(ctx.message.content)]
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
        guild_id = None
        lineno = -1
        itemno = -1
        
        for line in data:
            lineno += 1
            
            if line[0] == "X002":
                
                for item in line:
                    itemno += 1

                    if item.split("~")[0] == str(ctx.guild.id):
                        guild_id, block_content = item.split("~") 
                        block_content_list = block_content.split("+")

                        if new_filter not in block_content_list:
                            block_content = block_content + "+" + new_filter

                        else:
                            await ctx.send("This filter has already been added! You can remove it with ;filter remove user.")
                            return

                        item = guild_id + "~" + block_content
                        data[lineno][itemno] = item
                        writer = csv.writer(open("allinfodump.csv","w",newline=""))
                        writer.writerows(data)

                        await ctx.send("Filter added successfully!")
                        return
                    
                line.append(str(ctx.guild.id) + "~" + new_filter)
                writer = csv.writer(open("allinfodump.csv","w",newline=""))
                writer.writerows(data)
                await ctx.send("Filter created successfully!")
                            
            


    @filter.group()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a subcommand.\nAvailable subcommands: `text`, `user`.\n See `;help filter` for more information.") 

    @remove.command()
    @commands.has_permissions(manage_messages=True)
    async def text(self, ctx):

        remove_filter = "Text - " + ctx.message.content.lower()[20:len(ctx.message.content)]
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
        guild_id = None
        lineno = -1
        itemno = -1
        filterno = -1
        #print("gonna remove {}".format(remove_filter))
        
        for line in data:
            lineno += 1
            
            if line[0] == "X002":
                #X002,530780654133051453:Text - foo
                
                for item in line:
                    itemno += 1
                    #X002
                    #530780654133051453:Text - foo
                    if item.split("~")[0] == str(ctx.guild.id):
                        #print(item)

                        if remove_filter + "+" in item:
                            item2 = item
                            item2 = item2.replace(remove_filter + "+", "")
                            #print(item2)

                            data[lineno][itemno] = item2
                            writer = csv.writer(open("allinfodump.csv","w",newline=""))
                            writer.writerows(data)
                            await ctx.send("Filter removed successfully!")
                            return
                        
                        elif item.split("~")[1] == remove_filter:

                            data[lineno][itemno] = ""
                            writer = csv.writer(open("allinfodump.csv","w",newline=""))
                            writer.writerows(data)
                            await ctx.send("Filter removed successfully!")
                            return                           
              
                                                
                await ctx.send("This filter does not exist!")
                return

                            

    @remove.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx):

        remove_filter = "User - " + ctx.message.content.lower()[20:len(ctx.message.content)]
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
        guild_id = None
        lineno = -1
        itemno = -1
        filterno = -1
        
        for line in data:
            lineno += 1
            
            if line[0] == "X002":
                #X002,530780654133051453:Text - foo
                
                for item in line:
                    itemno += 1
                    #X002
                    #530780654133051453:Text - foo
                    if item.split("~")[0] == str(ctx.guild.id):

                        if remove_filter + "+" in item:
                            item2 = item
                            item2 = item2.replace(remove_filter + "+", "")

                            data[lineno][itemno] = item2
                            writer = csv.writer(open("allinfodump.csv","w",newline=""))
                            writer.writerows(data)
                            await ctx.send("Filter removed successfully!")
                            return
                        
                        elif item.split("~")[1] == remove_filter:

                            data[lineno][itemno] = ""
                            writer = csv.writer(open("allinfodump.csv","w",newline=""))
                            writer.writerows(data)
                            await ctx.send("Filter removed successfully!")
                            return                           
              
                                                
                await ctx.send("This filter does not exist!")
                return



    #listener events
    @commands.Cog.listener()
    @commands.has_permissions(manage_messages=False)
    async def on_message(self, message):

        if message.author == self.crdbot.user:
            return

        #if message.author == crdbot.user:
        #    return
        
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
        

        #this assumes that any entries are not the id of some server, so if you tried to filter out a server id (for whatever reason) this would not work. however, it is necessary because I am lazy and python is slow
        #this code has to be as performant as possible!
        if str(message.guild.id) in str(data):

            for item in data[2]:
                item_split = item.split("~")

                if item_split[0] == str(message.guild.id):
                    item_split.pop(0)
                    
                    for server_filter in item.split("+"):
                        server_filter = server_filter[7:len(server_filter)]

                        if server_filter in message.content.lower():
                            print("yea")
                            await message.delete()
            


        
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
    crdbot.add_cog(Filter(crdbot))
