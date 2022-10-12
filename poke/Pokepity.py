import discord
import pymongo
import os
import json
import urllib.request as urllib2
from discord.ext import commands
from discord.commands import Option
import datetime
from discord.ui import Select, Button, Modal, InputText, View
from discord.ext import commands
from discord.commands import Option
import numpy as np

guilds = [990445490401341511, 1020927428459241522, 989086863434334279, 494097970208178186, 1028690906901139486]

MONGODB = os.environ['MONGODB']

client = pymongo.MongoClient(MONGODB)
mydb = client["familiardb"]
mycol = mydb["user"]

class Pokepity(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command(name='pokepity', description='Check how many catches left for you to get pity at /pokecatch')
  async def pokemon_pity(self, ctx):
    userFind = mycol.find_one({"userid": str(ctx.author.id)})
    if userFind == None:
        await ctx.respond(
            f'Neee {ctx.author.name}-nyan, yuk /regist dulu yuk baru liat pokemon..',
            ephemeral=True)
        return

    epicPity = userFind["epicpity"]
    if epicPity > 30:
        epicPity = 30

    legendPity = userFind["legendpity"]
    if legendPity > 100:
        legendPity = 100

    embedVar = discord.Embed(
        title=f"〘 {ctx.user.name}-nyan's PokeCatch Pity 〙",
        description=
        f"- Epic : {30 - epicPity} catch(es) left!\n- Legendary : {100 - legendPity} catch(es) left!",
        color=0xee1515)
    embedVar.set_footer(text="— May good luck bless you in /pokecatch!",
                        icon_url=ctx.author.avatar.url)
    await ctx.respond(embed=embedVar)

def setup(bot):
  bot.add_cog(Pokepity(bot))