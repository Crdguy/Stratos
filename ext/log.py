from discord.ext import commands
import discord
import asyncio
import requests
import csv

class Log(commands.Cog):

    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.group()
    @commands.has_permissions(manage_channels=True)
    async def log(self, ctx):
        '''
        Group for log-related commands.
        '''
        if ctx.invoked_subcommand is None:
           await ctx.send("Please provide a subcommand.")

    @log.command()
    async def setchannel(self, ctx):
        '''
        Sets the channel logs are dumped to, to the one the command is run in. If no channel is specified logs will not be created.
        Takes no arguments.
        '''
        print("A")
        channel_id = str(ctx.message.channel.id)
        print("B")
        #we use code X001 for log channels
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
        print("C")
        
        for line in data:
            
            if line[0] == "X001":
                #find the line with the log code
                x = 0
                for instance in line:
                    
                    print(instance.split(":")[0])
                    if str(ctx.message.guild.id) == instance.split(":")[0]:
                        print("MATCH! index: {}".format(x))
                        del line[x]
                        line.insert(x,"{}:{}".format(str(ctx.message.guild.id),channel_id))
                        writer = csv.writer(open("allinfodump.csv","w",newline=""))
                        writer.writerows(data)
                        await ctx.send("Log channel updated!")
                        return

                        #there is already an entry for this server so we will overwrite
                    x = x + 1

                #if the code gets here it didn't find the server in the info dump csv, so let's make a new entry
                line.append(str(ctx.message.guild.id)+":"+channel_id)
                await ctx.send("Log channel selected!")
                writer = csv.writer(open("allinfodump.csv","w",newline=""))
                writer.writerows(data)
        
        
                #writer = csv.writer(open("allinfodump.csv","w",newline=""))
                #writer.writerows(data)


    async def sendlog(self, server_id, content):
        '''
        Small function that sends logs when called by another function to their respective server.
        '''
        data = list(csv.reader(open("allinfodump.csv","r"),delimiter=","))
        for line in data: 
            if line[0] == "X001":
                for instance in line:  
                    print(instance.split(":")[0])
                    if str(server_id) == instance.split(":")[0]:
                        logchannel = self.crdbot.get_channel(int(instance.split(":")[1]))
                        
        try:         
            await logchannel.send(embed=content)
        except:
            #no log channel
            return

    #log events, I don't think these can be added to a group
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return


        emb = discord.Embed(
                title = "Message Edit",
                type = "rich",
                description = "[Click to jump]({})".format(after.jump_url),
                colour = 0x0388fc,
                )

        emb.set_author(name=before.author, icon_url=before.author.avatar_url)
        emb.add_field(name="Before",value=before.content, inline=False)
        emb.add_field(name="After",value=after.content, inline=False)
        if before.content == after.content:
            pass
        else:
            emb.add_field(name="Additional Information",value="User ID: {0.author.id}\nMessage ID: {0.id}\nChannel ID: {0.channel.id}".format(before),inline=False)
            
        emb.add_field(name="Channel",value=before.channel.mention, inline=False)
        
        
        await Log.sendlog(self, str(before.guild.id), emb)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        
        emb = discord.Embed(
                title = "Message Deleted",
                type = "rich",
                colour = 0xf0280a,
                )

        emb.set_author(name=message.author, icon_url=message.author.avatar_url)
        emb.add_field(name="Content",value=message.content, inline=False)
        emb.add_field(name="Channel",value=message.channel.mention, inline=False)
        emb.add_field(name="Additional Information",value="User ID: {0.author.id}\nMessage ID: {0.id}\nChannel ID: {0.channel.id}".format(message),inline=False)
        
        await Log.sendlog(self, str(message.guild.id), emb)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        audit = True
        try:
            async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete):

                #compare ids because channels probably won't be identical
                if entry.target.id == channel.id and entry.action == discord.AuditLogAction.channel_delete:
                    #print("mhm")
                    
                    user = entry.user
                    break
        except:            
            audit = False
   
        emb = discord.Embed(
                title = "Channel Deleted",
                type = "rich",
                colour = 0xf0280a,
                )

        emb.add_field(name="Channel",value="#"+channel.name, inline=False)
        
        if audit == True:
            emb.set_author(name=user, icon_url=user.avatar_url)
            emb.add_field(name="Additional Information",value="User ID: {0.id}\nChannel ID: {1.id}".format(user,channel,inline=False))
        
        else:
            emb.add_field(name="Missing Permissions",value="Missing audit log permissions! Some data will be missing.",inline=False)
            emb.add_field(name="Additional Information",value="Channel ID: {}".format(channel.id),inline=False)
        
        await Log.sendlog(self, str(channel.guild.id), emb)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        audit = True
        try:
            async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create):

                #compare ids because channels probably won't be identical
                if entry.target.id == channel.id and entry.action == discord.AuditLogAction.channel_create:
                    #print("mhm")
                    
                    user = entry.user
                    break
        except:            
            audit = False
   
        emb = discord.Embed(
                title = "Channel Created",
                type = "rich",
                colour = 0xf0280a,
                )

        emb.add_field(name="Channel",value="#"+channel.name, inline=False)
        
        if audit == True:
            emb.set_author(name=user, icon_url=user.avatar_url)
            emb.add_field(name="Additional Information",value="User ID: {0.id}\nChannel ID: {1.id}".format(user,channel,inline=False))
        
        else:
            emb.add_field(name="Missing Permissions",value="Missing audit log permissions! Some data will be missing.",inline=False)
            emb.add_field(name="Additional Information",value="Channel ID: {}".format(channel.id),inline=False)
        
        await Log.sendlog(self, str(channel.guild.id), emb)        

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        audit = True
        #try:

        emb = discord.Embed(
                title = "Channel Updated",
                type = "rich",
                colour = 0x0388fc,
                )

        try:
            async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update):
                if entry.target.id == before.id and entry.action == discord.AuditLogAction.channel_update:
                    user = entry.user

                    print(entry)
                    print(entry.changes)

                    print(entry.changes.before)
                    #print(str(entry.changes.before.topic))


                    if hasattr(entry.changes.before, "name"):
                        emb.add_field(name="Channel Name",value="Before: {0.before.name}\nAfter: {0.after.name}".format(entry.changes),inline=False)
                                        
                    if hasattr(entry.changes.before, "type"):
                        emb.add_field(name="Channel Type",value="Before: {0.before.type}\nAfter: {0.after.type}".format(entry.changes),inline=False)

                    #position and overwrites cause the bot to read off the last log
                        
                    #if hasattr(entry.changes.before, "position"):
                    #    emb.add_field(name="Channel Position",value="Before: {0.before.position}\nAfter: {0.after.position}".format(entry.changes),inline=False)
                                        
                    if hasattr(entry.changes, "overwrites"):
                        emb.add_field(name="Overwrites",value="Placeholder")
                        #embed.add_field(name="Channel Overwrites",value="Before:\n{0.before.}\nAfter: {0.after.}".format(entry.changes),inline=False)
                                        
                    if hasattr(entry.changes.before, "topic"):
                        emb.add_field(name="Channel Topic",value="Before: {0.before.topic}\nAfter: {0.after.topic}".format(entry.changes),inline=False)
                                        
                    if hasattr(entry.changes.before, "bitrate"):
                        emb.add_field(name="Channel Bitrate",value="Before: {0.before.bitrate}kbps\nAfter: {0.after.bitrate}kbps".format(entry.changes),inline=False)

                    break
        except:
            audit = False
        
        if audit == True:
            emb.set_author(name=user, icon_url=user.avatar_url)
            emb.add_field(name="Additional Information",value="User ID: {0.id}\nChannel ID: {1.id}".format(user,after),inline=False)
        
        else:
            emb.add_field(name="Missing Permissions",value="Missing audit log permissions! Some data will be missing.",inline=False)
            emb.add_field(name="Additional Information",value="Channel ID: {}".format(after.id),inline=False)
        
        await Log.sendlog(self, str(after.guild.id), emb)
        
    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):

        emb = discord.Embed(
                
                type = "rich",
                colour = 0xf0280a,
                )
        #try:
        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_create):
            print(entry)

            if entry.action == discord.AuditLogAction.webhook_create:
                user = entry.user
                web_name = entry.after.name
                emb.title = "Webhook Created"

        
        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_update):
            print(entry)
            if entry.action == discord.AuditLogAction.webhook_update:
                user = entry.user
                web_name = entry.after.name
                emb.title = "Webhook Updated"        

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_delete):
            print(entry)
            if entry.action == discord.AuditLogAction.webhook_delete:
                user = entry.user
                web_name = entry.after.name
                emb.title = "Webhook Deleted"    
        #except:
        #    audit = False

        emb.set_author(name=user, icon_url=user.avatar_url)
        emb.add_field(name="Channel",value=channel.mention, inline=False)
        emb.add_field(name="Webhook Name",value=web_name, inline=False)
        emb.add_field(name="Additional Information",value="User ID: {0.id}\nMessage ID: {0.id}\nChannel ID: {1.id}".format(user,channel),inline=False)
        
        await Log.sendlog(self, str(channel.guild.id), emb)


    '''
    let's just forget about this one
    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, foo):
        #"foo" is a timestamp of when the message was pinned which is sort of useless
        audit = True
        try:
            async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.message_pin):
                print(entry)
                #compare ids because channels probably won't be identical
                if entry.target.id == channel.id and entry.action == discord.AuditLogAction.channel_pins_update:
                    #print("mhm")
                    
                    user = entry.user
                    print("YEA")
                    break
        except:
            try:
                async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.message_pin):
                    print(entry)
                    #compare ids because channels probably won't be identical
                    if entry.target.id == channel.id and entry.action == discord.AuditLogAction.channel_pins_update:
                        #print("mhm")
                        
                        user = entry.user
                        print("YUH")
                        break

            except:
                audit = False
   
        emb = discord.Embed(
                title = "Pins Updated",
                type = "rich",
                colour = 0x0388fc,
                )
        
        emb.add_field(name="Channel",value="#"+channel.name, inline=False)
        
        if audit == True:
            emb.set_author(name=user, icon_url=user.avatar_url)
            emb.add_field(name="Additional Information",value="User ID: {0.id}\nChannel ID: {1.id}".format(user,channel,inline=False))
        
        else:
            emb.add_field(name="Missing Permissions",value="Missing audit log permissions! Some data will be missing.",inline=False)
            emb.add_field(name="Additional Information",value="Channel ID: {}".format(channel.id),inline=False)
        
        await Log.sendlog(self, str(channel.guild.id), emb)        

    '''
    
    '''
    todo, requires formatting messages into a suitable format
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        #first we need to upload the messages to a hosting site, since it's probably going to be more than 2k characters - also downloading is overrated
        print(messages)
        messages2 = ""
        for message in messages:
            messages2.append(message+"\n")
        print(messages2)
        response = requests.post("http://hastebin.com", data=list(messages2))
        if response.status_code == 200:
            print(response.json()['key'])

        
        
        emb = discord.Embed(
                title = "Message Purge",
                type = "rich",
                colour = 0xf0280a,
                )

        emb.add_field(name="Content",value="temp", inline=False)
        emb.add_field(name="Channel",value=messages[0].channel.mention, inline=False)
        emb.add_field(name="Additional Information",value="Channel ID: {0.channel.id}".format(message))
        
        await Log.sendlog(self, str(message.guild.id), emb)
    '''
def setup(crdbot):

    crdbot.add_cog(Log(crdbot))
