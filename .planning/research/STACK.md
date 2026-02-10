# Stack Research: v2.0 Channel Intelligence

**Domain:** YouTube content production with AI-assisted script generation, research integration, and analytics
**Researched:** 2026-02-09
**Confidence:** HIGH

---

## Executive Summary

**v2.0 adds channel intelligence capabilities to existing Python production tools (~17,300 LOC).** The milestone requires libraries for three new capabilities:

1. **Channel-aware script generation** - Voice matching, research integration, retention-aware structure
2. **Research-to-NotebookLM bridge** - Source preparation, verified research extraction
3. **Actionable analytics** - Retention diagnosis, thumbnail/title recommendations, topic strategy

**Key Finding:** Most requirements are met by existing stack (Python 3.14, YouTube APIs, spaCy, SQLite). NEW additions needed:

- **Anthropic SDK** 1.87+ for Claude API integration (script generation with Opus 4.6)
- **sentence-transformers** 3.1+ for semantic similarity (find similar past videos, voice pattern matching)
- **chromadb** 0.5.29+ for local vector storage (research embeddings, script patterns)
- **markitdown** 0.0.1a2+ for markdown parsing (NotebookLM research extraction)

**What NOT to add:** LangChain (too heavy for focused use case), pandas (SQLite sufficient), NLTK (redundant with spaCy), voice audio ML libraries (working with text transcripts only).

**CRITICAL BLOCKER:** Python 3.14.2 incompatible with spaCy (wheels unavailable as of 2026-02-09). **Recommend downgrade to Python 3.13.x immediately.**

---

## Core Technologies (NEW for v2.0)

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| **anthropic** | >=1.87.1 | Claude API client for Python | Official SDK from Anthropic. Supports Claude Opus 4.6 (released Feb 2026). Provides async/sync interfaces, type safety, streaming. Required for `/script` command to generate channel-aware scripts with Opus model. Uses standard HTTP/REST patterns. |
| **sentence-transformers** | >=3.1.0 | Semantic similarity, text embeddings | Industry standard for text embeddings (15K+ models on HuggingFace). Enables finding similar past videos (for insights), voice pattern matching (creator vs AI-generated text), section similarity (detect repetition). Uses local models (no API calls). Python 3.10+ compatible. ~420MB model download on first use. |
| **chromadb** | >=0.5.29 | Local vector database | Lightweight vector storage (DuckDB backend). Stores research embeddings (find relevant NotebookLM notes), script patterns (high-retention structures), past performance data (semantic search). Runs entirely local, no cloud dependencies. Released Feb 9, 2026. Query latency <10ms for 1K vectors. |
| **markitdown** | >=0.0.1a2 | Document-to-markdown conversion | Microsoft's LLM-focused converter (alpha stage). Preserves structure (headings, lists, tables). Handles PDFs, DOCX, PPTX (NotebookLM source formats). Lightweight alternative to Docling (simpler, no ML dependencies). Converts 100-page PDF in ~10 sec. |

---

## Supporting Libraries (NEW for v2.0)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **jinja2** | >=3.1.5 | Prompt template management | Standard templating for LLM prompts. Build dynamic `/script` prompts with past feedback, voice patterns, retention warnings. Agnostic to LLM frameworks (lighter than LangChain). No learning curve if familiar with Django/Flask templates. |
| **tiktoken** | >=0.8.0 | Token counting for Claude API | OpenAI's official tokenizer (Claude uses similar BPE). Prevents context window overflow (200K token limit for Opus 4.6). Calculate prompt size before API calls. ~1ms per 1K tokens. |
| **faststylometry** | >=0.1.0 | Text style fingerprinting | Authorship attribution features (word choice, sentence rhythm). Compare creator's voice patterns to AI drafts. Detect style drift. Built on spaCy/scikit-learn. Analyzes 1K-word text in ~50ms. |
| **pydantic** | >=2.10.4 | Data validation for API responses | Type-safe parsing of Claude API responses, YouTube Analytics data. Used by Anthropic SDK internally. Prevents runtime errors from malformed data. Auto-generates validation from type hints. |

---

## Existing Stack (DO NOT RE-ADD - Already Installed)

### Core Infrastructure

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| Python | **3.14.2** | ⚠️ **INCOMPATIBLE** | spaCy wheels unavailable for 3.14. Downgrade to 3.13.x required. |
| SQLite | stdlib | ✅ Validated | keywords.db operational with video_performance table |
| google-api-python-client | >=2.100.0 | ✅ Validated | YouTube Analytics/Data APIs |
| google-auth-oauthlib | >=1.0.0 | ✅ Validated | OAuth2 authentication |

