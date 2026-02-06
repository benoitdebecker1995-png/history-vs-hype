# Research: Phase 7 - API Foundation

**Researched:** 2026-01-24
**Phase Goal:** YouTube Analytics API configured and secure, ready for data scripts

## 1. Google Cloud Setup Steps

### Project Creation
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project (e.g., "history-vs-hype-analytics")
3. Note the Project ID

### Enable APIs
Enable these APIs in APIs & Services > Library:
- **YouTube Analytics API** — for CTR, retention, watch time
- **YouTube Data API v3** — for video metadata, comments

### OAuth Consent Screen
1. Go to APIs & Services > OAuth consent screen
2. Select "External" (unless using Google Workspace)
3. Fill required fields:
   - App name: "History vs Hype Analytics"
   - User support email: your email
   - Developer contact: your email
4. Add scopes (see section 2)
5. Add your Google account as test user (required for unverified apps)

### Create OAuth Credentials
1. Go to APIs & Services > Credentials
2. Create Credentials > OAuth client ID
3. Application type: **Desktop app**
4. Download JSON, save as `client_secret.json`

**Important:** Unverified apps are limited to 100 users and show a warning screen. For personal use, this is fine.

## 2. Required API Scopes

```python
SCOPES = [
    'https://www.googleapis.com/auth/yt-analytics.readonly',      # Analytics data
    'https://www.googleapis.com/auth/youtube.readonly',            # Channel/video metadata
]
```

**Scope notes:**
- `yt-analytics.readonly` — Required for all analytics queries (CTR, retention, watch time)
- `youtube.readonly` — Required to list videos, get video IDs, fetch comments
- Both are "sensitive" scopes requiring consent screen setup

## 3. OAuth2 Flow for Desktop App

### Recommended Library Stack
```
google-api-python-client>=2.100.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
```

### Code Pattern (InstalledAppFlow)

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json

SCOPES = [
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/youtube.readonly',
]

def get_authenticated_service():
    creds = None
    token_path = 'credentials/token.json'
    client_secret_path = 'credentials/client_secret.json'

    # Load existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or get new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save token for next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('youtubeAnalytics', 'v2', credentials=creds)
```

### How It Works
1. First run: Opens browser for Google login
2. User authorizes app
3. Redirects to localhost:8080
4. Token saved to `token.json`
5. Subsequent runs: Uses saved token, auto-refreshes if expired

## 4. Secure Credential Storage

### Directory Structure
```
tools/
  youtube-analytics/
    credentials/           # gitignored
      client_secret.json   # OAuth client credentials
      token.json           # User's access/refresh tokens
    .gitignore
    requirements.txt
    analytics.py
```

### .gitignore for credentials folder
```gitignore
# YouTube API credentials - NEVER commit
credentials/
*.json
!requirements.txt
```

### Alternative: Environment Variables
For client_secret, could use .env:
```
YOUTUBE_CLIENT_ID=xxxxx
YOUTUBE_CLIENT_SECRET=xxxxx
```

**Recommendation:** Use `credentials/` folder approach — simpler for desktop use, JSON files work directly with Google libraries.

## 5. Available Metrics

### What the API CAN provide:

| Metric | API Field | Notes |
|--------|-----------|-------|
| Views | `views` | Total views |
| Watch time | `estimatedMinutesWatched` | Total minutes |
| Average view duration | `averageViewDuration` | Seconds |
| Likes/Dislikes | `likes`, `dislikes` | Engagement |
| Comments | `comments` | Count |
| Shares | `shares` | Count |
| Subscribers gained/lost | `subscribersGained`, `subscribersLost` | Net growth |
| Retention curve | `audienceWatchRatio` | Per-video, requires special report |
| Relative retention | `relativeRetentionPerformance` | vs similar-length videos |

### CTR Limitation (IMPORTANT)

**Impressions CTR (thumbnail click-through rate) may have limited API availability.**

Per [Google Issue Tracker #254665034](https://issuetracker.google.com/issues/254665034) and developer forums, `impressions` and `impressionClickThroughRate` are visible in YouTube Studio but not consistently available in the Analytics API for all report types.

**Workaround options:**
1. Use `video_thumbnail_impressions` and calculate CTR from views
2. Manual input from YouTube Studio for CTR
3. Check if metric is available in your specific report type

### Retention Report Special Requirements

From [Google documentation](https://developers.google.com/youtube/analytics/metrics):
- Must query **one video at a time** (no batch)
- `maxResults` capped at 200
- Uses `elapsedVideoTimeRatio` dimension (0.0 to 1.0)
- Returns `audienceWatchRatio` (absolute) and `relativeRetentionPerformance` (vs peers)

## 6. Common Pitfalls

### Quota Limits
- Default: 10,000 units/day
- Analytics query: ~1 unit per request
- Retention report: Higher cost (200 data points per video)
- **Mitigation:** Cache results, don't re-fetch same data

### Scope Issues
- Adding new scopes requires re-authorization
- Delete `token.json` to force re-auth with new scopes

### Token Expiry
- Access tokens expire in 1 hour
- Refresh tokens last indefinitely (unless revoked)
- Code should handle `creds.expired` and auto-refresh

### API Version
- YouTube Analytics API v2 is current
- YouTube Data API v3 is current
- Don't mix v1 code samples

### Windows-Specific
- Use forward slashes or raw strings for paths
- `localhost` redirect should work, but firewall may block port 8080

## 7. Minimal Working Example

```python
# test_connection.py
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

# First-time auth
flow = InstalledAppFlow.from_client_secrets_file('credentials/client_secret.json', SCOPES)
creds = flow.run_local_server(port=8080)

# Build service
youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)

# Test query - get channel views for last 30 days
response = youtube_analytics.reports().query(
    ids='channel==MINE',
    startDate='2025-12-25',
    endDate='2026-01-24',
    metrics='views,estimatedMinutesWatched',
    dimensions='day'
).execute()

print(response)
```

## 8. Recommendations

1. **Start with YouTube Data API** to list videos and get IDs
2. **Use InstalledAppFlow** — simplest for desktop apps
3. **Store credentials in gitignored `credentials/` folder**
4. **Handle CTR manually initially** — API support is inconsistent
5. **Cache retention data** — expensive to re-fetch
6. **Test with one video first** before building full pipeline

## Sources

- [YouTube Analytics API Documentation](https://developers.google.com/youtube/analytics)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/youtube/reporting/guides/authorization/installed-apps)
- [Python Quickstart](https://developers.google.com/youtube/v3/quickstart/python)
- [Metrics Reference](https://developers.google.com/youtube/reporting/v1/reports/metrics)
- [Audience Retention Reports](https://developers.google.com/youtube/analytics/metrics)

---

*Research complete: 2026-01-24*
