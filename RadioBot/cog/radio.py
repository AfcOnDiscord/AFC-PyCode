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


import nextcord
from nextcord.ext import commands
import nextwave

songs = {
    "Trashpop": "https://streams.ilovemusic.de/iloveradio19.mp3",
    "I Love Radio": "https://streams.ilovemusic.de/iloveradio1.mp3",
    "2 Dance": "https://streams.ilovemusic.de/iloveradio2.mp3",
    "2000+ Throwbacks": "https://streams.ilovemusic.de/iloveradio37.mp3",
    "2010+ Throwbacks": "https://streams.ilovemusic.de/iloveradio38.mp3",
    "Bass by HBZ": "https://streams.ilovemusic.de/iloveradio29.mp3",
    "Chillhop": "https://streams.ilovemusic.de/iloveradio17.mp3",
    "Dance 2023": "https://streams.ilovemusic.de/iloveradio36.mp3",
    "Dance First!": "https://streams.ilovemusic.de/iloveradio103.mp3",
    "Dance history": "https://streams.ilovemusic.de/iloveradio26.mp3",
    "Deutschrap Beste": "https://streams.ilovemusic.de/iloveradio6.mp3",
    "Deutschrap first!": "https://streams.ilovemusic.de/iloveradio104.mp3",
    "Greatest hits": "https://streams.ilovemusic.de/iloveradio16.mp3",
    "Hardstyle": "https://streams.ilovemusic.de/iloveradio21.mp3",
    "Hip Hop": "https://streams.ilovemusic.de/iloveradio3.mp3",
    "Hip Hop history": "https://streams.ilovemusic.de/iloveradio27.mp3",
    "Hits 2023": "https://streams.ilovemusic.de/iloveradio109.mp3",
    "Hits history": "https://streams.ilovemusic.de/iloveradio12.mp3",
    "X-Max": "https://streams.ilovemusic.de/iloveradio8.mp3",
    "The 90s": "https://streams.ilovemusic.de/iloveradio24.mp3",
    "Party Hard": "https://streams.ilovemusic.de/iloveradio14.mp3"
}

radio_urls = {
    "https://streams.ilovemusic.de/iloveradio19.mp3": "Trashpop",
    "https://streams.ilovemusic.de/iloveradio1.mp3": "I Love Radio",
    "https://streams.ilovemusic.de/iloveradio2.mp3": "2 Dance",
    "https://streams.ilovemusic.de/iloveradio37.mp3": "2000+ Throwbacks",
    "https://streams.ilovemusic.de/iloveradio38.mp3": "2010+ Throwbacks",
    "https://streams.ilovemusic.de/iloveradio29.mp3": "Bass by HBZ",
    "https://streams.ilovemusic.de/iloveradio17.mp3": "Chillhop",
    "https://streams.ilovemusic.de/iloveradio36.mp3": "Dance 2023",
    "https://streams.ilovemusic.de/iloveradio103.mp3": "Dance First!",
    "https://streams.ilovemusic.de/iloveradio26.mp3": "Dance history",
    "https://streams.ilovemusic.de/iloveradio6.mp3": "Deutschrap Beste",
    "https://streams.ilovemusic.de/iloveradio104.mp3": "Deutschrap first!",
    "https://streams.ilovemusic.de/iloveradio16.mp3": "Greatest hits",
    "https://streams.ilovemusic.de/iloveradio21.mp3": "Hardstyle",
    "https://streams.ilovemusic.de/iloveradio3.mp3": "Hip Hop",
    "https://streams.ilovemusic.de/iloveradio27.mp3": "Hip Hop history",
    "https://streams.ilovemusic.de/iloveradio109.mp3": "Hits 2023",
    "https://streams.ilovemusic.de/iloveradio12.mp3": "Hits history",
    "https://streams.ilovemusic.de/iloveradio8.mp3": "X-Max",
    "https://streams.ilovemusic.de/iloveradio24.mp3": "The 90s",
    "https://streams.ilovemusic.de/iloveradio14.mp3": "Party Hard"
}


class RadioCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await nextwave.NodePool.create_node(bot=self.bot, host="host", port=0000, password="password")

    @nextcord.slash_command(name="play", description="Play a song")
    async def _play(self, ctx: nextcord.Interaction, radio: str = nextcord.SlashOption(required=True, choices=songs)):
        vc: nextwave.Player = (ctx.guild.voice_client or await ctx.user.voice.channel.connect(cls=nextwave.Player))
        track = await nextwave.NodePool.get_node().get_tracks(cls=nextwave.Track, query=radio)
        if not vc.is_playing():
            await vc.play(track[0])
            await ctx.response.send_message(f"Playing **`{radio_urls[radio]}`**")
            return
        if vc.is_playing():
            if vc.is_paused():
                return await ctx.response.send_message(f"I'm paused, use **`/resume`** to resume the song")
            else:
                return await ctx.response.send_message(f"You need to stop the current song with **`/stop`** before playing another one")

    @nextcord.slash_command(name="pause", description="Pause the current song")
    async def _pause(self, ctx: nextcord.Interaction):
        vc: nextwave.Player = ctx.guild.voice_client
        if vc.is_paused() or not vc.is_playing():
            return await ctx.response.send_message("I'm already paused or there is no song playing :/")
        if vc.is_playing():
            await vc.pause()
            await ctx.response.send_message("I paused the song for you, daddy :3")

    @nextcord.slash_command(name="resume", description="Resume the current song")
    async def _resume(self, ctx: nextcord.Interaction):
        vc: nextwave.Player = ctx.guild.voice_client
        if not vc.is_paused():
            return await ctx.response.send_message("How to resume a song that is not paused?")

        if vc.is_paused():
            await vc.resume()
            await ctx.response.send_message("I resumed the song for you, daddy :3")

    @nextcord.slash_command(name="stop", description="Stop the current song")
    async def _stop(self, ctx: nextcord.Interaction):
        vc: nextwave.Player = ctx.guild.voice_client
        if not vc.is_playing():
            return await ctx.response.send_message("Bro, the song is already stopped :/")
        if vc.is_playing():
            await vc.stop()
            await ctx.response.send_message("I stopped the song for you, daddy :3")


def setup(bot: commands.Bot):
    bot.add_cog(RadioCog(bot))
