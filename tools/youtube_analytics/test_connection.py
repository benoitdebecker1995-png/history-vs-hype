"""
Test YouTube Analytics API connection.

Run this after setting up credentials to verify everything works.

Usage:
    python -m tools.youtube_analytics.test_connection
"""

from datetime import datetime, timedelta
from auth import get_authenticated_service


def test_analytics_connection():
    """Test YouTube Analytics API with a basic query."""
    print("=" * 50)
    print("Testing YouTube Analytics API Connection")
    print("=" * 50)

    # Get authenticated service
    analytics = get_authenticated_service('youtubeAnalytics', 'v2')

    # Query: channel views for last 30 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    print(f"\nQuerying views from {start_date} to {end_date}...")

    response = analytics.reports().query(
        ids='channel==MINE',
        startDate=start_date,
        endDate=end_date,
        metrics='views,estimatedMinutesWatched',
        dimensions='day'
    ).execute()

    # Parse response
    if 'rows' in response and response['rows']:
        total_views = sum(row[1] for row in response['rows'])
        total_minutes = sum(row[2] for row in response['rows'])
        print(f"\nSuccess! Last 30 days:")
        print(f"  Total views: {total_views:,}")
        print(f"  Watch time: {total_minutes:,.0f} minutes ({total_minutes/60:.1f} hours)")
        print(f"  Days with data: {len(response['rows'])}")
    else:
        print("\nAPI connected but no data returned (new channel or no views)")

    return True


def test_data_api_connection():
    """Test YouTube Data API with channel info query."""
    print("\n" + "=" * 50)
    print("Testing YouTube Data API Connection")
    print("=" * 50)

    youtube = get_authenticated_service('youtube', 'v3')

    response = youtube.channels().list(
        part='snippet,statistics',
        mine=True
    ).execute()

    if 'items' in response and response['items']:
        channel = response['items'][0]
        print(f"\nChannel: {channel['snippet']['title']}")
        print(f"Subscribers: {int(channel['statistics']['subscriberCount']):,}")
        print(f"Total views: {int(channel['statistics']['viewCount']):,}")
        print(f"Video count: {channel['statistics']['videoCount']}")
    else:
        print("\nAPI connected but no channel found")

    return True


if __name__ == '__main__':
    try:
        test_analytics_connection()
        test_data_api_connection()
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED - API connection working!")
        print("=" * 50)
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Is client_secret.json in credentials/ folder?")
        print("2. Did you add yourself as test user in OAuth consent screen?")
        print("3. Are both APIs enabled in Google Cloud Console?")
        raise
