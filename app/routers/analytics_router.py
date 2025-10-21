from fastapi import APIRouter, HTTPException
from app.services.outlook_service import fetch_all_emails_raw
from app.services.teams_service import fetch_all_teams_chats_raw
from app.dspy.outlook_analyzer import OutlookEmailAnalyzer
from app.dspy.teams_analyzer import TeamsChatsAnalyzer
from app.schemas.outlook import (
    OutlookEmail,
    OutlookMetadata,
    OutlookAnalysisResult,
)
from app.schemas.teams import (
    TeamMessage,
    TeamsMetadata,
    TeamsAnalysisResult,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/outlook/analyze", response_model=OutlookAnalysisResult)
async def analyze_outlook_emails() -> OutlookAnalysisResult:
    """
    Analyze Outlook emails using AI to provide productivity insights and suggestions.

    This endpoint:
    1. Fetches all emails from the user's Outlook account
    2. Analyzes them using DSPy and LLM to generate insights
    3. Returns comprehensive analytics including:
       - Email distribution (inbox, sent, spam, urgent)
       - Reply productivity metrics
       - Average response time
       - AI-generated suggestions for each conversation

    Returns:
        OutlookAnalysisResult: Comprehensive analysis with counts, metrics, and suggestions

    Raises:
        HTTPException: 500 if fetching emails, authentication, or LLM analysis fails
    """
    try:
        # Step 1: Fetch all emails from Outlook service
        email_data = await fetch_all_emails_raw()

        # Step 2: Convert dict response to Pydantic models
        # Parse metadata
        metadata = OutlookMetadata(**email_data["metadata"])

        # Parse emails list
        emails = [OutlookEmail(**email_dict) for email_dict in email_data["emails"]]

        # Step 3: Instantiate DSPy analyzer
        outlook_analyzer = OutlookEmailAnalyzer()

        # Step 4: Run analysis with LLM
        result = outlook_analyzer(all_email=emails, metadata=metadata)

        # Step 5: Return the analysis result
        return result.analysis_result

    except ValueError as e:
        # Handle missing environment variables or validation errors
        raise HTTPException(
            status_code=500, detail=f"Configuration or validation error: {str(e)}"
        )
    except Exception as e:
        # Handle other errors (authentication, API failures, LLM errors, etc.)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze Outlook emails: {type(e).__name__} - {str(e)}",
        )


@router.get("/teams/analyze", response_model=TeamsAnalysisResult)
async def analyze_teams_chats() -> TeamsAnalysisResult:
    """
    Analyze Teams chats and messages using AI to provide productivity insights and suggestions.

    This endpoint:
    1. Fetches all chats and messages from the user's Teams account
    2. Analyzes them using DSPy and LLM to generate insights
    3. Returns comprehensive analytics including:
       - Volume metrics (messages received, sent, replied)
       - Response metrics (average response time, reply rate)
       - Engagement metrics (proactive vs reactive, peak hours)
       - Quality indicators (message length patterns)
       - Productivity scores (overall, responsiveness, engagement, quality)
       - AI-generated insights and recommendations

    Returns:
        TeamsAnalysisResult: Comprehensive analysis with metrics, scores, insights, and summary

    Raises:
        HTTPException: 500 if fetching chats, authentication, or LLM analysis fails
    """
    try:
        # Step 1: Fetch all Teams chats and messages
        teams_data = await fetch_all_teams_chats_raw()

        # Step 2: Convert dict response to Pydantic models
        # Parse metadata
        metadata = TeamsMetadata(**teams_data["metadata"])

        # Parse messages list
        messages = [TeamMessage(**msg_dict) for msg_dict in teams_data["messages"]]

        # Step 3: Instantiate DSPy analyzer
        teams_analyzer = TeamsChatsAnalyzer()

        # Step 4: Run analysis with LLM
        result = teams_analyzer(all_messages=messages, metadata=metadata)

        # Step 5: Return the analysis result
        return result.analysis_result

    except ValueError as e:
        # Handle missing environment variables or validation errors
        raise HTTPException(
            status_code=500, detail=f"Configuration or validation error: {str(e)}"
        )
    except Exception as e:
        # Handle other errors (authentication, API failures, LLM errors, etc.)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze Teams chats: {type(e).__name__} - {str(e)}",
        )
