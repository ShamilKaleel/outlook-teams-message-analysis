import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient


async def fetch_all_emails():
    """Fetch all emails from Outlook and save to JSON file."""

    # Load environment variables from .env file
    load_dotenv()

    client_id = os.getenv("AZURE_CLIENT_ID")
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    # Validate environment variables
    if not all([client_id, tenant_id, client_secret]):
        print("Error: Missing required environment variables in .env file")
        print("Required: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET")
        return

    try:
        # Create credentials using client secret
        credential = ClientSecretCredential(
            tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
        )

        # Initialize Graph client
        scopes = ["https://graph.microsoft.com/.default"]
        client = GraphServiceClient(credentials=credential, scopes=scopes)

        print("Authenticated successfully!")
        print("Fetching emails from: MuznyM@Muzny986.onmicrosoft.com")

        # Target user email
        user_id = "MuznyM@Muzny986.onmicrosoft.com"

        # Fetch all messages with pagination
        all_emails = []
        messages = await client.users.by_user_id(user_id).messages.get()
        print(messages.value)

        # Process first batch
        if messages and messages.value:
            for message in messages.value:
                email_data = {
                    "id": message.id,
                    "subject": message.subject,
                    "from": (
                        {
                            "name": (
                                message.from_.email_address.name
                                if message.from_ and message.from_.email_address
                                else None
                            ),
                            "address": (
                                message.from_.email_address.address
                                if message.from_ and message.from_.email_address
                                else None
                            ),
                        }
                        if message.from_
                        else None
                    ),
                    "to_recipients": [
                        {
                            "name": recipient.email_address.name,
                            "address": recipient.email_address.address,
                        }
                        for recipient in (message.to_recipients or [])
                    ],
                    "cc_recipients": [
                        {
                            "name": recipient.email_address.name,
                            "address": recipient.email_address.address,
                        }
                        for recipient in (message.cc_recipients or [])
                    ],
                    "body_preview": message.body_preview,
                    "received_datetime": (
                        message.received_date_time.isoformat()
                        if message.received_date_time
                        else None
                    ),
                    "sent_datetime": (
                        message.sent_date_time.isoformat()
                        if message.sent_date_time
                        else None
                    ),
                    "is_read": message.is_read,
                    "has_attachments": message.has_attachments,
                    "importance": (
                        message.importance.value if message.importance else None
                    ),
                    "conversation_id": message.conversation_id,
                }
                all_emails.append(email_data)

            print(f"Fetched {len(all_emails)} emails so far...")

            # Handle pagination if there are more messages
            while messages.odata_next_link:
                print("Fetching next page...")
                messages = (
                    await client.users.by_user_id(user_id)
                    .messages.with_url(messages.odata_next_link)
                    .get()
                )

                if messages and messages.value:
                    for message in messages.value:
                        email_data = {
                            "id": message.id,
                            "subject": message.subject,
                            "from": (
                                {
                                    "name": (
                                        message.from_.email_address.name
                                        if message.from_ and message.from_.email_address
                                        else None
                                    ),
                                    "address": (
                                        message.from_.email_address.address
                                        if message.from_ and message.from_.email_address
                                        else None
                                    ),
                                }
                                if message.from_
                                else None
                            ),
                            "to_recipients": [
                                {
                                    "name": recipient.email_address.name,
                                    "address": recipient.email_address.address,
                                }
                                for recipient in (message.to_recipients or [])
                            ],
                            "cc_recipients": [
                                {
                                    "name": recipient.email_address.name,
                                    "address": recipient.email_address.address,
                                }
                                for recipient in (message.cc_recipients or [])
                            ],
                            "body_preview": message.body_preview,
                            "received_datetime": (
                                message.received_date_time.isoformat()
                                if message.received_date_time
                                else None
                            ),
                            "sent_datetime": (
                                message.sent_date_time.isoformat()
                                if message.sent_date_time
                                else None
                            ),
                            "is_read": message.is_read,
                            "has_attachments": message.has_attachments,
                            "importance": (
                                message.importance.value if message.importance else None
                            ),
                            "conversation_id": message.conversation_id,
                        }
                        all_emails.append(email_data)

                    print(f"Fetched {len(all_emails)} emails so far...")

        # Prepare output data
        output_data = {
            "metadata": {
                "total_count": len(all_emails),
                "fetched_at": datetime.now().isoformat(),
                "user_email": user_id,
            },
            "emails": all_emails,
        }

        # Save to JSON file
        output_file = "emails.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"\nSuccess! Fetched {len(all_emails)} emails")
        print(f"Emails saved to: {output_file}")

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        print(f"Details: {str(e)}")


if __name__ == "__main__":
    asyncio.run(fetch_all_emails())
