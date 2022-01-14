import datetime
from typing import Union

import discord
from discord.ext import commands


@commands.command()
async def userinfo(
    ctx: commands.Context,
    user: Union[discord.Member, discord.User, None] = None,
    channel: Union[discord.TextChannel, None] = None
) -> None:
    """Sends info about the user."""

    if user is None:
        user = ctx.message.author

    if channel is not None:
        try:
            messages = await channel.history(limit=1000).flatten()

        except discord.Forbidden:
            await ctx.send(f"Missing permissions to read {channel}.")
            return

        message_count = 0

        for message in messages:
            if message.author.id == user.id:
                message_count += 1

        activity = (
            f"\n**Activity** (your messages per {len(messages)} messages"
            f" in #{channel}): {message_count / len(messages):.1%}")

    else:
        activity = ""

    desc = (
        f"**Account Creation Date**: {user.created_at:%Y-%m-%d at %H:%M} (UTC+0)"
        f" ({(datetime.datetime.utcnow() - user.created_at).days} days ago)")

    embed = discord.Embed(
        title=f"{user}",
        colour=user.color)
    embed.set_thumbnail(url=str(user.avatar_url))

    if isinstance(user, discord.Member):
        assert user.joined_at is not None
        roles = "\n".join(role.mention for role in user.roles)
        desc += (
            f"\n**Join Date**: {user.joined_at:%Y-%m-%d at %H:%M} (UTC+0)"
            f"({(datetime.datetime.utcnow() - user.joined_at).days} days ago)"
            f"\n**Roles**:\n{roles}")

        if activity:
            desc += activity

        embed.description = desc

    else:
        embed.description = desc + "\nThis user is not in the server!"

    await ctx.send(embed=embed)


def setup(crdbot: commands.Bot):
    crdbot.add_command(userinfo)
