
import re
from urllib.parse import urlsplit

from pydantic import BaseModel, Field, field_validator


URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")


class PostRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Message containing exactly one CTA URL"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value):

        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty")

        urls = URL_PATTERN.findall(value)

        if len(urls) != 1:
            raise ValueError(
                "Message must contain exactly one CTA link"
            )

        url = urls[0].rstrip(".,!?;:)")

        try:
            parsed = urlsplit(url)

            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or "." not in parsed.hostname
            ):
                raise ValueError()

        except ValueError:
            raise ValueError("Please provide a valid URL")

        return value

from typing import Optional, Literal


class PlatformResult(BaseModel):

    platform: str

    status: Literal["success", "failed"]

    posted_url: Optional[str] = None

    public_access: bool = False

    date: Optional[str] = None

    time: Optional[str] = None

    error: Optional[str] = None


class PostingResponse(BaseModel):

    success: bool

    results: list[PlatformResult]
