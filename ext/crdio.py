import asyncio

import discord
from discord.ext import commands


@commands.command()
@commands.guild_only()
async def crdio(ctx: commands.Context) -> None:
    funnies = [
        "Seriously? React with \U0001F914 to proceed.",
        "Okay. I just want to warn you this is the suicide command. If you continue through with this command, you will kick yourself. React with \U0001F914 to proceed.",
        f"Jesus Christ, calm down there {ctx.author}. Let's not be so hasty. I'm being dead serious, this command will **ACTUALLY** kick you. You should stop now.",
        "Bloody hell. Okay, you have been warned. This is past my control now, and by reacting with \U0001F914 you confirm your demise."
        " This is the last warning. This is not a joke. If you react, you are kicked. Game over."
        " You'll have to go find another server invite, and everyone will laugh at you for getting yourself kicked over such a stupid thing."
        " But if you're really this thickheaded... again... you may proceed, by reacting \U0001F914."]

    for text in funnies:
        msg = await ctx.send(text)
        await msg.add_reaction("\U0001F914")

        try:
            await ctx.bot.wait_for(
                "reaction_add",
                check=lambda reaction, user: user == ctx.author and str(reaction.emoji) == "\U0001F914",
                timeout=600)

        except asyncio.TimeoutError:
            await ctx.send("I've decided to spare you.")
            return

    await ctx.send("Welp. Don't say I didn't warn ya. Kicking in 20 seconds, you may say your last goodbyes (or beg someone to shut me down, maybe)")
    await asyncio.sleep(10)
    await ctx.send("You thought I was kidding, didn't you? Let this be a lesson to trust the funny bot.")
    await asyncio.sleep(10)

    assert ctx.guild is not None

    try:
        await ctx.guild.kick(ctx.author, reason="Got memed by ;crdio")

    except (discord.Forbidden, discord.HTTPException):
        await ctx.send("Ah. Looks like I lack the permissions to kick you. Better luck next time.")


def setup(crdbot: commands.Bot):
    crdbot.add_command(crdio)
