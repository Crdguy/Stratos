from __future__ import annotations

import asyncio
import random

import discord
from discord.ext import commands

emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':bomb:']

def make_grid(size: int) -> list[list[str]]:
    """Generates a square grid of given size"""

    return [[""] * size for _ in range(size)]

def print_grid(grid: list[list[str]]) -> str:
    """Formats the grid into a string"""
    return "\n".join(map("".join, grid))

def print_spoiler_grid(grid: list[list[str]]) -> str:
    """Formats the grid into a string, with spoilers added"""
    return "\n".join("".join(f"||{cell}||" for cell in row) for row in grid)

def plant_mines(grid: list[list[str]], coeffs: tuple[float, float]) -> int:
    """Does the mine planting logic. Returns the number of mines planted."""
    lower, upper = coeffs

    size = len(grid)

    cells = size ** 2

    # generates a random number where 10% of total tiles <= mineno <= 30% of total tiles
    c = mines = round(random.uniform(lower * cells, upper * cells))

    while c:
        x = random.randrange(0, size)
        y = random.randrange(0, size)

        if grid[y][x] != emojis[-1]:
            grid[y][x] = emojis[-1]
            c -= 1

    return mines

def check_surrondings(grid: list[list[str]], x: int, y: int) -> int:
    """Returns number of bombs surrounding a given cell."""
    n = 0

    if x == 0:
        all_x = (0, 1)

    elif x == len(grid)-1:
        all_x = (x-1, x)

    else:
        all_x = (x-1, x, x+1)

    if y == 0:
        all_y = (0, 1)

    elif y == len(grid)-1:
        all_y = (y-1, y)

    else:
        all_y = (y-1, y, y+1)

    for px in all_x:
        for py in all_y:
            if px == x and py == y:
                continue

            if grid[py][px] == emojis[-1]:
                n += 1

    return n

diff_map = dict(
    easy  =(0.1, 0.2),
    normal=(0.15, 0.3),
    medium=(0.15, 0.3),
    hard  =(0.2, 0.4),
    expert=(0.3, 0.475),
    death =(0.4, 0.65))


@commands.command()
async def minesweeper(ctx: commands.Context, size: int = 8, difficulty: str = "normal") -> None:
    """
    Minesweeper.py by Chris Dance.
    Reformatted by Eneg.

    Version: 0.2.0

    release = final version for a while
    major = large update
    minor = small update
    hotfix = quick bug fix
    """

    if size > 14:
        raise commands.UserInputError("Grid of size > 14 is over 2000 characters in length.")

    if size <= 0:
        raise commands.UserInputError("Invalid grid size.")

    difficulty = difficulty.lower()

    if difficulty in diff_map:
        dif = diff_map[difficulty]

    else:
        for key in diff_map:
            if key.startswith(difficulty):
                dif = diff_map[key]
                difficulty = key
                break

        else:
            raise commands.UserInputError("Invalid difficulty passed.")

    grid = make_grid(size)

    total_mines = plant_mines(grid, dif)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != emojis[-1]:
                bombs = check_surrondings(grid, x, y)
                grid[y][x] = emojis[bombs]

    embed = discord.Embed(
        title=f"{size}x{size} grid Minesweeper game, requested by {ctx.message.author}\n"
              f"{total_mines} mines\n"
              f"**{difficulty.capitalize()}** Mode",
        description=print_spoiler_grid(grid),
        colour=ctx.author.color)

    embed.set_footer(
        text="A game of Minesweeper! Play by clicking the spoilers."
        " Try to click all tiles but the bombs."
        " If you click a bomb, you lose the game.\n"
        "React with \U0001F1F7 to reveal the mines if you give up.",
        icon_url=str(ctx.author.avatar_url))

    msg = await ctx.send(embed=embed)

    await msg.add_reaction("\U0001F1F7")

    try:
        await ctx.bot.wait_for(
            "reaction_add",
            check=lambda reaction, user: user == ctx.author and reaction.emoji == "\U0001F1F7",
            timeout=600)

    except asyncio.TimeoutError:
        return

    embed.description = print_grid(grid)
    embed.title = (f"{size}x{size} grid Minesweeper game, requested by {ctx.author}\n"
                   f"{total_mines} mines\n**{difficulty.capitalize()}** Mode\n"
                   f"Given up! Field has been revealed.")
    await msg.edit(embed=embed)


@minesweeper.error
async def minesweeper_error(ctx: commands.Context, err: commands.CommandError) -> None:
    await ctx.send(err)


def setup(crdbot: commands.Bot):
    crdbot.add_command(minesweeper)
    print("minesweeper loaded")
