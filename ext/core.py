from discord.ext import commands
import discord
import asyncio
import configparser
from glob import glob

#open "stratos.ini"
try:
    config = configparser.ConfigParser()
    config.read('stratos.ini')

except Exception:
    input("Error, something went wrong while parsing 'stratos.ini'. Ensure the file is not corrupt or missing.")
    exit(0)

class Help(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot


    @commands.command()
    async def help(self, ctx, command):

        if command == "fight":
            desc = "`;fight [character] [character2] [number of rounds]`. Makes two characters 'fight' each other."
        elif command == "ping":
            desc = "`;ping`. Tests the API's response time in milliseconds."
        elif command == "weather":
            desc = "`;weather [location] [currently, hourly]`. Displays the current or hourly forecast for any given location."
        elif command == "sd":
            desc = "`;sd`. Shuts down this bot. Only bot administrators have the permissions to execute this command."
        elif command == "dc":
            desc = "`;dc`. Disconnects the bot from a voice channel."
        elif command == "play":
            desc = "`;play [link]`. Joins the voice channel you're in, and plays a YouTube link."
        elif command == "pinfo":
            desc = "`;pinfo`. Displays info about the current or last played song."
        elif command == "quadratic":
            desc = "`;quadratic [a] [b] [c]`. Solves a quadratic equation using the values a, b and c using the quadratic formula. Also provides full method."
        elif command == "purge":
            desc = "`;purge [x] [optional: user]`. Deletes the last x messages.\n\nIf the `user` argument is passed (either by mentioning that user or adding their user ID) Stratos will look for as many messages that user has sent in the last x messages, and delete them. If you do `;purge 10 557309788480864256` for example, it might not delete 10 messages by Stratos, but rather all messages Stratos has sent in the last 10 messages."
        elif command == "setstatus":
            desc = "`;setstatus [0-4] [status]`. Sets the current status of the bot. Only Crdguy#9939 is able to execute this command."
        elif command == "ehlookup":
            desc = "`;ehlookup [subcommand] [options] [shipname]`. Simple usage: `;ehlookup [subcommand] [shipname]`. Returns information gathered from the most recent Event Horizon Database and calculates useful information such as ship cost, workshop level, and more.\n'subcommand' can be `ship` to find information about a ship, or `module` to return information on any module.\nOptions:\n`-fast` - Creates a lower quality ship image with a grid.\n`-superfast` - Creates a lower quality ship image without a grid.\n`-ultrafast` - Creates a low quality ship image that is not scaled  up. Ideal for extremely large ships.\n`-nolayout` - Shows all information about the ship without generating an output.\n`-myfile` - Upload a ship .json and information will be generated for the ship\n\nIf you would like to see a list of available ships, react with \U0001F522."
        elif command == "rust":
            desc = "`;rust [optional, mention a user]`. Mention a user or upload an image to 'rust' that image.\nThis command serves as a test for image manipulation. It may be removed or changed."
        elif command == "userinfo":
            desc = "`;userinfo [args]`. Simple usage: `;userinfo`. Returns useful information about a user, such as account creation and activity.\n\nArgs:\nYou may use both the `user` and the `channel` arguments in the same command.\n`user` - Mention a user or give their ID to display information about somebody else's account. Only works with users in the server.\n`channel` - Tag a channel to view your activity in that channel instead."
        elif command == "role":
            desc = "Temporary command. Placeholder for role assignment, which will be added at a later date."
        elif command == "feedback":
            desc = "`;feedback [information]`. Use this command to submit bug reports and feedback to the bot developer, Crdguy#9939. Put this information in the [information] field."
        elif command == "support":
            desc = "`;support`. Returns some useful information if you're having some issues or need help with Stratos."
        elif command == "minesweeper":
            desc = "`;minesweeper [args]`. Play a game of Minesweeper and see if you can beat a randomly generated grid up to size 14.\n\nArguments:\n`Difficulty` - pick from `easy`, `normal`, `hard`, `expert` or `death`. Defaults to `normal` if not specifed. Affects the amount of mines on the playing field.\n\n`Size` - pick a number from 1 to 14 to choose the grid size, i.e. picking 4 generates a 4x4 grid. Defaults to 8 if not specified."
        elif command == "ban":
            desc = "`;ban [user] [reason]`, where `user` is a mentioned user or an ID that will be banned, and an optional `reason` to ban them. Bans a user and prompts how many days to ban for, if you have the permissions to ban users. Can be used to ban users not in a server, by ID."
        elif command == "pong":
            desc = "`;pong`. Tests the API's response time in milliseconds."
        elif command == "xkcd":
            desc = "`;xkcd [args]`. Display a random or specified xkcd comic. If no arguments are given, Stratos will display a random comic.\n\nArguments:\n`Number` - if a number is given, Stratos will attempt to retrieve the comic with that number.\n\n`-c`, or `--current` - display the latest comic." 
        elif command == "crdio":
            desc = "`;crdio`. Natural selection."
        elif command == "kms":
            desc = "`;kms`. Self explanatory command."
        elif command == "rustlore":
            desc = "`;rustlore`. Uses a Markov chain algorithm to generate you the finest quality rust lore."
        elif command == "eh_description":
            desc = "`;eh_description`. Uses a Markov chain algorithm to generate hilarious fake descriptions for the amazing game Event Horizon."
        elif command == "file":
            desc = '''`;file [user] [channel] [action] [strike] [reason] [proof] (optional: comment - the first thing after the required arguments is counted as a comment. Use parentheses ("") to have a comment longer than one word)`. Filing command for Event Horizon staff as an alternative to the form.\n\nArguments:\n\n`user` - mention or ID of the offending user\n`channel` - the channel the restriction took place in. Make sure it is mentioned correctly.\n`action` - should be any of the following: "quarantine", "verbal warning", "purge", "role removal", "kick" or "ban". You can also use "q", "w", "p", "r", "k" or "ban" respectively as shorthand.\n`strike` - the number of strikes the user is now on, from 0 to 4.`reason` - a short sentence describing why the user was punished. Please give reasons longer than a sentence in quotations like this: "Spam in #general"\n`proof` - should be a url to a screenshot that has evidence of the offending act. Avoid using Discord's CDN here because the links to the image will expire in 2 years. Use Imgur or Gyazo instead, or anything similar.'''
        elif command == "rslookup":
            desc = "`;rslookup [user]`. Tool for admins to find a user's strike history. `user` should be a mentioned user or an ID."
        #elif command == "
        msg = await ctx.message.channel.send(desc)
        if command == "ehlookup":
            await msg.add_reaction("\U0001F522")
            passed = False
            while msg:
                await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U0001F522")
                msg2 = await ctx.fetch_message(msg.id)
                
                reactsO = msg2.reactions

                async for y in reactsO[0].users():
                    
                    
                    if ctx.message.author == y:

                        allships = []
                        with open("shiplookuptable.csv") as lookuptableraw:
                            lookuptable = csv.reader(lookuptableraw, delimiter=",")
                            for line in lookuptable:
                                #if line[0] != "shipname":
                                    
                                allships.append(line[0])
                        allships.pop(0)

                        allshiptemp = ""
                        emb = discord.Embed(
                            title = "List of Ships:",
                            type = "rich",
                            )

                        x = 0
                        while x != 20:
                            allshiptemp = allshiptemp + allships[x] + "\n"
                            x = x + 1
                        emb.description = allshiptemp
                        
                        await msg.edit(content="",embed = emb)
                        await msg.add_reaction("◀")
                        await msg.add_reaction("▶")
                        
                        
                        
                        msgc = msg
                        while msg == msgc:

                            react2 = await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji in ["▶","◀"])
                            msg2 = await ctx.fetch_message(msg.id)
                            reacts = msg2.reactions

                            #reacts[1] is ◀,2 is ▶
                            async for y in reacts[1].users():
                                if ctx.message.author == y:
                                    z = x
                                    allshiptemp = ""
                                    while x != z - 20:
                                        try:
                                            allshiptemp = allshiptemp + allships[x] + "\n"
                                        except IndexError:
                                            x = 0
                                            break
                                        x = x - 1

                                    emb.description = allshiptemp
                                    await msg.edit(content="",embed = emb)
                                    
                            async for y in reacts[2].users():
                                if ctx.message.author == y:
                                    z = x
                                    allshiptemp = ""
                                    while x != z + 20:
                                        try:
                                            allshiptemp = allshiptemp + allships[x] + "\n"
                                        except IndexError:
                                            remainder = 17-len(allships)%20
                                            newlines = ""
                                            for a in range(remainder):
                                                newlines = newlines + "\n<:blank:407248051053264900>"
                                            print(newlines)
                                            allshiptemp = allshiptemp + "**END OF LIST!**" + newlines
                                            break
                                            
                                        x = x + 1

                                    emb.description = allshiptemp
                                    await msg.edit(content="",embed = emb)


                      
     
    @help.error
    async def helpe_error(self, ctx,err):
        
        if isinstance(err, commands.MissingRequiredArgument):
            desc = "List of commands. Do `;help [command]` to view detailed command info."
            
            #add any commands that should not be appended to the list of commands 
            forbiddencommands = ["help","order","cubic","horizon","brap","reply"]
            
            for command in self.crdbot.commands:
                if str(command) not in forbiddencommands:
                    desc = desc + "\n" + str(command)
                
            emb = discord.Embed(
                title = "Command list",
                type = "rich",
                description = desc,
                )
            
            await ctx.message.channel.send(embed = emb)

            


