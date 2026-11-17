
import os
import httpx
from datetime import datetime, timezone


async def post_to_slack(message: str):

    token = os.getenv("SLACK_BOT_TOKEN")
    channel = os.getenv("SLACK_CHANNEL_ID")

    if not token or not channel:
        raise ValueError("Slack credentials are missing")

    base_url = "https://slack.com/api"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=20) as client:

        # Publish message
        response = await client.post(
            f"{base_url}/chat.postMessage",
            headers=headers,
            json={
                "channel": channel,
                "text": message
            }
        )

        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            raise RuntimeError(data.get("error"))

        timestamp = data["ts"]

        # Retrieve actual message permalink
        link_response = await client.get(
            f"{base_url}/chat.getPermalink",
            headers=headers,
            params={
                "channel": channel,
                "message_ts": timestamp
            }
        )

        link_data = link_response.json()

        posted_url = (
            link_data.get("permalink")
            if link_data.get("ok")
            else None
        )

    posted_at = datetime.fromtimestamp(
        float(timestamp), tz=timezone.utc
    ).astimezone()

    return {
        "platform": "Slack",
        "status": "success",
        "posted_url": posted_url,
        "message_id": timestamp,
        "date": posted_at.strftime("%Y-%m-%d"),
        "time": posted_at.strftime("%H:%M:%S"),
        "error": None
    }
