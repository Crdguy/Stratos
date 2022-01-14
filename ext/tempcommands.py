import asyncio
import random
import re
from typing import List

import discord
from discord.ext import commands


@commands.command()
async def minute_timer(ctx: commands.Context, minutes: int) -> None:
    """Counts down minutes until it reaches 0"""
    msg = await ctx.send(f"Timer started: {minutes} minutes remaining")

    while minutes > 0:
        await asyncio.sleep(60)
        minutes -= 1
        await msg.edit(content=f"{minutes} minutes remaining")

    await msg.edit(content="Timer's up!")


@commands.command()
@commands.is_owner()
async def ehcomp(ctx: commands.Context):
    """
    Provided by Eneg#8410 (190505392504045570)
    """
    channel = ctx.bot.get_channel(294514080272613377)
    assert isinstance(channel, discord.TextChannel)

    emojis = ('<:epix:598275090840551474>',
              '<:broepix:688682287751364608>', '<:epic:730435572396458014>')

    message = await channel.fetch_message(874633053320917033)

    reactions: List[discord.Reaction] = []

    for reaction in message.reactions:
        if isinstance(reaction.emoji, str):
            continue

        if reaction.emoji.name in {'epix', 'broepix', 'epic'}:
            reactions.append(reaction)

    epix, broepix, epic = reactions
    assert str(epix.emoji) == emojis[0]
    assert str(broepix.emoji) == emojis[1]
    assert str(epic.emoji) == emojis[2]

    epix_users = await epix.users().flatten()
    # everyone can participate so no filters applied
    epix_winner = random.choice(epix_users)

    major_staff_roles_id = {
        415922791913750530, 294512832190349312, 592028643044229150, 294512708613832704}

    assert ctx.guild is not None

    broepix_members = []

    async for user in broepix.users():
        member = await ctx.guild.fetch_member(user.id)
        print(member)

        if member is not None:
            broepix_members.append(member)

    broepix_winner = random.choice(broepix_members)

    colonel_brig_ids = {565580766285791252, 294512832190349312}

    epic_users = [
        member
        async for user in epic.users()
        if (member := await ctx.guild.fetch_member(user.id)) is not None
        if any(role.id in colonel_brig_ids for role in member.roles)
    ]

    epic_winner = random.choice(epic_users)

    string = (
        f'{epix_winner.mention} won {emojis[0]} lottery'
        f'\n{broepix_winner.mention} won {emojis[1]} lottery'
        f'\n{epic_winner.mention} won {emojis[2]} lottery'
    )

    await ctx.send(string, allowed_mentions=discord.AllowedMentions.none())


class Listener(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.guild and message.guild.id == 294511987684147212:
            links = []

            for match in re.finditer(
                r"(https://media.discordapp.net/attachments/)"
                r"\d{18}/\d{18}/.+.\.(?:mov|webm|mp4)",
                message.content):
                links.append("https://cdn.discordapp.com" + match.string[28:])

            if links:
                await message.channel.send(
                    "Media link detected! Media links only play in a browser."
                    " Here is the properly embedded CDN link: "
                    + "\n".join(links),
                    allowed_mentions=discord.AllowedMentions.none())


def setup(crdbot: commands.Bot):
    crdbot.add_cog(Listener(crdbot))
    crdbot.add_command(minute_timer)
