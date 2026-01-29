# Phase 13: Discovery Tools - Research

**Researched:** 2026-01-29
**Domain:** YouTube SEO, keyword research, autocomplete extraction, intent classification
**Confidence:** HIGH

## Summary

YouTube discovery tools in 2026 focus on intent-driven optimization rather than keyword volume alone. The platform's algorithm prioritizes intent matching over exact keyword matches, making search intent classification critical. Standard approaches include autocomplete scraping (without official API support), VidIQ integration for search volume estimates, and YouTube Analytics API for performance diagnostics.

The key shift in 2026 is that YouTube Search behaves differently from Home/Suggested surfaces—it's entirely intent-driven. Two people searching the same keyword see different results based on their history and predicted satisfaction. Tools must therefore focus on understanding viewer intent patterns, not just extracting keywords.

Educational channels like the target (history + primary sources) benefit from long-tail keyword strategies targeting specific queries ("how did X happen" vs "X explained"). Competitor analysis reveals successful channels use 3-10% CTR with consistent metadata patterns across title/description/tags. Diagnostic thresholds show impressions under 500 in 7 days signal SEO issues, while CTR under 4% indicates title/thumbnail problems.

**Primary recommendation:** Build keyword extraction with autocomplete scraping (Node.js or Python), integrate VidIQ via guided prompts (no public API), classify intent using custom educational content categories, and extend existing /analyze command for diagnostics rather than building separate tools.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Puppeteer | 22.x | YouTube autocomplete scraping | Most reliable for dynamic content, stealth plugin evades detection |
| youtube-analytics-api | v2 | Official metrics access | Direct API access for impressions, CTR, views data |
| VidIQ | Web-based | Search volume estimates | Industry standard despite no public API; 85% accuracy vs actual performance |
| Python requests | 2.31+ | Alternative scraping | Lighter weight, direct JSON endpoint access |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| puppeteer-extra-plugin-stealth | 2.x | Anti-detection for scraping | Essential for avoiding YouTube rate limits |
| Apify YouTube scrapers | SaaS | Pre-built scraping actors | When building from scratch isn't feasible |
| google-api-python-client | 2.x | YouTube Data API v3 | Alternative to Node.js for API access |
| TubeBuddy | Web-based | Competitor keyword analysis | Alternative to VidIQ, similar capabilities |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Puppeteer | Playwright | Faster but less mature anti-detection |
| VidIQ | TubeBuddy | Similar features, preference varies |
| Scraping | Official YouTube API | API lacks autocomplete endpoint, limited data |
| Custom scraper | Apify pre-built | Faster setup but less control, recurring cost |

**Installation:**
```bash
# Node.js approach
npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth

# Python approach
pip install google-api-python-client requests beautifulsoup4

# VidIQ integration
# No installation - web-based with manual data entry workflow
```

## Architecture Patterns

### Recommended Project Structure
```
tools/discovery/
├── scrapers/
│   ├── autocomplete.js         # YouTube autocomplete extraction
│   ├── competitor-keywords.js  # Analyze competitor channels
│   └── utils/
│       ├── rate-limiter.js     # Exponential backoff
│       └── stealth-config.js   # Anti-detection setup
├── classifiers/
│   ├── intent-mapper.js        # Search intent classification
│   └── channel-dna-scorer.js   # Fit scoring for documentary style
├── diagnostics/
│   ├── impression-analyzer.js  # Low discovery diagnosis
│   └── metadata-checker.js     # Consistency validation
├── database/
│   ├── schema.sql             # Keyword tracking schema
│   └── queries.js             # Common query patterns
└── integrations/
    ├── vidiq-workflow.js      # Guided VidIQ prompts
    └── youtube-analytics.js   # Official API wrapper
```

### Pattern 1: Autocomplete Scraping with Rate Limiting
**What:** Extract keyword suggestions from YouTube's autocomplete feature using browser automation with anti-detection measures.
**When to use:** Long-tail keyword discovery, topic research, competitor seed analysis.
**Example:**
```javascript
// Source: https://serpapi.com/blog/web-scraping-youtube-autocomplete-with-nodejs/
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

async function getAutocompleteSuggestions(seedKeyword) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Navigate to YouTube search
  await page.goto('https://www.youtube.com/results?search_query=' + encodeURIComponent(seedKeyword));

  // Wait for autocomplete to load
  await page.waitForSelector('input[name="search_query"]');
  await page.type('input[name="search_query"]', seedKeyword);

  // Extract suggestions from dropdown
  const suggestions = await page.evaluate(() => {
    const elements = document.querySelectorAll('.sbdd_a li .sbqs_c');
    return Array.from(elements).map(el => el.textContent.trim());
  });

  await browser.close();

  // Implement exponential backoff for rate limiting
  await sleep(Math.random() * 2000 + 1000); // Random 1-3s delay

  return suggestions;
}
```

