from __future__ import annotations

import time
from typing import Any, TypedDict

import aiohttp
import discord
from discord.ext import commands
from typing_extensions import NotRequired


class NameEntry(TypedDict):
    name: str
    changedToAt: NotRequired[int]


class MCResponse(TypedDict):
    id: str
    name: str
    properties: list[dict[str, Any]]
    name_history: list[NameEntry]


@commands.command()
async def mclookup(ctx: commands.Context, username: str) -> None:
    """Lookup a MC player"""

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://mc-heads.net/minecraft/profile/{username}") as response:
            info: MCResponse = await response.json()

    names = []

    for entry in info["name_history"]:
        name = entry["name"]

        if "changedToAt" in entry:
            timestamp = entry["changedToAt"]
            struct = time.localtime(timestamp/1000)
            name += time.strftime(' (as of %d/%m/%Y at %H:%M GMT+0)', struct)

        names.append(name)

    embed = discord.Embed(
        title="Direct download",
        description="**Name History:**\n" + "\n".join(names),
        url=f"https://mc-heads.net/download/{username}",
        colour=0x8cc43d)

    embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
    embed.set_author(name=username)
    embed.set_image(url=f"https://mc-heads.net/body/{username}")
    embed.set_footer(text="Avatars provided by MCHeads!")
    await ctx.send(embed=embed)

def setup(crdbot: commands.Bot):
    crdbot.add_command(mclookup)
