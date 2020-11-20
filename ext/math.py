from discord.ext import commands
import discord
import asyncio
import math
import numpy

class MathCommands(commands.Cog):

    def __init__(self, crdbot):
        self.crdbot = crdbot
        
    @commands.command(pass_context=True)
    async def quadratic(self,ctx, a, b, c):

        imaginary = False
        
        a = int(a)
        b = int(b)
        c = int(c)

        
        s1 = -b

        s2 = b**2

        s3 = int(4* a *c)

        s4 = s2 - s3

        s5 = 2 * a

        #await ctx.send("(-({}) +- sqrt(({})^2-4({})({})))/2({})".format(b,b,a,c,a))
                         
        #await ctx.send("({} +- sqrt({}-{}))/{}".format(s1,s2,s3,s5))

        s6 = s2 - s3

        #await ctx.send("({} +- sqrt({}))/{}".format(s1,s6,s5))

        try:
            s7 = math.sqrt(s6)
        except Exception:
            imaginary = True
            s7 = "sqrt({})".format(s6)
            print("divide by 0 1")
            #return()
          
        #await ctx.send("({} +- {})/{}".format(s1,s7,s5))

        if imaginary == True:
            s8 = "{}+{}".format(s1,s7)
        else:
            s8 = s1 + s7

          
        #await ctx.send("Solution 1:\n{}/{}".format(s8,s5))
          

        try:
            if imaginary == True:
                s9 = "{}/{}".format(s8,s5)
            else:
                s9 = s8/s5
        except ZeroDivisionError:
            imaginary == True
            print("divide by 0 2")
            s9 = "{}/{}".format(s8,s5)
            #return()

        #await ctx.send("x = {}".format(s9))

        if imaginary == True:
            s10 = "{}-{}".format(s1,s7)
        else:
            s10 = s1 - s7

        #await ctx.send("Solution 2:\n{}/{}".format(s10,s5))

        try:
            if imaginary == True:
                s11 = "{}/{}".format(s10,s5)
            else:
                s11 = s10/s5
        except ZeroDivisionError:
            imaginary = True
            print("divide by 0 3")
            s11 = "{}/{}".format(s10,s5)
            #return()

        



        #await ctx.send("x = {}".format(s11))
        solution = "(-({}) +- sqrt(({})^2-4({})({})))/2({})\n({} +- sqrt({}-{}))/{}\n({} +- sqrt({}))/{}\n({} +- {})/{}\nSolution 1:\n{}/{}\nx = {}\nSolution 2:\n{}/{}\nx = {}".format(b,b,a,c,a,s1,s2,s3,s5,s1,s6,s5,s1,s7,s5,s8,s5,s9,s10,s5,s11) 
        
        emb = discord.Embed(
            title = "Solving quadratic equation {}x² + {}x + {}".format(a,b,c),
            #description = solution,
            colour = 0x8cc43d,
            
            )
        if imaginary == True:
            emb.title = "Solving quadratic equation {}x² + {}x + {} - Error, imaginary number!".format(a,b,c)
            
        emb.add_field(name = "Solution 1", value = "Solution 1:\n{}/{}\nx = {}".format(s8,s5,s9), inline = True)
        emb.add_field(name = "Solution 2", value = "Solution 2:\n{}/{}\nx = {}".format(s10,s5,s11), inline = True)
        emb.add_field(name = "Method", value = "-({}) +- sqrt(({})^2-4({})({})))/2({})\n({} +- sqrt({}-{}))/{}\n({} +- sqrt({}))/{}\n({} +- {})/{}".format(b,b,a,c,a,s1,s2,s3,s5,s1,s6,s5,s1,s7,s5), inline = False)
        await ctx.send(embed = emb)

    @quadratic.error
    async def quadratic_error(err,ctx):
        
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing one or more arguments. Correct command format: `;quadratic [a] [b] [c]`")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send("Looks like one of the arguments (a, b or c) is incorrect. Are they all integers (whole numbers)?")

    @commands.command(pass_context=True)
    async def cubic(self, ctx, a, b, c, d):

        imaginary = False

        
        a = int(a)
        b = int(b)
        c = int(c)
        d = int(d)



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

        unreal = False
        
        try:
            s11 = math.sqrt(s7 + s10)
        except ValueError:
            print("error, sqr({}+{}) is unreal".format(s7,s10))
            s11 = "i"
            unreal = True
            
        solution = solution + "\nx = ³√({} + {})  +  ³√({} - {})  +  {}".format(q,s11,q,s11,p)

        if unreal == True:
            await ctx.send(solution)
        else:
            s12 = numpy.cbrt(q + s11)

            s13 = numpy.cbrt(q - s11)

            solution = solution + "\nx = {}  +  {}  +  {}".format(s12,s13,p)

            x = s12 + s13 + p
        
            await ctx.send(solution)

            await ctx.send("solution is {}".format(x))


def setup(crdbot):

    crdbot.add_cog(MathCommands(crdbot))
