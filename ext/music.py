from discord.ext import commands
import discord
import asyncio
import random
import string

try:
    import youtube_dl
except:
    youtube_dl = None

class Music(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.command(pass_context=True)
    async def dc(self, ctx):
        for x in self.crdbot.voice_clients:
            if(x.guild == ctx.message.guild):
                return await x.disconnect()

        await ctx.send("Not connected to a voice channel!")

    @commands.command(pass_context=True)
    async def play(self, ctx, link):
        
        cchannel = ctx.message.author.voice.channel 

        voice = await cchannel.connect()

        def youtubedl(link):

            randomfilename = "".join(random.choice(string.ascii_letters + string.digits) for x in range(6))
             
            options = {
                "format": "best",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                "outtmpl": "downloadcrap/{}.mp3".format(randomfilename)
                
                
                }

            with youtube_dl.YoutubeDL(options) as yt:
                yt.download([link])

            return "downloadcrap/" + randomfilename + ".mp3"
                

            #await message.edit(content="Done!\nDownload link: {}\nFile size: {}".format(request.json()["url"],os.path.getsize("downloadcrap/{}.mp3".format(epix))))
            


        
        source = discord.FFmpegOpusAudio(source=youtubedl(link))
        voice.play(source)




        #out with the old

        '''
        #queue.append(link)
        #played = 0
        #try:
        cchannel = ctx.message.author.voice.channel 

        voice = await cchannel.connect()
        #
        except:
            await ctx.send("Looks like you're not in a voice channel I can access!")
            return
        #
        #while played != len(queue):
        #try:
        player = discord.FFmpegPCMAudio(source=link).read()
        #except:
        #await ctx.send("Error, unable to download from link. Are you sure that's a YouTube link?")
        #player = voice.create_ffmpeg_player("deadinside.wma")
        #while True:
        #player2 = discord.PCMAudio(player)
        #src = discord.AudioSource()
        #src.read()
        #voice.play(source=player)
        voice.send_audio_packet(data=player,encode=True)
        #voice.send_audio_packet(

        #variable defining mess
        #
        global ptitle, pdesc, puplo, pupdt, pmins, psec, plike, pdislike, pview, puploader
        ptitle = player.title
        pdesc = player.description
        puplo = player.uploader
        pupdt = player.upload_date
        pdura = player.duration
        pmins = 0
        while pdura > 60:
            pdura = pdura - 60
            pmins = pmins+1
        if pdura < 10:
            psec = "0{}".format(pdura)
        else:
            psec = pdura
        
        plike = player.likes
        pdislike = player.dislikes
        pview = player.views
        puploader = ctx.message.author.name
        '''
        #ends here
        
        #await ctx.send("Now playing! '{}', requested by {}.".format(ptitle,puploader))

    '''
    @play.error
    async def play_error(ctx,err):
        
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing a link. Correct command format: `;play [link]`")
    '''

    @commands.command(pass_context=True)
    async def pinfo(ctx):
        #a = 0
        try:
            playinfo = discord.Embed(title = "Currently playing - '{}', requested by {}.".format(ptitle, puploader),
        
            description = "**Duration:** {}:{}\n**Likes:** {}\n**Dislikes:** {}\n**Video description:**\n{}\n".format(pmins,psec,plike,pdislike,pdesc, colour = 0x8cc43d, thumbnail = "https://cdn.discordapp.com/attachments/530795138415591434/530795750389579816/spiderbee.png"))
        except:
            await ctx.send("Looks like nothing is playing right now!")

        await crdbot.send_message(ctx.message.channel, embed=playinfo)



def setup(crdbot):

    crdbot.add_cog(Music(crdbot))
