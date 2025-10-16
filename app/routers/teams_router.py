from fastapi import APIRouter, HTTPException
from app.services.teams_service import fetch_all_teams_chats_raw

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


@router.get("/chats")
async def get_all_chats():
    """
    Fetch all Teams chats and messages (received + replies) and return raw Graph API response data.

    This endpoint captures:
    - All chats for the user
    - All messages from each chat (including received messages, sent messages/replies, and system events)

    Returns:
        dict: Raw chat and message data with metadata
            {
                "metadata": {
                    "total_chats": int,
                    "total_messages": int,
                    "fetched_at": str,
                    "user_email": str
                },
                "chats": [raw chat objects from Graph API],
                "messages": [raw message objects from Graph API]
            }

    Raises:
        HTTPException: 500 if authentication or API call fails
    """
    try:
        result = await fetch_all_teams_chats_raw()
        return result
    except ValueError as e:
        # Handle missing environment variables
        raise HTTPException(
            status_code=500,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        # Handle other errors (authentication, API failures, etc.)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch Teams chats: {type(e).__name__} - {str(e)}"
        )
