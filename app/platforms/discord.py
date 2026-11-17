
import os
import httpx

from datetime import datetime


async def post_to_discord(message: str):

    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")

    if not bot_token or not channel_id:
        raise ValueError("Discord credentials are missing")

    base_url = "https://discord.com/api/v10"

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=20) as client:

        # Get channel details to retrieve server ID
        channel_response = await client.get(
            f"{base_url}/channels/{channel_id}",
            headers=headers
        )

        channel_response.raise_for_status()

        channel_data = channel_response.json()
        guild_id = channel_data.get("guild_id")

        if not guild_id:
            raise ValueError("This is not a server text channel")

        # Publish the message
        payload = {
            "content": message,
            "allowed_mentions": {
                "parse": []
            }
        }

        response = await client.post(
            f"{base_url}/channels/{channel_id}/messages",
            headers=headers,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

    message_id = data["id"]

    posted_at = datetime.fromisoformat(
        data["timestamp"].replace("Z", "+00:00")
    )

    posted_url = (
        f"https://discord.com/channels/"
        f"{guild_id}/{channel_id}/{message_id}"
    )

    return {
        "platform": "Discord",
        "status": "success",
        "posted_url": posted_url,
        "message_id": message_id,
        "date": posted_at.strftime("%Y-%m-%d"),
        "time": posted_at.strftime("%H:%M:%S"),
        "error": None
    }
