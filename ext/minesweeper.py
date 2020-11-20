from discord.ext import commands
import discord
import asyncio
import random

class Minesweeper(commands.Cog):
    def __init__(self, crdbot):
        self.crdbot = crdbot


    @commands.command()
    async def minesweeper(self, ctx, *args):
        #documentation
        '''
        Minesweeper.py by Chris Dance.

        Version: 0.1.2_minor

        release = final version for a while
        major = large update
        minor = small update
        hotfix = quick bug fix

        '''

        size = 8

        dif = 0.15,0.3,"normal"

        for arg in args:

            print(arg)
            try:
                arg2 = int(arg)
                if isinstance(arg2,int):
                    size = int(arg)
                    
            except:

                if arg in ["easy","e"]:
                    dif = 0.1,0.2,"easy"
                if arg in ["normal","medium,","n","m"]:
                    dif = 0.15,0.3,"normal"
                if arg in ["hard","h"]:
                    dif = 0.2,0.4,"hard"
                if arg in ["expert","ex"]:
                    dif = 0.3,0.475,"expert"
                if arg in ["death","d"]:
                    dif = 0.4,0.65,"death"


        #define variables
        lis = []
        minesplanted = 0
        user = False
        useext = False

        #MANUAL OVERRIDE - SET TO "False" TO NOT USE SPOILER

        spoilers = True

        #end init

        #a function that prints the grid
        def printgrid():

          out = ""
          x = 0
          
          #loop until the whole grid is printed
          while x != n:

            out = out + grid[x] + "\n"
            x = x + 1

          return out


        #a function that generates a grid given two inputs n and m, where n is the size of the grid in the x coordinate and m is the size of the grid in the y coordinate
        def gridsize(n,m):

            x = 0
            canvasx = "."
              
            #generate a string with as many dots as the number "n"
            while x != n-1:
                
                canvasx = canvasx + "."
                x = x + 1

            x = 0
            canvasy = [canvasx]
            
            #repeat "canvasx" m times and output to the list canvasy
            while x != m-1:       
            
                canvasy.append(canvasx)
                x = x + 1
                #print(canvasy)

            return(canvasy)

        #a function that plants a mine somewhere at random in the list "grid"
        def plantmine():
            
            #pick a random line in the minesweeper grid
            num = random.randint(0,m-1)
            #pick a random character in the line
            pick = random.randint(0,n-1)
            
            gridtemp = grid[num]
            
            gridtempL = gridtemp[0:pick]
            gridtempR = gridtemp[pick:len(gridtemp)-1]#-2]

            grid[num] = gridtempL + "X" + gridtempR



        #split and process input by calling gridsize()
        n = int(size)
        if n > 14:
            await ctx.send("Sorry, a grid larger than 14x14 is over 2000 characters in length. Try generating a grid slightly smaller.")
            return
        if n <= 0:
            await ctx.send("Sorry, but a grid of size {} isn't really possible. Try again.".format(n))
            return
        m = n

        #redefine grid - it will be used as the string that contains the minesweeper grid
        grid = gridsize(n,m)
        x = 0 


        #generates a random number where 10% of total tiles <= mineno <= 30% of total tiles
        

        
        mineno = round((random.uniform(dif[0]*(len(grid)**2), dif[1]*(len(grid)**2))))
        
        while minesplanted != mineno:
            plantmine()
            minesplanted = minesplanted + 1
        '''
            
        if minesplanted > minescounted:
          #print("looks like some mines were lost. fixing...")      
          plantmine()  

        '''
        printgrid()

        #start to number grid

        posx = -1
        posy = -1
        newgrid = grid
        start = True

        for y in grid:
          posy = posy + 1

          nearby = 0
          
          while posx != len(y)-1:
            posx = posx + 1
            x = 0
            nearby = 0

            if y[posx] != "X":
              
              try:
                if y[posx+1] == "X" and posx < n-1:#right
                  nearby = nearby + 1
              except IndexError:
                pass
              if y[posx-1] == "X" and posx > 0:#left
                nearby = nearby + 1

              try:
                
                if grid[posy-1][posx] == "X" and start == False:#up
                  nearby = nearby + 1
              except IndexError:
                pass        
              try:
                if grid[posy+1][posx] == "X":#down
                  nearby = nearby + 1
              except IndexError:
                pass

              try:
                if grid[posy-1][posx+1] == "X" and start == False and posx < n-1:#topright
                  nearby = nearby + 1
              except IndexError:
                pass
              if grid[posy-1][posx-1] == "X" and start == False and posx > 0:#topleft
                nearby = nearby + 1
                
              try:
                if grid[posy+1][posx+1] == "X" and posx < n-1:#bottomright
                  nearby = nearby + 1
              except IndexError:
                pass
              try:
                if grid[posy+1][posx-1] == "X" and posx > 0:#bottomleft
                  nearby = nearby + 1
              except IndexError:
                pass
              
              x = nearby
              #print(nearby)
              
              gridtempL = newgrid[posy][0:posx]
              gridtempR = newgrid[posy][posx+1:len(y)-1]

              newgrid[posy] = gridtempL + str(x) + gridtempR
            else:
              if posx == int(n)-1:
                newgrid[posy] = newgrid[posy][0:posx] + "X"
                
          posx = -1
          start = False

        grid = newgrid
        grid = printgrid()


        totalmines = len(grid) - len(grid.replace("X",""))

          
        #discord stuff now

        if spoilers == True:
            spoilerstring = "||"
        else:
            spoilerstring = ""

        #emotify
        x = 0
        newgrid = ""

        #unspoilt grid for reveal
        unspoilt = ""
        
        while x != len(grid)-1:

            if "1" == grid[x]:
                newgrid = newgrid + spoilerstring + ":one:" + spoilerstring
                unspoilt = unspoilt + ":one:" 
              
            elif "2" == grid[x]:
                newgrid = newgrid + spoilerstring + ":two:" + spoilerstring
                unspoilt = unspoilt + ":two:"
              
            elif "3" == grid[x]:
                newgrid = newgrid + spoilerstring + ":three:" + spoilerstring
                unspoilt = unspoilt + ":three:"
              
            elif "4" == grid[x]:
                newgrid = newgrid + spoilerstring + ":four:" + spoilerstring
                unspoilt = unspoilt + ":four:"
              
            elif "5" == grid[x]:
                newgrid = newgrid + spoilerstring + ":five:" + spoilerstring
                unspoilt = unspoilt + ":five:"
              
            elif "6" == grid[x]:
                newgrid = newgrid + spoilerstring + ":six:" + spoilerstring
                unspoilt = unspoilt + ":six:"
              
            elif "7" == grid[x]:
                newgrid = newgrid + spoilerstring + ":seven:" + spoilerstring
                unspoilt = unspoilt + ":seven:"
              
            elif "8" == grid[x]:
                newgrid = newgrid + spoilerstring + ":eight:" + spoilerstring
                unspoilt = unspoilt + ":eight:" 
              
            elif "9" == grid[x]:
                newgrid = newgrid + spoilerstring + ":nine:" + spoilerstring
                unspoilt = unspoilt + ":nine:" 
              
            elif "X" == grid[x]:
                newgrid = newgrid + spoilerstring + ":bomb:" + spoilerstring
                unspoilt = unspoilt + ":bomb:" 
              
            elif "0" == grid[x]:
                newgrid = newgrid + spoilerstring + ":zero:" + spoilerstring
                unspoilt = unspoilt + ":zero:"
              
            elif "\n" == grid[x]:
                newgrid = newgrid + "\n"
                unspoilt = unspoilt + "\n" 
            x = x + 1

        #grid = newgrid
        print("ok")

        #await ctx.send(newgrid) 
        
        emb = discord.Embed(title = "{}x{} grid Minesweeper game, requested by {}\n{} mines\n**{}** Mode".format(n,m,ctx.message.author,totalmines,dif[2].capitalize()),
        type = "rich",
        description = newgrid,
        colour = ctx.message.author.color
        )#0x8cc43d,


        emb.set_footer(text="A game of Minesweeper! Play by clicking the spoilers. Try to click all tiles but the bombs. If you click a bomb, you lose the game.\nReact with \U0001F1F7 to reveal the mines if you give up.",icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}".format(ctx.message.author))
        msg = await ctx.send(embed=emb)#, file=f)

        await msg.add_reaction("\U0001F1F7")
        #passed = False
        while msg:
            await self.crdbot.wait_for("reaction_add", check = lambda reaction, user:reaction.emoji == "\U0001F1F7")
            msg2 = await ctx.fetch_message(msg.id)
            
            reactsO = msg2.reactions

            async for y in reactsO[0].users():
                
                
                if ctx.message.author == y:
                    emb.description = unspoilt
                    emb.title = "{}x{} grid Minesweeper game, requested by {}\n{} mines\n**{}** Mode\nGiven up! Field has been revealed.".format(n,m,ctx.message.author,totalmines,dif[2].capitalize())
                    await msg.edit(embed = emb)




    #'''
    @minesweeper.error
    async def minesweeper_error(self, ctx, err):

        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing an argument. Correct command format: `;minesweeper x`, where x is the grid size. If x is 8, the grid will be 8\*8.")

        if isinstance(err, commands.CommandInvokeError):
            await ctx.send("Incorrect command format, or you tried to generate a grid larger than 14x14. Correct command format: `;minesweeper x`, where x is the grid size. If x is 8, the grid will be 8\*8.")

    #'''

def setup(crdbot):

    crdbot.add_cog(Minesweeper(crdbot))
