# Multi-Platform Poster

A FastAPI starter for routing one message to Telegram, Discord, Slack, Bluesky,
and Matrix.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Run the API:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## API

`POST /posts`

```json
{
  "message": "Hello from one place!",
  "platforms": ["telegram", "discord"]
}
```

`GET /health` returns the service health status.

The platform modules are adapter stubs: they report `not_implemented` until
their API clients are connected. The credential names in `.env.example` are
provided for that implementation; the app does not currently use them to post.

## Tests

```powershell
pytest
```
