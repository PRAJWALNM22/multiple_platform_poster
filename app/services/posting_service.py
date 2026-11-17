
import asyncio

from datetime import datetime
from app.platforms.telegram import post_to_telegram
from app.platforms.discord import post_to_discord
from app.platforms.slack import post_to_slack
from app.platforms.bluesky import post_to_bluesky
from app.platforms.matrix import post_to_matrix


PLATFORMS = [
    ("Telegram", post_to_telegram),
    ("Discord", post_to_discord),
    ("Slack", post_to_slack),
    ("Bluesky", post_to_bluesky),
    ("Matrix", post_to_matrix),
]


async def execute_platform(name, function, message):

    try:
        result = await function(message)

        # Normalize the result
        return {
            "platform": name,
            "status": "success",
            "posted_url": result.get("posted_url"),
            "public_access": result.get("public_access", False),
            "date": result.get("date"),
            "time": result.get("time"),
            "error": None
        }

    except Exception as error:

        return {
            "platform": name,
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": str(error)
        }


async def publish_to_all(message):

    tasks = [
        execute_platform(name, function, message)
        for name, function in PLATFORMS
    ]

    results = await asyncio.gather(*tasks)

    return {
        "success": any(
            result["status"] == "success"
            for result in results
        ),
        "results": results
    }
