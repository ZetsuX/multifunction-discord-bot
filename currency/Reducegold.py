import discord
import os
import pymongo
from discord.ext import commands
from discord import app_commands

MONGODB = os.environ['MONGODB']

client = pymongo.MongoClient(MONGODB)
mydb = client["familiardb"]
mycol = mydb["user"]


class Reducegold(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='reducegold',
        description=
        'Reduce gold for the mentioned user (or to self if without mention)')
    @app_commands.checks.has_any_role('Encoder Magang', 'Owner')
    @app_commands.describe(
        number="Number of gold to reduce",
        member="The member to reduce gold from (or self if empty)")
    async def gold_reduce(self,
                          ctx: discord.Interaction,
                          number: int,
                          member: discord.Member = None):
        if number <= 0:
            await ctx.response.send_message(
                f'Neee anata ngga jelas deh, {ctx.user.name}-nyan',
                ephemeral=True)
            return

        await ctx.response.defer()

        if not member:
            userID = ctx.user.id
        else:
            userID = member.id

        userFind = mycol.find_one({"userid": str(userID)})
        mentionUser = '<@' + str(userID) + '>'
        if userFind == None:
            await ctx.followup.send(
                f'{mentionUser}-nyan belum terdaftar nih, /regist dulu yuk')

        else:
            goldCount = userFind["gold"]
            if goldCount == 0:
                await ctx.followup.send(
                    f'Goldnya {mentionUser}-nyan sudah habis nih, apalagi yang mau dikurangi'
                )
            else:
                goldCount -= number
                if goldCount < 0:
                    goldCount = 0
                newvalues = {"$set": {"gold": goldCount}}
                mycol.update_one(userFind, newvalues)
                await ctx.followup.send(
                    f'Goldnya {mentionUser}-nyan berhasil dikurangi menjadi {goldCount}'
                )


async def setup(bot):
    await bot.add_cog(Reducegold(bot))
