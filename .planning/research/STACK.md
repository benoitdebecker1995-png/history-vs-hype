# Technology Stack: Script Quality, Discovery & NotebookLM Integration

**Project:** History vs Hype v1.2
**Researched:** 2026-01-27
**Context:** Subsequent milestone — adding to existing YouTube Analytics API integration

---

## Executive Summary

**Current Stack (DO NOT change):**
- Python 3.x (~5,000 lines in tools/youtube-analytics/)
- YouTube Analytics API v2 + YouTube Data API v3
- OAuth2 authentication with token refresh
- Markdown-based workflows
- Claude Code slash commands

**New Stack Recommendations:**

| Component | Technology | Why | Integration Point |
|-----------|------------|-----|-------------------|
| **Script Quality** | Claude 4.5 API + textstat + py-readability-metrics | Best LLM + proven readability scoring | New Python module |
| **Discovery/SEO** | YouTube autocomplete endpoint + pytrends + YouTube Data API | Undocumented but stable endpoint + free Trends access | New Python module |
| **NotebookLM** | Manual workflow (NO API) | Enterprise API in alpha, not production-ready | Workflow optimization only |
| **Text Analysis** | spaCy + textstat | Industry standard NLP + comprehensive readability | Script quality module |

**Critical Finding: NotebookLM has NO production-ready API.** Focus on workflow optimization, not technical integration.

---

## 1. Script Quality Improvements

### Problem Statement

