"""
Pydantic schemas for Teams API responses.

These models define the structure of Teams chat and message data
returned by the Microsoft Graph API endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TeamsMetadata(BaseModel):
    """
    Metadata about the Teams data fetch operation.

    Attributes:
        total_chats: Total number of chats retrieved
        total_messages: Total number of messages retrieved across all chats
        fetched_at: ISO 8601 timestamp of when the data was fetched
        user_email: Email address of the user whose data was fetched
    """
    total_chats: int = Field(..., description="Total number of chats retrieved")
    total_messages: int = Field(..., description="Total number of messages retrieved")
    fetched_at: str = Field(..., description="ISO 8601 timestamp of fetch time")
    user_email: str = Field(..., description="Target user's email address")


class TeamChat(BaseModel):
    """
    Represents a single Teams chat.

    Attributes:
        chat_id: Unique identifier for the chat
        chat_type: Type of chat (oneOnOne, group, meeting)
        topic: Chat topic/title (may be None for one-on-one chats)
        created_at: ISO 8601 timestamp of when the chat was created
        last_updated_at: ISO 8601 timestamp of last activity in the chat
    """
    chat_id: str = Field(..., description="Unique identifier for the chat")
    chat_type: Optional[str] = Field(None, description="Chat type (oneOnOne, group, meeting)")
    topic: Optional[str] = Field(None, description="Chat topic/title")
    created_at: Optional[str] = Field(None, description="ISO 8601 timestamp of creation")
    last_updated_at: Optional[str] = Field(None, description="ISO 8601 timestamp of last update")


class TeamMessage(BaseModel):
    """
    Represents a single message within a Teams chat.

    This model includes all analytics-relevant fields extracted from
    Microsoft Graph API message objects.

    Attributes:
        message_id: Unique identifier for the message
        chat_id: ID of the chat this message belongs to
        chat_type: Type of the parent chat (oneOnOne, group, meeting)
        created_at: ISO 8601 timestamp of message creation
        last_modified_at: ISO 8601 timestamp of last modification
        last_edited_at: ISO 8601 timestamp of last edit (if edited)
        deleted_at: ISO 8601 timestamp of deletion (if deleted)
        sender_id: User ID of the message sender
        sender_name: Display name of the message sender
        content: Message content/body
        content_type: Content type (text, html, etc.)
        message_length: Character length of the message content
        message_type: Type of message (message, systemEventMessage, etc.)
        importance: Message importance level (normal, high, urgent)
        reply_to_id: ID of the message this is replying to (if a reply)
        is_reply: Boolean indicating if this message is a reply
    """
    # Identifiers
    message_id: str = Field(..., description="Unique message identifier")
    chat_id: str = Field(..., description="Parent chat identifier")
    chat_type: Optional[str] = Field(None, description="Parent chat type")

    # Timestamps
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    last_modified_at: Optional[str] = Field(None, description="ISO 8601 last modified timestamp")
    last_edited_at: Optional[str] = Field(None, description="ISO 8601 last edited timestamp")
    deleted_at: Optional[str] = Field(None, description="ISO 8601 deletion timestamp")

    # Sender information
    sender_id: Optional[str] = Field(None, description="Sender's user ID")
    sender_name: Optional[str] = Field(None, description="Sender's display name")

    # Content
    content: Optional[str] = Field(None, description="Message content/body")
    content_type: Optional[str] = Field(None, description="Content type (text, html, etc.)")
    message_length: int = Field(0, description="Character length of message content")

    # Message metadata
    message_type: Optional[str] = Field(None, description="Message type (message, systemEventMessage, etc.)")
    importance: Optional[str] = Field(None, description="Importance level (normal, high, urgent)")

    # Reply tracking
    reply_to_id: Optional[str] = Field(None, description="ID of message being replied to")
    is_reply: bool = Field(False, description="Whether this message is a reply")


class TeamsChatsResponse(BaseModel):
    """
    Complete response model for Teams chats endpoint.

    Contains metadata about the operation and lists of chats and messages.

    Attributes:
        metadata: Metadata about the fetch operation
        chats: List of all chats retrieved
        messages: List of all messages across all chats
    """
    metadata: TeamsMetadata = Field(..., description="Fetch operation metadata")
    chats: list[TeamChat] = Field(..., description="List of all chats")
    messages: list[TeamMessage] = Field(..., description="List of all messages")
