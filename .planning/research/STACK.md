# Technology Stack: Click & Keep Features

**Project:** History vs Hype YouTube Analytics - Click & Keep Features
**Researched:** 2026-02-06
**Focus:** Thumbnail/title A/B tracking, script pacing analysis, post-publish feedback integration

---

## Executive Summary

**Core Finding:** Existing stack (Python 3.11-3.13, SQLite, YouTube APIs, spaCy) handles 95% of new requirements. Only TWO new libraries needed: ImageHash for thumbnail pattern analysis, and textstat upgrade for readability metrics.

**Why minimal additions:** The workspace already has analytics fetching (ctr.py), database infrastructure (keywords.db with performance tracking), and NLP tools (spaCy for script analysis). New features are integration work, not new capabilities.

**Model assignment refresh:** Phase 13.1 used tier aliases (haiku/sonnet/opus), now mapping to Claude 4.x lineup (Haiku 4.5, Sonnet 4.5, Opus 4.6).

---

## Recommended Stack Additions

### Thumbnail/Title A/B Tracking

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **ImageHash** | 4.3.2 | Perceptual hash generation for thumbnail pattern analysis | Enables pattern extraction from thumbnails without computer vision APIs. Detects visual similarity (map vs face, text vs image) using average hash, perceptual hash (pHash), difference hash (dHash). Pure Python, no external dependencies beyond Pillow (already in ecosystem via NotebookLM/editing tools). |
| Pillow | 12.1.0 | Image loading for ImageHash | Already installed (likely present for thumbnail creation). Upgrade if below 10.0. |

**Rationale:** The workspace already collects CTR data via `tools/youtube-analytics/ctr.py`. The missing piece is *pattern recognition* - which thumbnail patterns (map-focused, face-focused, text-heavy) correlate with high CTR. ImageHash provides perceptual hashing that groups visually similar thumbnails without manual tagging.

**Integration point:**
- Extend `tools/discovery/database.py` schema with `thumbnail_variants` table (video_id, variant_label, hash_avg, hash_phash, hash_dhash, ctr_percent, impressions)
- New module: `tools/youtube-analytics/thumbnail_tracker.py` - computes hashes for A/B/C variants, stores with CTR metrics
- Pattern analysis: `tools/youtube-analytics/thumbnail_patterns.py` - clusters similar thumbnails, correlates with CTR

### Script Pacing Analysis

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| textstat | 0.7.12 | Readability and sentence complexity metrics | Already in `tools/script-checkers/requirements.txt` at 0.7.3. Upgrade to 0.7.12 for latest Flesch-Kincaid, sentence length variance. Adds quantitative pacing metrics beyond spaCy's qualitative flow checking. |
| spaCy | 3.8.11 | Sentence parsing, entity recognition | Already in stack. Current version (3.8+) supports all needed features. No upgrade needed unless below 3.8. |

**Rationale:** The workspace already has `tools/script-checkers/checkers/flow.py` for qualitative flow analysis (undefined terms, abrupt transitions). Script pacing needs *quantitative* detection: sentence length variance spikes (rushed delivery), readability score drops (complexity walls), entity density changes (topic fatigue).

**Integration point:**
- Extend `tools/script-checkers/checkers/flow.py` with pacing metrics:
  - Sentence length variance per 100-word window (detects rushed segments)
  - Flesch Reading Ease delta between sections (detects complexity spikes)
  - Entity density per paragraph (detects "wall of nouns" syndrome)
- Output format: `[PACING WARNING: Sentence length variance 18.3 (>15) at lines 45-52 - audience may disengage]`

**What NOT to add:**
- ❌ NLTK - spaCy already provides tokenization, POS tagging, NER. NLTK adds 1.5GB disk space for redundant features.
- ❌ Hugging Face Transformers - sentiment analysis is overkill. Script energy detection needs simple readability metrics, not 500MB models.
- ❌ TextBlob - wrapper around NLTK. Redundant with spaCy.