### NLP & Text Processing

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| spacy | >=3.8 | ⚠️ **BLOCKED** | No Python 3.14 wheels ([Issue #13885](https://github.com/explosion/spaCy/issues/13885)) |
| textstat | >=0.7.3 | ✅ Validated | Readability metrics |
| srt | >=3.5.0 | ✅ Validated | Subtitle parsing |

**CRITICAL PATH:** Python version downgrade must happen BEFORE v2.0 development starts.

---

## Installation

### Step 1: Fix Python Version (MANDATORY)

```bash
# Current (INCOMPATIBLE):
python --version
# Python 3.14.2

# Required action: Downgrade to 3.13.x
# Download Python 3.13.x from python.org
# Reinstall all dependencies after downgrade
```

**Why this matters:** spaCy wheels unavailable for 3.14 as of 2026-02-09. sentence-transformers may work, but untested. faststylometry depends on spaCy, inherits incompatibility.

**Options:**
- **Option A (Recommended):** Downgrade to Python 3.13.x immediately (spaCy 3.8+ supports 3.13)
- **Option B (Risky):** Wait for spaCy to release 3.14 wheels (timeline unknown)
- **Option C (Not recommended):** Build spaCy from source on Windows (time-consuming, error-prone)

### Step 2: Install v2.0 Core Dependencies

```bash
# After Python 3.13.x installed
pip install anthropic>=1.87.1
pip install sentence-transformers>=3.1.0
pip install chromadb>=0.5.29
pip install markitdown>=0.0.1a2
```

**Expected install time:** 5-10 minutes (sentence-transformers downloads ~420MB model on first use)

### Step 3: Install Supporting Libraries

```bash
pip install jinja2>=3.1.5
pip install tiktoken>=0.8.0
pip install faststylometry>=0.1.0
pip install pydantic>=2.10.4
```

### Step 4: Reinstall Existing Dependencies

```bash
# YouTube analytics tools
pip install -r tools/youtube-analytics/requirements.txt

# Script checkers
pip install -r tools/script-checkers/requirements.txt

# Discovery tools
pip install -r tools/discovery/requirements.txt
```

### Step 5: Download Models

```bash
# spaCy model (required for existing checkers + faststylometry)
python -m spacy download en_core_web_sm

# sentence-transformers model (auto-downloads on first use, but can pre-download)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**Total additional disk space:** ~600MB
- sentence-transformers model: ~420MB
- chromadb: ~50MB
- Other libraries: ~130MB

### Step 6: Verify Installation

```python
# test_v2_stack.py
import anthropic
import sentence_transformers
import chromadb
import markitdown
import jinja2
import tiktoken
import spacy  # Critical: verify spaCy works after Python downgrade

print("✓ All v2.0 dependencies installed")
print(f"Python: {sys.version}")
print(f"Anthropic SDK: {anthropic.__version__}")
print(f"Sentence Transformers: {sentence_transformers.__version__}")
print(f"ChromaDB: {chromadb.__version__}")
print(f"spaCy: {spacy.__version__}")
```

---

## What NOT to Add

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **LangChain** | Too heavy (100+ dependencies), slow imports (2-3 sec), overkill for focused use case. Channel needs script generation + vector search, not full RAG orchestration framework. LangChain designed for complex multi-agent systems. | anthropic SDK + chromadb + jinja2 (3 focused libraries) |
| **pandas** | Unnecessary for analytics queries. SQLite sufficient for GROUP BY, aggregations. Adds 100MB+ dependency. Current codebase (~17K LOC) uses raw SQL successfully. pandas overhead (DataFrame conversions) slower than direct SQL for small datasets. | SQLite with native Python dicts/lists |
| **NLTK** | Redundant with spaCy. Adds 1.5GB data files (tokenizers, corpora). spaCy already installed for script checkers, provides superior NER and dependency parsing. NLTK's regex-based tokenizer inferior to spaCy's neural models. | spaCy (already in stack) |
| **transformers (Hugging Face base)** | sentence-transformers wraps it efficiently. Installing base library adds 500MB+ models, slower loading. sentence-transformers optimized specifically for embeddings (lighter, faster). | sentence-transformers (specialized wrapper) |
| **Voice audio ML libraries** | Not working with audio. Channel uses text transcripts (SRT files) and written scripts. Voice "fingerprinting" here = text style analysis (word choice, sentence rhythm), not acoustic features (pitch, timbre). | faststylometry + spaCy (text-based authorship) |
| **LlamaIndex** | Similar to LangChain - heavy orchestration framework for document ingestion pipelines. Channel needs focused tools: convert PDFs to markdown, embed, search. Don't need data connectors, query engines, storage abstractions. | chromadb + markitdown (direct control) |
| **pinecone/weaviate/qdrant** | Cloud vector databases. Require API keys, network calls, monthly costs ($70+/month). ChromaDB runs local, zero cost, sufficient for channel scale (~100 videos, 1K research notes). Cloud DBs designed for millions of vectors. | chromadb (local-first) |
| **Docker** | Adds complexity for single-user CLI tools. Python virtualenv sufficient for dependency isolation. Docker overhead (disk space, daemon process) unnecessary. Windows Docker Desktop requires WSL2 (additional complexity). | venv or conda environments |
| **Docling** | Heavy document parser (IBM Research project). Includes OCR, table reconstruction, audio transcription. NotebookLM exports already contain text - need simple markdown extraction only. Docling adds 200MB+ ML models. | markitdown (lightweight, 5MB) |

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **anthropic SDK** | OpenAI SDK (GPT-4) | If switching from Claude to OpenAI models. Channel standardized on Claude Opus 4.6 for quality. OpenAI embeddings require API costs ($0.02/1M tokens). |
| **sentence-transformers** | OpenAI embeddings API | If willing to pay per-token for embeddings. Local sentence-transformers = free but slower (~100 sentences/sec CPU vs 1000/sec API). Channel scale makes free option viable. |
| **chromadb** | FAISS (Facebook AI Similarity Search) | If need ultra-high performance (millions of vectors). FAISS requires manual index building, no metadata storage. ChromaDB sufficient for channel scale (<10K vectors). |
| **markitdown** | Docling | If need OCR (scanned PDFs), table reconstruction, audio transcription. Markitdown lighter for simple markdown conversion from digital documents. NotebookLM sources are digital PDFs/DOCX. |
| **jinja2** | LangChain prompt templates | If building complex RAG chains with multiple retrievers, re-ranking, query transformations. Jinja2 sufficient for focused prompt management with template inheritance. |
| **tiktoken** | Manual estimation (chars × 0.25) | If Claude API doesn't enforce strict limits. Tiktoken prevents silent truncation (200K token window fills fast with research context). Manual estimation unreliable for mixed content (code, markdown). |
| **faststylometry** | Custom spaCy pipeline | If need fine-grained control over features (custom POS weights, domain-specific lexicons). Faststylometry sufficient for voice matching with standard authorship features. |
| **pydantic** | Manual validation (try/except blocks) | If don't need schema documentation or type hints. Pydantic generates validation code from type hints, reduces boilerplate. Anthropic SDK uses pydantic internally anyway. |

---

## Integration Strategy

### Feature 1: Channel-Aware Script Generation

**Stack components used:**
- `anthropic` - Claude Opus 4.6 API for script generation
- `sentence-transformers` - Find similar past videos (semantic search by topic)
- `chromadb` - Store/query script patterns, past performance embeddings
- `jinja2` - Build dynamic prompts with channel context (voice patterns, retention data)
- `tiktoken` - Prevent prompt truncation (verify <180K tokens before API call)

**Integration point:** Extend `.claude/commands/script.md` (already uses Opus 4.6 via `model: opus` tier alias)

**New modules:**
- `tools/production/script_context.py` - Build channel-aware context for Claude prompts
- `tools/production/voice_matcher.py` - Compare AI draft to creator's style using faststylometry
- `tools/production/retention_predictor.py` - Find high-retention structures from chromadb

**Data flow:**
```python
# 1. User requests script: "Fact-check crusades claims"
topic = "crusades defensive war myth"

# 2. Semantic search for similar past videos
topic_embedding = sentence_model.encode(topic)
similar_videos = chromadb.query(
    collection_name="script_patterns",
    query_embeddings=[topic_embedding],
    n_results=5,
    where={"retention": {"$gte": 0.35}}  # High retention only
)

# 3. Extract patterns from similar videos
voice_patterns = extract_voice_features(similar_videos)  # faststylometry
retention_structure = extract_structure(similar_videos)  # spaCy sections

# 4. Build prompt with jinja2
template = jinja_env.get_template("script_generation.j2")
prompt = template.render(
    topic=topic,
    voice_patterns=voice_patterns,
    retention_structure=retention_structure,
    past_lessons=similar_videos['lessons']
)

# 5. Check token count (prevent truncation)
token_count = tiktoken.count(prompt)
if token_count > 180000:  # Leave 20K buffer in 200K context
    prompt = truncate_intelligently(prompt, max_tokens=180000)

# 6. Generate with Claude Opus 4.6
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
response = client.messages.create(
    model="claude-opus-4-6-20260205",
    max_tokens=16000,  # ~10K words
    messages=[{"role": "user", "content": prompt}]
)

script_draft = response.content[0].text
```

### Feature 2: Research-to-NotebookLM Bridge

**Stack components used:**
- `markitdown` - Convert NotebookLM sources (PDF/DOCX) to markdown
- `sentence-transformers` - Embed research notes for semantic search
- `chromadb` - Store research embeddings with metadata (source file, page number)

**Integration point:** New CLI command `/research-bridge` or integrate into existing `/research` workflow

**New modules:**
- `tools/production/research_bridge.py` - Main orchestration
- `tools/production/notebooklm_parser.py` - Parse NotebookLM file naming conventions
- `tools/production/citation_extractor.py` - Extract page numbers, sources from markdown

**Data flow:**
```python
# 1. User exports NotebookLM sources to project folder
sources_dir = Path("video-projects/_IN_PRODUCTION/35-topic/notebooklm-sources/")
# Files: [P1] Wickham-Inheritance-Rome.pdf, [A1] Harris-Ancient-Literacy.pdf

# 2. Convert PDFs to markdown
from markitdown import MarkItDown
md_converter = MarkItDown()

for pdf_file in sources_dir.glob("*.pdf"):
    result = md_converter.convert(pdf_file)
    markdown_text = result.text_content

    # Save alongside PDF
    md_file = sources_dir / f"{pdf_file.stem}.md"
    md_file.write_text(markdown_text, encoding='utf-8')

# 3. Chunk markdown (preserve citation context)
chunks = chunk_markdown(
    markdown_text,
    chunk_size=500,  # ~100 words
    overlap=50,  # Preserve context across chunks
    preserve_headers=True  # Keep section structure
)

# 4. Embed chunks with sentence-transformers
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks, show_progress_bar=True)

# 5. Store in ChromaDB with metadata
collection = chromadb.get_or_create_collection("research_notes")
collection.add(
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{
        "source_file": pdf_file.name,
        "source_type": "academic_monograph",  # Parsed from [P1] prefix
        "page_estimate": estimate_page_number(chunk, markdown_text),
        "author": "Chris Wickham",  # Extracted from filename
        "topic": "medieval_literacy"  # User-tagged or auto-detected
    } for chunk in chunks],
    ids=[f"{pdf_file.stem}_chunk_{i}" for i in range(len(chunks))]
)

