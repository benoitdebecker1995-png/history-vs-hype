"""
YouTube Analytics API OAuth2 Authentication Module

Usage:
    from auth import get_authenticated_service

    youtube_analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    youtube_data = get_authenticated_service('youtube', 'v3')
"""

import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# API scopes - analytics readonly + video/channel metadata readonly
SCOPES = [
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/youtube.readonly',
]

# Paths relative to this file
CREDENTIALS_DIR = Path(__file__).parent / 'credentials'
CLIENT_SECRET_PATH = CREDENTIALS_DIR / 'client_secret.json'
TOKEN_PATH = CREDENTIALS_DIR / 'token.json'


def get_credentials():
    """
    Get valid OAuth2 credentials.

    On first run: Opens browser for authorization.
    On subsequent runs: Loads from token.json, refreshes if expired.

    Returns:
        google.oauth2.credentials.Credentials: Valid credentials object

    Raises:
        FileNotFoundError: If client_secret.json is missing
    """
    if not CLIENT_SECRET_PATH.exists():
        raise FileNotFoundError(
            f"OAuth client secret not found at {CLIENT_SECRET_PATH}\n"
            "Download from Google Cloud Console > APIs & Services > Credentials"
        )

    creds = None

    # Load existing token if available
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Opening browser for authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_PATH),
                SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Save for next run
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())
        print(f"Token saved to {TOKEN_PATH}")

    return creds


def get_authenticated_service(api_name='youtubeAnalytics', api_version='v2'):
    """
    Build an authenticated API service.

    Args:
        api_name: 'youtubeAnalytics' or 'youtube'
        api_version: 'v2' for Analytics, 'v3' for Data API

    Returns:
        googleapiclient.discovery.Resource: Authenticated API service

    Example:
        # For analytics (CTR, retention, watch time)
        analytics = get_authenticated_service('youtubeAnalytics', 'v2')

        # For video/channel data (metadata, comments)
        youtube = get_authenticated_service('youtube', 'v3')
    """
    creds = get_credentials()
    return build(api_name, api_version, credentials=creds)


if __name__ == '__main__':
    # Quick test when run directly
    print("Testing authentication...")
    creds = get_credentials()
    print(f"Authentication successful!")
    print(f"Token expires: {creds.expiry}")