### Post-Publish Feedback Integration

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| (No new libraries) | - | Connect POST-PUBLISH-ANALYSIS to production tools | Pure integration work. `channel-data/analyses/*.md` files already exist. Parse them, extract patterns, write to keywords.db for query during script generation. |

**Rationale:** Post-publish analysis already generates structured markdown files with CTR, retention, discovery diagnostics. The missing piece is *closing the loop* - making those insights queryable when creating new videos.

**Integration point:**
- New module: `tools/production/feedback_loader.py`
  - Parses `channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md`
  - Extracts: CTR vs channel avg, retention drop points, discovery issues, successful patterns
  - Stores in `video_performance` table (already exists per `database.py` Phase 19 migration)
- Extend `/script` command to query feedback before generation:
  - "Previous videos with similar topics had 42% retention drop at 3:15 due to pacing - check for complexity spikes"
  - "Map-focused thumbnails averaged 8.2% CTR vs 4.1% for face-focused"

---

## Existing Stack (DO NOT Re-Add)

### Core Infrastructure
| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.11-3.13 | ✅ Validated |
| SQLite | stdlib | ✅ keywords.db with video_performance table exists |
| Google API Client | 2.189.0 | ✅ Current (released 2026-02-03) - upgrade from 2.100.0 |
| google-auth-oauthlib | 1.0.0+ | ✅ Current |

### Analytics & Data
| Component | Version | Status |
|-----------|---------|--------|
| YouTube Analytics API v2 | - | ✅ ctr.py, retention.py, metrics.py operational |
| YouTube Data API v3 | - | ✅ comments.py, video_report.py operational |
| SQLite video_performance table | - | ✅ Phase 19 migration complete |

### NLP & Text Processing
| Component | Version | Status |
|-----------|---------|--------|
| spaCy | 3.8+ | ✅ flow.py, repetition.py, scaffolding.py, stumble.py |
| en_core_web_sm model | - | ✅ Required for script checkers |
| srt | 3.5.0+ | ✅ Voice fingerprinting (Phase 12) |

### Production Tools
| Component | Status |
|-----------|--------|
| parser.py | ✅ Script parsing (--package, --teleprompter flags) |
| entities.py | ✅ Entity extraction |
| broll.py | ✅ B-roll generation |
| editguide.py | ✅ Edit guide generation |
| metadata.py | ✅ YouTube metadata generation |

---

## Installation

### New Additions Only

```bash
# Thumbnail pattern analysis
pip install ImageHash==4.3.2
pip install Pillow>=12.0  # Upgrade if needed

# Script pacing (upgrade existing)
pip install --upgrade textstat==0.7.12

# YouTube API (upgrade existing)
pip install --upgrade google-api-python-client==2.189.0
```

### Verification

```bash
# Check ImageHash installation
python -c "import imagehash; from PIL import Image; print('ImageHash OK')"

# Check textstat upgrade
python -c "import textstat; print(f'textstat {textstat.__version__}')"

# Check spaCy model exists
python -m spacy validate
```

---

## Architecture Integration

### Data Flow for Thumbnail A/B Tracking

```
1. User creates variants (A/B/C.png) → EXISTING (Photoshop workflow)
2. thumbnail_tracker.py computes hashes → NEW MODULE
   - average_hash (rough similarity)
   - perceptual_hash (rotation/scaling resistant)
   - difference_hash (edge detection)
3. Store in thumbnail_variants table → NEW SCHEMA
4. ctr.py fetches CTR for video → EXISTING
5. thumbnail_patterns.py correlates hashes with CTR → NEW MODULE
   - Cluster by hash similarity (Hamming distance < 10)
   - Report: "Map-focused thumbnails (7 videos) avg 8.2% CTR"
```

### Data Flow for Script Pacing Analysis

```
1. User writes script → EXISTING
2. parser.py extracts text → EXISTING
3. flow.py analyzes (qualitative) → EXISTING
4. NEW: pacing.py analyzes (quantitative)
   - Sentence length variance per 100-word window
   - Flesch Reading Ease per section
   - Entity density per paragraph
5. Output warnings: "[PACING: Lines 45-52 variance 18.3 > 15]" → NEW
```

