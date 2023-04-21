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
import rich
from rich.table import Table
from nextcord.ext import commands


async def on_ready_text(bot: commands.Bot):
    app_info = await bot.application_info()
    owner = app_info.owner.name
    table = Table(show_header=True, header_style="white bold",
                  title="Bot Informations", border_style="white", box=rich.box.ROUNDED, title_style="bold")
    table.add_column("OWNER", style="yellow bold")
    table.add_column("BOT", style="cyan bold")
    table.add_column("ID", style="magenta bold")
    table.add_column("GUILDS", style="green bold")

    table.add_row(
        str(owner),
        bot.user.name,
        str(bot.user.id),
        str(len(bot.guilds)),
    )

    return table
