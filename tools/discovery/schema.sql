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