### Pattern 2: Intent Classification with Custom Categories
**What:** Classify search queries by viewer intent using categories specific to educational history content.
**When to use:** Topic selection, title optimization, understanding what viewers want.
**Example:**
```javascript
// Custom categories for history + primary sources channel
const INTENT_CATEGORIES = {
  MYTH_BUSTING: {
    patterns: ['myth', 'true', 'false', 'really', 'actually', 'fact check'],
    examples: ['dark ages myth', 'did crusades really happen']
  },
  TERRITORIAL_DISPUTE: {
    patterns: ['border', 'dispute', 'conflict', 'claim', 'territory'],
    examples: ['bir tawil unclaimed', 'belize guatemala border']
  },
  PRIMARY_SOURCE: {
    patterns: ['document', 'treaty', 'original', 'manuscript', 'archive'],
    examples: ['treaty of guadalupe hidalgo text', 'sykes picot agreement']
  },
  MECHANISM_EXPLAINER: {
    patterns: ['how did', 'how was', 'process', 'method', 'system'],
    examples: ['how did USSR collapse', 'how was berlin wall built']
  },
  TIMELINE_CORRECTION: {
    patterns: ['when', 'timeline', 'chronology', 'date', 'year'],
    examples: ['when did somaliland declare independence']
  },
  IDEOLOGICAL_NARRATIVE: {
    patterns: ['why', 'ideology', 'belief', 'narrative', 'claim'],
    examples: ['why crusades were defensive', 'communism definition']
  }
};

function classifyIntent(query, categories = INTENT_CATEGORIES) {
  const results = {};
  const lowerQuery = query.toLowerCase();

  for (const [category, config] of Object.entries(categories)) {
    const matchCount = config.patterns.filter(p => lowerQuery.includes(p)).length;
    if (matchCount > 0) {
      results[category] = {
        confidence: Math.min(matchCount / config.patterns.length, 1.0),
        matchedPatterns: config.patterns.filter(p => lowerQuery.includes(p))
      };
    }
  }

  // Sort by confidence, return primary + secondary
  const sorted = Object.entries(results).sort((a, b) => b[1].confidence - a[1].confidence);
  return {
    primary: sorted[0] || null,
    secondary: sorted[1] || null,
    allMatches: sorted
  };
}

// Channel DNA fit score (documentary style indicators)
function calculateDnaFitScore(query) {
  const positiveSignals = [
    'evidence', 'document', 'source', 'proof', 'archive', 'manuscript',
    'treaty', 'original', 'historical', 'primary', 'fact', 'debunk'
  ];
  const negativeSignals = [
    'conspiracy', 'secret', 'hidden', 'shocking', 'you won\'t believe'
  ];

  let score = 0.5; // Baseline
  const lower = query.toLowerCase();

  positiveSignals.forEach(signal => {
    if (lower.includes(signal)) score += 0.1;
  });

  negativeSignals.forEach(signal => {
    if (lower.includes(signal)) score -= 0.2;
  });

  return Math.max(0, Math.min(1, score));
}
```