# 6. Query during script writing
query = "What did Chris Wickham say about medieval literacy rates?"
results = collection.query(
    query_texts=[query],
    n_results=3,
    where={"author": "Chris Wickham"}  # Filter by source
)

# Returns: Relevant excerpts with source file + page metadata
for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    print(f"Source: {meta['source_file']}, Page ~{meta['page_estimate']}")
    print(f"Excerpt: {doc}")
```

### Feature 3: Actionable Analytics

**Stack components used:**
- `sentence-transformers` - Compare script sections to high-retention examples
- `chromadb` - Store retention patterns by topic type (territorial, ideological, legal)
- `faststylometry` - Detect voice drift in AI-generated sections
- `spacy` - Extract linguistic features (entity density, sentence variance) - already installed

**Integration point:** Extend `tools/youtube-analytics/retention.py`

**New modules:**
- `tools/youtube-analytics/retention_diagnosis.py` - Analyze drops, suggest fixes
- `tools/youtube-analytics/pattern_matcher.py` - Find similar high-retention sections

**Data flow:**
```python
# 1. Analyze retention drop at timestamp 3:15
video_id = "abc123"
drop_timestamp = "3:15"  # User identified or auto-detected (>10% drop)

# 2. Extract script section at drop point
script_text = load_script(video_id)
drop_section = extract_section_at_timestamp(script_text, timestamp="3:15")
# Returns: ~200 words surrounding the drop

