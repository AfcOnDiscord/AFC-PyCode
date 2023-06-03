from quart import Quart, request, jsonify, abort, render_template, redirect, url_for
import json
import os
from utils.user import get_user_data
from utils.topgg import send_post_request, auth

app = Quart(__name__)
app.secret_key = os.urandom(32)

webhook = "Your webhook here"


@app.route("/")
async def index():
    return jsonify({"webhook": "Hello, world!"})


@app.route("/topgg/", methods=["POST"])
async def topgg():
    authorization = request.headers["Authorization"]
    if not await auth(authorization):
        return jsonify({"error": "401 Unauthorized"})

    data = json.loads(await request.data)

    user, avatar_url = await get_user_data(data)

    webhook_data = {
        "username": f"{user['username']}",
        "avatar_url": str(avatar_url),
        "content": f"**User :** {user['username']}#{user['discriminator']}\n**ID :** {data['user']}",
    }

    await send_post_request(webhook, webhook_data)

    return data


if __name__ == "__main__":
    app.run(host=your host, port=your port)