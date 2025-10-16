"""
Pydantic schemas for Outlook API responses.

These models define the structure of Outlook email data
returned by the Microsoft Graph API endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class EmailRecipient(BaseModel):
    """
    Represents an email recipient (used in to, cc, bcc, reply_to fields).

    Attributes:
        email: Email address of the recipient
        name: Display name of the recipient
    """
    email: str = Field(..., description="Email address of the recipient")
    name: str = Field(..., description="Display name of the recipient")


class OutlookMetadata(BaseModel):
    """
    Metadata about the Outlook email fetch operation.

    Attributes:
        total_count: Total number of emails retrieved
        fetched_at: ISO 8601 timestamp of when the data was fetched
        user_email: Email address of the user whose data was fetched
    """
    total_count: int = Field(..., description="Total number of emails retrieved")
    fetched_at: str = Field(..., description="ISO 8601 timestamp of fetch time")
    user_email: str = Field(..., description="Target user's email address")


class OutlookEmail(BaseModel):
    """
    Represents a single Outlook email message.

    This model includes all analytics-relevant fields extracted from
    Microsoft Graph API email message objects.

    Attributes:
        message_id: Unique identifier for the message
        conversation_id: ID of the conversation thread this message belongs to
        folder_id: ID of the parent folder containing this message
        internet_message_id: Internet standard message ID
        created_at: ISO 8601 timestamp of message creation
        sent_at: ISO 8601 timestamp of when message was sent
        received_at: ISO 8601 timestamp of when message was received
        last_modified_at: ISO 8601 timestamp of last modification
        sender_email: Email address of the sender
        sender_name: Display name of the sender
        to_recipients: List of To recipients
        cc_recipients: List of CC recipients
        bcc_recipients: List of BCC recipients
        reply_to: List of Reply-To addresses
        subject: Email subject line
        body_preview: Preview/snippet of the email body
        importance: Message importance level (normal, high, low)
        is_draft: Whether this message is a draft
        is_read: Whether this message has been read
        has_attachments: Whether this message has attachments
        flag_status: Status of the message flag (flagged, complete, notFlagged)
        is_reply: Boolean indicating if this message is a reply
        recipient_count: Total number of recipients (to + cc + bcc)
    """
    # Identifiers
    message_id: str = Field(..., description="Unique message identifier")
    conversation_id: Optional[str] = Field(None, description="Conversation thread identifier")
    folder_id: Optional[str] = Field(None, description="Parent folder identifier")
    internet_message_id: Optional[str] = Field(None, description="Internet standard message ID")

    # Timestamps
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    sent_at: Optional[str] = Field(None, description="ISO 8601 sent timestamp")
    received_at: Optional[str] = Field(None, description="ISO 8601 received timestamp")
    last_modified_at: Optional[str] = Field(None, description="ISO 8601 last modified timestamp")

    # Sender information
    sender_email: Optional[str] = Field(None, description="Sender's email address")
    sender_name: Optional[str] = Field(None, description="Sender's display name")

    # Recipients
    to_recipients: list[EmailRecipient] = Field(default_factory=list, description="List of To recipients")
    cc_recipients: list[EmailRecipient] = Field(default_factory=list, description="List of CC recipients")
    bcc_recipients: list[EmailRecipient] = Field(default_factory=list, description="List of BCC recipients")
    reply_to: list[EmailRecipient] = Field(default_factory=list, description="List of Reply-To addresses")

    # Content
    subject: Optional[str] = Field(None, description="Email subject line")
    body_preview: Optional[str] = Field(None, description="Preview/snippet of email body")

    # Metadata
    importance: Optional[str] = Field(None, description="Message importance (normal, high, low)")
    is_draft: Optional[bool] = Field(None, description="Whether message is a draft")
    is_read: Optional[bool] = Field(None, description="Whether message has been read")
    has_attachments: Optional[bool] = Field(None, description="Whether message has attachments")
    flag_status: Optional[str] = Field(None, description="Flag status (flagged, complete, notFlagged)")

    # Derived fields
    is_reply: bool = Field(False, description="Whether this message is a reply")
    recipient_count: int = Field(0, description="Total number of recipients")


class OutlookEmailsResponse(BaseModel):
    """
    Complete response model for Outlook emails endpoint.

    Contains metadata about the operation and list of email messages.

    Attributes:
        metadata: Metadata about the fetch operation
        emails: List of all email messages retrieved
    """
    metadata: OutlookMetadata = Field(..., description="Fetch operation metadata")
    emails: list[OutlookEmail] = Field(..., description="List of all emails")
