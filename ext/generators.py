from discord.ext import commands
import discord
import asyncio
import markovify
from glob import glob
import random
import io


class Generators(commands.Cog):
    def __init__(self, crdbot):
        self.crdbot = crdbot

    @commands.command()
    async def rustlore(self, ctx):
        models = []

        #title the lore
        start = "Rusted Generations"

        with open("Funny EH Names/count.txt") as file:
            count = int(file.read()) + 1
        with open("Funny EH Names/count.txt", "w") as file:
            file.write(str(count))

        first = [
            "Fall",
            "Rise",
            "Destruction",
            "Punishment",
            "Rapture",
            "Dawn",
            "Rusting",
            "Absolution",
            "Rusted Revenge",
            "War",
            "Wrath",
            "Oxidising",
            "WD40ing",
            "Tarnishing",
            ]
        last = [
            "Eobnur",
            "Rustfungi",
            "Jan Salo",
            "WD40K Missiles",
            "The Scavengers",
            "The Unknown",
            "The Zumbalari",
            "Chaos",
            "Eobnurians",
            "North Korerans",
            "Fart",
            "Rustaša",
            "Ram Horizon",
            
            
            ]

        title = start + " " + str(count) + ": " + random.choice(first) + " of " + random.choice(last)
            

        for f in glob("Funny EH Names/Rust Lore/*.txt"):
            with open(str(f)) as file:
                models.append(markovify.Text(file.read(), well_formed=False))

        model_combo = markovify.combine(models)
        stuff = []

        for x in range(10):
            stuff.append(model_combo.make_sentence())

        output = title + "\n"
        for x in stuff:
            output = output + " " + x

        await ctx.send(output)


    @commands.command()
    async def eh_description(self, ctx):
        models = []

        for f in glob("Funny EH Names/Descriptions/*.txt"):
            file = io.open(f, mode="r", encoding="utf-8")
            models.append(markovify.Text(file, well_formed=False))

        model_combo = markovify.combine(models)
        stuff = []

        for x in range(10):
            stuff.append(model_combo.make_sentence())

        output = ""
        for x in stuff:
            try:
                output = output + " " + x
            except:
                pass
        await ctx.send(output)
        
def setup(crdbot):

    crdbot.add_cog(Generators(crdbot))
