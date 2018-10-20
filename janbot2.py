import os
import discord
from discord.ext import commands

client = discord.Client()

@client.event
async def on_ready():
    print("Zalogowano jako " + str(bot.user))

def main():
    try:
        client.run(os.getenv('TOKEN'))
    except Exception as e:
        print("Exception: " + str(e))

if __name__ == "__main__":
    main()
