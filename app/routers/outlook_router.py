from fastapi import APIRouter, HTTPException
from app.services.outlook_service import fetch_all_emails_raw

router = APIRouter(prefix="/outlook", tags=["Outlook"])


@router.get("/emails")
async def get_all_emails():
    """
    Fetch all Outlook emails and return raw Graph API response data.

    Returns:
        dict: Raw email data with metadata
            {
                "metadata": {
                    "total_count": int,
                    "fetched_at": str,
                    "user_email": str
                },
                "emails": [raw message objects from Graph API]
            }

    Raises:
        HTTPException: 500 if authentication or API call fails
    """
    try:
        result = await fetch_all_emails_raw()
        return result
    except ValueError as e:
        # Handle missing environment variables
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        # Handle other errors (authentication, API failures, etc.)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch emails: {type(e).__name__} - {str(e)}",
        )
