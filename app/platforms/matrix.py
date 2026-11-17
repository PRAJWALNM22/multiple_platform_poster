
import os
import httpx
from datetime import datetime, timezone
from urllib.parse import quote


async def post_to_matrix(message: str):

    homeserver = os.getenv("MATRIX_HOMESERVER")
    token = os.getenv("MATRIX_ACCESS_TOKEN")
    room_id = os.getenv("MATRIX_ROOM_ID")

    if not all([homeserver, token, room_id]):
        raise ValueError("Matrix credentials are missing")

    encoded_room = quote(room_id, safe="")

    url = (
        f"{homeserver}/_matrix/client/v3/rooms/"
        f"{encoded_room}/send/m.room.message"
        f"/{datetime.now(timezone.utc).timestamp()}"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "msgtype": "m.text",
        "body": message
    }

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.put(
            url,
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        data = response.json()

    event_id = data["event_id"]

    return {
        "platform": "Matrix",
        "status": "success",
        "posted_url": None,
        "message_id": event_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "error": None
    }
