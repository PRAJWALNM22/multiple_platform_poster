# Multi-Platform Poster API – How It Works

## Overview

The Multi-Platform Poster API is built using FastAPI and Python. It allows a user to publish a single message to five different platforms through one API endpoint.

Instead of making separate API requests to each platform, the application accepts one message and distributes it to Telegram, Discord, Slack, Bluesky, and Matrix.

The application uses asynchronous execution so that publishing operations can run concurrently. Each platform is handled independently, ensuring that a failure on one platform does not interrupt the others.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/PRAJWALNM22/multiple_platform_poster
cd multiple_platform_poster
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

For Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and provide the required credentials for all five platforms.

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL=your_telegram_channel

DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_discord_channel_id

SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_CHANNEL_ID=your_slack_channel_id

BLUESKY_HANDLE=your_bluesky_handle
BLUESKY_APP_PASSWORD=your_bluesky_app_password

MATRIX_HOMESERVER=your_matrix_homeserver
MATRIX_ACCESS_TOKEN=your_matrix_access_token
MATRIX_ROOM_ID=your_matrix_room_id
```

Replace the placeholder values with your actual platform credentials. Keep `.env` private and do not commit it to Git.

### 5. Start the FastAPI server

```bash
uvicorn app.main:app --reload --port 4000
```

The application will run at:

`http://127.0.0.1:4000`

### 6. Access API documentation

Open the following URL in your browser:

`http://127.0.0.1:4000/docs`

Use Swagger UI to test the `/posting` endpoint.

### 7. Send a test request

Select `POST /posting`, click **Try it out**, and provide:

```json
{
    "message": "Check out our latest update https://example.com"
}
```

Click **Execute** to publish the message to all five configured platforms and view the individual results.

### 8. Run automated tests

To execute the test suite:

```bash
python -m pytest -v
```

The tests verify API health, message validation, and successful request handling using mocked publishing responses.

## Application Workflow

The application follows this flow:

```text
             Client Request
                   |
                   v
             POST /posting
                   |
                   v
          Request Validation
              (schemas.py)
                   |
          +--------+--------+
          |                 |
       Invalid            Valid
          |                 |
          v                 v
      HTTP 422       Posting Service
                   (posting_service.py)
                           |
                           v
                  Execute Platforms
                    Concurrently
                           |
          +----------------+----------------+
          |        |       |       |        |
          v        v       v       v        v
       Telegram Discord Slack Bluesky Matrix
          |        |       |       |        |
          +--------+-------+-------+--------+
                           |
                           v
                  Collect All Results
                           |
                           v
                  JSON API Response
```

## 1. API Request – `main.py`

The application exposes a POST endpoint:

`POST /posting`

The client sends a JSON request containing the message.

Example:

```json
{
    "message": "Check out our latest update https://example.com"
}
```

The endpoint receives the request and passes the message to the posting service after request validation.

## 2. Request Validation – `schemas.py`

Pydantic is used to validate the incoming request.

Before publishing, the application checks:

- The message must not be empty.
- The message must contain no more than 200 characters.
- The message must contain exactly one valid HTTP or HTTPS URL.

If the request does not satisfy these conditions, FastAPI returns a `422 Unprocessable Entity` response.

Invalid messages are rejected before any platform API is called.

## 3. Configuration Management – `config.py`

Platform credentials and configuration values are stored in environment variables and loaded from the `.env` file.

Each platform uses its corresponding credentials, such as bot tokens, access tokens, app passwords, channel IDs, and room IDs.

This keeps sensitive credentials separate from the application source code.

## 4. Posting Service – `posting_service.py`

This module coordinates the publishing process.

It maintains a list of supported platforms and their respective publishing functions.

When a valid message arrives, the service creates an asynchronous task for each platform.

Python's `asyncio.gather()` is used to execute these tasks concurrently.

Each task is wrapped in an exception-handling function. This ensures that an error from one platform is captured independently and does not stop the other publishing operations.

## 5. Platform Integrations

Each platform has its own module inside `app/platforms/`.

| Module | Responsibility |
|---|---|
| `telegram.py` | Publishes messages using the Telegram Bot API |
| `discord.py` | Publishes messages using the Discord REST API |
| `slack.py` | Publishes messages using the Slack Web API |
| `bluesky.py` | Publishes posts using the Bluesky AT Protocol |
| `matrix.py` | Publishes messages using the Matrix Client-Server API |

Each integration handles communication with its respective platform and returns the publishing result.

The result contains information such as the platform name, posting status, available post URL, timestamp, public accessibility, and error details.

## 6. Independent Error Handling

Each platform publishing operation is executed independently.

For example, consider a request where Telegram fails but the other platforms succeed.

| Platform | Status |
|---|---|
| Telegram | Failed |
| Discord | Success |
| Slack | Success |
| Bluesky | Success |
| Matrix | Success |

The application captures the Telegram error while allowing the remaining four operations to complete.

This prevents a single platform failure from interrupting the entire publishing process.

## 7. Response Generation

After all platform tasks finish, the posting service collects their results and returns a consolidated response.

The response includes:

- Overall operation status.
- Individual platform status.
- Published post URL, when available.
- Public accessibility information.
- Posting date and time.
- Error details for failed operations.

Example response structure:

```json
{
    "success": true,
    "results": [
        {
            "platform": "Telegram",
            "status": "success",
            "posted_url": "https://t.me/example",
            "public_access": true,
            "date": "2026-11-17",
            "time": "12:30:00",
            "error": null
        },
        {
            "platform": "Discord",
            "status": "failed",
            "posted_url": null,
            "public_access": false,
            "date": null,
            "time": null,
            "error": "Example platform error"
        }
    ]
}
```

The response above is illustrative; actual results depend on the platform APIs.

## 8. Testing – `tests/test_posting.py`

Pytest and FastAPI's TestClient are used to test the API.

The test suite verifies:

- API health check.
- Rejection of messages without URLs.
- Rejection of messages containing multiple URLs.
- Rejection of messages exceeding 200 characters.
- Acceptance of valid messages.
- Rejection of empty messages.

The successful request test uses mocking to simulate platform responses. This prevents automated tests from publishing actual messages to the connected platforms.

## Overall Design

The application separates responsibilities into different modules:

- **API Layer:** Receives HTTP requests.
- **Validation Layer:** Checks incoming message data.
- **Configuration Layer:** Loads platform credentials.
- **Service Layer:** Coordinates asynchronous publishing.
- **Integration Layer:** Communicates with individual platform APIs.
- **Testing Layer:** Verifies application behavior.

This modular structure makes the application easier to maintain and allows additional platform integrations to be added independently.