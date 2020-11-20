from discord.ext import commands
import discord
import asyncio
import requests
import configparser
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="C.R.D.")

try:
    config = configparser.ConfigParser()
    config.read('stratos.ini')

except Exception:
    input("Error, something went wrong while parsing 'stratos.ini'. Ensure the file is not corrupt or missing.")
    exit(0)

class Weather(commands.Cog):
    
    def __init__(self, crdbot):
        self.crdbot = crdbot
        
    @commands.command()
    async def weather(self, ctx, loc, time):
        

        loc = loc.replace("_"," ")
        loc = loc.replace("-"," ")

        location = geolocator.geocode(loc)
        lat = location.latitude
        long = location.longitude
        #fcast = forecast(config["API Keys"]["darkskyKey"],lat,long)
        #fcast = json.dumps(urllib.request.urlopen("https://api.darksky.net/forecast/{}/{},{}?units=si&exclude=minutely,hourly,daily,alerts".format(config["API Keys"]["darkskyKey"],lat,long)))
        fcast = requests.get("https://api.darksky.net/forecast/{}/{},{}?units=si".format(config["API Keys"]["darkskyKey"],lat,long)).json()
        #print(fcast)
        
        hourl = ["hourly","hour","h"]
        dail = ["daily","dail","d"]
        currl = ["currently","current","curr","c"]

        print(time)
        
        if time in hourl:
            data = fcast["hourly"]["data"][1]
            fc = "Hourly"
        elif time in dail:
            data = fcast["daily"]
            fc = "Daily"
        elif time in currl:
            data = fcast["currently"]#["data"][1]
            fc = "Current"
        #else:
        #    await ctx.send("Did not recognise second argument. Correct command format: `;weather [location] [currently, hourly]`")
        #    return


        try:
            print(fcast["alerts"]["title"])
        except Exception as e:
            print("error,",e)
            print("no alerts, bro")
        
        print(fc)
        print("Icon: {}".format(data["icon"]))
        if data["icon"] == "clear-day":
            icon = "https://i.ibb.co/mvmpC6C/sunny.png"
        elif data["icon"] == "clear-night":
            icon = "https://i.ibb.co/wCZcrK5/clear-night.png"
        elif data["icon"] == "rain":
            icon = "https://i.ibb.co/hLb7TNW/rainy.png"
        elif data["icon"] == "snow":
            icon = "https://i.ibb.co/8sZDGjt/snow.png"
        elif data["icon"] == "sleet":
            icon = "https://i.ibb.co/PjfFSKM/sleet.png"
        elif data["icon"] == "wind":
            icon = "https://i.ibb.co/Gxmk02p/wind.png"
        elif data["icon"] == "fog":
            icon = "https://i.ibb.co/nBWn42N/fog.png"
        elif data["icon"] == "cloudy":
            icon = "https://i.ibb.co/qJgjz2q/cloudy.png"
        elif data["icon"] == "partly-cloudy-day":
            icon = "https://i.ibb.co/F4RH4Zh/partly-cloudy-day.png"
        elif data["icon"] == "partly-cloudy-night":
            icon = "https://i.ibb.co/9W1kn8y/partly-cloudy-night.png"
        else:
            icon = "https://cdn.discordapp.com/attachments/530795138415591434/530795583062016010/CRDindustries.png"

        wind = round((data["windSpeed"]/2.237),2)
        bearing = str(data["windBearing"])+"°"
        precip = str(round(data["precipProbability"]*100,2))+"%"
        humid = str(round(data["humidity"]*100,2))+"%"
        vis = round((data["visibility"]*1.60934),2)


        if fc != "Daily":
            temp = round(data["temperature"],2)#temp = round((data["temperature"]-32)*(5/9),2)
            tempF = round(((data["temperature"]*(9/5))+32),2)
            atemp = round(data["apparentTemperature"],2)#round((data["apparentTemperature"]-32)*(5/9),2)
            atempF = round(((data["apparentTemperature"]*(9/5))+32),2)
            desc = "{}\n\nTemperature: {}°C ({}°F)\nFeels like: {}°C ({}°F)\nHumidity: {}\nPrecipitation chance: {}\nVisibility: {} miles ({}km)\nPressure: {}mbar\n\n\n\n".format(
            fcast["daily"]["summary"],temp,tempF,atemp,atempF,humid,precip,data["visibility"],vis,data["pressure"])

        else:
            tempH = round(data["temperatureHigh"],2)#round((data["temperatureHigh"]-32)*(5/9),2)
            tempHF = round(((data["temperatureHigh"]*(9/5))+32),2)
            tempL = round(data["temperatureLow"],2)#round((data["temperatureLow"]-32)*(5/9),2)
            tempLF = round(((data["temperatureLow"]*(9/5))+32),2)
            atempH = round(data["apparentTemperatureHigh"],2)#round((data["apparentTemperatureHigh"]-32)*(5/9),2)
            atempHF = round(((data["apparentTemperatureHigh"]*(9/5))+32),2)
            atempL = round(data["apparentTemperatureLow"],2)#round((data["apparentTemperatureLow"]-32)*(5/9),2)
            atempHF = round(((data["apparentTemperatureLow"]*(9/5))+32),2)
            
            desc = "{}\n\nTemperature: Highs of {}°C ({}°F), lows of {}°C ({}°F)\nFeels like highs of {}°C ({}°F), lows of {}°C ({}°F)\nWind speed: {}m/s ({}mph)\n\nWind bearing: {}\nHumidity: {}\nPrecipitation chance: {}\nVisibility: {} miles ({}km)\nPressure: {}mbar\n\n\n\nPowered by DarkSky API https://darksky.net/poweredby/ (I'm legally required to put this 'somewhere prominent in my app or service')".format(
            fcast["daily"]["summary"],tempH,tempHF,tempL,tempLF,atempH,atempHF,atempL,atempHL,wind,data["windSpeed"],bearing,humid,precip,data["visibility"],vis,data["pressure"]),
        


        
        emb = discord.Embed(title = "{} forecast in {}".format(fc, location),
        type = "rich",
        description = desc,
        colour = 0x8cc43d,
        )
        emb.set_footer(text="Powered by DarkSky API - https://darksky.net/poweredby/")# (I'm legally required to put this 'somewhere prominent in my app or service')")
        emb.set_thumbnail(url=icon),
        await ctx.send(embed = emb)

    #'''
    @weather.error
    async def weather_error(self, ctx,err):
        print("yikes, bro") 
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Missing one or more arguments. Correct command format: `;weather [location] [currently, hourly]`")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send("I did not recognise your location. Is the spelling correct? You may also want to use underscores (_) for locations with multiple words.")
        else:
            await ctx.send("HUH")
    #'''   
def setup(crdbot):

    crdbot.add_cog(Weather(crdbot))
