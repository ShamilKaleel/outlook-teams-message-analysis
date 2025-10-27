import os
from datetime import datetime, timezone
from config.settings import get_graph_client
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.users.item.chats.chats_request_builder import (
    ChatsRequestBuilder,
)
from msgraph.generated.chats.item.messages.messages_request_builder import (
    MessagesRequestBuilder,
)


def format_message_for_analytics(message, chat_id, chat_type):
    """
    Extract analytics-relevant fields from a message object.

    Args:
        message: Message object from Graph API
        chat_id: ID of the chat this message belongs to
        chat_type: Type of the chat (oneOnOne, group, meeting)

    Returns:
        dict: Structured message data for analytics with fields:
            - message_id, chat_id, chat_type
            - created_at, last_modified_at, last_edited_at, deleted_at
            - sender_id, sender_name
            - content, content_type, message_length
            - message_type, importance
            - reply_to_id, is_reply
    """
    # Extract sender information
    sender_id = None
    sender_name = None
    if message.from_ and message.from_.user:
        sender_id = message.from_.user.id
        sender_name = message.from_.user.display_name

    # Extract message content
    content = None
    content_type = None
    message_length = 0
    if message.body:
        content = message.body.content
        content_type = (
            str(message.body.content_type) if message.body.content_type else None
        )
        message_length = len(content) if content else 0

    # Build structured message object
    return {
        # Identifiers
        "message_id": message.id,
        "chat_id": chat_id,
        "chat_type": chat_type,
        # Timestamps
        "created_at": (
            message.created_date_time.isoformat() if message.created_date_time else None
        ),
        "last_modified_at": (
            message.last_modified_date_time.isoformat()
            if message.last_modified_date_time
            else None
        ),
        "last_edited_at": (
            message.last_edited_date_time.isoformat()
            if message.last_edited_date_time
            else None
        ),
        "deleted_at": (
            message.deleted_date_time.isoformat() if message.deleted_date_time else None
        ),
        # Sender
        "sender_id": sender_id,
        "sender_name": sender_name,
        # Content
        "content": content,
        "content_type": content_type,
        "message_length": message_length,
        # Message metadata
        "message_type": str(message.message_type) if message.message_type else None,
        "importance": str(message.importance) if message.importance else None,
        # Reply tracking
        "reply_to_id": message.reply_to_id,
        "is_reply": message.reply_to_id is not None,
    }


async def fetch_all_teams_chats_raw():
    """
    Fetch all Teams chats and messages optimized for analytics.
    Returns structured data with only analytics-relevant fields.

    Returns:
        dict: Dictionary containing metadata and structured analytics data
            {
                "metadata": {
                    "total_chats": int,
                    "total_messages": int,
                    "fetched_at": str (ISO format),
                    "user_email": str
                },
                "chats": [
                    {
                        "chat_id": str,
                        "chat_type": str (oneOnOne, group, meeting),
                        "topic": str,
                        "created_at": str (ISO format),
                        "last_updated_at": str (ISO format)
                    }
                ],
                "messages": [
                    {
                        "message_id": str,
                        "chat_id": str,
                        "chat_type": str,
                        "created_at": str,
                        "sender_id": str,
                        "sender_name": str,
                        "content": str,
                        "message_length": int,
                        "is_reply": bool,
                        ... (15 fields total for analytics)
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

    # Fetch all chats and messages
    all_chats = []
    all_messages = []

    # Configure query parameters for optimized chat fetching
    query_params = ChatsRequestBuilder.ChatsRequestBuilderGetQueryParameters(
        select=["id", "chatType", "topic", "createdDateTime", "lastUpdatedDateTime"],
        top=50,  # Maximum items per page
    )
    request_config = RequestConfiguration(query_parameters=query_params)

    # Get chats with pagination and optimized query
    chats_response = await client.users.by_user_id(user_email).chats.get(
        request_configuration=request_config
    )

    while chats_response:
        if chats_response.value:
            # Store formatted chat data
            for chat in chats_response.value:
                chat_data = {
                    "chat_id": chat.id,
                    "chat_type": str(chat.chat_type) if chat.chat_type else None,
                    "topic": chat.topic,
                    "created_at": (
                        chat.created_date_time.isoformat()
                        if chat.created_date_time
                        else None
                    ),
                    "last_updated_at": (
                        chat.last_updated_date_time.isoformat()
                        if chat.last_updated_date_time
                        else None
                    ),
                }
                all_chats.append(chat_data)

            # For each chat, fetch all messages with analytics optimization
            for chat in chats_response.value:
                if chat.id:
                    chat_type = str(chat.chat_type) if chat.chat_type else None
                    await fetch_chat_messages_raw(
                        client, chat.id, chat_type, all_messages
                    )

        # Handle pagination for chats
        if chats_response.odata_next_link:
            chats_response = (
                await client.users.by_user_id(user_email)
                .chats.with_url(chats_response.odata_next_link)
                .get()
            )
        else:
            break

    # Prepare output data with metadata
    output_data = {
        "metadata": {
            "total_chats": len(all_chats),
            "total_messages": len(all_messages),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "user_email": user_email,
        },
        "chats": all_chats,
        "messages": all_messages,
    }

    return output_data


async def fetch_chat_messages_raw(client, chat_id, chat_type, all_messages):
    """
    Fetch analytics-optimized messages from a specific chat with pagination handling.
    Uses query parameters to fetch only required fields for analytics.

    Args:
        client: GraphServiceClient instance
        chat_id: The ID of the chat to fetch messages from
        chat_type: Type of the chat (oneOnOne, group, meeting)
        all_messages: List to append formatted messages to

    Raises:
        Exception: If fetching messages fails
    """
    try:
        # Configure query parameters for optimized data fetching
        # Note: Chat messages endpoint does NOT support $select or $orderby
        # Only $top is supported for pagination optimization
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            top=50,  # Maximum items per page (reduces pagination requests by ~50%)
        )
        request_config = RequestConfiguration(query_parameters=query_params)

        # Get messages for this chat with optimized query
        messages_response = await client.chats.by_chat_id(chat_id).messages.get(
            request_configuration=request_config
        )

        while messages_response:
            if messages_response.value:
                # Format and store analytics-relevant message data
                for message in messages_response.value:
                    formatted_message = format_message_for_analytics(
                        message, chat_id, chat_type
                    )
                    all_messages.append(formatted_message)

            # Handle pagination for messages
            if messages_response.odata_next_link:
                messages_response = (
                    await client.chats.by_chat_id(chat_id)
                    .messages.with_url(messages_response.odata_next_link)
                    .get()
                )
            else:
                break

    except Exception as e:
        # Silently skip chats that cannot be accessed (e.g., external/federated chats)
        if "Forbidden" in str(e) or "Tenant Id mismatch" in str(e):
            pass  # Expected for external chats with app permissions
        else:
            print(
                f"Unexpected error fetching messages from chat {chat_id}: {type(e).__name__} - {str(e)}"
            )
