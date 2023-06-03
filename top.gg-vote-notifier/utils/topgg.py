import aiohttp


async def send_post_request(webhook, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook, data=data) as resp:
            pass


async def auth(authorization):
    if (
        authorization != "your authorization here"
    ):  # https://top.gg/bot/<bot_id>/webhooks -> Authorization
        return False
    else:
        return True
