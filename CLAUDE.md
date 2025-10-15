# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Microsoft Graph SDK integration project for capturing Outlook emails (incoming and outgoing) using the Microsoft Graph API. The application uses Azure Active Directory authentication with application permissions.

**Target Email**: MuznyM@Muzny986.onmicrosoft.com

**Application Permissions**:
- ChannelMessage.Read.All
- Chat.Read.All
- Mail.Read
- Mail.ReadWrite
- Team.ReadBasic.All
- User.Read
- User.Read.All

## Environment Setup

This project uses `uv` as the package manager (not pip or poetry).

### Initial Setup
```bash
# Install dependencies
uv sync

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS
```

### Environment Variables
The project requires Azure authentication credentials in `.env`:
- `AZURE_CLIENT_ID`: Application (client) ID from Azure AD
- `AZURE_TENANT_ID`: Directory (tenant) ID from Azure AD
- `AZURE_CLIENT_SECRET`: Client secret from Azure AD

**IMPORTANT**: Never commit `.env` file - credentials are already tracked in git and should be rotated.

## Development Commands

### Running the Application
```bash
uv run main.py
```

### Adding Dependencies
```bash
# Add a new package
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

### Updating Dependencies
```bash
uv sync 
```

## Code Architecture

### Authentication Flow
The project uses `azure-identity` library for authentication with Microsoft Graph API. The typical flow is:
1. Load credentials from environment variables using `python-dotenv`
2. Create `ClientSecretCredential` with Azure AD credentials
3. Initialize `GraphServiceClient` from `msgraph-sdk`
4. Make authenticated API calls to Microsoft Graph endpoints

### Key Dependencies
- **azure-identity (>=1.25.1)**: Handles Azure AD authentication
- **msgraph-sdk (>=1.46.0)**: Microsoft Graph API SDK for Python
- **python-dotenv (>=1.1.1)**: Loads environment variables from .env file

## Microsoft Graph API Usage

### Common Mail Operations
```python
# Example: Reading user's mailbox
result = await graph_client.users.by_user_id('user-id').messages.get()

# Example: Reading specific message
message = await graph_client.users.by_user_id('user-id').messages.by_message_id('message-id').get()
```

### API Endpoints for Email
- `/users/{user-id}/messages` - Access user mailbox
- `/users/{user-id}/mailFolders` - Access mail folders (Inbox, Sent, etc.)
- `/users/{user-id}/messages?$filter=...` - Filter messages by criteria

## Important Notes

- The project uses **Python 3.11+** (specified in pyproject.toml)
- All async operations should use `asyncio` since msgraph-sdk is async-based
- When working with mail operations, be mindful of pagination for large result sets
- Use `$select` query parameters to limit returned properties and improve performance
