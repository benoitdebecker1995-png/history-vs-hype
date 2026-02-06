# Session Progress - History vs Hype Channel Infrastructure

**Last Updated:** 2025-12-26

---

## Context: What We're Building

The user runs **History vs Hype**, a YouTube channel focused on evidence-based myth-busting about geopolitics, colonial history, and ideological narratives.

**Channel Stats:** ~200 subscribers, 82K+ views, 30-35% retention (excellent for educational content)

**Current Focus:** Building infrastructure to:
1. Analyze channel performance data programmatically
2. Study competitor creator styles (Kraut, Knowing Better, Shaun, etc.)
3. Improve research and fact-checking workflows

---

## Current Task: YouTube Data Integration

### Status: MCP APPROACH FAILED - NEED ALTERNATIVE

**What happened:**
- The package `@anthropic-ai/claude-code-mcp-youtube-data` does NOT exist on npm
- Community alternative `zubeid-youtube-mcp-server` has dependency bugs
- Need alternative approach for pulling YouTube data

**API Key (Still Valid):** AIzaSyAE8B9kDhMpv6D7pOcLUOhweFeAeqSMJBE

### Alternative Approaches

**Option 1: Direct YouTube Data API via WebFetch (Simplest)**
- Use WebFetch to call YouTube Data API endpoints directly
- No dependencies, works immediately
- Limited by API quotas (10,000 units/day)

**Option 2: Manual YouTube Studio Export**
- Export CSV from YouTube Studio Analytics
- Already have data through Jan 19, 2025 in `video-projects/_ANALYTICS/COMPLETE-PERFORMANCE-DATABASE.md`
- User knows the workflow, reliable

**Option 3: Build Custom MCP Server**
- More work but full control
- Would need to create Node.js MCP server
- Overkill for current needs

### Current Data Status
- **Last Update:** January 19, 2025
- **Total Videos:** 165
- **Total Views:** 82,649
- **Total Watch Time:** 590.84 hours
- **Subscribers:** ~200

### Recommended Next Steps
1. [ ] Use YouTube Studio export for fresh data (manual but reliable)
2. [ ] Update COMPLETE-PERFORMANCE-DATABASE.md with new exports
3. [ ] Remove non-existent MCP config from .claude.json

---

## Completed Earlier This Session

### Transcript Corrections (for style analysis)
We cleaned up auto-generated transcripts of competitor creators to use as style references:

| Creator | Video | Status | Notes |
|---------|-------|--------|-------|
| Kraut | Vodka | ✅ Fixed | ethyl alcohol, en masse, social strife, Stolichnaya |
| Kraut | Authoritarianism | ✅ Fixed | mestnichestvo, Zemsky Sobor, kormlenie, caesaropapist |
| Kraut | Russia Big | ✅ Clean | Minor errors, Johnny Harris style noted |
| Finnish Interview | Intelligence | ✅ Kept | Valuable lecture on Russian intelligence |
| Knowing Better | Lost Cause | ✅ Clean | Good reference |
| Knowing Better | Columbus | ✅ Clean | Minor proper nouns |
| Fall of Civilizations | Bronze Age | ✅ Clean | Minor proper nouns |
| Historia Civilis | Caesar | ✅ Clean | Very clean transcript |
| Shaun | Hiroshima | ✅ Clean | Excellent quality |

**Fix Scripts Created:**
- `D:/History vs Hype/tools/fix-vodka.ps1`
- `D:/History vs Hype/tools/fix-authoritarianism.ps1`

**Transcripts Location:** `D:/History vs Hype/transcripts/`

---

## Future Improvements Queue

After YouTube MCP is working:
1. **Retention curve analysis** - Export from YouTube Studio, analyze dropout points
2. **Academic source library** - Database of verified sources across videos
3. **Better transcription** - Whisper AI for cleaner competitor transcripts
4. **Competitor thumbnail archive** - Visual reference database

---

## Key Files to Know About

- `CLAUDE.md` - Main project instructions (comprehensive)
- `.claude/SCRIPTWRITING-STYLE-GUIDE.md` - Kraut/Alex O'Connor style patterns
- `.claude/USER-PREFERENCES.md` - User's working style preferences
- `channel-data/COMPLETE-PERFORMANCE-DATABASE.md` - Video performance data
- `transcripts/` - Competitor creator transcripts for style analysis

---

## To Resume After Restart

Tell Claude: "test YouTube MCP"

This will verify the MCP server is working and pull channel stats.
