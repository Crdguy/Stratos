import random
from typing import TypedDict, Union

import aiohttp
import discord
from discord.ext import commands


class xkcdResponse(TypedDict):
    month: str
    num: int
    link: str
    year: str
    news: str
    safe_title: str
    transcript: str
    alt: str
    img: str
    title: str
    day: str


@commands.command()
async def xkcd(ctx: commands.Context, arg: Union[int, str, None] = None) -> None:
    """Sends a random or specified xkcd comics."""
    largest = 2430  # something like 2430 at time of writing (hello from 15 Jan 2020, future me!) yeah hi future you

    if arg is None:
        num = random.randint(1, largest)

    elif isinstance(arg, int):
        num = arg

    elif arg.lower() in {"-c", "--current"}:
        num = 0

    else:
        raise commands.UserInputError("Invalid flag or number.")

    if num == 0:
        link = "http://xkcd.com/info.0.json"

    else:
        link = f"http://xkcd.com/{num}/info.0.json"

    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if response.status == 404:
                raise commands.UserInputError("Specified comic does not exist.")

            raw: xkcdResponse = await response.json()

    embed = discord.Embed(
        title=raw["title"],
        description=raw["alt"],
        colour=ctx.author.color,
        url=f"http://xkcd.com/{raw['num']}/")
    embed.set_image(url=raw["img"])
    embed.set_footer(
        text="Uploaded: {day}/{month}/{year}, DD/MM/YYYY".format_map(raw),
        icon_url=str(ctx.author.avatar_url))

    await ctx.send(embed=embed)


def setup(crdbot: commands.Bot):
    crdbot.add_command(xkcd)
