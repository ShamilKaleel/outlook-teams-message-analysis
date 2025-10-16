import os
from datetime import datetime, timezone
from config.settings import get_graph_client


async def fetch_all_teams_chats_raw():
    """
    Fetch all Teams chats and messages for the user and return raw Graph API response data.
    This includes all received messages and replies from all chats.

    Returns:
        dict: Dictionary containing metadata, raw chat data, and raw message data
            {
                "metadata": {
                    "total_chats": int,
                    "total_messages": int,
                    "fetched_at": str (ISO format),
                    "user_email": str
                },
                "chats": [list of raw chat objects],
                "messages": [list of raw message objects from all chats]
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

    # Get chats with pagination
    chats_response = await client.users.by_user_id(user_email).chats.get()

    while chats_response:
        if chats_response.value:
            # Store raw chat data
            for chat in chats_response.value:
                all_chats.append(chat.__dict__)

            # For each chat, fetch all messages (received + replies)
            for chat in chats_response.value:
                if chat.id:
                    await fetch_chat_messages_raw(client, chat.id, all_messages)

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


async def fetch_chat_messages_raw(client, chat_id, all_messages):
    """
    Fetch all raw messages from a specific chat with pagination handling.
    This captures all messages including received messages, replies, and system events.

    Args:
        client: GraphServiceClient instance
        chat_id: The ID of the chat to fetch messages from
        all_messages: List to append fetched messages to

    Raises:
        Exception: If fetching messages fails
    """
    try:
        # Get raw messages for this chat
        messages_response = await client.chats.by_chat_id(chat_id).messages.get()

        while messages_response:
            if messages_response.value:
                # Store raw message data using __dict__ to get all properties
                for message in messages_response.value:
                    all_messages.append(message.__dict__)

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
        # Log error but don't stop fetching other chats
        print(
            f"Error fetching messages from chat {chat_id}: {type(e).__name__} - {str(e)}"
        )
