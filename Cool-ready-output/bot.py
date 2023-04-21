# ----------------- WATERMARK ----------------- #
"""
 ________  ________ ________     
|\   __  \|\  _____\\   ____\    
\ \  \|\  \ \  \__/\ \  \___|    
 \ \   __  \ \   __\\ \  \       
  \ \  \ \  \ \  \_| \ \  \____  
   \ \__\ \__\ \__\   \ \_______\
    \|__|\|__|\|__|    \|_______|
"""
# ----------------- WATERMARK ----------------- #
import dotenv
import nextcord
from nextcord.ext import commands
from rich.console import Console
import os
from dotenv import load_dotenv
from settings import *


dotenv_file = dotenv.find_dotenv()
load_dotenv(dotenv_file)

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(intents=nextcord.Intents.all(), help_command=None,
                   case_insensitive=True)


@bot.event
async def on_ready():
    console = Console()
    console.print(await on_ready_text(bot))

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
