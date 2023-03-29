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

import os
import openai
import aiosqlite
import nextcord
from nextcord.ext import commands, tasks
from dotenv import load_dotenv, find_dotenv

# # # # # # # # # # # # # # # # # # # # # # # #
# -------------- Dein API KEY --------------- #
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
# ------------------------------------------- #
# # # # # # # # # # # # # # # # # # # # # # # #


class gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.t = None

    async def get_chat(self, prompt):
        completion = openai.ChatCompletion.create(
            n=1,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content

    async def is_user_in_db(self, user_id, guild_id):
        async with aiosqlite.connect("openai.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT user_id FROM openai WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
                result = await cursor.fetchone()
                if result is None:
                    return False
                else:
                    return True

    async def add_user_to_db(self, user_id, guild_id):
        async with aiosqlite.connect("openai.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("INSERT INTO openai (user_id, guild_id) VALUES (?, ?)", (user_id, guild_id))
                await db.commit()

    async def remove_user_from_db(self, user_id, guild_id):
        async with aiosqlite.connect("openai.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM openai WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
                await db.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("openai.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS openai (id INTEGER PRIMARY KEY, user_id INTEGER, guild_id INTEGER)")
                await db.commit()
        self._loop_remove_users.start()

    @tasks.loop(seconds=30)
    async def _loop_remove_users(self):
        async with aiosqlite.connect("openai.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM openai")
                await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        if message.channel.id == 1052218472521814096:
            if message.content.startswith("--"):
                return
            if await self.is_user_in_db(message.author.id, message.guild.id):
                return await message.reply("Please wait for your previous request to finish.")
            msg = await message.reply(f"Please wait ...")
            await self.add_user_to_db(message.author.id, message.guild.id)
            try:
                self.t = await self.get_chat(message.content)
            except Exception as e:
                print(e)
                await msg.edit(content="An error occurred. Please try again later.")
                await self.remove_user_from_db(message.author.id, message.guild.id)
                return
            if len(self.t) > 2000:
                messages = []
                for i in range(0, len(self.t), 2000):
                    messages.append(self.t[i:i+2000])
                for msg2 in messages:
                    await message.reply(msg2)
                await msg.delete()
                return await self.remove_user_from_db(message.author.id, message.guild.id)
            await msg.edit(content=self.t)
            await self.remove_user_from_db(message.author.id, message.guild.id)


def setup(bot):
    bot.add_cog(gpt(bot))
