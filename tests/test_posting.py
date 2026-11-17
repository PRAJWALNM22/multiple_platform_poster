
import app.main as main
from fastapi.testclient import TestClient

client = TestClient(main.app)

# 1. Test whether the API is running
def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Multi Platform Poster API is running"


# 2. Test rejection when message has no URL
def test_post_rejects_message_without_url():
    response = client.post(
        "/posting",
        json={"message": "Hello everyone!"}
    )

    assert response.status_code == 422


# 3. Test rejection when message contains multiple URLs
def test_post_rejects_multiple_urls():
    response = client.post(
        "/posting",
        json={
            "message": "Visit https://example.com and https://google.com"
        }
    )

    assert response.status_code == 422


# 4. Test rejection when message exceeds 200 characters
def test_post_rejects_long_message():
    response = client.post(
        "/posting",
        json={
            "message": "A" * 190 + " https://example.com"
        }
    )

    assert response.status_code == 422


# 5. Test successful request without making actual platform posts
def test_post_accepts_valid_message(monkeypatch):

    async def mock_publish(message):
        return {
            "success": True,
            "results": [
                {
                    "platform": name,
                    "status": "success",
                    "posted_url": None,
                    "public_access": False,
                    "date": None,
                    "time": None,
                    "error": None
                }
                for name in [
                    "Telegram",
                    "Discord",
                    "Slack",
                    "Bluesky",
                    "Matrix"
                ]
            ]
        }

    monkeypatch.setattr(
        main,
        "publish_to_all",
        mock_publish
    )

    response = client.post(
        "/posting",
        json={
            "message": "Hello! https://example.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["results"]) == 5

    assert [
        result["platform"] for result in data["results"]
    ] == [
        "Telegram",
        "Discord",
        "Slack",
        "Bluesky",
        "Matrix"
    ]


# 6. Test rejection of an empty message
def test_post_rejects_empty_message():
    response = client.post(
        "/posting",
        json={"message": ""}
    )

    assert response.status_code == 422
