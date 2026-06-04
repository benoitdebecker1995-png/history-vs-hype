"""
YouTube Analytics API OAuth2 Authentication Module

Usage:
    from auth import get_authenticated_service

    youtube_analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    youtube_data = get_authenticated_service('youtube', 'v3')
"""

import os
import socket
from pathlib import Path

from tools.logging_config import get_logger
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

logger = get_logger(__name__)

# API scopes - analytics readonly + video/channel metadata readonly + comment read
SCOPES = [
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
]

# Bound every API socket so a stalled server can't hang a backfill forever.
# httplib2 (under googleapiclient) honors socket.setdefaulttimeout(). On timeout
# the call raises socket.timeout, which per-video fetch loops catch and skip.
# NOTE: applied only AFTER get_credentials() returns — setting it before the
# interactive OAuth flow would abort run_local_server while it waits on the
# browser redirect (the user may take longer than the timeout to sign in).
API_SOCKET_TIMEOUT_SECONDS = 120

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
            logger.info("Refreshing expired token...")
            try:
                creds.refresh(Request())
            except RefreshError:
                logger.warning("Refresh token revoked — need full re-authorization")
                creds = None
        if not creds or not creds.valid:
            logger.info("Opening browser for authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_PATH),
                SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Save for next run
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())
        logger.info("Token saved to %s", TOKEN_PATH)

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
    # Safe to set now: interactive OAuth (if any) already completed above.
    socket.setdefaulttimeout(API_SOCKET_TIMEOUT_SECONDS)
    return build(api_name, api_version, credentials=creds)


if __name__ == '__main__':
    # Quick test when run directly
    print("Testing authentication...")
    creds = get_credentials()
    print(f"Authentication successful!")
    print(f"Token expires: {creds.expiry}")
