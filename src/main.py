from discord_bot import DiscordBot

def main():
    bot = DiscordBot() # Create an instance of the bot
    bot.run() # Call the run method to start the bot

if __name__ == "__main__": # Telling Python which function to execute first when the script is run directly
    main()