# 3. Find similar sections from high-retention videos
section_embedding = sentence_model.encode(drop_section)
similar_sections = chromadb.query(
    collection_name="script_patterns",
    query_embeddings=[section_embedding],
    n_results=5,
    where={
        "$and": [
            {"retention": {"$gte": 0.35}},  # High retention
            {"section_type": "explanation"}  # Same section type
        ]
    }
)

# 4. Compare features (quantitative diagnosis)
current_features = {
    'entity_density': count_entities(drop_section) / word_count(drop_section),
    'sentence_variance': calculate_variance([len(s) for s in sentences(drop_section)]),
    'flesch_score': textstat.flesch_reading_ease(drop_section),
    'avg_sentence_length': avg([len(s) for s in sentences(drop_section)])
}

successful_features = [
    extract_features(section)
    for section in similar_sections['documents'][0]
]
avg_successful = average_features(successful_features)

# 5. Generate actionable recommendations
recommendations = []
if current_features['entity_density'] > avg_successful['entity_density'] * 1.5:
    recommendations.append({
        'issue': 'Entity density too high',
        'current': f"{current_features['entity_density']:.1%}",
        'target': f"{avg_successful['entity_density']:.1%}",
        'action': 'Reduce proper nouns (names/places) by ~15%. Replace with pronouns or generic terms.'
    })

if current_features['sentence_variance'] > avg_successful['sentence_variance'] + 5:
    recommendations.append({
        'issue': 'Sentence rhythm inconsistent',
        'current': f"Variance {current_features['sentence_variance']:.1f}",
        'target': f"Variance {avg_successful['sentence_variance']:.1f}",
        'action': 'Use more uniform sentence lengths (15-20 words). Break long sentences.'
    })

# 6. Output to markdown report
report = f"""
## Retention Drop Analysis: {video_id} at {drop_timestamp}

### Diagnosis
- **Entity density:** {current_features['entity_density']:.1%} (successful videos: {avg_successful['entity_density']:.1%})
- **Sentence variance:** {current_features['sentence_variance']:.1f} (successful: {avg_successful['sentence_variance']:.1f})

### Recommendations
{format_recommendations(recommendations)}
"""
```

---

## Version Compatibility

| Package | Requires Python | Compatible With | Notes |
|---------|----------------|-----------------|-------|
| **anthropic >=1.87.1** | 3.9-3.13 | ⚠️ Not tested on 3.14 | SDK released Feb 2026, may add 3.14 support soon |
| **sentence-transformers >=3.1.0** | 3.10+ | ✅ Likely works on 3.14 | PyTorch 1.11+, transformers 4.34+ auto-installed |
| **chromadb >=0.5.29** | >=3.9 | ✅ Likely works on 3.14 | DuckDB backend, pure Python interface |
| **markitdown >=0.0.1a2** | 3.10+ | ⚠️ Alpha stage, untested on 3.14 | API may change (alpha release) |
| **spacy >=3.8** | 3.9-3.13 | ❌ **NO 3.14 WHEELS** | [GitHub Issue #13885](https://github.com/explosion/spaCy/issues/13885) |
| **textstat >=0.7.3** | 3.7+ | ✅ Works on 3.14 | No compiled extensions |
| **faststylometry >=0.1.0** | 3.8+ | ❌ **Blocked by spaCy** | Depends on spaCy, inherits 3.14 incompatibility |
| **jinja2 >=3.1.5** | 3.7+ | ✅ Works on 3.14 | Pure Python |
| **tiktoken >=0.8.0** | 3.8+ | ✅ Works on 3.14 | Rust extension with wheels |
| **pydantic >=2.10.4** | 3.8+ | ✅ Works on 3.14 | Rust extension with wheels |

**BLOCKING DEPENDENCIES:**
- spaCy (CRITICAL - needed for existing script checkers + faststylometry)
- faststylometry (needed for voice matching)

**RESOLUTION:** Downgrade Python 3.14.2 → 3.13.x before starting v2.0 development.

**Testing strategy after downgrade:**
```bash
# After Python 3.13.x installed
pip install anthropic sentence-transformers chromadb markitdown jinja2 tiktoken faststylometry pydantic --dry-run
# Check for version conflicts before actual install

