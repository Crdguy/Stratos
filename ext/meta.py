from discord.ext import commands
import discord
import asyncio
import requests
try:
    import youtube_dl
except:
    youtube_dl = None
import random

class Meta(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot



    @commands.command()
    async def xkcd(self, ctx, *args):
        
        for arg in args:
            try:
                foo = int(arg)
                if isinstance(foo,int):
                    num = foo
                else:
                    num = random.randint(1,2430)#something like 2430 at time of writing (hello from 15 Jan 2020, future me!)
            except:
                num = random.randint(1,2430)
                
                if arg.lower() == "-c" or arg.lower() == "--current":
                    num = 0

        if not args:
            num = random.randint(1,2430)
            #print("hmm yes")
            

        if num == 0:
            raw = requests.get("http://xkcd.com/info.0.json").json()
        else:
            raw = requests.get("http://xkcd.com/{}/info.0.json".format(num)).json()
            
        date = "{}/{}/{}, DD/MM/YYYY".format(raw["day"],raw["month"],raw["year"])

        #print(raw)
        #print(date)

        
        emb = discord.Embed(title=raw["title"],
        type = "rich",
        description = raw["alt"],
        colour = ctx.message.author.color,
        url = "http://xkcd.com/{}/".format(raw["num"]),
        
        )#0x8cc43d,
        emb.set_image(url=raw["img"])
        emb.set_footer(text="Uploaded: {}".format(date),icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}".format(ctx.message.author))
        
        await ctx.send(embed=emb)


    @commands.command()
    async def role(self, ctx,role):
        a = 0

        
    @commands.command()
    async def youtubedl(self, ctx, link):
        #try:
        async with ctx.channel.typing():
            
            status = "Initialising!"
            message = await ctx.send("Processing! Status: {}".format(status))
            
            epix = "".join(random.choice(string.ascii_letters + string.digits) for x in range(6))
             
            options = {
                "format": "best",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                "outtmpl": "downloadcrap/{}.mp3".format(epix)
                
                
                }

            
            await message.edit(content="Processing! Status: Downloading!")
            with youtube_dl.YoutubeDL(options) as yt:
                yt.download([link])

            await message.edit(content="Processing! Status: Uploading to host!")
            request = requests.post('https://api.anonymousfiles.io', files={'file': open("downloadcrap/{}.mp3".format(epix),"rb")})

            await message.edit(content="Done!\nDownload link: {}\nFile size: {}".format(request.json()["url"],os.path.getsize("downloadcrap/{}.mp3".format(epix))))
            

    @commands.Cog.listener()
    async def on_message(self, message):
        #print("yeah")
        if self.crdbot.user.mention in message.content:
            await message.channel.send("Hello {}, I am Stratos. To see my commands, do `;help`.".format(message.author))


def setup(crdbot):

    crdbot.add_cog(Meta(crdbot))
