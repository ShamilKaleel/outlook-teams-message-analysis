# Microsoft Graph SDK API

A FastAPI-based REST API for capturing Outlook emails and Teams chat messages using the Microsoft Graph API with Azure Active Directory authentication.

## Features

- **Outlook Email Capture**: Fetch all emails (incoming and outgoing) with raw Graph API data
- **Teams Chat Capture**: Fetch all Teams chats and messages (received messages and replies)
- **Raw Data Export**: Returns complete raw Graph API response data
- **Pagination Handling**: Automatically handles pagination for large datasets
- **RESTful API**: Built with FastAPI for high performance and easy integration

## Prerequisites

- Python 3.11 or higher
- Azure AD application with the following permissions:
  - `ChannelMessage.Read.All`
  - `Chat.Read.All`
  - `Mail.Read`
  - `Mail.ReadWrite`
  - `Team.ReadBasic.All`
  - `User.Read`
  - `User.Read.All`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Microsoft-Graph-SDK
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Create a `.env` file in the project root:
```env
AZURE_CLIENT_ID=your-client-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_SECRET=your-client-secret
TARGET_USER_EMAIL=user@yourdomain.com
```

## Usage

### Start the API Server

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### API Endpoints

#### Get All Outlook Emails
```http
GET /outlook/emails
```

Returns all emails with metadata including total count, fetch timestamp, and raw email data.

#### Get All Teams Chats
```http
GET /teams/chats
```

Returns all Teams chats and messages with metadata including chat details and message content.

#### Health Check
```http
GET /health
```

## Development

### Run Test Scripts

Test Outlook email fetching:
```bash
uv run tests/outlook_chats.py
```

Test Teams chat fetching:
```bash
uv run tests/teams_chats.py
```

### Add Dependencies

```bash
uv add <package-name>
```

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **Microsoft Graph SDK** - Official Python SDK for Microsoft Graph API
- **Azure Identity** - Azure Active Directory authentication
- **Uvicorn** - ASGI server for running the application
- **Python-dotenv** - Environment variable management

## Project Structure

```
project/
├── app/
│   ├── routers/          # FastAPI route handlers
│   ├── services/         # Business logic for Graph API calls
│   └── utils/            # Utility functions
├── config/
│   └── settings.py       # Azure configuration and Graph client
├── tests/
│   ├── outlook_chats.py  # Outlook test script
│   └── teams_chats.py    # Teams test script
├── main.py               # FastAPI application entry point
└── .env                  # Environment variables (not committed)
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
