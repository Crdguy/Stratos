from discord.ext import commands
import discord
import asyncio

class Crdio(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot
    

    @commands.command(pass_context=True)
    async def crdio(self, ctx):
        msg = await ctx.send("Seriously? React with \U0001F914 to proceed.")

        await msg.add_reaction("\U0001F914")
        
        #passed = False
        while msg:
            await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U0001F914")
            msg2 = await ctx.fetch_message(msg.id)
            
            reactsO = msg2.reactions

            async for y in reactsO[0].users():
                
                if ctx.message.author == y:
                    
                    msg3 = await ctx.send("Okay. I just want to warn you this is the suicide command. If you continue through with this command, you will ban yourself. React with \U0001F914 to proceed.")
                    await msg3.add_reaction("\U0001F914")
                    msg1 = False
                    msg2 = False

                    while msg3:
                        await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U0001F914")
                        msg4 = await ctx.fetch_message(msg3.id)
                        
                        reactsO2 = msg4.reactions

                        async for y in reactsO2[0].users():
                            
                            
                            if ctx.message.author == y:

                                msg5 = await ctx.send("Jesus Christ, calm down there {}. Let's not be so hasty. I'm being dead serious, this command will **ACTUALLY** ban you. You should stop now.".format(ctx.message.author))
                                await msg5.add_reaction("\U0001F914")
                                msg3 = False
                                msg4 = False                            

                                while msg5:
                                        await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U0001F914")
                                        msg6 = await ctx.fetch_message(msg5.id)
                                        
                                        reactsO3 = msg6.reactions

                                        async for y in reactsO3[0].users():
                                            
                                            
                                            if ctx.message.author == y:

                                                msg7 = await ctx.send("Bloody hell. Okay, you have been warned. This is past my control now, and by reacting with \U0001F914 you confirm your demise. This is the last warning. If you react, you are banned. Game over. You'll have to ask the admins to unban you, and they will probably just laugh their arses off at you for being banned by such a stupid thing. But if you're really this thickheaded... again... you may proceed, by reacting \U0001F914.")
                                                await msg7.add_reaction("\U0001F914")
                                                msg5 = False
                                                msg6 = False  
        
                                                while msg7:
                                                    
                                                        await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U0001F914")
                                                        msg8 = await ctx.fetch_message(msg7.id)
                                                        
                                                        reactsO4 = msg8.reactions

                                                        async for y in reactsO4[0].users():
                                                            
                                                            
                                                            if ctx.message.author == y:
                                                    
                                                                await ctx.send("Welp. Don't say I didn't warn ya. Banning in 10 seconds, you may say your last goodbyes (or beg someone to shut me down, maybe)")
                                                                msg7 = False
                                                                msg8 = False  

                                                                await asyncio.sleep(10)
                                                                try:
                                                                    await ctx.guild.ban(discord.Object(id=ctx.author.id),reason="Got memed by ;crdio",delete_message_days=0)
                                                                except:
                                                                    await ctx.send("Ah. Looks like I lack the permissions to ban you. Better luck next time.")


def setup(crdbot):

    crdbot.add_cog(Crdio(crdbot))
