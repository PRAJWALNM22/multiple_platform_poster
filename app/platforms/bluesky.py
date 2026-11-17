
import os
from datetime import datetime, timezone

from atproto import AsyncClient


async def post_to_bluesky(message: str):

    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_APP_PASSWORD")

    if not handle or not password:
        raise ValueError("Bluesky credentials are missing")

    client = AsyncClient()

    # Authenticate
    await client.login(handle, password)

    # Publish post
    response = await client.send_post(text=message)

    # Extract record key from AT Protocol URI
    post_id = response.uri.rsplit("/", 1)[-1]

    posted_url = (
        f"https://bsky.app/profile/{handle}/post/{post_id}"
    )

    posted_at = datetime.now(timezone.utc).astimezone()

    return {
        "platform": "Bluesky",
        "status": "success",
        "posted_url": posted_url,
        "message_id": post_id,
        "date": posted_at.strftime("%Y-%m-%d"),
        "time": posted_at.strftime("%H:%M:%S"),
        "error": None
    }