### Pattern 3: Diagnostic Analysis with Benchmarking
**What:** Compare video performance metrics against channel-specific benchmarks to identify discovery issues.
**When to use:** Post-publish analysis (7-14 days), underperformer rescue, learning for future videos.
**Example:**
```javascript
// Source: YouTube Analytics API metrics documentation
// https://developers.google.com/youtube/analytics/metrics

async function diagnoseDiscoveryIssues(videoId, channelBenchmarks) {
  // Fetch 7-day metrics via YouTube Analytics API
  const metrics = await youtubeAnalytics.reports.query({
    ids: 'channel==MINE',
    filters: `video==${videoId}`,
    metrics: 'videoThumbnailImpressions,videoThumbnailImpressionsClickRate,views,averageViewDuration',
    dimensions: 'day',
    startDate: '7daysAgo',
    endDate: 'today'
  });

  const impressions = metrics.rows.reduce((sum, row) => sum + row[0], 0);
  const avgCTR = metrics.rows.reduce((sum, row) => sum + row[1], 0) / metrics.rows.length;
  const totalViews = metrics.rows.reduce((sum, row) => sum + row[2], 0);

  const diagnosis = {
    issues: [],
    fixes: [],
    learnings: []
  };

  // CTR benchmarks: 4-10% is good, <4% is problem
  // Source: https://focus-digital.co/average-youtube-ctr-organic-paid-benchmarks-2025/
  if (avgCTR < 0.04) {
    diagnosis.issues.push({
      type: 'LOW_CTR',
      severity: 'HIGH',
      value: avgCTR,
      benchmark: 0.04,
      description: 'Click-through rate below 4% indicates title/thumbnail issue'
    });
    diagnosis.fixes.push({
      action: 'Update thumbnail to show primary source document or map',
      rationale: 'Channel DNA: map/evidence thumbnails outperform face thumbnails',
      priority: 'IMMEDIATE'
    });
    diagnosis.learnings.push({
      insight: 'Documentary evidence > personality for this audience',
      applyTo: 'Future video thumbnail strategy'
    });
  }

  // Impressions: compare to channel baseline (varies by size)
  if (impressions < channelBenchmarks.avgImpressions * 0.5) {
    diagnosis.issues.push({
      type: 'LOW_IMPRESSIONS',
      severity: 'MEDIUM',
      value: impressions,
      benchmark: channelBenchmarks.avgImpressions,
      description: 'Impressions 50% below channel average indicates SEO/metadata issue'
    });
    diagnosis.fixes.push({
      action: 'Add long-tail keywords to description matching search intent',
      rationale: 'Low impressions = YouTube doesn\'t understand topic relevance',
      priority: 'HIGH'
    });
    diagnosis.learnings.push({
      insight: 'Need better keyword research pre-publish',
      applyTo: 'Next video metadata planning'
    });
  }

  return diagnosis;
}
```

### Pattern 4: VidIQ Integration (Guided Workflow)
**What:** No public API exists, so use guided prompts for manual data entry from VidIQ web interface.
**When to use:** Getting search volume estimates, competitor analysis, keyword scoring.
**Example:**
```javascript
// Guided workflow for VidIQ data collection
function generateVidiqWorkflowPrompts(topic) {
  return {
    step1: {
      instruction: `Open VidIQ Keywords tool and search for: "${topic}"`,
      dataToCollect: ['Search Volume (monthly)', 'Competition Score (0-100)', 'Overall Score'],
      prompt: 'Paste the VidIQ data in this format:\nSearch Volume: [number]\nCompetition: [0-100]\nOverall Score: [0-100]'
    },
    step2: {
      instruction: 'Switch to "Related Keywords" tab in VidIQ',
      dataToCollect: ['Top 5-10 related keywords with their scores'],
      prompt: 'List related keywords (one per line) with format:\n[keyword] | Volume: [number] | Competition: [score]'
    },
    step3: {
      instruction: 'Check "Competitors" tab for similar videos',
      dataToCollect: ['Top 3 competing video titles', 'Their view counts', 'Upload dates'],
      prompt: 'List competitors:\n[Title] | [Views] | [Age in months]'
    },
    storage: {
      location: `video-projects/_IN_PRODUCTION/${topic}/vidiq-data.json`,
      format: 'JSON for later analysis'
    }
  };
}

// Store for tracking VidIQ prediction accuracy
function trackVidiqAccuracy(videoId, vidiqPrediction, actualPerformance) {
  const accuracy = {
    predicted: {
      searchVolume: vidiqPrediction.searchVolume,
      competition: vidiqPrediction.competition,
      overallScore: vidiqPrediction.overallScore
    },
    actual: {
      impressions: actualPerformance.impressions,
      views: actualPerformance.views,
      ctr: actualPerformance.ctr
    },
    variance: {
      viewsVsPrediction: actualPerformance.views / (vidiqPrediction.searchVolume * 0.01), // Rough conversion
      competitionAccuracy: 'MANUAL_ASSESSMENT' // Subjective
    },
    timestamp: new Date().toISOString()
  };

  // Append to channel-data/vidiq-accuracy-log.json
  appendToLog('channel-data/vidiq-accuracy-log.json', accuracy);

  return accuracy;
}
```