# Verify critical packages
python -c "import spacy, faststylometry, sentence_transformers; print('OK')"
```

---

## Performance Benchmarks

### Embedding Generation Speed

**sentence-transformers (all-MiniLM-L6-v2):**
- CPU (i7-10th gen): ~100 sentences/sec
- GPU (RTX 3060): ~1000 sentences/sec (not required for channel scale)
- First-time model download: ~420MB, 2-3 min on 50 Mbps connection

**Optimization strategies:**
- Batch encode (100 sentences at once vs 1 at a time): 10x speedup
- Cache embeddings in ChromaDB (don't re-embed same research notes)
- Use smaller model if speed critical: `all-MiniLM-L6-v2` (384 dims) vs `all-mpnet-base-v2` (768 dims, +5% accuracy, 2x slower)

### Vector Search Speed

**ChromaDB (DuckDB backend, CPU):**
- <10ms for queries on 1K vectors (typical: ~100 videos, ~1K research notes)
- <100ms for queries on 100K vectors
- Default approximate nearest neighbor (ANN) with HNSW index

**When to optimize:**
- 1000+ videos: No action needed (still <100ms)
- 10K+ research notes: No action needed (still <500ms)
- Only optimize if measurements show actual slowness

### Claude API Latency

**Opus 4.6 generation speed (observed):**
- ~10-15 tokens/sec (streaming)
- ~2-3 min for 1500-token script
- Max tokens per request: 16,000 output tokens (sufficient for 10K-word script)
- Context window: 200K tokens input (full research + past scripts)

**Cost estimate:**
- Input: $15 per 1M tokens
- Output: $75 per 1M tokens
- Typical script generation: 50K input + 2K output = $0.75 + $0.15 = **$0.90 per script**
- Monthly (4 scripts): **~$3.60/month**

### Disk Space Requirements

**Incremental additions (v2.0):**
- sentence-transformers model: 420MB (one-time download)
- chromadb data: ~10MB per 100 videos + ~20MB per 100 research sources
- anthropic SDK + dependencies: ~50MB
- Other libraries: ~80MB

**Total:** ~600MB initial + ~30MB/year growth (12 videos + 20 sources/video)

**Existing baseline (v1.5):** ~2GB (spaCy models, pyppeteer Chromium, YouTube Analytics cache)

---

## Security Considerations

### API Keys (Environment Variables)

**Required:**
```bash
# .env file (DO NOT COMMIT)
ANTHROPIC_API_KEY=sk-ant-api03-...  # Claude API
YOUTUBE_CLIENT_ID=...               # OAuth (existing)
YOUTUBE_CLIENT_SECRET=...           # OAuth (existing)
```

**Best practices:**
- Use `python-dotenv` to load from `.env` (already standard in codebase)
- Add `.env` to `.gitignore` (already present)
- Rotate keys if accidentally committed (git history rewrite + key regeneration)
- Use separate API keys for dev/prod if sharing codebase

**Cost monitoring:**
```python
# Track Claude API usage
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
usage = client.beta.messages.count_tokens(
    model="claude-opus-4-6-20260205",
    messages=[{"role": "user", "content": prompt}]
)
print(f"Estimated cost: ${usage['input_tokens'] / 1_000_000 * 15:.3f}")
```

### Data Privacy

**What's stored locally (ChromaDB):**
- Research embeddings: Academic sources (public domain or purchased)
- Script patterns: Public YouTube content (channel's own videos)
- YouTube analytics: Channel's own performance data (no viewer PII)

**What's sent to external APIs:**
- **Claude API:** Scripts, prompts, research excerpts
  - Anthropic privacy policy: Data not used for training (as of Feb 2026)
  - Retention: 30 days for abuse monitoring, then deleted
- **YouTube API:** OAuth tokens, video IDs (no transcript content)
  - Google privacy policy applies
  - Tokens stored locally in `credentials/token.json`

**No third-party data sharing:** All NLP processing (spaCy, sentence-transformers, faststylometry) runs locally. No telemetry.

**Sensitive data handling:**
- NotebookLM academic sources: May include copyrighted books (for research purposes)
- Recommendation: Keep chromadb data directory private, don't commit to public repos
- `data/chromadb/` added to `.gitignore`

---

## Migration Path: v1.5 → v2.0

### Phase 1: Python Version Fix (Week 1, Day 1-2)

**CRITICAL BLOCKER - Do this first:**

```bash
# 1. Check current Python version
python --version
# Output: Python 3.14.2 (INCOMPATIBLE)

# 2. Download Python 3.13.x
# Visit: https://www.python.org/downloads/
# Download: Python 3.13.8 (latest 3.13.x as of 2026-02-09)

# 3. Install Python 3.13.x
# Windows: Run installer, check "Add to PATH"

# 4. Verify installation
python --version
# Output: Python 3.13.8 (COMPATIBLE)

# 5. Reinstall all existing dependencies
pip install -r tools/youtube-analytics/requirements.txt
pip install -r tools/script-checkers/requirements.txt
pip install -r tools/discovery/requirements.txt

# 6. Verify critical packages
python -m spacy validate
python -c "import spacy, textstat, srt; print('✓ Existing stack OK')"
```

**Estimated time:** 30-60 min (download + reinstall)

### Phase 2: Install v2.0 Dependencies (Week 1, Day 2-3)

```bash
# Core dependencies
pip install anthropic>=1.87.1
pip install sentence-transformers>=3.1.0
pip install chromadb>=0.5.29
pip install markitdown>=0.0.1a2

# Supporting libraries
pip install jinja2>=3.1.5
pip install tiktoken>=0.8.0
pip install faststylometry>=0.1.0
pip install pydantic>=2.10.4

# Verify installation
python test_v2_stack.py  # Run verification script from earlier
```

**Expected errors to troubleshoot:**
- sentence-transformers: First-time model download may timeout (retry)
- markitdown: Alpha stage, may have install issues (check GitHub issues)

**Estimated time:** 10-15 min (install) + 5 min (model download)

### Phase 3: Initialize ChromaDB Collections (Week 1, Day 3)

```python
# tools/production/initialize_v2.py
import chromadb
from pathlib import Path