class Core(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot 

    @commands.command(pass_context=True)
    async def sd(self, ctx):
        if str(ctx.message.author.id) in config["General Settings"]["admins"]:
            try:
                await ctx.send("Shutting down...")
                await self.crdbot.change_presence(status=discord.Status.offline)
                await self.crdbot.logout()
            except RuntimeError:
                print("Closed!")

    @commands.command()
    async def setstatus(self, ctx, statType):
        if ctx.message.author.id == 186069912081399808:
            statType = int(statType)
            if statType < 0:
                await ctx.send("It doesn't work like that.")
                return()
            playgame = ctx.message.content[12:len(ctx.message.content)]
            await self.crdbot.change_presence(activity=discord.Game(type=statType, name=playgame))
            await ctx.send("ok")

    '''
    @setstatus.error
    async def setstatus_error(self, err, ctx):
        
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing an argument. Correct command format: `;setstatus [0 - 3] [game]`")
    '''


    @commands.command()
    async def reload_ext(self, ctx, *extensions):
        if ctx.message.author.id == 186069912081399808:
            extensions = list(extensions) #screw tuples
            print(extensions)
            
            if len(extensions) == 0:
                #if no extensions are given, just reload all of them
                for f in glob("ext/*.py"):
                    #f is the path to the file, so we can format it to get the module name
                    f = str(f).replace("\\" , ".").replace(".py","")
                    print(f)
                    try:
                        self.crdbot.reload_extension(f)
                    except Exception as e:
                        await ctx.send("Critical error while loading extension {}! Error: {}".format(f,e))
                        print(e)
                await ctx.send("Successfully reloaded all extensions!")
                    
            else:
                #at least 1 extension is given, so load each one given

                x = 0
                while x != len(extensions):
                    
                    print(extensions[x])
                    try:
                        self.crdbot.reload_extension(extensions[x])
                        x = x + 1
                    except:
                        await ctx.send("Ignoring the extension '{}' as it does not exist.".format(extensions[x]))
                        print("removing {}".format(extensions[x]))
                        extensions.remove(extensions[x])
                        
                    print("exit")

                #convert list into a nice string
                stringext = ""
                for ext in extensions:
                    stringext = stringext + ext + ", "
                stringext = stringext[0:len(stringext)-2]
                
                await ctx.send("Successfully loaded the extension(s) {}!".format(stringext))
            
               

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(";leave"):
            if str(message.author.id) == '186069912081399808':
                servertl = crdbot.get_guild(message.guild.id)
                await message.channel.send("Really leave server? (check command line)")
                leave = input("Are you sure you want to leave?")
                if "y" in leave:
                    print("Okay. Leaving server {}...".format(servertl))
                    await message.channel.send("Goodbye, {}.".format(servertl))
                    await self.crdbot.leave_server(servertl)
                else:
                    print("Alright.")
                    await message.channel.send("Aborted.")
            else:
                await message.channel.send("That's a bit rude, isn't it?")


        if message.content.startswith('cmd'):
            if message.author.id == 186069912081399808:
                print("ok")
                #try:
                await message.delete()
                #await crdbot.delete_message(message)
                c = input("Crdbot experimental console opened. Type 'help' for all commands. Note that commands here will only apply to the channel 'console' was typed in!")
                if c == 'speak':
                    y = 0
                    while 1:
                        x = input("Enter what I should say.")
                        await message.channel.send(x)
                        y = input("Should I stop?")
                        if y == "yes":
                            return

                if c == 'tts':
                    y = 0
                    while 1:
                        x = input("Enter what I should say.")
                        await message.channel.send(x,tts=True)
                        y = input("Should I stop?")
                        if y == "yes":
                            return
                        
                if c == 'exit':
                    return
                if c == 'sd':
                    print("Sayonara.")
                    await crdbot.logout()
                if c == 'forcesd':
                    exit(0)
                if c == 'help':
                    print("Current commands: speak (type a message), exit (close console), sd (shut down bot), forcesd (aggressively shut down), help (displays this message")
                else: 
                    print("Command unrecognised! Exiting experimental console.")
                #except Exception:
                    #print("No delete permission!")

def setup(crdbot):

    crdbot.add_cog(Help(crdbot))
    crdbot.add_cog(Core(crdbot))