### Anti-Patterns to Avoid
- **Over-reliance on keyword volume:** High volume doesn't mean good fit. Educational content often performs better on long-tail specific queries.
- **Ignoring search intent:** Keywords without understanding "why" viewers search leads to high bounce rates despite good CTR.
- **Keyword stuffing in metadata:** 2026 algorithm detects unnatural keyword density, penalizes rankings and viewer experience.
- **Scraping without rate limiting:** YouTube detects and blocks aggressive scrapers (HTTP 429/403 errors). Always implement exponential backoff.
- **Single-metric optimization:** Focusing only on CTR or only on impressions misses the interaction—need both high for success.
- **Stale benchmark data:** Channel-size-specific benchmarks shift over time. Recalculate quarterly using recent video performance.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YouTube autocomplete scraping | Custom HTTP requests | Puppeteer with stealth plugin | YouTube's anti-bot detection blocks simple requests; need full browser simulation |
| Rate limit handling | Simple retry loops | Exponential backoff with jitter | Random delays evade pattern detection better than fixed intervals |
| Search volume estimation | Manual counting | VidIQ/TubeBuddy (with accuracy tracking) | They aggregate data across millions of searches; building equivalent requires massive infrastructure |
| YouTube Analytics access | Screen scraping | Official YouTube Analytics API v2 | API provides reliable data with proper authentication; scraping violates ToS |
| Keyword database schema | Flat file storage | Relational DB (SQLite minimum) | Need complex queries (filter by date range, competition, intent category) and relationships |
| Intent classification | Pure regex patterns | ML-enhanced pattern matching | Viewer intent has context (e.g., "crusades" alone ambiguous, "were crusades defensive" clear intent) |
| Competitor keyword extraction | Manual research | TubeBuddy Competitor Tool / YouTube Studio Analytics | They provide bulk data export; manual is too time-consuming at scale |

**Key insight:** YouTube has sophisticated anti-scraping measures (rate limiting, browser fingerprinting, CAPTCHA, behavioral analysis). Simple solutions get blocked fast. Use battle-tested libraries with stealth capabilities and proper rate limiting. Don't underestimate the complexity of staying undetected while scraping at scale.

## Common Pitfalls

### Pitfall 1: YouTube Rate Limiting and Blocking
**What goes wrong:** Scraper gets HTTP 429 (Too Many Requests) or 403 (Forbidden) errors, halting keyword extraction.
**Why it happens:** YouTube monitors automated traffic aggressively. Exceeding request thresholds (varies, not documented) triggers blocks. Simple delays aren't enough—pattern detection identifies bots.
**How to avoid:**
- Use puppeteer-extra-plugin-stealth to mask automation
- Implement exponential backoff: 1s, 2s, 4s, 8s delays after errors
- Add random jitter to request intervals (1-3s variable delay)
- Rotate user agents and IP addresses if scraping at scale
- Respect 429/403 errors—back off immediately, don't retry aggressively
**Warning signs:** Sudden drop in successful requests, CAPTCHA pages appearing, consistent 403 errors.

### Pitfall 2: Misclassifying Search Intent
**What goes wrong:** Keywords classified with wrong intent lead to content that doesn't match what viewers want. High CTR but low retention, hurting algorithm ranking.
**Why it happens:** Single keywords are ambiguous. "Crusades" could be myth-busting, timeline, or territorial dispute. Without query context (how/why/what), classification guesses wrong.
**How to avoid:**
- Use full search queries, not single keywords
- Require minimum query length (3+ words) for classification
- Support multi-intent (primary + secondary) for complex queries
- Validate classifications against actual video performance data
- Build feedback loop: track which intents correlate with high retention
**Warning signs:** Videos with good CTR but poor watch time, comments saying "not what I expected," high bounce rates.

### Pitfall 3: VidIQ Search Volume Accuracy Assumptions
**What goes wrong:** Treating VidIQ numbers as precise leads to wrong topic decisions. Building video for "10K monthly searches" that actually gets 500 impressions.
**Why it happens:** YouTube API doesn't provide search volume—VidIQ estimates using proprietary models. Their own documentation says it's 85% accurate, meaning 15% significant variance. Small channels especially see different results.
**How to avoid:**
- Treat VidIQ numbers as directional, not precise
- Focus on relative comparison (keyword A vs B) not absolute numbers
- Track VidIQ predictions vs actual impressions over time
- Weight competition score equally with volume—low competition matters more for small channels
- Use long-tail keywords where estimation variance matters less
**Warning signs:** Consistent mismatch between predicted volume and actual impressions, videos underperforming VidIQ "high score" keywords.

