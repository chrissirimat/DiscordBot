from os import path
import discord
from discord.ext import commands
import random

class WordleGame:
    def __init__(self):
        current_directory = path.dirname(path.realpath(__file__))
        parent_directory = path.dirname(current_directory)
        file_path = path.join(parent_directory, 'wordle.txt')
        with open(file_path, 'r') as f:
            self.word_list = [line.strip() for line in f]
            
        self.target_word = random.choice(self.word_list)
        print(self.target_word)
        self.guesses = []

        current_directory = path.dirname(path.realpath(__file__))
        parent_directory = path.dirname(current_directory)
        file_path = path.join(parent_directory, 'dictionary.txt')
        with open(file_path, 'r') as f:
            self.dictionary = [line.strip() for line in f]

    def guess(self, word):
        word = word.lower()
        if len(word) != 5:
            return "Guesses must be 5 letters long.", False

        if word not in self.dictionary:
            return "Guesses must be actual words", False

        if len(self.guesses) >= 6:
            return "You've reached the maximum number of guesses.", False

        self.guesses.append(word)

        if word == self.target_word:
            return "Congratulations! You've guessed the word.", True

        result = []
        for i in range(5):
            if word[i] == self.target_word[i]:
                result.append('🟩')
            elif word[i] in self.target_word:
                result.append('🟨')
            else:
                result.append('🟥')

        return "".join(result), False

class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.group(invoke_without_command=True)
    async def wordle(self, ctx):
        await ctx.send("Please use `!wordle start` to start a game or `!wordle end` to end a game.")

    @wordle.command()
    async def start(self, ctx):
        if ctx.channel.id in self.games:
            await ctx.send("A game is already ongoing in this channel.")
            return

        self.games[ctx.channel.id] = WordleGame()
        await ctx.send("Started a new game of Wordle!")

    @wordle.command(aliases=['max'])
    async def guess(self, ctx, word: str):
        game = self.games.get(ctx.channel.id)
        if not game:
            await ctx.send("No game is currently ongoing in this channel.")
            return

        print(game.guess(word))
        result, guessed = game.guess(word)
    

        await ctx.send(result)


        if guessed or len(game.guesses) >= 6:
            del self.games[ctx.channel.id]
            await ctx.send("Ended the game of Wordle.")



    @wordle.command()
    async def end(self, ctx):
        if ctx.channel.id not in self.games:
            await ctx.send("No game is currently ongoing in this channel.")
            return

        del self.games[ctx.channel.id]
        await ctx.send("Ended the game of Wordle.")

async def setup(bot):
   await bot.add_cog(Wordle(bot))

