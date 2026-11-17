
import os
import httpx

from datetime import datetime


async def post_to_telegram(message: str):

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel = os.getenv("TELEGRAM_CHANNEL")

    if not bot_token or not channel:
        raise ValueError("Telegram credentials are missing")

    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": channel,
        "text": message
    }

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.post(
            api_url,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            raise RuntimeError(
                data.get("description", "Telegram posting failed")
            )

    posted_message = data["result"]

    message_id = posted_message["message_id"]
    chat_username = posted_message["chat"].get("username")

    # Construct public URL for a public channel
    posted_url = (
        f"https://t.me/{chat_username}/{message_id}"
        if chat_username
        else None
    )

    # Telegram provides the actual message timestamp
    posted_at = datetime.fromtimestamp(
        posted_message["date"]
    ).astimezone()

    return {
        "platform": "Telegram",
        "status": "success",
        "posted_url": posted_url,
        "public_access": posted_url is not None,
        "date": posted_at.strftime("%Y-%m-%d"),
        "time": posted_at.strftime("%H:%M:%S"),
        "error": None
    }
