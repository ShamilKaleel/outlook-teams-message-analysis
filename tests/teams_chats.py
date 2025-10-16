import asyncio
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient


async def fetch_all_teams_chats_raw():
    """
    Fetch all Teams chat messages for MuznyM@Muzny986.onmicrosoft.com
    and export raw Graph API responses to teams_chats_raw.json
    """

    # Load environment variables
    load_dotenv()

    # Validate environment variables
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        print(
            "Error: Missing required environment variables (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)"
        )
        return

    try:
        # Initialize Graph client with application permissions
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        client = GraphServiceClient(
            credentials=credential, scopes=["https://graph.microsoft.com/.default"]
        )

        print("Authenticated successfully!")

        # Target user ID
        user_id = "MuznyM@Muzny986.onmicrosoft.com"

        # Fetch all chats and messages
        print(f"Fetching Teams chats for {user_id}...")
        all_chats = []
        all_messages = []

        # Get chats with pagination
        chats_response = await client.users.by_user_id(user_id).chats.get()

        while chats_response:
            if chats_response.value:
                # Store raw chat data
                for chat in chats_response.value:
                    all_chats.append(chat.__dict__)

                print(f"Fetched {len(all_chats)} chats so far...")

                # For each chat, fetch raw messages
                for chat in chats_response.value:
                    if chat.id:
                        print(f"Fetching messages from chat: {chat.id}")
                        await fetch_chat_messages_raw(client, chat.id, all_messages)

            # Handle pagination for chats
            if chats_response.odata_next_link:
                chats_response = (
                    await client.users.by_user_id(user_id)
                    .chats.with_url(chats_response.odata_next_link)
                    .get()
                )
            else:
                break

        print(f"Total chats found: {len(all_chats)}")
        print(f"Total messages found: {len(all_messages)}")

        # Prepare raw output data
        output_data = {
            "metadata": {
                "total_chats": len(all_chats),
                "total_messages": len(all_messages),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "user_email": user_id,
            },
            "chats": all_chats,
            "messages": all_messages,
        }

        # Save raw data to JSON file
        with open("teams_chats_raw.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

        print(f"Raw Teams chats and messages exported to teams_chats_raw.json")

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        print(f"Details: {str(e)}")


async def fetch_chat_messages_raw(client, chat_id, all_messages):
    """
    Fetch all raw messages from a specific chat with pagination handling
    """
    try:
        # Get raw messages for this chat
        messages_response = await client.chats.by_chat_id(chat_id).messages.get()

        while messages_response:
            if messages_response.value:
                # Store raw message data
                for message in messages_response.value:
                    all_messages.append(message.__dict__)

                print(
                    f"  Fetched {len(messages_response.value)} raw messages from chat {chat_id}"
                )

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
        print(
            f"Error fetching messages from chat {chat_id}: {type(e).__name__} - {str(e)}"
        )


if __name__ == "__main__":
    asyncio.run(fetch_all_teams_chats_raw())