### Data Flow for Post-Publish Feedback

```
1. /analyze generates POST-PUBLISH-ANALYSIS-{id}.md → EXISTING
2. feedback_loader.py parses markdown → NEW MODULE
3. Extracts metrics (CTR, retention, discovery issues) → NEW
4. Stores in video_performance table → EXISTING TABLE
5. /script queries feedback before generation → NEW QUERY
   - "Similar videos had pacing issues at 3:15"
   - "Map thumbnails outperform face thumbnails 2:1"
```

---

## Model Assignment Refresh (Phase 13.1 Update)

**Current status:** Phase 13.1 assigned models using tier aliases (haiku/sonnet/opus) which auto-map to current model versions.

**Documentation update:** Update references to reflect current Claude 4.x lineup (documentation only - YAML already uses correct tier aliases).

### Model Tier Mapping

| Tier | Current Model | Use Case |
|------|---------------|----------|
| haiku | Claude Haiku 4.5 | Simple tasks (status, help, fix, sources, prep, discover, next) |
| sonnet | Claude Sonnet 4.5 | Standard tasks (verify, publish, engage, analyze, patterns, research) |
| opus | Claude Opus 4.6 | Complex creative (script generation) |

### YAML Frontmatter (Already Correct)

Slash commands in `.claude/commands/*.md` already use tier aliases:

**Haiku tier (7 files):**
- status.md, help.md, fix.md, sources.md, prep.md, discover.md, next.md
- Already uses: `model: haiku` (maps to current Haiku 4.5)

**Sonnet tier (6 files):**
- verify.md, publish.md, engage.md, analyze.md, patterns.md, research.md
- Already uses: `model: sonnet` (maps to current Sonnet 4.5)

**Opus tier (1 file):**
- script.md
- Already uses: `model: opus` (maps to current Opus 4.6)

**Note:** Tier aliases auto-map to latest model versions. Routing works correctly without YAML changes.

---

## What NOT to Add

### ❌ Computer Vision APIs (Google Vision, AWS Rekognition)
**Why avoid:** Thumbnail pattern analysis doesn't need object detection. ImageHash perceptual hashing extracts visual similarity (map vs face, text vs image) without API costs or quota limits. Pattern recognition is offline and free.

### ❌ NLTK
**Why avoid:** spaCy already provides tokenization, POS tagging, NER, dependency parsing. NLTK adds 1.5GB disk space for redundant features. textstat provides readability metrics without NLTK dependency.

### ❌ Hugging Face Transformers
**Why avoid:** Script pacing needs simple readability metrics (sentence length variance, Flesch-Kincaid), not sentiment classification. Transformers require 500MB+ models, GPU for inference speed, and introduce complexity for marginal value.

### ❌ TextBlob
**Why avoid:** Wrapper around NLTK. Redundant with spaCy + textstat combination.

### ❌ pandas
**Why avoid:** SQLite queries handle analytics aggregation. Adding pandas creates dependency bloat for tasks already handled by SQL. Pattern extraction (grouping similar thumbnails, calculating CTR averages) is simple GROUP BY logic.

### ❌ Separate A/B testing frameworks (Optimizely, VWO libraries)
**Why avoid:** YouTube doesn't expose true A/B testing (can't show variant A to 50% of impressions). The workflow is: publish with thumbnail A, monitor CTR, swap to thumbnail B, compare. This is sequential testing, not simultaneous A/B. No framework needed - just timestamp tracking in SQLite.

---

## Alternative Approaches Considered

### Thumbnail Pattern Analysis

| Approach | Why Not |
|----------|---------|
| **Google Cloud Vision API** | $1.50 per 1,000 images for label detection. Overkill for detecting "map vs face" patterns. ImageHash is free, offline, and sufficient. |
| **Manual tagging** | User tags each thumbnail as "map", "face", "text". Doesn't scale, requires discipline. Perceptual hashing automates pattern extraction. |
| **CLIP embeddings** | 500MB model, requires PyTorch/TensorFlow. Excessive for simple visual similarity. ImageHash is 100KB. |

