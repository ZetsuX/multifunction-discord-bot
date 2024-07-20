import discord
import pymongo
import os
import json
import urllib.request as urllib2
from discord.ext import commands
from discord import app_commands

MONGODB = os.environ['MONGODB']

client = pymongo.MongoClient(MONGODB)
mydb = client["familiardb"]
mycol = mydb["user"]


class Pokeinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='pokeinfo',
        description='Check the information of a specific pokemon')
    @app_commands.describe(poke="The name of pokemon to check")
    async def pokemon_info(self, ctx: discord.Interaction, poke: str):
        pokeFind = mycol.find_one({"func": "pokedb"})
        pokeBasic = pokeFind["basic"]
        pokeElite = pokeFind["elite"]
        pokeEpic = pokeFind["epic"]
        pokeLegend = pokeFind["legend"]
        poke = poke[0].upper() + poke[1:].lower()

        if poke.lower() == 'porygon-z':
            poke = 'Porygon-Z'

        if poke in pokeBasic or poke in pokeElite or poke in pokeEpic or poke in pokeLegend:
            response = urllib2.urlopen(
                f'https://some-random-api.ml/pokemon/pokedex?pokemon={poke.lower()}'
            )
            data = json.loads(response.read())
            embedVar = discord.Embed(
                title=f"PokeInfo!",
                description=f'{poke} | ID : {str(data["id"])}',
                color=0xee1515)
            eleString = ', '.join(data["type"])
            evoString = ', '.join(data["family"]["evolutionLine"])
            if len(evoString) == 0:
                evoString = poke

            if poke in pokeBasic:
                rarityChk = 'Basic'

            elif poke in pokeElite:
                rarityChk = 'Advanced'

            elif poke in pokeEpic:
                rarityChk = 'Epic'

            elif poke in pokeLegend:
                rarityChk = 'Legendary'

            embedVar.add_field(name=f"[ General ]",
                               value='```' + f'Type     : {eleString}\n' +
                               f'Rarity   : {rarityChk}\n' +
                               f'Gen      : {data["generation"]}\n' +
                               f'Species  : {data["species"][0]}\n' +
                               f'Height   : {data["height"]}\n' +
                               f'Weight   : {data["weight"]}\n' + '```',
                               inline=True)

            embedVar.add_field(
                name=f"[ Stats (Lv. 1) ]",
                value='```' + f'HP       : {str(data["stats"]["hp"])}\n'
                f'Atk      : {str(data["stats"]["attack"])}\n' +
                f'Sp. Atk  : {str(data["stats"]["sp_atk"])}\n' +
                f'Def      : {str(data["stats"]["defense"])}\n' +
                f'Sp. Def  : {str(data["stats"]["sp_def"])}\n' +
                f'Speed    : {str(data["stats"]["speed"])}\n' + '```',
                inline=True)

            embedVar.add_field(
                name=f"[ Evolutionary ]",
                value='```' +
                f'Stage    : {data["family"]["evolutionStage"]}\n' +
                f'EvoPath  : {evoString}\n' + '```',
                inline=False)
            embedVar.set_thumbnail(url=data['sprites']['animated'])
            embedVar.set_footer(text=data["description"],
                                icon_url=data["sprites"]["normal"])
            await ctx.response.send_message(embed=embedVar)

        else:
            await ctx.response.send_message(
                "Pokemon yang anata cari tidak / belum terdaftar, coba dicek lagi yah..",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(Pokeinfo(bot))
