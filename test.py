
from app.config import settings

credentials = {
    "Telegram": [
        settings.TELEGRAM_BOT_TOKEN,
        settings.TELEGRAM_CHANNEL
    ],
    "Discord": [
        settings.DISCORD_BOT_TOKEN,
        settings.DISCORD_CHANNEL_ID
    ],
    "Slack": [
        settings.SLACK_BOT_TOKEN,
        settings.SLACK_CHANNEL_ID
    ],
    "Bluesky": [
        settings.BLUESKY_HANDLE,
        settings.BLUESKY_APP_PASSWORD
    ],
    "Matrix": [
        settings.MATRIX_HOMESERVER,
        settings.MATRIX_ACCESS_TOKEN,
        settings.MATRIX_ROOM_ID
    ]
}

for platform, values in credentials.items():
    status = all(values)
    print(f"{platform}: {'Loaded' if status else 'MISSING'}")
