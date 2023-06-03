import aiohttp


async def get_user_data(data):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://discord.com/api/users/{data['user']}",
            headers={"Authorization": f"Bot bot_token_here"},  # Any bot token
        ) as resp:
            user_infos_from_discord_api = await resp.json()
            if user_infos_from_discord_api["avatar"] is None:
                avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
            else:
                avatar_url = f"https://cdn.discordapp.com/avatars/{data['user']}/{user_infos_from_discord_api['avatar']}.png"

    return user_infos_from_discord_api, avatar_url
