"""
API Client for Analytics Dashboard

Handles communication with the FastAPI backend to fetch
Outlook and Teams analytics results.
"""

import requests
from typing import Optional, Dict, Any


class AnalyticsAPIClient:
    """Client for fetching analytics from the FastAPI backend."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize API client.

        Args:
            base_url: Base URL of the FastAPI server
        """
        self.base_url = base_url.rstrip("/")
        self.outlook_endpoint = f"{self.base_url}/analytics/outlook/analyze"
        self.teams_endpoint = f"{self.base_url}/analytics/teams/analyze"

    def fetch_outlook_analytics(self) -> Optional[Dict[str, Any]]:
        """
        Fetch Outlook analytics from the API.

        Returns:
            Analytics data dictionary or None if request fails
        """
        try:
            response = requests.get(self.outlook_endpoint, timeout=300)  # 5 min timeout for LLM processing
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Could not connect to API at {self.outlook_endpoint}. "
                "Please ensure the FastAPI server is running."
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                "Request timed out. The LLM analysis may be taking longer than expected."
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error fetching Outlook analytics: {str(e)}")

    def fetch_teams_analytics(self) -> Optional[Dict[str, Any]]:
        """
        Fetch Teams analytics from the API.

        Returns:
            Analytics data dictionary or None if request fails
        """
        try:
            response = requests.get(self.teams_endpoint, timeout=300)  # 5 min timeout for LLM processing
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Could not connect to API at {self.teams_endpoint}. "
                "Please ensure the FastAPI server is running."
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                "Request timed out. The LLM analysis may be taking longer than expected."
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error fetching Teams analytics: {str(e)}")

    def check_health(self) -> bool:
        """
        Check if the API server is running.

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
