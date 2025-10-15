# Microsoft Graph SDK Email Capture - AI Coding Agent Instructions

## Project Overview
This is a **single-purpose Microsoft Graph API client** that fetches all emails from a specific Microsoft 365 mailbox (`MuznyM@Muzny986.onmicrosoft.com`) and exports them to JSON. The project uses Azure AD app registration with application permissions for server-to-server authentication.

## Critical Architecture Knowledge

### Authentication Flow Pattern
- Uses `ClientSecretCredential` from `azure-identity` (not user interactive flows)
- **Required scope**: `["https://graph.microsoft.com/.default"]` for application permissions
- All Graph operations require this specific user ID: `MuznyM@Muzny986.onmicrosoft.com`

### Async-First Design
- **All Microsoft Graph operations are async** - use `await` for Graph client calls
- Main execution pattern: `asyncio.run(fetch_all_emails())` in `if __name__ == "__main__"`
- Pagination is handled manually with `messages.odata_next_link` loops

### Data Extraction Pattern
The project follows a specific email data transformation pattern in `main.py`:
```python
email_data = {
    "id": message.id,
    "from": {"name": message.from_.email_address.name, "address": message.from_.email_address.address},
    "received_datetime": message.received_date_time.isoformat(),
    # ... specific field mapping
}
```

## Development Workflow

### Package Management - UV Only
- **Use `uv` commands exclusively** (not pip/poetry):
  - `uv sync` - install/update dependencies
  - `uv add <package>` - add dependencies
  - `uv run main.py` - run the application

### Environment Setup Requirements
1. **`.env` file must contain** (check `.env` for current values):
   - `AZURE_CLIENT_ID` - Azure AD app registration client ID
   - `AZURE_TENANT_ID` - Azure AD tenant ID  
   - `AZURE_CLIENT_SECRET` - Azure AD app secret
2. **Python 3.11+** required (specified in `pyproject.toml`)

### Application Permissions Context
The Azure AD app has these **application permissions** (not delegated):
- `Mail.Read`, `Mail.ReadWrite` - primary email access
- `ChannelMessage.Read.All`, `Chat.Read.All` - Teams integration (not actively used)
- `User.Read.All` - user profile access

## Code Patterns & Conventions

### Error Handling Pattern
- Environment validation before Graph client initialization
- Try-catch around entire Graph operations with type-specific error reporting:
  ```python
  except Exception as e:
      print(f"Error occurred: {type(e).__name__}")
      print(f"Details: {str(e)}")
  ```

### Pagination Implementation
- **Always handle pagination** for email fetching using `odata_next_link`
- Progress logging: `print(f"Fetched {len(all_emails)} emails so far...")`
- Batch processing with status updates between pages

### Output Format Standard
JSON output in `emails.json` follows this structure:
```json
{
  "metadata": {"total_count": N, "fetched_at": "ISO-timestamp", "user_email": "target-email"},
  "emails": [/* array of email objects */]
}
```

## Microsoft Graph API Integration

### Client Initialization Pattern
```python
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = GraphServiceClient(credentials=credential, scopes=["https://graph.microsoft.com/.default"])
```

### Email Access Pattern
- Primary endpoint: `client.users.by_user_id(user_id).messages.get()`
- **User ID is email address**: `"MuznyM@Muzny986.onmicrosoft.com"`
- Pagination: `client.users.by_user_id(user_id).messages.with_url(next_link).get()`

### Field Access Safety
The codebase uses defensive programming for Graph API fields:
- Check `message.from_` and `message.from_.email_address` before accessing properties
- Use list comprehensions with null-safe access: `for recipient in (message.to_recipients or [])`
- Convert enums explicitly: `message.importance.value if message.importance else None`

## Common Development Tasks

### Testing Authentication
Run `uv run main.py` - authentication success prints "Authenticated successfully!"

### Adding New Email Fields
1. Extend the `email_data` dictionary in both main loop and pagination loop
2. Follow the null-safe pattern: `field.value if field else None`
3. Convert datetime objects: `datetime_field.isoformat() if datetime_field else None`

### Debugging Microsoft Graph Issues
- Check Azure AD app permissions in Azure portal
- Verify `.env` credentials match Azure AD app registration
- Microsoft Graph API responses are verbose - inspect `messages.value` structure

## File Structure Context
- `main.py` - single-file application, contains all logic
- `emails.json` - output file (gitignored, contains actual email data)
- `pyproject.toml` - minimal UV configuration with 3 core dependencies
- `.env` - credentials (tracked in git but should be rotated)
- `CLAUDE.md` - legacy AI instructions (this file supersedes it)