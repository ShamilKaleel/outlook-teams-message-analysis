import os
from datetime import datetime, timezone
from config.settings import get_graph_client
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.users.item.messages.messages_request_builder import (
    MessagesRequestBuilder,
)


def format_email_for_analytics(message):
    """
    Extract analytics-relevant fields from an email message object.

    Args:
        message: Message object from Graph API

    Returns:
        dict: Structured email data for analytics with fields:
            - message_id, conversation_id, folder_id, internet_message_id
            - created_at, sent_at, received_at, last_modified_at
            - sender_email, sender_name
            - to_recipients, cc_recipients, bcc_recipients, reply_to
            - subject, body_preview
            - importance, is_draft, is_read, has_attachments
            - flag_status, is_reply, recipient_count
    """
    # Extract sender information
    sender_email = None
    sender_name = None
    if message.from_ and message.from_.email_address:
        sender_email = message.from_.email_address.address
        sender_name = message.from_.email_address.name

    # Extract recipients
    to_recipients = []
    if message.to_recipients:
        to_recipients = [
            {"email": r.email_address.address, "name": r.email_address.name}
            for r in message.to_recipients
            if r and r.email_address
        ]

    cc_recipients = []
    if message.cc_recipients:
        cc_recipients = [
            {"email": r.email_address.address, "name": r.email_address.name}
            for r in message.cc_recipients
            if r and r.email_address
        ]

    bcc_recipients = []
    if message.bcc_recipients:
        bcc_recipients = [
            {"email": r.email_address.address, "name": r.email_address.name}
            for r in message.bcc_recipients
            if r and r.email_address
        ]

    reply_to = []
    if message.reply_to:
        reply_to = [
            {"email": r.email_address.address, "name": r.email_address.name}
            for r in message.reply_to
            if r and r.email_address
        ]

    # Extract flag status
    flag_status = None
    if message.flag:
        flag_status = str(message.flag.flag_status) if message.flag.flag_status else None

    # Calculate derived fields
    recipient_count = len(to_recipients) + len(cc_recipients) + len(bcc_recipients)
    is_reply = message.conversation_id is not None and len(to_recipients) > 0

    # Build structured email object
    return {
        # Identifiers
        "message_id": message.id,
        "conversation_id": message.conversation_id,
        "folder_id": message.parent_folder_id,
        "internet_message_id": message.internet_message_id,
        # Timestamps
        "created_at": message.created_date_time.isoformat() if message.created_date_time else None,
        "sent_at": message.sent_date_time.isoformat() if message.sent_date_time else None,
        "received_at": message.received_date_time.isoformat() if message.received_date_time else None,
        "last_modified_at": message.last_modified_date_time.isoformat() if message.last_modified_date_time else None,
        # Sender
        "sender_email": sender_email,
        "sender_name": sender_name,
        # Recipients
        "to_recipients": to_recipients,
        "cc_recipients": cc_recipients,
        "bcc_recipients": bcc_recipients,
        "reply_to": reply_to,
        # Content
        "subject": message.subject,
        "body_preview": message.body_preview,
        # Metadata
        "importance": str(message.importance) if message.importance else None,
        "is_draft": message.is_draft,
        "is_read": message.is_read,
        "has_attachments": message.has_attachments,
        "flag_status": flag_status,
        # Derived fields
        "is_reply": is_reply,
        "recipient_count": recipient_count,
    }


async def fetch_all_emails_raw():
    """
    Fetch all emails from Outlook optimized for analytics.
    Returns structured data with only analytics-relevant fields.

    Returns:
        dict: Dictionary containing metadata and structured email data
            {
                "metadata": {
                    "total_count": int,
                    "fetched_at": str (ISO format),
                    "user_email": str
                },
                "emails": [
                    {
                        "message_id": str,
                        "conversation_id": str,
                        "subject": str,
                        "sender_email": str,
                        "to_recipients": list,
                        "sent_at": str,
                        "received_at": str,
                        "importance": str,
                        "is_read": bool,
                        ... (24 fields total for analytics)
                    }
                ]
            }

    Raises:
        Exception: If authentication or API call fails
    """
    # Load target user email from environment
    user_email = os.getenv("TARGET_USER_EMAIL")

    # Initialize Graph client
    client = get_graph_client()

    # Configure query parameters for optimized data fetching
    query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
        select=[
            "id",
            "conversationId",
            "parentFolderId",
            "internetMessageId",
            "createdDateTime",
            "sentDateTime",
            "receivedDateTime",
            "lastModifiedDateTime",
            "from",
            "toRecipients",
            "ccRecipients",
            "bccRecipients",
            "replyTo",
            "subject",
            "bodyPreview",
            "importance",
            "isDraft",
            "isRead",
            "hasAttachments",
            "flag",
        ],
        top=1000,  # Maximum items per page (vs default 10)
        orderby=["receivedDateTime desc"],
    )
    request_config = RequestConfiguration(query_parameters=query_params)

    # Fetch all messages with pagination and optimized query
    all_emails = []
    messages = await client.users.by_user_id(user_email).messages.get(
        request_configuration=request_config
    )

    # Process first batch
    if messages and messages.value:
        for message in messages.value:
            # Format and store analytics-relevant email data
            formatted_email = format_email_for_analytics(message)
            all_emails.append(formatted_email)

        # Handle pagination if there are more messages
        while messages.odata_next_link:
            messages = (
                await client.users.by_user_id(user_email)
                .messages.with_url(messages.odata_next_link)
                .get()
            )

            if messages and messages.value:
                for message in messages.value:
                    formatted_email = format_email_for_analytics(message)
                    all_emails.append(formatted_email)

    # Prepare output data with metadata
    output_data = {
        "metadata": {
            "total_count": len(all_emails),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "user_email": user_email,
        },
        "emails": all_emails,
    }

    return output_data