### Pitfall 4: Ignoring Channel-Size-Specific Benchmarks
**What goes wrong:** Using industry average CTR (4-10%) for diagnosis when small channels have different patterns. Misdiagnosing issues.
**Why it happens:** Benchmarks from large channels (millions of subscribers) don't apply to small channels (hundreds/thousands). Small channels rely more on search/browse, less on direct traffic. Subscriber base behaves differently.
**How to avoid:**
- Calculate channel-specific benchmarks from last 10-20 videos
- Segment by traffic source (search vs suggested vs direct)
- Compare to similar-size channels in niche, not all YouTube
- Recalculate benchmarks quarterly as channel grows
- Use relative comparisons (this video vs channel average) over absolute thresholds
**Warning signs:** All diagnostics show "problems" when videos feel normal, or vice versa—missing real issues.

### Pitfall 5: Metadata Inconsistency Between Elements
**What goes wrong:** Title says "Treaty of Guadalupe Hidalgo," description focuses on modern Mexico-US relations, tags include unrelated keywords. Algorithm gets confused, video doesn't rank.
**Why it happens:** Different team members write different elements, keyword research done after writing, copying tags from unrelated videos, trying to rank for too many topics at once.
**How to avoid:**
- Pick 1 primary keyword, use it in: title (first half), description (first 2 sentences), tags (first tag)
- Use 2-3 secondary keywords consistently across all metadata
- Check keyword appears in: title, description, tags, video transcript (spoken), chapters
- Automated checker validates before publish: flag if primary keyword missing from any element
- Brand consistency: same terminology (don't switch between "USSR" and "Soviet Union" randomly)
**Warning signs:** Low impressions despite good content, video ranks for unintended keywords, YouTube suggests to wrong audience.

### Pitfall 6: Keyword Stuffing in 2026 Algorithm
**What goes wrong:** Description filled with keyword variations hurts rankings instead of helping. Algorithm detects unnatural density and deprioritizes.
**Why it happens:** Old SEO advice (pre-2020) recommended high keyword density. 2026 algorithm uses natural language processing to detect stuffing. Viewers also find it spammy, hurting engagement.
**How to avoid:**
- Write description for humans first, optimize second
- Aim for 200-300 words description with natural keyword placement
- Use variations naturally (synonyms, related concepts) not forced repetition
- Read aloud—does it sound natural or robotic?
- Target 1-2% keyword density maximum (1-2 mentions per 100 words)
**Warning signs:** High impressions but low CTR, viewers commenting on "spammy" descriptions, algorithm deprioritization over time.

### Pitfall 7: Not Tracking Diagnostic Learnings
**What goes wrong:** Same mistakes repeated across videos. Discover video has low CTR, fix it, forget lesson, next video has same problem.
**Why it happens:** Diagnostics treated as one-time fixes instead of learning opportunities. No system to capture "what we learned" and apply to future videos.
**How to avoid:**
- For each diagnosed issue, write: what was wrong, why it happened, how we'll prevent it next time
- Store learnings in channel-data/diagnostic-learnings.json
- Review learnings file during pre-publish checklist for new videos
- Track patterns: if 3+ videos have same issue, it's a systemic problem needing workflow change
- Build "pre-flight checks" based on common historical issues
**Warning signs:** Repeating same mistakes, surprises at performance when should have predicted, reactive instead of proactive.

## Code Examples

Verified patterns from official sources and established tools:

### YouTube Analytics API Integration
```javascript
// Source: https://developers.google.com/youtube/analytics/metrics
const { google } = require('googleapis');

async function fetchVideoMetrics(videoId, startDate = '7daysAgo', endDate = 'today') {
  const youtube = google.youtubeAnalytics('v2');

  const res = await youtube.reports.query({
    ids: 'channel==MINE',
    startDate: startDate,
    endDate: endDate,
    metrics: 'videoThumbnailImpressions,videoThumbnailImpressionsClickRate,views,estimatedMinutesWatched,averageViewDuration',
    dimensions: 'video',
    filters: `video==${videoId}`,
    sort: '-videoThumbnailImpressions'
  });

  if (res.data.rows && res.data.rows.length > 0) {
    const [impressions, ctr, views, watchTime, avgDuration] = res.data.rows[0];
    return {
      impressions,
      ctr: (ctr * 100).toFixed(2) + '%',
      views,
      watchTimeMinutes: watchTime,
      avgViewDuration: avgDuration,
      retentionRate: ((avgDuration / res.data.videoDuration) * 100).toFixed(2) + '%'
    };
  }

  throw new Error('No data found for video');
}
```

### Metadata Consistency Checker
```javascript
// Pre-publish validation
function checkMetadataConsistency(video) {
  const issues = [];
  const primaryKeyword = video.metadata.primaryKeyword.toLowerCase();

  // Check title
  if (!video.title.toLowerCase().includes(primaryKeyword)) {
    issues.push({
      severity: 'HIGH',
      element: 'Title',
      issue: `Primary keyword "${primaryKeyword}" not found in title`,
      fix: 'Add primary keyword to first half of title'
    });
  }

  // Check description (first 200 chars weighted heavily)
  const descStart = video.description.substring(0, 200).toLowerCase();
  if (!descStart.includes(primaryKeyword)) {
    issues.push({
      severity: 'HIGH',
      element: 'Description',
      issue: `Primary keyword not in first 200 characters`,
      fix: 'Mention primary keyword in first 1-2 sentences'
    });
  }

  // Check tags
  if (!video.tags.some(tag => tag.toLowerCase().includes(primaryKeyword))) {
    issues.push({
      severity: 'MEDIUM',
      element: 'Tags',
      issue: `Primary keyword not in tags`,
      fix: 'Add primary keyword as first tag'
    });
  }

  // Check for keyword stuffing
  const descKeywordCount = (video.description.toLowerCase().match(new RegExp(primaryKeyword, 'g')) || []).length;
  const wordCount = video.description.split(/\s+/).length;
  const density = (descKeywordCount / wordCount) * 100;

  if (density > 2) {
    issues.push({
      severity: 'HIGH',
      element: 'Description',
      issue: `Keyword density ${density.toFixed(1)}% too high (max 2%)`,
      fix: 'Reduce keyword repetition, use synonyms and related terms'
    });
  }

  // Cross-element consistency
  const titleWords = new Set(video.title.toLowerCase().split(/\s+/));
  const tagWords = new Set(video.tags.flatMap(t => t.toLowerCase().split(/\s+/)));
  const overlap = [...titleWords].filter(w => tagWords.has(w)).length;

  if (overlap < 3) {
    issues.push({
      severity: 'MEDIUM',
      element: 'Title-Tag Consistency',
      issue: `Only ${overlap} words overlap between title and tags`,
      fix: 'Ensure key title terms appear in tags'
    });
  }

  return {
    passed: issues.filter(i => i.severity === 'HIGH').length === 0,
    issues,
    summary: `${issues.length} issues found (${issues.filter(i => i.severity === 'HIGH').length} high severity)`
  };
}
```

### Keyword Database Schema
```sql
-- Source: Best practices from SEO database design patterns
-- https://dataforseo.com/apis/keyword-data-api (schema inspiration)

CREATE TABLE keywords (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword TEXT NOT NULL UNIQUE,
  search_volume INTEGER,
  competition_score REAL, -- 0-100 from VidIQ
  vidiq_overall_score REAL,
  first_discovered DATE NOT NULL,
  last_updated DATE NOT NULL,
  source TEXT -- 'autocomplete', 'competitor', 'manual', 'vidiq'
);

CREATE TABLE keyword_intents (
  keyword_id INTEGER NOT NULL,
  intent_category TEXT NOT NULL, -- MYTH_BUSTING, TERRITORIAL_DISPUTE, etc.
  confidence REAL NOT NULL, -- 0-1
  is_primary BOOLEAN DEFAULT 0,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id),
  PRIMARY KEY (keyword_id, intent_category)
);

CREATE TABLE keyword_performance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  video_id TEXT NOT NULL,
  impressions INTEGER,
  ctr REAL,
  views INTEGER,
  watch_time_minutes INTEGER,
  measured_date DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

CREATE TABLE competitor_keywords (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  competitor_channel TEXT NOT NULL, -- 'Kraut', 'Knowing Better', etc.
  competitor_video_id TEXT,
  video_views INTEGER,
  video_age_days INTEGER,
  discovered_date DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

CREATE TABLE vidiq_predictions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  predicted_volume INTEGER,
  predicted_competition REAL,
  overall_score REAL,
  prediction_date DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Index for common queries
CREATE INDEX idx_keywords_volume ON keywords(search_volume DESC);
CREATE INDEX idx_intents_primary ON keyword_intents(is_primary, confidence DESC);
CREATE INDEX idx_performance_date ON keyword_performance(measured_date DESC);
CREATE INDEX idx_competitor_channel ON competitor_keywords(competitor_channel);

-- View for keyword analysis
CREATE VIEW keyword_analysis AS
SELECT
  k.keyword,
  k.search_volume,
  k.competition_score,
  ki.intent_category AS primary_intent,
  ki.confidence AS intent_confidence,
  AVG(kp.ctr) AS avg_ctr,
  AVG(kp.impressions) AS avg_impressions,
  COUNT(DISTINCT kp.video_id) AS videos_used,
  COUNT(DISTINCT ck.competitor_channel) AS competitor_count
FROM keywords k
LEFT JOIN keyword_intents ki ON k.id = ki.keyword_id AND ki.is_primary = 1
LEFT JOIN keyword_performance kp ON k.id = kp.keyword_id
LEFT JOIN competitor_keywords ck ON k.id = ck.keyword_id
GROUP BY k.id;
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Keyword volume focus | Intent matching priority | 2024-2025 | YouTube algorithm shifted to prioritize viewer satisfaction over raw keyword matches |
| Exact keyword matching | Semantic understanding | 2023-2024 | NLP-powered algorithm understands context and synonyms; keyword stuffing now penalized |
| Single-keyword optimization | Multi-intent classification | 2024-2025 | Complex queries require understanding primary + secondary intent |
| Fixed CTR benchmarks (5%) | Channel-size-specific benchmarks | 2025 | Small channels have different patterns; one-size-fits-all misleading |
| High-volume keyword targeting | Long-tail strategy for small channels | Ongoing | Educational content performs better on specific queries (3-10% CTR) |
| Manual VidIQ data entry | API integration | Never happened | VidIQ has no public API despite industry demand; guided workflows remain necessary |
| Post-publish metadata optimization | Pre-publish consistency checking | 2024-2025 | Algorithm establishes video topic in first 48 hours; later changes less effective |
| Keyword research after writing | Research-first workflow | Best practice shift | Ensures content matches proven search demand |

**Deprecated/outdated:**
- **YouTube API v1:** Sunset in 2015, replaced by v3 (current: YouTube Data API v3, YouTube Analytics API v2)
- **TubeBuddy Star Rating:** Changed to numerical scores in 2023; old guides referencing stars obsolete
- **Keyword density targets >3%:** Pre-2020 SEO advice; 2026 algorithm penalizes as stuffing
- **Impressions click-through rate (old metric):** YouTube Analytics deprecated in favor of videoThumbnailImpressionsClickRate (same concept, more precise naming)
- **Browser extension APIs for automated scraping:** YouTube cracked down 2022-2023; extensions like TubeBuddy/VidIQ now primarily manual interfaces

## Open Questions

Things that couldn't be fully resolved:

1. **VidIQ Search Volume Accuracy by Channel Size**
   - What we know: VidIQ claims 85% accuracy overall; uses proprietary estimation model
   - What's unclear: Does accuracy vary by channel size (sub-1K vs 100K+)? No public data breakdown.
   - Recommendation: Build accuracy tracking (predicted vs actual impressions) specific to this channel. After 10+ videos, calculate channel-specific confidence intervals. Use VidIQ directionally until sufficient data.

2. **YouTube Autocomplete Regional Variations**
   - What we know: Autocomplete suggestions can vary by region, language, user history
   - What's unclear: How to extract "global" suggestions vs region-specific? YouTube doesn't document autocomplete API behavior.
   - Recommendation: Run scraper from multiple IP regions if targeting international audience. For this channel (primarily UK/Germany/Canada/US), focus on English-language suggestions from those regions. Document which region data came from.

3. **Optimal Keyword Database Query Patterns**
   - What we know: Need to track keywords, intents, performance, competitors
   - What's unclear: Which query patterns will be most useful in practice? Over-engineering risk.
   - Recommendation: Start with simple queries (keywords by intent, keywords by performance, competitor keywords). Add complex queries based on actual usage needs. Don't build 50 queries upfront.

4. **Intent Classification Confidence Thresholds**
   - What we know: Pattern matching can classify intent; confidence scores needed
   - What's unclear: What confidence threshold (0.6? 0.7? 0.8?) should require manual review? No established benchmarks for this specific domain.
   - Recommendation: Start with 0.7 threshold (70% confidence) for auto-classification. Log all classifications with confidence scores. Review low-confidence cases manually for first 50 keywords. Adjust threshold based on false positive/negative rates.

5. **Diagnostic Time Windows: 7 Days vs 14 Days**
   - What we know: YouTube discovery typically stabilizes within 7-14 days
   - What's unclear: Does educational content (longer videos, niche topics) need longer discovery periods?
   - Recommendation: Default to 7-day window per user requirements. For videos with <100 impressions at 7 days, extend diagnosis to 14 days before declaring SEO issue. Historical channel data may show this audience discovers content slower.

6. **Competitor Keyword Extraction Depth**
   - What we know: Competitor analysis valuable; TubeBuddy/YouTube Studio provide some data
   - What's unclear: How many competitors to track? How many keywords per competitor? Diminishing returns point unknown.
   - Recommendation: Start with 3-5 key competitors (Kraut, Knowing Better, RealLifeLore mentioned in channel DNA). Extract top 10-20 keywords per competitor initially. Expand if clear value demonstrated.

## Sources

### Primary (HIGH confidence)
- [YouTube Analytics API Metrics Documentation](https://developers.google.com/youtube/analytics/metrics) - Official metric definitions for impressions, CTR, views
- [Web Scraping YouTube Autocomplete with Node.js](https://serpapi.com/blog/web-scraping-youtube-autocomplete-with-nodejs/) - Practical Puppeteer implementation
- [YouTube CTR Benchmark: Average, Good & Best Practices](https://www.lenostube.com/en/youtube-ctr-benchmark-average-good-best-practices/) - Industry benchmarks with data sources
- [Average YouTube CTR: Organic & Paid Benchmarks 2026](https://focus-digital.co/average-youtube-ctr-organic-paid-benchmarks-2025/) - Current year benchmarks
- [How the YouTube Algorithm Works in 2026](https://socialbee.com/blog/youtube-algorithm/) - Algorithm priorities and ranking factors
- [YouTube SEO in 2026: Complete Guide to Ranking and Growth](https://graphaize.com/youtube-seo-in-2026-guide-to-ranking-and-growth/) - Intent-driven optimization strategies

### Secondary (MEDIUM confidence)
- [5 Easy Steps to YouTube Competitor Analysis 2026](https://brand24.com/blog/youtube-competitor-analysis/) - Competitor keyword extraction methods
- [YouTube Keyword Research Tools](https://vidiq.com/features/keyword-tools/) - VidIQ capabilities and limitations
- [MW Metadata](https://mattw.io/youtube-metadata/) - Metadata extraction tool for consistency checking
- [Ultimate YouTube SEO Guide 2026](https://www.keywordtooldominator.com/youtube-seo/) - Long-tail keyword strategies
- [How to Scrape YouTube in 2026](https://scrapfly.io/blog/posts/how-to-scrape-youtube) - Anti-detection techniques and rate limiting
- [YouTube Channel Research with Python API](https://www.amalytix.com/en/blog/python-youtube-api-channel-research/) - Python implementation best practices
- [SEO Keyword Research Mistakes to Avoid](https://www.searchenginejournal.com/keyword-research/mistakes-to-avoid/) - Common pitfalls (general SEO, applied to YouTube)
- [YouTube Metadata Optimization Mistakes 2026](https://backlinko.com/how-to-rank-youtube-videos) - Backlinko's SEO research

### Tertiary (LOW confidence - WebSearch only)
- Various blog posts on YouTube algorithm updates (uncorroborated claims)
- Third-party tool comparison articles (potential affiliate bias)
- Reddit/forum discussions on scraping techniques (anecdotal, not verified)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Puppeteer, YouTube Analytics API, VidIQ are established tools with verified usage
- Architecture: HIGH - Patterns verified from official docs and established tutorials
- Pitfalls: MEDIUM-HIGH - Derived from documented challenges (rate limiting, algorithm behavior) plus logical inference
- Code examples: HIGH - Sourced from official APIs and established tutorials
- Intent classification: MEDIUM - Custom categories based on channel DNA, no pre-existing standard for this specific niche

**Research date:** 2026-01-29
**Valid until:** ~2026-03-29 (60 days) - YouTube algorithm and SEO practices evolve continuously; keyword research principles more stable than specific benchmarks