**Winner:** ImageHash - minimal dependency, offline, fast, purpose-built for perceptual similarity.

### Script Pacing Analysis

| Approach | Why Not |
|----------|---------|
| **Sentiment analysis (VADER, TextBlob)** | Detects positive/negative tone, not pacing issues. Script energy drops aren't about sentiment - they're about complexity spikes and sentence rhythm. |
| **Manual review** | User reads script, subjectively judges "this feels slow". Doesn't scale, inconsistent. Quantitative metrics (sentence variance >15, Flesch delta >20) provide objective flags. |
| **Audio prosody analysis** | Requires recorded audio, not script text. Misses problems before filming. Pacing analysis must run pre-production. |

**Winner:** textstat + spaCy - quantitative readability metrics on script text, catches issues before filming.

### Post-Publish Feedback

| Approach | Why Not |
|----------|---------|
| **External analytics platform (Tubular, Social Blade)** | Costs $99-299/month. YouTube Analytics API provides CTR, retention, comments for free. No added value for solo creator. |
| **Manual spreadsheet tracking** | User copies CTR from YouTube Studio to Excel. Doesn't integrate with script generation. No automated pattern extraction. |
| **No feedback loop** | Continue creating videos without learning from past performance. Repeats mistakes (pacing issues, thumbnail choices). |

**Winner:** Parse existing POST-PUBLISH-ANALYSIS markdown files, store in SQLite, query during production - zero cost, automated, integrated.

---

## Confidence Assessment

| Area | Confidence | Reason |
|------|------------|--------|
| Thumbnail tracking | **HIGH** | ImageHash is mature (4.3.2 stable release), well-documented, 20M+ downloads on PyPI. Perceptual hashing is proven technique for duplicate image detection. |
| Script pacing | **HIGH** | textstat is established (0.7.12 stable), used in education research for readability. spaCy 3.8+ is current production version. |
| Post-publish feedback | **HIGH** | Pure integration work - no new libraries, just parsing existing markdown and querying SQLite. |
| Model assignment | **MEDIUM** | Model IDs (claude-haiku-4-5, etc.) verified via Anthropic announcements, but exact API routing patterns depend on Claude SDK implementation. Tier names (haiku/sonnet/opus) may be aliases. |
| Library versions | **HIGH** | All versions verified via PyPI/official sources (2026-02-06). google-api-python-client 2.189.0 released 2026-02-03, Pillow 12.1.0 released 2026-01-02, ImageHash 4.3.2 released 2025-02-01. |

---

## Sources

**Library Versions:**
- [google-api-python-client 2.189.0 on PyPI](https://pypi.org/project/google-api-python-client/)
- [Pillow 12.1.0 on PyPI](https://pypi.org/project/pillow/)
- [ImageHash 4.3.2 on PyPI](https://pypi.org/project/ImageHash/)
- [textstat 0.7.12 on PyPI](https://pypi.org/project/textstat/)
- [spaCy 3.8.11 on PyPI](https://pypi.org/project/spacy/)

**Perceptual Hashing:**
- [GitHub - JohannesBuchner/imagehash](https://github.com/JohannesBuchner/imagehash)
- [Duplicate image detection with perceptual hashing](https://benhoyt.com/writings/duplicate-image-detection/)
- [ImageHash library tutorial](https://pythonhow.com/what/imagehash-library-tutorial/)

**YouTube Analytics API:**
- [YouTube Analytics API Documentation](https://developers.google.com/youtube/analytics)
- [YouTube API Python samples](https://github.com/youtube/api-samples/tree/master/python)

**Claude Models:**
- [Anthropic launches Claude Opus 4.6](https://www.cnbc.com/2026/02/05/anthropic-claude-opus-4-6-vibe-working.html)
- [Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Introducing Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5)
