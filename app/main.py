
from fastapi import FastAPI

from app.config import settings
from app.schemas import PostRequest, PostingResponse
from app.services.posting_service import publish_to_all


app = FastAPI(
    title="Multi Platform Poster",
    description="Publish one message across five platforms.",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "message": "Multi Platform Poster API is running",
        "platforms": [
            "Telegram",
            "Discord",
            "Slack",
            "Bluesky",
            "Matrix"
        ]
    }


@app.post("/posting", response_model=PostingResponse)
async def create_post(request: PostRequest):

    result = await publish_to_all(request.message)

    return result
