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
