"""
YouTube Analytics API OAuth2 Authentication Module

Usage:
    from auth import get_authenticated_service

    youtube_analytics = get_authenticated_service('youtubeAnalytics', 'v2')
    youtube_data = get_authenticated_service('youtube', 'v3')
"""

import os
import socket
import sys
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

# Loopback port for the interactive consent redirect. 0 = let the OS pick a free one.
# It used to be a hard-coded 8080, which collided: on 2026-08-03 the 07:45 HvH-GrowthRefresh run
# died with `[WinError 10048] Only one usage of each socket address ... is normally permitted`
# because HvH-CtrTracker (07:30, terminated at its PT20M limit) still held the port. This client is
# an `installed` (Desktop) type with a plain `http://localhost` redirect, and Google's loopback flow
# accepts ANY port for that client type — so a fixed port bought nothing and cost a daily outage.
OAUTH_LOOPBACK_PORT = 0

# Set by the routine wrappers. Also inferred when neither stdin nor stdout is a terminal.
NONINTERACTIVE_ENV_VAR = 'HVH_NONINTERACTIVE'


class InteractiveAuthRequired(RuntimeError):
    """Re-authorization is needed but nobody can answer a browser prompt.

    Raised instead of blocking on `run_local_server` in a scheduled/headless run. Mirrors the
    claude-CLI pre-flight in `.claude/routines/_lib-preflight.ps1`: a dead session must fail fast
    with an actionable message, not hang until the task's execution-time limit kills it.
    """


def _is_noninteractive() -> bool:
    """True when no human can complete a browser consent flow.

    The env var is an explicit override in BOTH directions; only when it is unset do we infer
    from the streams. A terminal keeps its browser flow even with output redirected, because
    stdin is still a tty there — under Task Scheduler neither stream is.
    """
    flag = os.environ.get(NONINTERACTIVE_ENV_VAR, '').strip().lower()
    if flag in {'1', 'true', 'yes'}:
        return True
    if flag in {'0', 'false', 'no'}:
        return False
    try:
        return not (sys.stdin.isatty() or sys.stdout.isatty())
    except (AttributeError, ValueError):
        # Detached or closed streams — a scheduled run, not a terminal.
        return True


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
            if _is_noninteractive():
                raise InteractiveAuthRequired(
                    "YouTube OAuth needs re-authorization, and this run is non-interactive "
                    "(scheduled task or piped output) so the browser consent flow cannot be "
                    "completed.\n"
                    "  The routine was NOT run. This is not a model or repo problem.\n"
                    "  FIX: open a terminal (as THIS Windows user) and run:\n"
                    "       python -m tools.youtube_analytics.auth --login\n"
                    f"  That refreshes {TOKEN_PATH.name}; the scheduled routines then resume on "
                    "their own."
                )
            logger.info("Opening browser for authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_PATH),
                SCOPES
            )
            creds = flow.run_local_server(port=OAUTH_LOOPBACK_PORT)

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


def main(argv=None) -> int:
    """CLI: check the stored token, or re-run the interactive consent flow.

    `--login` is the command the non-interactive failure message tells the user to run, so it must
    keep working from a terminal even when every scheduled routine is refusing to.
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog='python -m tools.youtube_analytics.auth',
        description='Check or refresh the YouTube API OAuth token.',
        epilog=(
            'Examples:\n'
            '  python -m tools.youtube_analytics.auth            # check the stored token\n'
            '  python -m tools.youtube_analytics.auth --login    # re-authorize in a browser\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--login',
        action='store_true',
        help='force the interactive browser flow even from a piped/redirected shell',
    )
    args = parser.parse_args(argv)

    if args.login:
        # The user asked for it at a terminal; the headless guard must not veto that.
        os.environ[NONINTERACTIVE_ENV_VAR] = '0'

    try:
        creds = get_credentials()
    except InteractiveAuthRequired as exc:
        print(exc)
        return 78  # same actionable code the routine pre-flight uses for a dead session

    print('Authentication successful.')
    print(f'Token expires: {creds.expiry}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