Current pain: AI-generated scripts need heavy revision (unnatural flow, repetitions, academic phrasing that doesn't work spoken).

### Recommended Stack

#### 1.1 Claude API (Anthropic)

**Purpose:** Script generation with optimized prompts

**Models & Pricing (2026):**

| Model | Input Cost | Output Cost | Context Window | Use Case |
|-------|-----------|-------------|----------------|----------|
| Claude Sonnet 4.5 | $3/M tokens | $15/M tokens | 200K standard | Script generation |
| Claude Sonnet 4.5 (>200K) | $6/M tokens | $22.50/M tokens | Up to 1M tokens | Large research context |
| Claude Haiku 4.5 | $1/M tokens | $5/M tokens | 200K | Quick revisions |

**Key Features for This Use Case:**
- **200K context window** - Entire style guide + examples + research in one prompt
- **Prompt caching** - Reduces costs by 90% and latency by 85% for repeated style rules
- **Prompt improver** - Console tool for optimizing generation prompts
- **Chain-of-thought** - Explicit reasoning before generation improves quality

**Implementation Strategy:**
1. Use prompt caching for style guide (`.claude/REFERENCE/STYLE-GUIDE.md` stays in cache)
2. Feed research from NotebookLM as context
3. Apply best practices from Anthropic's prompt engineering guide
4. Estimated cost: $0.50-$2.00 per script (assuming 20K input, 3K output with caching)

**Confidence:** HIGH - Official API, well-documented, already using Claude Code

**Sources:**
- [Anthropic Claude API Pricing 2026](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration)
- [Prompt Caching Guide](https://www.aifreeapi.com/en/posts/claude-api-prompt-caching-guide)
- [Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Context Windows Documentation](https://platform.claude.com/docs/en/build-with-claude/context-windows)

#### 1.2 Readability Analysis

**Purpose:** Objective metrics for script quality (sentence length, complexity, readability level)

**Library:** `py-readability-metrics` + `textstat`

**Installation:**
```bash
pip install py-readability-metrics textstat
```

**Metrics to Track:**

| Metric | Library | Target Range | Why |
|--------|---------|--------------|-----|
| Flesch Reading Ease | py-readability-metrics | 60-70 | Conversational but not simplistic |
| Flesch-Kincaid Grade | py-readability-metrics | 8-10 | High school level (YouTube standard) |
| Average sentence length | textstat | 12-18 words | Spoken delivery sweet spot |
| Syllables per word | textstat | 1.5-2.0 | Natural speech patterns |
| SMOG Index | py-readability-metrics | 10-12 | Comprehension difficulty |

**Usage:**
```python
from readability import Readability

r = Readability(script_text)
flesch = r.flesch_kincaid()
fog = r.gunning_fog()
# Flag sections outside target ranges
```

**Output:** JSON report with:
- Overall readability score
- Per-section analysis
- Sentences flagged for revision (too long, too complex)
- Comparison to previous scripts

**Confidence:** HIGH - Established libraries with clear documentation

**Sources:**
- [py-readability-metrics GitHub](https://github.com/cdimascio/py-readability-metrics)
- [textstat PyPI](https://pypi.org/project/textstat/)
- [Readability Index NLP Guide](https://www.geeksforgeeks.org/python/readability-index-pythonnlp/)

#### 1.3 Repetition Detection

**Purpose:** Flag word/phrase repetition that sounds robotic

**Library:** `spaCy` + custom analysis

**Installation:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

**Detection Strategy:**

1. **N-gram repetition** - Detect repeated 3-5 word phrases within 500-word windows
2. **Semantic similarity** - Use spaCy's word vectors to detect "saying the same thing differently"
3. **Filler word frequency** - Track "essentially," "basically," "kind of" usage

**Implementation:**
```python
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def detect_repetition(text, window=500):
    doc = nlp(text)

    # N-gram repetition
    trigrams = [doc[i:i+3].text for i in range(len(doc)-2)]
    repeated = [ng for ng, count in Counter(trigrams).items() if count > 2]

    # Filler words
    fillers = ["essentially", "basically", "kind of", "sort of"]
    filler_count = sum(token.text.lower() in fillers for token in doc)

    return {
        "repeated_phrases": repeated,
        "filler_count": filler_count,
        "filler_budget": 5  # Target threshold
    }
```

**Confidence:** HIGH - spaCy is industry standard, custom logic straightforward

**Sources:**
- [spaCy Documentation](https://spacy.io/)
- [TextDescriptives for spaCy](https://arxiv.org/pdf/2301.02057)
- [Text Similarity Methods](https://www.newscatcherapi.com/blog-posts/ultimate-guide-to-text-similarity-with-python)

#### 1.4 Natural Language Generation Evaluation (Optional)

**Purpose:** Benchmark script quality against reference scripts

**Libraries:** ROUGE and BLEU metrics via `evaluate` or `nltk`

**Installation:**
```bash
pip install evaluate rouge-score nltk
```

**Use Case:**
- Compare generated script to "gold standard" previous scripts
- Measure how similar the style is to approved voice patterns
- Track improvement over time

**Implementation:**
```python
from evaluate import load

rouge = load('rouge')
results = rouge.compute(
    predictions=[generated_script],
    references=[reference_script]
)
# Higher ROUGE-L = closer to reference style
```

**Recommendation:** OPTIONAL - Use only if you want quantitative style drift tracking. Subjective review may be sufficient.

**Confidence:** MEDIUM - Metrics exist but correlation with "good script" is unclear

**Sources:**
- [BLEU and ROUGE Explained](https://doc.superannotate.com/docs/guide-bleu-rouge)
- [NLG Evaluation Metrics Guide](https://plainenglish.io/blog/evaluating-nlp-models-a-comprehensive-guide-to-rouge-bleu-meteor-and-bertscore-metrics-d0f1b1)
- [LLM Evaluation Metrics](https://medium.com/data-science-in-your-pocket/llm-evaluation-metrics-explained-af14f26536d2)

---

## 2. Discovery & SEO Optimization

### Problem Statement

Current pain: Topic selection is manual guesswork. No data on search volume, keyword difficulty, or trending topics.

### Recommended Stack

#### 2.1 YouTube Autocomplete (Undocumented Endpoint)

**Purpose:** Discover what viewers are actually searching for

**Endpoint:** `https://clients1.google.com/complete/search`

**Status:** Undocumented but stable. Used by community for years. YouTube doesn't provide official autocomplete API.

**Parameters:**
- `client=youtube`
- `hl=en` (language)
- `ds=yt` (YouTube dataset)
- `q=[search term]`

**Response Format:** JSON array of autocomplete suggestions

**Implementation:**
```python
import requests

def get_youtube_suggestions(query):
    url = "https://clients1.google.com/complete/search"
    params = {
        "client": "youtube",
        "hl": "en",
        "ds": "yt",
        "q": query
    }
    response = requests.get(url, params=params)
    # Parse JSON response
    suggestions = response.json()[1]  # Second element contains suggestions
    return [s[0] for s in suggestions]

# Example: get_youtube_suggestions("somaliland")
# Returns: ["somaliland documentary", "somaliland recognition", ...]
```

**Use Cases:**
- Topic discovery: "What are people searching for about [topic]?"
- Title optimization: Test title variants to see if they appear in autocomplete
- Related topics: Discover adjacent search terms

**Rate Limits:** None documented. Use respectful rate limiting (1 req/sec).

**Risk Assessment:** LOW - Endpoint has been stable for years, used by multiple tools (Apify, BOTSTER, keyword tools). Not officially supported but not blocked.

**Confidence:** HIGH - Multiple tools rely on this, community-validated approach

**Sources:**
- [Hacking YouTube Suggest API](https://dev.to/adrienshen/hacking-together-your-own-youtube-suggest-api-c0o)
- [YouTube Autocomplete Scraper - Apify](https://apify.com/scraper-mind/youtube-autocomplete-scraper)
- [How to Scrape YouTube Autocomplete](https://blog.apify.com/how-to-scrape-youtube-search-keywords/)

#### 2.2 Google Trends (pytrends)

**Purpose:** Understand search volume trends over time

**Library:** `pytrends` (unofficial but widely used)

**Installation:**
```bash
pip install pytrends
```

**Status:** Google Trends has NO official API. `pytrends` is a pseudo-API that scrapes Google Trends. It breaks occasionally when Google changes backend, but the community maintains it.

**Implementation:**
```python
from pytrends.request import TrendReq

pytrend = TrendReq(hl='en-US', tz=360)

# Compare topics
pytrend.build_payload(
    kw_list=['somaliland', 'taiwan', 'western sahara'],
    timeframe='today 12-m'
)
data = pytrend.interest_over_time()

# Related queries
related = pytrend.related_queries()
```

**Use Cases:**
- Validate topic interest over time
- Compare multiple topic ideas
- Identify trending moments (e.g., news events that spike searches)
- Discover related search terms

**Limitations:**
- Breaks when Google changes backend (community fixes within days)
- Incomplete data (not full search volume numbers)
- Rate limited (use delays between requests)

**Alternative (Commercial):** Glimpse API ($$$) - More reliable, full data access, used by Fortune 50. Overkill for solo creator.

**Recommendation:** Use pytrends for validation, not as single source of truth. Cross-reference with YouTube autocomplete.

**Confidence:** MEDIUM - Works but fragile, requires maintenance

**Sources:**
- [pytrends PyPI](https://pypi.org/project/pytrends/)
- [pytrends GitHub](https://github.com/GeneralMills/pytrends)
- [Pytrends Alternatives 2026](https://meetglimpse.com/software-guides/pytrends-alternatives/)
- [How to Scrape Google Trends 2026](https://brightdata.com/blog/web-data/how-to-scrape-google-trends)

#### 2.3 YouTube Data API v3 (Already Integrated)

**Purpose:** Get video performance data for keyword research

**Current Status:** Already using YouTube Data API v3 for analytics

**Additional Use Cases for Discovery:**

1. **Search endpoint** - Query YouTube for existing videos on topic
2. **Video statistics** - Check view counts, engagement on competitor videos
3. **Channel analysis** - Study successful channels in niche

**New Usage:**
```python
# Use existing auth from tools/youtube-analytics/auth.py

def search_youtube_videos(query, max_results=10):
    """Find existing videos on topic"""
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        order="viewCount"
    )
    return request.execute()

def get_video_stats(video_id):
    """Check competitor performance"""
    request = youtube.videos().list(
        part="statistics,snippet",
        id=video_id
    )
    return request.execute()
```

**Use Cases:**
- Competitive analysis: "Who else covered this topic?"
- Gap analysis: "What angle hasn't been covered?"
- Performance benchmarks: "What view counts are realistic?"

**Quota:** 10,000 units/day (already allocated). Search costs 100 units per query.

**Confidence:** HIGH - Already integrated, official API

**Sources:**
- [YouTube Data API Search Documentation](https://developers.google.com/youtube/v3/docs/search/list)
- [YouTube API Complete Guide 2026](https://getlate.dev/blog/youtube-api)

#### 2.4 Third-Party APIs (Keyword Research)

**Available Options:**

| Service | Features | Cost | Recommendation |
|---------|----------|------|----------------|
| YouTube Keyword Research API (Zyla) | Search volume, competition, difficulty | Paid (pricing varies) | NOT RECOMMENDED - adds complexity |
| YouTube Trending Topics API (Zyla) | Real-time trending topics | Paid | NOT RECOMMENDED - news-first approach violates channel DNA |
| TubeBuddy Keyword Explorer | Search data, competition | $9-49/mo | Manual tool, not API |
| VidIQ | Topic suggestions, optimization | Pro plan | NO API AVAILABLE |

**Recommendation:** Skip third-party APIs. Combine free tools (YouTube autocomplete + pytrends + YouTube Data API) for sufficient keyword research.

**Why Skip Paid APIs:**
- Adds cost for marginal benefit
- Overkill for solo creator (1-2 videos/month)
- Free tools provide 80% of value
- VidIQ manual workflow already works

**Confidence:** HIGH - Paid APIs not necessary for this use case

**Sources:**
- [YouTube Keyword Research API - Zyla](https://zylalabs.com/api-marketplace/data/youtube+keyword+research+api/2490)
- [VidIQ Features 2026](https://www.getapp.com/marketing-software/a/vidiq/)
- [TubeBuddy Keyword Explorer](https://www.tubebuddy.com/tools/keyword-explorer/)

#### 2.5 Metadata Optimization

**Purpose:** Optimize titles, descriptions, tags based on data

**Current Approach:** Manual + VidIQ suggestions

**New Approach:** Data-driven validation

**Workflow:**
1. Generate title variants (existing: `/publish --titles`)
2. **NEW:** Check each variant against YouTube autocomplete
3. **NEW:** Check search trends in pytrends
4. **NEW:** Search YouTube API for existing video performance
5. Select variant with best discovery potential

**No New APIs Needed** - Compose existing tools

**Implementation:**
```python
def validate_title(title_variants):
    """Score title variants for discoverability"""
    scores = {}

    for title in title_variants:
        # Extract key phrase
        key_phrase = extract_key_phrase(title)

        # Check autocomplete
        suggestions = get_youtube_suggestions(key_phrase)
        autocomplete_score = 1 if key_phrase in suggestions else 0

        # Check trends
        trends_data = get_trends(key_phrase)
        trend_score = calculate_trend_score(trends_data)

        # Check existing videos
        existing = search_youtube_videos(key_phrase)
        competition_score = calculate_competition(existing)

        scores[title] = {
            "autocomplete": autocomplete_score,
            "trend": trend_score,
            "competition": competition_score,
            "total": autocomplete_score + trend_score + competition_score
        }

    return scores
```

**Confidence:** HIGH - Clear composition of existing tools

---

## 3. NotebookLM Integration

### Critical Finding: NO Production-Ready API

**Status as of 2026-01-27:**

NotebookLM Enterprise API exists but is in **alpha** with significant limitations:
- **v1alpha** version (pre-production)
- Limited to notebook creation and management
- Podcast generation API separate (also alpha)
- Requires Google Cloud project + NotebookLM Enterprise subscription
- Enterprise-focused (VPC, HIPAA compliance)
- Not designed for solo creator workflow

**Official API Limitations:**
- Cannot programmatically query notebooks for answers
- Cannot automate research extraction
- Cannot pull citations/page numbers via API
- Core use case (interactive research) not exposed in API

**Unofficial Alternatives:**

| Tool | Type | Status | Recommendation |
|------|------|--------|----------------|
| notebooklm-py (teng-lin) | Python library | Community-maintained | LOW confidence - reverse engineering |
| nblm-rs (K-dash) | Rust/Python SDK | Unofficial | LOW confidence - unofficial client |
| Apify NotebookLM API | Scraper/exporter | Commercial service | NOT NEEDED - export feature |
| AutoContent API | Third-party proxy | Commercial | NOT NEEDED - adds complexity |

**Confidence:** HIGH - Multiple sources confirm API limitations

**Sources:**
- [NotebookLM Enterprise API Documentation](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks)
- [Does NotebookLM Have an API?](https://autocontentapi.com/blog/does-notebooklm-have-an-api)
- [How to Access NotebookLM Via API - Google Forum](https://discuss.ai.google.dev/t/how-to-access-notebooklm-via-api/5084)
- [NotebookLM API Launch 2026](https://blockchain.news/ainews/notebooklm-launches-direct-notebook-access-boosting-ai-productivity-tools-in-2026)

### Recommended Approach: Workflow Optimization (NOT Technical Integration)

Since NotebookLM has no usable API for the core workflow, focus on **process improvements** instead:

#### 3.1 Structured Export Workflow

**Current Pain:** Copy-paste from NotebookLM to VERIFIED-RESEARCH.md is manual

**Solution:** Standardized templates for NotebookLM prompts

**Implementation:**
1. Create prompt library in `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` (already exists)
2. Add structured output requests to prompts:
   ```
   Please provide findings in this format:

   CLAIM: [factual claim]
   SOURCE: [Author, Title, Page X]
   QUOTE: "[exact quote]"
   CONFIDENCE: [HIGH/MEDIUM/LOW]
   ```
3. NotebookLM "Save to Notes" feature → structured notes → easier copy-paste

**Benefit:** Reduces manual reformatting, maintains verification standards

**Confidence:** HIGH - Process improvement, no API needed

#### 3.2 NotebookLM Best Practices Documentation

**Current State:** Workflow documented in CLAUDE.md

**Enhancement:** Expand NotebookLM guidance in `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`

**Add:**
- Naming conventions for sources (`[P1] Primary-Source.pdf`, `[A1] Author-Book.pdf`)
- Notebook organization strategy (Act 1, Act 2, Act 3 notebooks)
- Citation extraction workflow (click citation → copy page number → save to notes)
- Customized Audio Overview prompts (use "Customize" feature for targeted discussions)
- Interactive Mode usage (clarify confusing points with podcast hosts)

**Benefit:** Faster research, fewer errors, better citations

**Confidence:** HIGH - Leveraging existing NotebookLM features

#### 3.3 Research-to-Script Pipeline

**Current Workflow:**
1. NotebookLM research (manual)
2. Copy-paste to VERIFIED-RESEARCH.md
3. Claude generates script from VERIFIED-RESEARCH.md
4. Manual revision cycle

**Optimized Workflow:**
1. NotebookLM research with structured prompts
2. Export notes to VERIFIED-RESEARCH.md (still manual, but faster)
3. **NEW:** Claude API script generation with full context (200K tokens)
4. **NEW:** Automated quality checks (readability, repetition)
5. Targeted revision based on metrics

**Key Improvement:** Replace Claude web interface with Claude API for script generation
- Full style guide + research in context (200K tokens)
- Prompt caching reduces cost/latency
- Repeatable, versioned prompts

**Benefit:** Better first drafts, fewer revision cycles, lower cognitive load

**Confidence:** HIGH - Practical process improvement

---

## 4. Integration Architecture

### Module Structure

```
tools/
├── youtube-analytics/       # EXISTING - v1.1
│   ├── auth.py
│   ├── metrics.py
│   ├── analyze.py
│   └── patterns.py
├── script-quality/          # NEW - v1.2
│   ├── __init__.py
│   ├── generate.py          # Claude API script generation
│   ├── readability.py       # Readability metrics
│   ├── repetition.py        # Repetition detection
│   └── quality_report.py    # Combined quality report
└── discovery/               # NEW - v1.2
    ├── __init__.py
    ├── autocomplete.py      # YouTube autocomplete
    ├── trends.py            # Google Trends (pytrends)
    ├── youtube_search.py    # YouTube Data API search
    └── keyword_report.py    # Combined keyword research report
```

### Slash Command Integration

**New Commands:**

| Command | Module | Function |
|---------|--------|----------|
| `/script --generate` | script-quality/generate.py | Generate script via Claude API |
| `/script --quality` | script-quality/quality_report.py | Readability + repetition analysis |
| `/research --keywords [topic]` | discovery/keyword_report.py | Autocomplete + trends + competition |
| `/publish --validate-title` | discovery/keyword_report.py | Score title variants for discovery |

**Existing Commands Enhanced:**

| Command | Enhancement | Module |
|---------|-------------|--------|
| `/script` | Add quality metrics after generation | script-quality/ |
| `/publish --titles` | Add discovery scoring | discovery/ |

### Data Flow

```
1. Topic Research Flow
   User: /research --keywords "somaliland independence"
   ↓
   discovery/keyword_report.py
   ├→ autocomplete.py → YouTube suggestions
   ├→ trends.py → Google Trends data
   └→ youtube_search.py → Competitor analysis
   ↓
   Output: KEYWORD-RESEARCH.md in project folder

2. Script Generation Flow
   User: /script --generate 1-somaliland-2025
   ↓
   script-quality/generate.py
   ├→ Read VERIFIED-RESEARCH.md
   ├→ Read .claude/REFERENCE/STYLE-GUIDE.md
   ├→ Claude API with prompt caching
   ↓
   Output: SCRIPT.md
   ↓
   Auto-run: quality_report.py
   ├→ readability.py → Readability metrics
   └→ repetition.py → Repetition detection
   ↓
   Output: SCRIPT-QUALITY-REPORT.md

3. Title Optimization Flow
   User: /publish --validate-title 1-somaliland-2025
   ↓
   discovery/keyword_report.py
   ├→ Extract title variants from YOUTUBE-METADATA.md
   ├→ Score each via autocomplete + trends + search
   ↓
   Output: Title recommendation with scores
```

---

## 5. Dependencies & Installation

### Python Requirements (NEW)

```python
# requirements-v1.2.txt

# Script Quality
anthropic>=0.18.0           # Claude API
py-readability-metrics>=1.4.5
textstat>=0.7.3
spacy>=3.7.0
en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Discovery/SEO
pytrends>=4.9.2
requests>=2.31.0

# Evaluation (OPTIONAL)
evaluate>=0.4.1
rouge-score>=0.1.2
nltk>=3.8.1

# EXISTING (v1.1) - DO NOT REMOVE
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.100.0
```

### Installation Script

```bash
# Install new dependencies
pip install anthropic py-readability-metrics textstat spacy pytrends

# Download spaCy English model
python -m spacy download en_core_web_sm

# Optional: NLG evaluation
pip install evaluate rouge-score nltk
```

### Environment Variables (NEW)

```bash
# .env file

# EXISTING - YouTube API
YOUTUBE_API_KEY=...
YOUTUBE_CLIENT_SECRET=...

# NEW - Claude API
ANTHROPIC_API_KEY=sk-ant-...    # Get from console.anthropic.com
```

---

## 6. Cost Estimates

### Monthly Operating Costs (Solo Creator, 2 videos/month)

| Service | Usage | Cost | Notes |
|---------|-------|------|-------|
| **Claude API (Script Generation)** | 2 scripts/month, 20K input + 3K output each | $1.20/month | With prompt caching: ~$0.50/month |
| **YouTube Data API** | 10,000 units/day quota | FREE | Already allocated |
| **YouTube Autocomplete** | ~50 queries/month | FREE | Undocumented but free |
| **Google Trends (pytrends)** | ~20 queries/month | FREE | Unofficial but free |
| **spaCy, textstat** | Local processing | FREE | Open source |

**Total New Costs: $0.50-$1.20/month**

**One-Time Costs:** $0 (all open source or free tier)

### Cost Optimization Strategies

1. **Prompt caching:** Reuse style guide in cache (saves 90% on repeated context)
2. **Batch processing:** Generate multiple title variants in one API call
3. **Local processing:** All analysis (readability, repetition) runs locally, no API costs

---

## 7. Risk Assessment

### Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| YouTube autocomplete endpoint changes | MEDIUM | Monitor community tools, have fallback to manual research |
| pytrends breaks (Google backend change) | MEDIUM | Wait for community fix (usually <1 week), use autocomplete as backup |
| Claude API costs exceed budget | LOW | Prompt caching + monitoring, costs are predictable |
| spaCy model accuracy issues | LOW | Thresholds are tunable, human review remains |
| Rate limiting on undocumented APIs | LOW | Implement respectful delays (1 req/sec) |

### Integration Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Slash command complexity increases | MEDIUM | Clear help text, flag-based organization |
| Multiple data sources conflict | LOW | Clear precedence: autocomplete > trends > manual |
| Script quality metrics don't correlate with success | MEDIUM | Track metrics vs. performance, adjust thresholds |

### Workflow Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| NotebookLM API becomes available mid-project | LOW | Current manual workflow works, API would be enhancement |
| Over-reliance on automation reduces editorial judgment | MEDIUM | Metrics inform, don't decide. Human review remains |
| Tool maintenance burden | LOW | Minimize dependencies, use stable libraries |

---

## 8. What NOT to Add (and Why)

### 8.1 VidIQ API Integration

**Status:** NO API AVAILABLE

VidIQ does not provide a public API. Community tools exist (VidIQ-Pack on GitHub) but rely on scraping/exports, not official API access.

**Recommendation:** Continue manual VidIQ workflow. Not worth reverse engineering.

**Sources:**
- [VidIQ Features Review 2026](https://www.getapp.com/marketing-software/a/vidiq/)
- [VidIQ Help Center](https://support.vidiq.com/en)

### 8.2 Paid Keyword Research APIs

**Services:** YouTube Keyword Research API (Zyla), YouTube Trending Topics API (Zyla), TubeBuddy API

**Why Skip:**
- Cost: $20-100/month for minimal marginal benefit
- Overkill: Solo creator (1-2 videos/month) doesn't need enterprise-level keyword tools
- Free tools sufficient: YouTube autocomplete + pytrends + YouTube Data API cover 80% of use case
- Validation: Current VidIQ Pro + manual research already works

**Recommendation:** Use free tools. Paid APIs are for agencies/high-volume creators.

### 8.3 NotebookLM Unofficial APIs

**Services:** notebooklm-py, nblm-rs, AutoContent API, Apify NotebookLM API

**Why Skip:**
- **Reverse engineering risk:** Unofficial clients may break when Google changes backend
- **Limited functionality:** Export-only APIs don't solve core workflow (interactive research)
- **Added complexity:** Another service to maintain and debug
- **Enterprise API in alpha:** Official API coming but not production-ready

**Recommendation:** Wait for official NotebookLM API to reach production. Focus on workflow optimization (structured prompts, export templates).

### 8.4 Video Editing Automation

**Out of scope:** CLAUDE.md explicitly excludes "Video editing automation"

**Recommendation:** Keep focus on pre-production (research, scripts) and post-production analysis (analytics). Editing stays manual in DaVinci Resolve.

### 8.5 Predictive Analytics

**Out of scope:** CLAUDE.md explicitly excludes "Predictive analytics — focus on learning, not prediction"

**Recommendation:** Analyze what happened (patterns), don't predict what will happen. Discovery tools suggest topics, not guarantee success.

---

## 9. Alternatives Considered

### Alternative: Open-Source NotebookLM Clone

**Option:** Use [Open Notebook](https://github.com/lfnovo/open-notebook) - open source NotebookLM implementation

**Pros:**
- Self-hosted, full control
- Can integrate with custom workflows
- No Google Cloud dependency

**Cons:**
- Requires deployment and maintenance
- Feature parity with NotebookLM unclear
- User already has NotebookLM Enterprise subscription
- Migration effort (move existing notebooks)

**Decision:** NOT RECOMMENDED - NotebookLM already works, manual workflow is acceptable

### Alternative: Glimpse API for Google Trends

**Option:** Use Glimpse (commercial Google Trends API) instead of pytrends

**Pros:**
- More reliable (doesn't break when Google changes)
- Complete data (not sampled)
- Used by Fortune 50

**Cons:**
- Cost: $$$$ (enterprise pricing)
- Overkill for solo creator
- pytrends works 95% of the time

**Decision:** NOT RECOMMENDED - Free pytrends sufficient, paid API doesn't justify cost for 1-2 videos/month

### Alternative: OpenAI GPT-4 for Script Generation

**Option:** Use OpenAI GPT-4/GPT-4 Turbo instead of Claude

**Pros:**
- Slightly lower cost ($2.50/$10 per M tokens for GPT-4 Turbo)
- Wider adoption, more community resources

**Cons:**
- Smaller context window (128K vs Claude's 200K)
- Claude's prompt engineering is already established in project
- Claude Code already in use, API integration simpler
- Anthropic's constitutional AI approach better for nuanced historical content

**Decision:** NOT RECOMMENDED - Stick with Claude for consistency and larger context

---

## 10. Roadmap Integration Points

### How This Stack Enables Roadmap Phases

| Roadmap Phase | Stack Component | How It Helps |
|---------------|----------------|--------------|
| **Phase 1: Topic Research** | Discovery module (autocomplete + trends + search) | Data-driven topic validation |
| **Phase 2: Script Generation** | Claude API + style guide caching | Better first drafts, less revision |
| **Phase 3: Script Quality Check** | Readability + repetition analysis | Objective quality metrics, flag issues early |
| **Phase 4: Title Optimization** | Discovery module (autocomplete scoring) | Test title variants for discoverability |
| **Phase 5: NotebookLM Workflow** | Structured prompts + export templates | Faster research extraction |

### Dependencies Between Components

```
Discovery module
├→ Informs topic selection (Phase 1)
├→ Validates title variants (Phase 4)
└→ Used independently of script-quality module

Script Quality module
├→ Depends on: VERIFIED-RESEARCH.md (from NotebookLM)
├→ Depends on: .claude/REFERENCE/STYLE-GUIDE.md
├→ Outputs: SCRIPT.md + SCRIPT-QUALITY-REPORT.md
└→ Used independently of discovery module

NotebookLM workflow
├→ Feeds into: VERIFIED-RESEARCH.md
├→ Used before: Script Quality module
└→ Independent of API integration (manual workflow optimized)
```

### Build Order Recommendation

1. **Phase 1:** Discovery module (simple, no dependencies)
2. **Phase 2:** Script quality analysis (readability + repetition, no Claude API yet)
3. **Phase 3:** Claude API script generation (most complex, depends on quality metrics)
4. **Phase 4:** NotebookLM workflow optimization (documentation only, no code)
5. **Phase 5:** Integration testing and slash command updates

**Rationale:** Build from simple to complex, validate each component independently before integration.

---

## 11. Success Metrics

### How to Measure If This Stack Works

| Goal | Metric | Target | Measurement |
|------|--------|--------|-------------|
| Better first drafts | Revision cycles per script | 1-2 (down from 3-4) | Manual tracking |
| Script quality | Flesch Reading Ease score | 60-70 (conversational) | Automated |
| Repetition reduction | Filler word count | <5 per script | Automated |
| Topic validation | Topics with >10K monthly searches | 50%+ of topics | Discovery module |
| Title optimization | Titles appearing in autocomplete | 70%+ of published videos | Discovery module |
| NotebookLM efficiency | Time from research to VERIFIED-RESEARCH.md | <2 hours (down from 3-4) | Manual tracking |

### What "Good" Looks Like

**Script Quality:**
- Script reads naturally on first take (no stumbles)
- Readability scores in target ranges (60-70 FRE, 8-10 grade level)
- Fewer than 3 repeated phrases per script
- User says "This sounds like me" without heavy revision

**Discovery:**
- Topic validation data available before research begins
- Title variants scored objectively (not just gut feeling)
- Keyword research takes <30 minutes (down from 1-2 hours)
- 1-2 "hidden gem" topics discovered per month (low competition, decent volume)

**NotebookLM Workflow:**
- Structured notes copy-paste directly to VERIFIED-RESEARCH.md
- Fewer "I need to go back and find the page number" moments
- Research completeness checkable (all claims have sources)

---

## 12. Confidence Assessment

| Area | Confidence Level | Reason |
|------|------------------|--------|
| **Claude API** | HIGH | Official API, well-documented, already using Claude |
| **Readability metrics** | HIGH | Established libraries (py-readability-metrics, textstat) |
| **Repetition detection** | HIGH | spaCy is industry standard, custom logic straightforward |
| **YouTube autocomplete** | HIGH | Undocumented but stable, community-validated for years |
| **Google Trends (pytrends)** | MEDIUM | Works but fragile, requires maintenance when Google changes |
| **NotebookLM API** | HIGH (that it doesn't exist) | Multiple sources confirm alpha status, not production-ready |
| **NLG evaluation (ROUGE/BLEU)** | MEDIUM | Metrics exist but correlation with "good script" unclear |
| **Cost estimates** | HIGH | Transparent pricing, calculable from usage |
| **Integration complexity** | MEDIUM | New modules, but clear separation of concerns |

---

## 13. Open Questions for User

Before implementing this stack, clarify:

1. **Claude API budget:** Is $0.50-$1.20/month acceptable? (Estimate based on 2 scripts/month)
2. **NotebookLM workflow:** Are you open to structured prompt templates, or prefer current freeform approach?
3. **Quality metrics:** Which readability metrics matter most? (Sentence length? Grade level? Syllables per word?)
4. **Discovery scope:** Topic validation only, or also title/keyword optimization?
5. **Automation level:** Generate scripts fully automated (Claude API), or keep manual Claude Code interaction?
6. **Risk tolerance:** Comfortable using undocumented YouTube autocomplete endpoint? (Stable but not officially supported)

---

## Sources

### NotebookLM API Research
- [NotebookLM Enterprise API Documentation](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks)
- [Does NotebookLM Have an API?](https://autocontentapi.com/blog/does-notebooklm-have-an-api)
- [How to Access NotebookLM Via API](https://discuss.ai.google.dev/t/how-to-access-notebooklm-via-api/5084)
- [NotebookLM API Launch 2026](https://blockchain.news/ainews/notebooklm-launches-direct-notebook-access-boosting-ai-productivity-tools-in-2026)
- [NotebookLM Evolution 2023-2026](https://medium.com/@jimmisound/the-cognitive-engine-a-comprehensive-analysis-of-notebooklms-evolution-2023-2026-90b7a7c2df36)

### YouTube Discovery APIs
- [YouTube Data API Search](https://developers.google.com/youtube/v3/docs/search/list)
- [Hacking YouTube Suggest API](https://dev.to/adrienshen/hacking-together-your-own-youtube-suggest-api-c0o)
- [YouTube Autocomplete Scraper - Apify](https://apify.com/scraper-mind/youtube-autocomplete-scraper)
- [How to Scrape YouTube Autocomplete](https://blog.apify.com/how-to-scrape-youtube-search-keywords/)
- [YouTube API Complete Guide 2026](https://getlate.dev/blog/youtube-api)

### Google Trends
- [pytrends PyPI](https://pypi.org/project/pytrends/)
- [pytrends GitHub](https://github.com/GeneralMills/pytrends)
- [Pytrends Alternatives 2026](https://meetglimpse.com/software-guides/pytrends-alternatives/)
- [How to Scrape Google Trends 2026](https://brightdata.com/blog/web-data/how-to-scrape-google-trends)

### Text Analysis & Readability
- [py-readability-metrics GitHub](https://github.com/cdimascio/py-readability-metrics)
- [textstat PyPI](https://pypi.org/project/textstat/)
- [Readability Index NLP Guide](https://www.geeksforgeeks.org/python/readability-index-pythonnlp/)
- [spaCy Documentation](https://spacy.io/)
- [TextDescriptives for spaCy](https://arxiv.org/pdf/2301.02057)
- [Text Similarity Methods](https://www.newscatcherapi.com/blog-posts/ultimate-guide-to-text-similarity-with-python)

### NLG Evaluation Metrics
- [BLEU and ROUGE Explained](https://doc.superannotate.com/docs/guide-bleu-rouge)
- [NLG Evaluation Metrics Guide](https://plainenglish.io/blog/evaluating-nlp-models-a-comprehensive-guide-to-rouge-bleu-meteor-and-bertscore-metrics-d0f1b1)
- [LLM Evaluation Metrics](https://medium.com/data-science-in-your-pocket/llm-evaluation-metrics-explained-af14f26536d2)

### Claude API
- [Anthropic Claude API Pricing 2026](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration)
- [Prompt Caching Guide](https://www.aifreeapi.com/en/posts/claude-api-prompt-caching-guide)
- [Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Context Windows Documentation](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)

### Third-Party Tools
- [VidIQ Features Review 2026](https://www.getapp.com/marketing-software/a/vidiq/)
- [YouTube Keyword Research API - Zyla](https://zylalabs.com/api-marketplace/data/youtube+keyword+research+api/2490)
- [TubeBuddy Keyword Explorer](https://www.tubebuddy.com/tools/keyword-explorer/)
- [YouTube Metadata Optimization Guide](https://air.io/en/youtube-hacks/youtube-metadata-your-gateway-to-high-rankings-and-global-views)

---

*Research complete. Ready for roadmap creation.*