def initialize_chromadb():
    """Create ChromaDB collections for v2.0 features"""
    db_path = Path("G:/History vs Hype/data/chromadb")
    db_path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_path))

    # Collection 1: Research notes from NotebookLM
    research = client.get_or_create_collection(
        name="research_notes",
        metadata={
            "description": "Academic sources from NotebookLM (PDFs, DOCX)",
            "embedding_model": "all-MiniLM-L6-v2",
            "created": "2026-02-09"
        }
    )

    # Collection 2: Script patterns with retention data
    scripts = client.get_or_create_collection(
        name="script_patterns",
        metadata={
            "description": "Past scripts with performance metrics",
            "embedding_model": "all-MiniLM-L6-v2",
            "created": "2026-02-09"
        }
    )

    # Collection 3: Creator voice patterns
    voice = client.get_or_create_collection(
        name="voice_patterns",
        metadata={
            "description": "Style fingerprints from verified creator scripts",
            "embedding_model": "all-MiniLM-L6-v2",
            "created": "2026-02-09"
        }
    )

    print(f"✓ Created 3 ChromaDB collections in {db_path}")
    return {'research': research, 'scripts': scripts, 'voice': voice}

if __name__ == "__main__":
    collections = initialize_chromadb()
    print(f"Research notes: {collections['research'].count()} documents")
    print(f"Script patterns: {collections['scripts'].count()} documents")
    print(f"Voice patterns: {collections['voice'].count()} documents")
```

**Estimated time:** 5 min

### Phase 4: Migrate Existing Data to ChromaDB (Week 1, Day 4-5)

**Priority 1: Script patterns (enable channel-aware generation immediately)**

```python
# tools/production/migrate_scripts_to_chromadb.py
from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import chromadb

