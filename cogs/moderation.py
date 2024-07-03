import discord
from discord.ext import commands
from os import path

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        current_directory = path.dirname(path.realpath(__file__))
        parent_directory = path.dirname(current_directory)
        file_path = path.join(parent_directory, 'bannedWords.txt')
        
        with open(file_path, 'r') as f:
            self.banned_words = f.read().splitlines()
            self.filter_on = False
            print(self.banned_words)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if any(word in message.content.lower() for word in self.banned_words) and self.filter_on == True:
            await message.delete()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, amount: int):
        if amount > 20:
            await ctx.send("You can't delete more than 20 messages at once.")
        elif amount == 0:
            await ctx.send("Can't delete 0 messages")
        else:
            await ctx.channel.purge(limit=amount+1)

    @commands.command()
    async def filter(self, ctx):
        if self.filter_on == False:
            self.filter_on = True
            await ctx.send("Chat filter turned on")
        else:
            self.filter_on = False
            await ctx.send("Chat filter turned off")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
