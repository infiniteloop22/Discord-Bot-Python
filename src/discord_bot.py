import discord
from discord.ext import commands
import json
import datetime
import requests
import random
import asyncio

class DiscordBot():
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True # Ensure that the bot can read message content
        # Create the bot instance
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        # Store the start time
        self.start_time = datetime.datetime.utcnow()

        # Event: When the bot is ready
        @self.bot.event
        async def on_ready():
            print(f'Logged in as {self.bot.user}')
        
        # Command: Responds to !ping
        @self.bot.command()
        async def ping(ctx):
            await ctx.send("Pong!")

        @self.bot.command()
        async def uptime(ctx):
            uptime = datetime.datetime.utcnow() - self.start_time

            uptime_str = f"Uptime: {uptime.seconds} seconds"
            await ctx.send(uptime_str)
        
        @self.bot.command()
        async def trivia(ctx):
            # Fetch trivia questions from the Open Trivia Database API
            response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
            data = response.json() # Parse the JSON response

            # Randomly select one question
            question_data = random.choice(data['results'])

            # Create the info dictionary
            info = { 
                "question" : question_data['question'], 
                "correct_answer" : question_data['correct_answer'], 
                "options" : question_data['incorrect_answers'] 
            }

            # Append the correct answer to the list of options
            info['options'].append(info['correct_answer'])

            # Shuffle the options so the correct answer isn't always in the same position
            random.shuffle(info['options'])

            # Send the question and options to the user
            await ctx.send(f"**Question:** {info['question']}")
            await ctx.send("**Options:**")
            # Looping over each element in info['options'], but giving both the index (idx) and the value (option) starting from index 1.
            for i in range(len(info["options"])): # Return each element from the list starting at index 1 rather than 0
                await ctx.send(f"{i+1}. {info['options'][i]}")

            # Wait for user's answer
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

            try:
                # Wait for the user's message (with a timeout of 30 seconds)
                msg = await self.bot.wait_for('message', check=check, timeout=30)

                # Check if the answer is correct
                user_answer = int(msg.content)  # Convert the user's input to an integer
                if info['options'][user_answer - 1] == info['correct_answer']: # List is 0-indexed, so -1 
                    await ctx.send(f"Correct! The right answer was: {info['correct_answer']}")
                else:
                    await ctx.send(f"Wrong! The right answer was: {info['correct_answer']}")

            except asyncio.TimeoutError:
                await ctx.send("You took too long to answer!")


    def load_api_key(self) -> str:
        with open(".\src\config.json", 'r') as file:
            config = json.load(file)
        return config["DISCORD_TOKEN"]

    def run(self):
        token = self.load_api_key()
        self.bot.run(token)