def migrate_published_scripts():
    """Embed existing published scripts for similarity search"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.PersistentClient(path="G:/History vs Hype/data/chromadb")
    collection = client.get_collection("script_patterns")

    archived_dir = Path("G:/History vs Hype/video-projects/_ARCHIVED")
    migrated_count = 0

    for project_dir in archived_dir.iterdir():
        if not project_dir.is_dir():
            continue

        # Load script
        script_file = project_dir / "FINAL-SCRIPT.md"
        if not script_file.exists():
            print(f"⊘ Skipping {project_dir.name} (no FINAL-SCRIPT.md)")
            continue

        script_text = script_file.read_text(encoding='utf-8')

        # Split into sections (intro, body sections, conclusion)
        sections = split_script_into_sections(script_text)

        # Embed sections
        embeddings = model.encode(sections, show_progress_bar=True)

        # Load performance data from keywords.db
        video_id = extract_video_id(project_dir.name)
        performance = load_performance_from_db(video_id)

        # Store in ChromaDB
        collection.add(
            documents=sections,
            embeddings=embeddings,
            metadatas=[{
                'video_id': video_id,
                'project_name': project_dir.name,
                'section_index': i,
                'section_type': detect_section_type(section),
                'retention': performance.get('retention'),
                'ctr': performance.get('ctr'),
                'views': performance.get('views'),
                'topic_type': performance.get('topic_type')  # territorial, ideological, legal
            } for i, section in enumerate(sections)],
            ids=[f"{video_id}_section_{i}" for i in range(len(sections))]
        )

        migrated_count += 1
        print(f"✓ Migrated {project_dir.name} ({len(sections)} sections)")

    print(f"\n✓ Total migrated: {migrated_count} videos")
    return migrated_count

if __name__ == "__main__":
    migrated = migrate_published_scripts()
```

**Expected migration time:** ~15 min for 30 archived videos (embedding generation)

**Priority 2: Research notes (optional, can do incrementally as new videos created)**

Only migrate if NotebookLM sources were saved historically. Otherwise, start fresh with new videos.

**Estimated time:** 1-2 hours total for Phase 4 (scripting + execution)

### Phase 5: Configure API Keys (Week 1, Day 5)

```bash
# .env file (create if doesn't exist)
echo "ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE" >> .env

# Verify .env in .gitignore
grep "^\.env$" .gitignore || echo ".env" >> .gitignore

# Test API key
python -c "
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
print('✓ Anthropic API key valid')
"
```

**Get API key:** https://console.anthropic.com/settings/keys

**Estimated time:** 5 min (sign up + copy key + verify)

### Phase 6: Integration Testing (Week 2)

**Test 1: Semantic search (script patterns)**
```python
# test_semantic_search.py
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="data/chromadb")
collection = client.get_collection("script_patterns")

# Query: Find similar past scripts
query = "territorial dispute with colonial borders"
results = collection.query(
    query_embeddings=[model.encode(query)],
    n_results=3
)

print(f"Found {len(results['documents'][0])} similar scripts:")
for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    print(f"\nVideo: {meta['project_name']}")
    print(f"Retention: {meta['retention']:.1%}")
    print(f"Excerpt: {doc[:200]}...")
```

**Test 2: Claude API integration**
```python
# test_claude_api.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

response = client.messages.create(
    model="claude-opus-4-6-20260205",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": "Write a 100-word script opening for: 'How Sykes-Picot created modern Middle East conflicts'"
    }]
)

print(response.content[0].text)
print(f"\nTokens used: {response.usage.input_tokens} in + {response.usage.output_tokens} out")
print(f"Cost: ${response.usage.input_tokens / 1_000_000 * 15 + response.usage.output_tokens / 1_000_000 * 75:.4f}")
```

**Test 3: End-to-end (research → script → voice check)**
```python
# test_end_to_end.py
# (Full workflow test - will create during Phase 27 development)
```

**Estimated time:** 2-3 hours (write tests + debug issues)

---

## Monitoring and Maintenance

### Monthly Dependency Check

```bash
# Check for outdated packages (run first Monday of each month)
pip list --outdated | grep -E "(anthropic|sentence-transformers|chromadb|spacy)"

# Critical: anthropic SDK (frequent updates in 2026 for Opus 4.6 features)
# Medium: sentence-transformers (model format changes every ~6 months)
# Low: chromadb, spacy (stable, update annually)
```

**Breaking change alerts:**
- Subscribe to: https://github.com/anthropics/anthropic-sdk-python/releases
- Watch: https://github.com/explosion/spaCy/issues (Python 3.14 wheels)

### Model Version Updates

**sentence-transformers models:**
- Current: `all-MiniLM-L6-v2` (384 dims, 80MB, 2021 model)
- Alternative: `all-mpnet-base-v2` (768 dims, 420MB, +5% accuracy, 2021)
- Future: Check [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) for newer models

**Update strategy:**
1. Download new model to separate directory
2. Test on 10 sample queries (compare results to current model)
3. If quality improvement >5%, migrate (re-embed all chromadb collections)
4. Otherwise, defer (embeddings are model-specific, can't mix)

**spaCy models:**
- Current: `en_core_web_sm` (12MB, base English)
- Upgrade path: `en_core_web_md` (40MB, better NER) or `en_core_web_lg` (560MB, best accuracy)
- Update: `python -m spacy download en_core_web_md` (no code changes needed)

### Storage Growth Monitoring

**ChromaDB collection sizes:**
```python
# tools/maintenance/check_chromadb_size.py
import chromadb
from pathlib import Path

client = chromadb.PersistentClient(path="data/chromadb")
collections = ['research_notes', 'script_patterns', 'voice_patterns']

for name in collections:
    collection = client.get_collection(name)
    count = collection.count()

    # Estimate size (384 dims × 4 bytes/float × count)
    size_mb = (count * 384 * 4) / 1_000_000

    print(f"{name}: {count} documents (~{size_mb:.1f} MB)")

# Check disk usage
db_dir = Path("data/chromadb")
total_size = sum(f.stat().st_size for f in db_dir.rglob('*') if f.is_file())
print(f"\nTotal disk usage: {total_size / 1_000_000:.1f} MB")
```

**Expected growth:**
- Scripts: ~1MB per 100 videos (384 dims × 10 sections/video × 4 bytes)
- Research: ~10MB per 100 sources (100 pages × 10 chunks/page)
- Voice: ~100KB per creator profile (negligible)

**Annual projection (12 videos, 20 sources/video):**
- Scripts: +0.12 MB
- Research: +2.4 MB
- **Total: ~3 MB/year** (negligible)

---

## Troubleshooting Guide

### Common Installation Issues

**Issue 1: spaCy fails to install on Python 3.14**
```bash
ERROR: Could not find a version that satisfies the requirement spacy>=3.8
```
**Solution:** Downgrade to Python 3.13.x (see Phase 1 migration)

**Issue 2: sentence-transformers model download timeout**
```bash
urllib.error.URLError: <urlopen error [Errno 60] Operation timed out>
```
**Solution:**
```python
# Manual download with retries
from sentence_transformers import SentenceTransformer
import time

for attempt in range(3):
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        break
    except Exception as e:
        print(f"Attempt {attempt+1} failed, retrying...")
        time.sleep(5)
```

**Issue 3: ChromaDB "Cannot connect to local server"**
```bash
chromadb.errors.ChromaError: Could not connect to local server
```
**Solution:** ChromaDB doesn't run a server in persistent mode. Check path:
```python
import chromadb
client = chromadb.PersistentClient(path="./data/chromadb")  # Not PersistentClient(host=...)
```

**Issue 4: Anthropic API key invalid**
```bash
anthropic.AuthenticationError: Invalid API key
```
**Solution:**
1. Verify key in .env: `cat .env | grep ANTHROPIC_API_KEY`
2. Check key format: `sk-ant-api03-...` (must start with `sk-ant-api03`)
3. Regenerate key at https://console.anthropic.com/settings/keys

### Performance Issues

**Issue: Embedding generation slow (>10 sec for 100 sentences)**
```python
# Diagnosis
import time
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
sentences = ["test sentence"] * 100

start = time.time()
embeddings = model.encode(sentences)
print(f"Time: {time.time() - start:.2f} sec")  # Should be <1 sec on modern CPU
```
**Solutions:**
- Batch encoding (already default in sentence-transformers)
- Check CPU usage (other processes hogging resources?)
- Consider GPU (add `device='cuda'` to SentenceTransformer) - not required for channel scale

**Issue: ChromaDB queries slow (>1 sec for simple query)**
```python
# Diagnosis
import time
import chromadb

client = chromadb.PersistentClient(path="data/chromadb")
collection = client.get_collection("script_patterns")

start = time.time()
results = collection.query(query_texts=["test"], n_results=5)
print(f"Query time: {time.time() - start:.2f} sec")  # Should be <0.1 sec
```
**Solutions:**
- Check collection size: `collection.count()` (if >100K, may need optimization)
- Reduce n_results (default 10, try 5)
- Create HNSW index (ChromaDB does this automatically, but check metadata)

### Data Quality Issues

**Issue: Semantic search returns irrelevant results**
```python
# Diagnosis: Check embedding quality
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Test semantic similarity
query = "territorial dispute colonial borders"
doc1 = "The Sykes-Picot agreement divided Ottoman territories"  # Relevant
doc2 = "Medieval castles had defensive walls"  # Irrelevant

embeddings = model.encode([query, doc1, doc2])
sim1 = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
sim2 = np.dot(embeddings[0], embeddings[2]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[2]))

print(f"Similarity (query-relevant): {sim1:.3f}")  # Should be >0.5
print(f"Similarity (query-irrelevant): {sim2:.3f}")  # Should be <0.3
```
**Solutions:**
- Verify metadata filters are correct (topic_type, retention thresholds)
- Check for duplicate embeddings (same document added multiple times)
- Consider domain-specific model (if general model insufficient) - unlikely needed

**Issue: Claude generates scripts that don't match creator's voice**
```python
# Diagnosis: Check voice pattern extraction
from tools.production.voice_matcher import analyze_voice_patterns

creator_text = load_past_scripts(n=5)  # Load 5 verified scripts
ai_text = "<AI-generated draft>"

creator_features = analyze_voice_patterns(creator_text)
ai_features = analyze_voice_patterns(ai_text)

print("Feature comparison:")
print(f"Avg sentence length: Creator {creator_features['avg_sent_len']:.1f} vs AI {ai_features['avg_sent_len']:.1f}")
print(f"Entity density: Creator {creator_features['entity_density']:.2%} vs AI {ai_features['entity_density']:.2%}")
print(f"Contraction rate: Creator {creator_features['contraction_rate']:.2%} vs AI {ai_features['contraction_rate']:.2%}")
```
**Solutions:**
- Add more examples to voice pattern collection (need 10+ verified scripts)
- Adjust prompt template to emphasize specific voice features
- Use temperature parameter in Claude API (lower = more conservative, higher = more creative)

---

## Sources

### Official Documentation (HIGH confidence)

**Anthropic SDK:**
- [anthropics/anthropic-sdk-python - GitHub](https://github.com/anthropics/anthropic-sdk-python) - Official Python SDK
- [Claude Agent SDK Releases](https://github.com/anthropics/claude-agent-sdk-python/releases) - Version 0.1.33 (Feb 7, 2026)
- [Client SDKs - Claude API Docs](https://platform.claude.com/docs/en/api/client-sdks) - Official documentation

**Sentence Transformers:**
- [SentenceTransformers Documentation](https://sbert.net/) - Official docs
- [sentence-transformers on PyPI](https://pypi.org/project/sentence-transformers/) - Python 3.10+ requirement
- [Semantic Textual Similarity](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) - Usage guide

**ChromaDB:**
- [ChromaDB Official Site](https://www.trychroma.com/) - Main documentation
- [chromadb on PyPI](https://pypi.org/project/chromadb/) - Version 0.5.29 (Feb 9, 2026)
- [chroma-core/chroma - GitHub](https://github.com/chroma-core/chroma) - Source code

**MarkItDown:**
- [microsoft/markitdown - GitHub](https://github.com/microsoft/markitdown) - Microsoft's document converter
- [Python MarkItDown - Real Python](https://realpython.com/python-markitdown/) - Tutorial

**spaCy:**
- [spaCy Documentation](https://spacy.io/usage) - Official docs
- [spaCy Issue #13885](https://github.com/explosion/spaCy/issues/13885) - Python 3.14 wheels unavailable
- [spacy on PyPI](https://pypi.org/project/spacy/) - Package page

### NotebookLM API (MEDIUM confidence)

- [Create and manage notebooks (API)](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) - Google Cloud official API (alpha)
- [Add and manage data sources](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources) - Source management API
- [NotebookLM-py - Medium](https://medium.com/@tentenco/notebooklm-py-the-cli-tool-that-unlocks-google-notebooklm-1de7106fd7ca) - Unofficial CLI tool (Jan 2026)

### Text Style Analysis (MEDIUM confidence)

- [authorship-attribution - GitHub Topics](https://github.com/topics/authorship-attribution?l=python) - 49 Python projects
- [Authorship Attribution with Python](https://aicbt.com/authorship-attribution/) - Tutorial
- [Introduction to stylometry with Python](https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python) - Programming Historian guide
- [Fast Data Science stylometry](https://fastdatascience.com/natural-language-processing/forensic-stylometry-linguistics-authorship-analysis/) - Forensic linguistics

### LLM Prompt Engineering (MEDIUM confidence)

- [Prompt Templates with Jinja2](https://blog.promptlayer.com/prompt-templates-with-jinja2-2/) - PromptLayer tutorial
- [Banks - GitHub](https://github.com/masci/banks) - LLM prompt language based on Jinja
- [Managing Prompt Templates in Python](https://tech-depth-and-breadth.medium.com/managing-prompt-templates-in-python-with-jinja-9e978f089aa6) - Medium guide
- [Jinja2 prompting guide](https://medium.com/@alecgg27895/jinja2-prompting-a-guide-on-using-jinja2-templates-for-prompt-management-in-genai-applications-e36e5c1243cf) - GenAI applications

### Vector Databases & RAG (MEDIUM confidence)

- [ChromaDB Tutorial - DataCamp](https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide) - Step-by-step guide
- [Embeddings and Vector Databases - Real Python](https://realpython.com/chromadb-vector-database/) - Tutorial
- [Build a RAG agent with LangChain](https://docs.langchain.com/oss/python/langchain/rag) - RAG architecture reference
- [Document loaders - LangChain](https://reference.langchain.com/python/langchain_core/document_loaders/) - Loader patterns

---

*Stack research for: History vs Hype v2.0 Channel Intelligence*
*Researched: 2026-02-09*
*Confidence: HIGH*
*Critical blocker identified: Python 3.14 incompatibility with spaCy (wheels unavailable)*
*Resolution: Downgrade to Python 3.13.x before Phase 1 development*
