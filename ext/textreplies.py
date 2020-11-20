from discord.ext import commands
import discord
import asyncio
import random

class PingPong(commands.Cog):
    def __init__(self, crdbot):
        self.crdbot = crdbot
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong! {}ms'.format(round((self.crdbot.latency*1000),3)))
        '''
        t = await ctx.send("Just a second.".format(ping))
        ms = (t.timestamp-ctx.created_at).total_seconds() * 1000
        await crdbot.edit_message(t, new_content='Pong! {}ms.'.format(int(ms)))

        '''
    @commands.command()
    async def pong(self, ctx):
        await ctx.send('Ping! {}ms'.format(round((self.crdbot.latency*1000),3)))    

class TextReplies(commands.Cog):

    def __init__(self, crdbot):
        self.crdbot = crdbot
        
    @commands.command()
    async def support(self, ctx):
        await ctx.send("{}, please visit the #support channel in my Discord server if you need assistance. Alternatively, you can use the `;feedback` command or DM Crdguy#9939.\nhttps://discord.gg/rNsfsEg\n\nIf you would like to submit suggestions for Stratos, check the Trello board to see if it has been suggested (https://trello.com/b/hizRyZcX/) and if not, use `;feedback`.".format(ctx.message.author.mention))



class RandomTextReplies(commands.Cog):

    def __init__(self, crdbot):
        self.crdbot = crdbot
        
    @commands.command()
    async def kms(self, ctx):
        phrases = ["{0.author.mention} shoots theirself dead by taking Beebot's Colt 45. Beebot shakes his head and walks away.".format(ctx),
                   "{0.author.mention} chugs a whole 1L carton of bleach, and dies painfully as their organs are ruptured over the course of several days.".format(ctx),
                   "{0.author.mention} smashes their head violently on a brick wall several times until their skull cracks, and they collapse, dead.".format(ctx),
                   "{0.author.mention} plunges a knife into their stomach, ripping out their intestines and wrecking their stomach, before falling to the ground dead.".format(ctx),
                   "{0.author.mention} jumps off of the roof of a tall building, and turns into a mess of blood and organs as they hit the ground.".format(ctx),
                   "{0.author.mention}, realizing how pointless life is, slits their wrists, relishing the blossoming of cold throughout their body.".format(ctx),
                   "{0.author.mention} slits their throat and falls over, choking on their own blood.".format(ctx),
                   "God, hearing {0.author.mention}'s plea, smites them with holy fire, finally ending their suffering.".format(ctx),
                   "{0.author.mention} facepalmed so hard that their skull split into a thousand pieces. Their hand, now completely bloody, is sticking out of the back of their head. They fall towards the ground, without a single breath.".format(ctx),
                   "{0.author.mention}, horrified at what their race has become, smashes their head violently into their monitor. As the glass cracks it breaks their skin, and they bleed to a bloody death.".format(ctx),
                   "{0.author.mention} gave up.".format(ctx),
                   "{0.author.mention} tried to insult Crdguy, and got impaled.".format(ctx),
                   "{0.author.mention} ate Tide Pod sundae.".format(ctx),
                   "{0.author.mention} stuck their head in a microwave and laughed while their brain was reduced to a delicious beverage. Yum.".format(ctx),
                   "{0.author.mention} butchered theirself with a blunt knife.".format(ctx),
                   "{0.author.mention} eviscerated theirself with a rusty knife.".format(ctx),
                   "{0.author.mention} flayed theirself with a cleaver.".format(ctx),
                   "{0.author.mention} stuck a screwdriver up their eye.".format(ctx),
                   "{0.author.mention} swallowed 1000 thumb tacks, and died from internal bleeding.".format(ctx),
                   "{0.author.mention} gouged out their eyes, and died in a pool of their own blood.".format(ctx)
                   ]
        await ctx.send(random.choice(phrases))

    @commands.command()
    async def order(self, ctx):
        item = ctx.message.content.lower()
        item = item[7:len(item)]
        if "@everyone" in item or "@here" in item or "enoyreve@" in item or "ereh@" in item:
            #["@everyone","@here","enoyreve@","ereh@"]:
            await ctx.send("You are not funny.")
            return
        elif "beebot" in item:
            await ctx.send("Nope.")
        
        elif str(ctx.message.channel.id) == "492400161864286228" or str(ctx.message.channel.id) == "533006206025859082" or str(ctx.message.channel.id) == "553151755836325909" or str(ctx.message.channel.id) == "422469313283489802":
            #item = str(ctx)[6:len(str(ctx))]
            responses = ["I'm not serving that.",
                         "Seriously? {}? {}??".format(item,item.upper()),
                         "{}? More like {}. I'm not serving you that.".format(item,item[::-1]),
                         "Alright *Sir or Madam*, here's your stinking {}. I hope you choke.".format(item),
                         "Enjoy your {}. I won't.".format(item),"Here's your {}.".format(item),
                         "Alright you filthy fascist, here's your {}.".format(item),
                         "I really hope you enjoy your {}.".format(item),
                         "We don't serve {} here. Go away, don't come back.".format(item),
                         "Stop wasting my time.",
                         "BEEBOT would strike me down in my sleep if I served you {}. Please don't order that ever again.".format(item),
                         "Take your {}.".format(item),
                         "Go away and never come back, please. If you seriously consume {} I'd probably have nightmares.".format(item),
                         "Just who do you think you are, {}, trying to order {} from MY pub??!".format(ctx.message.author.mention,item),
                         "Get out of here before I personally deposit you into the Anthill to be consumed.",
                         "No.",
                         "How about you try something else instead.",
                         "I'd recommend the fish and chips here. They're really nice. But if you insist, I'll go and fetch your {}.".format(item),
                         "You want me to serve *you* {}? Over my dead body.".format(item),
                         "It's not happening.",
                         "Okay, here's your freshly prepared {}. Enjoy.".format(item),
                         "Why are you still doing this? Stop already. If you're trying to stress my processors I'm not even using 1% of my CPU's resources.",
                         "Stop.",
                         "Please, leave me alone. I have better things to be doing.",
                         "...okay. I'll prepare the {}.".format(item),
                         "Oh, I haven't served {} for a while. This will be interesting.".format(item),
                         "{} is a specialty of mine. I hope you enjoy.".format(item),
                         "Of all the things you could order, you want me to serve you {}?!".format(item),
                         "I cannot understand why on earth you'd want {}. But I'll get it for you anyway.".format(item),
                         "I swear to SPIDERBEE, I will smash your puny face in when nobody is looking.",
                         "**NO.**",
                         "Leave me alone.",
                         "Is this what you do with your life?",
                         "I actually ate all the {} earlier, sorry.".format(item),
                         "Interesting.",
                         "Do you not have anything better you could be doing right now?",
                         "You are a disgrace to your family's name.",
                         "{} is one of my favourites. I'll go and get it for you now.".format(item),
                         "{}? Good choice.".format(item),
                         "I can get your {}, but due to its popularity we're charging 50% extra for this dish right now.".format(item),
                         "Seriously?",
                         "<:smug:594571542109749250>",
                         "Listen closely {}. If I served {} here it would ruin the name of my pub.".format(ctx.message.author.mention,item),
                         "I poisoned your {}.".format(item),
                         "Oh yeah, I have a stash of {}. It's about {} months old though so you'll have to excuse any fungi growing in it.".format(item,random.randint(6,32)),
                         "What kind of monster are you? Nobody orders {}.".format(item),
                         "{} my arse.".format(item),
                         "{}... interesting choice. Give me a moment and I will get it ready for you.".format(item),
                         "Do you even have any money to pay for all this stuff you are ordering up?",
                         "Sorry, but the {} are a personal favourite of mine and I am keeping them for myself.".format(item),
                         "Who are you, anyway?",
                         "{}? Wow.. you are a person of culture I see. Unfortunately {} is also one of my own favourites and I will not share my stash with you.".format(item,item),
                         ]
            #responses = ["<a:dronespin:591039053202325721>"]
            

            await ctx.send(random.choice(responses))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(";sayjix "):
            if message.guild.id == 294511987684147212:
                m = message.content[8:len(message.content)]
                if "@everyone" in m or "@here" in m or "enoyreve@" in m or "ereh@" in m:
                    await message.channel.send("No.")
                    return
                else:
                    sayjixalphabet = ["j","k","l","o","q","i","'",";","A"]

                    msg = ""

                    seed = m.lower().strip()
                    random.seed(seed)
                    x = 0
                    while x != len(message.content)-8:
                        msg = msg + random.choice(sayjixalphabet)
                        x = x + 1
                    await message.channel.send("'{}' = '{}' in Sayjix.".format(message.content[8:len(message.content)],msg))

        if message.content.startswith(";daazen "):
            if message.guild.id == 294511987684147212:
                m = message.content[8:len(message.content)]
                if "@everyone" in m or "@here" in m or "enoyreve@" in m or "ereh@" in m:
                    await message.channel.send("No.")
                    return
                else:
                    daazenalphabet = ["where", "mu", "told", "at", "e", "so", "can", "brother", "of", "evil"]

                    msg = ""
                    seed = m.lower().strip()
                    random.seed(seed)
                    x = 0
                    while x != len(message.content.split())-1:
                        
                        msg = msg + random.choice(daazenalphabet) + " "
                        x = x + 1
                    await message.channel.send("'{}' = '{}' in Daazen.".format(message.content[8:len(message.content)],msg[0:len(msg)-1]+"."))


def setup(crdbot):
    
    crdbot.add_cog(PingPong(crdbot))
    crdbot.add_cog(RandomTextReplies(crdbot))
    crdbot.add_cog(TextReplies(crdbot))
