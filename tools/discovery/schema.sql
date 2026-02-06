-- YouTube Keyword Discovery Database Schema
-- Purpose: Track keywords from autocomplete, manual input, and competitor analysis
-- For: YouTube topic discovery and search intent classification

-- Main keywords table
CREATE TABLE IF NOT EXISTS keywords (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword TEXT NOT NULL UNIQUE,
  search_volume INTEGER,
  competition_score REAL, -- 0-100 from VidIQ
  vidiq_overall_score REAL,
  first_discovered DATE NOT NULL,
  last_updated DATE NOT NULL,
  source TEXT -- 'autocomplete', 'competitor', 'manual', 'vidiq'
);

-- Search intent classifications
CREATE TABLE IF NOT EXISTS keyword_intents (
  keyword_id INTEGER NOT NULL,
  intent_category TEXT NOT NULL, -- MYTH_BUSTING, TERRITORIAL_DISPUTE, etc.
  confidence REAL NOT NULL, -- 0-1
  is_primary BOOLEAN DEFAULT 0,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id),
  PRIMARY KEY (keyword_id, intent_category)
);

-- Performance tracking when keywords used in videos
CREATE TABLE IF NOT EXISTS keyword_performance (
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

-- Competitor keyword tracking
CREATE TABLE IF NOT EXISTS competitor_keywords (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  competitor_channel TEXT NOT NULL, -- 'Kraut', 'Knowing Better', etc.
  competitor_video_id TEXT,
  video_views INTEGER,
  video_age_days INTEGER,
  discovered_date DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- VidIQ prediction accuracy tracking
CREATE TABLE IF NOT EXISTS vidiq_predictions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  predicted_volume INTEGER,
  predicted_competition REAL,
  overall_score REAL,
  prediction_date DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_keywords_volume ON keywords(search_volume DESC);
CREATE INDEX IF NOT EXISTS idx_keywords_source ON keywords(source);
CREATE INDEX IF NOT EXISTS idx_intents_primary ON keyword_intents(is_primary, confidence DESC);
CREATE INDEX IF NOT EXISTS idx_performance_date ON keyword_performance(measured_date DESC);
CREATE INDEX IF NOT EXISTS idx_competitor_channel ON competitor_keywords(competitor_channel);

-- View for keyword analysis
CREATE VIEW IF NOT EXISTS keyword_analysis AS
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

-- ============================================================================
-- DEMAND RESEARCH TABLES (Phase 15)
-- Purpose: Track trend data, competition metrics, and opportunity scores
-- ============================================================================

-- Trend data over time (for trend direction analysis)
CREATE TABLE IF NOT EXISTS trends (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  fetched_at DATETIME NOT NULL,
  interest INTEGER NOT NULL, -- 0-100 normalized Google Trends interest
  trend_direction TEXT, -- 'rising', 'stable', 'declining'
  percent_change REAL, -- +45.2 or -20.1 percentage change
  region TEXT DEFAULT 'US',
  source TEXT DEFAULT 'google_trends',
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Competitor channel metadata
CREATE TABLE IF NOT EXISTS competitor_channels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  channel_id TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  subscriber_count INTEGER,
  total_views INTEGER,
  video_count INTEGER,
  last_updated DATE NOT NULL
);

-- Competitor videos per keyword (for competition counting)
CREATE TABLE IF NOT EXISTS competitor_videos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  video_id TEXT NOT NULL UNIQUE,
  channel_id INTEGER NOT NULL,
  keyword_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  view_count INTEGER,
  published_at DATE,
  video_age_days INTEGER,
  discovered_at DATE NOT NULL,
  FOREIGN KEY (channel_id) REFERENCES competitor_channels(id),
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Calculated opportunity scores (demand/competition ratio)
CREATE TABLE IF NOT EXISTS opportunity_scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  demand_score REAL NOT NULL, -- autocomplete position proxy
  competition_score REAL NOT NULL, -- video + channel count
  opportunity_ratio REAL NOT NULL, -- demand/competition
  opportunity_category TEXT NOT NULL, -- 'High', 'Medium', 'Low'
  calculated_at DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Prediction accuracy tracking (for Phase 18 validation)
CREATE TABLE IF NOT EXISTS validations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  predicted_score REAL NOT NULL,
  actual_views INTEGER,
  actual_ctr REAL,
  prediction_date DATE NOT NULL,
  validation_date DATE,
  accuracy_score REAL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Indexes for demand research queries
CREATE INDEX IF NOT EXISTS idx_trends_keyword_time ON trends(keyword_id, fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_trends_fetch_time ON trends(fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_opportunity_ratio ON opportunity_scores(opportunity_ratio DESC, calculated_at DESC);
CREATE INDEX IF NOT EXISTS idx_competitor_videos_keyword ON competitor_videos(keyword_id, discovered_at DESC);

-- ============================================================================
-- CLASSIFICATION COLUMNS (Phase 16)
-- Purpose: Store format, angle, and quality classifications for competitor videos
-- ============================================================================

-- Classification columns for competitor analysis (Phase 16)
ALTER TABLE competitor_videos ADD COLUMN format TEXT;
ALTER TABLE competitor_videos ADD COLUMN angles TEXT;
ALTER TABLE competitor_videos ADD COLUMN quality_tier TEXT;
ALTER TABLE competitor_videos ADD COLUMN classified_at DATE;

-- Indexes for Phase 16 competition filtering
CREATE INDEX IF NOT EXISTS idx_competitor_format ON competitor_videos(keyword_id, format);
CREATE INDEX IF NOT EXISTS idx_competitor_quality ON competitor_videos(keyword_id, quality_tier);

-- ============================================================================
-- PRODUCTION CONSTRAINT COLUMNS (Phase 17)
-- Purpose: Store production feasibility assessments for keywords
-- ============================================================================

-- Production constraint columns for fail-fast filtering (Phase 17)
ALTER TABLE keywords ADD COLUMN production_constraints TEXT;  -- JSON: animation_required, document_score, sources_found
ALTER TABLE keywords ADD COLUMN constraint_checked_at DATE;
ALTER TABLE keywords ADD COLUMN is_production_blocked BOOLEAN DEFAULT 0;

-- Index for production filtering queries
CREATE INDEX IF NOT EXISTS idx_keywords_blocked
  ON keywords(is_production_blocked, constraint_checked_at DESC);

-- ============================================================================
-- LIFECYCLE STATE COLUMNS (Phase 18)
-- Purpose: Track keyword progression from discovery to publication
-- ============================================================================

-- Lifecycle state columns for keyword progression tracking (Phase 18)
ALTER TABLE keywords ADD COLUMN lifecycle_state TEXT DEFAULT 'DISCOVERED';
ALTER TABLE keywords ADD COLUMN lifecycle_updated_at DATE;
ALTER TABLE keywords ADD COLUMN opportunity_score_final REAL;
ALTER TABLE keywords ADD COLUMN opportunity_category TEXT;

-- Lifecycle history tracking table
CREATE TABLE IF NOT EXISTS lifecycle_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  from_state TEXT NOT NULL,
  to_state TEXT NOT NULL,
  transitioned_at DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Index for lifecycle queries
CREATE INDEX IF NOT EXISTS idx_lifecycle_history
  ON lifecycle_history(keyword_id, transitioned_at DESC);

-- ============================================================================
-- VIDEO PERFORMANCE TABLE (Phase 19)
-- Purpose: Track subscriber conversion and performance metrics for own videos
-- ============================================================================

-- Video performance tracking for conversion analysis
CREATE TABLE IF NOT EXISTS video_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT UNIQUE NOT NULL,
    title TEXT,
    views INTEGER,
    subscribers_gained INTEGER,
    subscribers_lost INTEGER,
    conversion_rate REAL,
    watch_time_minutes REAL,
    avg_view_duration_seconds INTEGER,
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    topic_type TEXT,
    angles TEXT,
    published_at DATE,
    fetched_at DATE NOT NULL,
    classified_at DATE
);

-- Indexes for performance queries
CREATE INDEX IF NOT EXISTS idx_performance_conversion ON video_performance(conversion_rate DESC);
CREATE INDEX IF NOT EXISTS idx_performance_topic ON video_performance(topic_type);
CREATE INDEX IF NOT EXISTS idx_performance_fetched ON video_performance(fetched_at DESC);

-- ============================================================================
-- VARIANT TRACKING TABLES (Phase 27)
-- Purpose: Store thumbnail/title variants for A/B testing and CTR tracking
-- ============================================================================

-- Thumbnail variant storage
CREATE TABLE IF NOT EXISTS thumbnail_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    variant_letter TEXT NOT NULL,
    file_path TEXT NOT NULL,
    perceptual_hash TEXT,
    visual_pattern_tags TEXT,
    created_at DATE NOT NULL,
    FOREIGN KEY (video_id) REFERENCES video_performance(video_id)
);

CREATE INDEX IF NOT EXISTS idx_thumbnail_video ON thumbnail_variants(video_id);
CREATE INDEX IF NOT EXISTS idx_thumbnail_hash ON thumbnail_variants(perceptual_hash);

-- Title variant storage
CREATE TABLE IF NOT EXISTS title_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    variant_letter TEXT NOT NULL,
    title_text TEXT NOT NULL,
    character_count INTEGER NOT NULL,
    formula_tags TEXT,
    created_at DATE NOT NULL,
    FOREIGN KEY (video_id) REFERENCES video_performance(video_id)
);

CREATE INDEX IF NOT EXISTS idx_title_video ON title_variants(video_id);

-- CTR snapshot tracking (monthly)
CREATE TABLE IF NOT EXISTS ctr_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    ctr_percent REAL NOT NULL,
    impression_count INTEGER NOT NULL,
    view_count INTEGER NOT NULL,
    active_thumbnail_id INTEGER,
    active_title_id INTEGER,
    is_late_entry BOOLEAN DEFAULT 0,
    recorded_at DATE NOT NULL,
    FOREIGN KEY (video_id) REFERENCES video_performance(video_id),
    FOREIGN KEY (active_thumbnail_id) REFERENCES thumbnail_variants(id),
    FOREIGN KEY (active_title_id) REFERENCES title_variants(id)
);

CREATE INDEX IF NOT EXISTS idx_ctr_video_date ON ctr_snapshots(video_id, snapshot_date DESC);

-- ============================================================================
-- FEEDBACK STORAGE (Phase 27)
-- Purpose: Track video performance feedback and section-level notes
-- ============================================================================

-- Feedback columns on video_performance
ALTER TABLE video_performance ADD COLUMN retention_drop_point INTEGER;
ALTER TABLE video_performance ADD COLUMN discovery_issues TEXT;
ALTER TABLE video_performance ADD COLUMN lessons_learned TEXT;

-- Section-level feedback
CREATE TABLE IF NOT EXISTS section_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    section_name TEXT NOT NULL,
    retention_percent REAL,
    notes TEXT,
    created_at DATE,
    FOREIGN KEY (video_id) REFERENCES video_performance(video_id)
);

CREATE INDEX IF NOT EXISTS idx_section_feedback_video ON section_feedback(video_id);
