from fastapi import APIRouter, HTTPException
from app.services.outlook_service import fetch_all_emails_raw
from app.schemas.outlook import OutlookEmailsResponse

router = APIRouter(prefix="/outlook", tags=["Outlook"])


@router.get("/emails", response_model=OutlookEmailsResponse)
async def get_all_emails() -> OutlookEmailsResponse:
    """
    Fetch all Outlook emails with structured analytics data.

    Returns:
        OutlookEmailsResponse: Structured response containing:
            - metadata: Fetch operation details (total_count, fetched_at, user_email)
            - emails: List of email objects with analytics-relevant fields (24 fields total)

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
