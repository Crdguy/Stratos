import cmath
import math

import discord
import numpy
from discord.ext import commands


@commands.command()
async def quadratic(ctx: commands.Context, a: float, b: float, c: float = 0) -> None:
    """Solves a quadratic equation."""
    # ∆ = b² - 4ac
    # x = (-b ± √∆) / 2a

    if a == 0:
        raise commands.UserInputError("Provided equation is not quadratic")

    delta = b**2 - 4*a*c

    try:
        delta_sqrt = math.sqrt(delta)
        imaginary = False

    except ValueError:
        delta_sqrt = cmath.sqrt(delta)
        imaginary = True

    sol1 = -b + delta_sqrt
    x1 = sol1 / (a*2)

    sol2 = -b - delta_sqrt
    x2 = sol2 / (a*2)

    embed = discord.Embed(
        title=f"Solving quadratic equation {a:.5g}x² + {b:.5g}x + {c:.5g}"
        + " - imaginary domain" if imaginary else "",
        colour=0x8cc43d)

    embed.add_field(
        name="Solution 1",
        value=f"`{sol1:.5g} / {a*2:.5g}`\n`x = {x1:.10g}`",
        inline=True)
    embed.add_field(
        name="Solution 2",
        value=f"`{sol2:.5g} / {a*2:.5g}`\n`x = {x2:.10g}`",
        inline=True)
    embed.add_field(
        name="Method",
        value=f"`-({b:.5g}) ± √(({b:.5g})² - 4({a:.5g})({c:.5g}))) / ({a:.5g}*2)`\n"
              f"`({-b:.5g} ± √({b**2:.5g}{-4*a*c:+.5g})) / {a*2:.5g}`\n"
              f"`({-b:.5g} ± √{delta:.5g}) / {a*2:.5g}\n`"
              f"`({-b:.5g} ± {delta_sqrt:.5g}) / {a*2:.5g}`")
    await ctx.send(embed=embed)


@commands.command()
async def cubic(ctx: commands.Context, a: int, b: int, c: int, d: int) -> None:
    """Solves a cubic equation."""

    imaginary = False

    solution = "x = ³√(q + √(q² + (r - p²)³))  +  ³√(q - √(q² + (r - p²)³))  +  p\nwhere:\np = -b/3a\nq = p³ + (bc-3ad)/(6a²)\nr = c/3a\n"

    #find p

    solution = solution + "\np = -{}/3({})".format(b,a)

    p = -(b)/(3*a)

    solution = solution + "\np = {}\n".format(p)

    #find q

    solution = solution + "\nq = ({})³ + (({})({}) - 3({})({}))/(6({})²)".format(p,b,c,a,d,a)

    s0 = p**3

    s1 = b*c

    s2 = 3*a*d

    s3 = a**2

    solution = solution + "\nq = {} + ({}-{})/(6({}))".format(s0,s1,s2,s3)

    s4 = s1 - s2

    s5 = 6*s3

    solution = solution + "\nq = {} + {}/{}".format(s0,s4,s5)

    q = s0 + (s4/s5)

    solution = solution + "\nq = {}\n".format(q)

    #find r

    solution = solution +"\nr = {}/3({})".format(c,a)

    s6 = 3*a

    solution = solution + "\nr = {}/{}".format(c,s6)

    r = c/s6

    solution = solution + "\nr = {}\n".format(r)

    #solve for x

    solution = solution + "\nx = ³√({} + √(({})² + ({} - ({})²)³))  +  ³√({} - √(({})² + ({} - ({})²)³))  +  {}".format(q,q,r,p,q,q,r,p,p)

    s7 = q**2

    s8 = p**2

    #good luck, 19/3/2019

    solution = solution + "\nx = ³√({} + √({} + ({} - {})³))  +  ³√({} - √({} + ({} - {})³))  +  {}".format(q,s7,r,s8,q,s7,r,s8,p)

    s9 = r - s8

    s10 = s9**3

    solution = solution + "\nx = ³√({} + √({} + {}))  +  ³√({} - √({} + {}))  +  {}".format(q,s7,s10,q,s7,s10,p)

    try:
        s11 = math.sqrt(s7 + s10)
    except ValueError:
        print("error, sqr({}+{}) is unreal".format(s7,s10))
        s11 = "i"
        imaginary = True

    solution = solution + "\nx = ³√({} + {})  +  ³√({} - {})  +  {}".format(q,s11,q,s11,p)

    if imaginary == True:
        await ctx.send(solution)
    else:
        s12: float = numpy.cbrt(q + s11)  # type: ignore

        s13: float = numpy.cbrt(q - s11)  # type: ignore

        solution = solution + "\nx = {}  +  {}  +  {}".format(s12,s13,p)

        x = s12 + s13 + p

        await ctx.send(solution)

        await ctx.send("solution is {}".format(x))


def setup(crdbot: commands.Bot):
    crdbot.add_command(quadratic)
    crdbot.add_command(cubic)
