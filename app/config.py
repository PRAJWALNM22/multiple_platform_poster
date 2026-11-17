
import os
from pathlib import Path
from dotenv import load_dotenv

# Find project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Explicitly load .env from project root
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)


class Settings:

    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL")

    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

    BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
    BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

    MATRIX_HOMESERVER = os.getenv("MATRIX_HOMESERVER")
    MATRIX_ACCESS_TOKEN = os.getenv("MATRIX_ACCESS_TOKEN")
    MATRIX_ROOM_ID = os.getenv("MATRIX_ROOM_ID")


settings = Settings()
