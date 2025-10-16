import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

# Load environment variables
load_dotenv()

# Azure AD credentials
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

# Target user email
TARGET_USER_EMAIL = "MuznyM@Muzny986.onmicrosoft.com"

# Microsoft Graph scopes
GRAPH_SCOPES = ["https://graph.microsoft.com/.default"]


def get_graph_client() -> GraphServiceClient:
    """
    Create and return a Microsoft Graph Service Client with application permissions.

    Returns:
        GraphServiceClient: Authenticated Graph client instance

    Raises:
        ValueError: If required environment variables are missing
    """
    if not all([AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET]):
        raise ValueError(
            "Missing required environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET"
        )

    # Create credentials using client secret
    credential = ClientSecretCredential(
        tenant_id=AZURE_TENANT_ID,
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET,
    )

    # Initialize and return Graph client
    client = GraphServiceClient(credentials=credential, scopes=GRAPH_SCOPES)

    return client
