import os
from datetime import datetime, timezone
from config.settings import get_graph_client


async def fetch_all_emails_raw():
    """
    Fetch all emails from Outlook and return raw Graph API response data.

    Returns:
        dict: Dictionary containing metadata and raw email data
            {
                "metadata": {
                    "total_count": int,
                    "fetched_at": str (ISO format),
                    "user_email": str
                },
                "emails": [list of raw message objects]
            }

    Raises:
        Exception: If authentication or API call fails
    """
    # Load target user email from environment
    user_email = os.getenv("TARGET_USER_EMAIL")

    # Initialize Graph client
    client = get_graph_client()

    # Fetch all messages with pagination
    all_emails = []
    messages = await client.users.by_user_id(user_email).messages.get()

    # Process first batch
    if messages and messages.value:
        for message in messages.value:
            # Store raw message data using __dict__ to get all properties
            all_emails.append(message.__dict__)

        # Handle pagination if there are more messages
        while messages.odata_next_link:
            messages = (
                await client.users.by_user_id(user_email)
                .messages.with_url(messages.odata_next_link)
                .get()
            )

            if messages and messages.value:
                for message in messages.value:
                    all_emails.append(message.__dict__)

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
