from fastapi import APIRouter, HTTPException
from app.services.teams_service import fetch_all_teams_chats_raw
from app.schemas.teams import TeamsChatsResponse

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


@router.get("/chats", response_model=TeamsChatsResponse)
async def get_all_chats() -> TeamsChatsResponse:
    """
    Fetch all Teams chats and messages (received + replies) with structured analytics data.

    This endpoint captures:
    - All chats for the user
    - All messages from each chat (including received messages, sent messages/replies, and system events)

    Returns:
        TeamsChatsResponse: Structured response containing:
            - metadata: Fetch operation details (total_chats, total_messages, fetched_at, user_email)
            - chats: List of chat objects with analytics-relevant fields
            - messages: List of message objects with analytics-relevant fields

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
