# Domain Pitfalls: Niche Discovery Tools for YouTube

**Domain:** YouTube niche discovery and opportunity scoring
**Researched:** 2026-01-31
**Confidence:** HIGH

---

## Executive Summary

Building niche discovery tools for YouTube content creators involves three distinct pitfall categories: **data acquisition** (getting reliable data without being blocked), **filtering accuracy** (matching opportunities to production constraints), and **system integration** (connecting discovery to existing workflow without creating parallel systems). The most critical pitfalls are invisible filtering errors (missing perfect opportunities due to overly restrictive rules) and data staleness (making decisions on outdated opportunity windows).

**Key insight:** Most niche discovery tools fail not from poor algorithms, but from optimizing for the wrong creator. A topic with 100K monthly searches and low competition is worthless if it requires animation skills you don't have or violates your channel's documentary tone.

---

## Critical Pitfalls

### Pitfall 1: Ignoring Production Constraint Filtering

**What goes wrong:** Discovery tool surfaces "perfect" opportunities that are impossible to produce given channel constraints (no animation, academic sources required, solo creator timeline). Creator wastes time researching topics that fail at script phase.

**Why it happens:** Generic niche discovery tools optimize for demand/competition only. They don't filter by: visual format requirements (animation vs. document-heavy), research depth (Wikipedia vs. academic papers), production complexity (solo vs. team), or timeline constraints (can primary sources be accessed in reasonable time?).

**Consequences:**
- 5-10 hours wasted on preliminary research for unproduceable topics
- Creator frustration and tool abandonment
- Missed truly viable opportunities buried in unfiltered results
- Gap between "opportunity found" and "video shipped" never closes

**Prevention:**
1. **Define production constraint schema FIRST** before building scoring:
   ```python
   PRODUCTION_CONSTRAINTS = {
       'visual_style': ['documents', 'maps', 'footage', 'text_overlays'],
       'visual_forbidden': ['animation', 'original_illustrations', '3D_renders'],
       'research_depth': 'academic_sources_required',  # Not Wikipedia-only
       'source_accessibility': 'public_archives_or_purchasable',  # Not classified documents
       'production_team_size': 'solo',
       'max_research_timeline': '2-4 weeks'  # For NotebookLM phase
   }
   ```

2. **Add fit scoring BEFORE opportunity scoring:**
   ```python
   def calculate_fit_score(topic, constraints):
       fit = 0.5  # Baseline

       # Can visual requirements be met?
       if topic['requires_animation']:
           return 0.0  # HARD BLOCK

       # Are primary sources accessible?
       if topic['primary_sources'] in ['available_digitally', 'university_library', 'purchasable']:
           fit += 0.3
       elif topic['primary_sources'] == 'classified_or_unavailable':
           return 0.0  # HARD BLOCK

       # Does it fit documentary tone?
       if any(word in topic['title'].lower() for word in ['secret', 'shocking', 'hidden']):
           fit -= 0.4  # Clickbait language penalty

       if any(word in topic['description'] for word in ['treaty', 'document', 'manuscript', 'archive']):
           fit += 0.2  # Document-friendly bonus

       return min(1.0, max(0.0, fit))

   # Only score opportunities with fit >= 0.6
   viable_topics = [t for t in topics if calculate_fit_score(t, PRODUCTION_CONSTRAINTS) >= 0.6]
   ```

3. **Test with known failures:** "Roman Empire animated timeline" should score 0.0 (requires animation). "CIA classified documents on X" should score 0.0 (sources unavailable). If tool surfaces these, filtering is broken.

4. **Make constraints user-editable:** Don't hardcode. As channel grows (hires animator), constraints change. Store in `channel-data/production-constraints.json`, reload on each discovery run.

**Warning signs:**
- Discovery tool outputs 50+ opportunities but creator can't produce any
- Phrase "this would be great IF we had [unavailable resource]" repeated
- Gap between research phase and script phase growing (topics dying in research)
- Tool accuracy rated "good" but no videos shipped from discovered topics

**Detection:**
- Track discovery-to-production conversion rate: `videos_shipped / topics_researched`
- If rate <20% after first 10 topics, filtering is too permissive
- Survey unproduced topics: categorize WHY they failed (constraints, not quality)

**Phase to address:** Phase 1 (Demand Research) — Add constraint filtering BEFORE volume/competition scoring

---

### Pitfall 2: Data Staleness and Opportunity Window Closure

**What goes wrong:** Tool identifies "low competition" opportunity in January, creator starts research in February, completes script in March, publishes in April — and by then 5 competitors have covered it. Window closed.

**Why it happens:** YouTube moves fast. VidIQ scan showing "only 3 videos on this topic" is a snapshot. Tool doesn't track: trending momentum (is competition growing?), deadline urgency (treaty expiring, court ruling pending), or search volume trajectory (spiking or declining?). Historical channel data shows outlier performers had news hooks (Belize: ICJ ruling, Somaliland: recognition debates).

**Consequences:**
- Publish into saturated space after months of work
- Low impressions despite "high volume" keyword (outdated data)
- Missed first-mover advantage on breaking historical relevance
- Creator frustration: "tool said this was an opportunity!"

**Prevention:**
1. **Add timestamp tracking to ALL data:**
   ```sql
   CREATE TABLE opportunities (
       id INTEGER PRIMARY KEY,
       topic TEXT,
       demand_score REAL,
       competition_score REAL,
       opportunity_score REAL,
       discovered_at TIMESTAMP NOT NULL,
       competition_count INTEGER,
       last_refreshed TIMESTAMP,
       -- CRITICAL: Track data age
       days_since_refresh INTEGER GENERATED ALWAYS AS (
           julianday('now') - julianday(last_refreshed)
       ) STORED
   );

   -- Flag stale opportunities
   CREATE VIEW stale_opportunities AS
   SELECT * FROM opportunities WHERE days_since_refresh > 7;
   ```

2. **Implement competition growth tracking:**
   ```python
   def check_opportunity_staleness(topic_id):
       # Re-scrape competition weekly
       current_competition = count_youtube_videos(topic)
       original_competition = db.get_original_competition(topic_id)

       growth_rate = (current_competition - original_competition) / original_competition

       if growth_rate > 0.5:  # 50% more competitors
           return {
               'status': 'CLOSING',
               'urgency': 'HIGH',
               'message': f'Competition grew {growth_rate*100:.0f}% since discovery',
               'action': 'Prioritize or skip'
           }

       return {'status': 'OPEN', 'urgency': 'NORMAL'}
   ```

3. **Add deadline/urgency detection:**
   ```python
   URGENCY_PATTERNS = {
       'treaty_expiring': r'treaty.*(?:expires|expiring|ends).*(\d{4})',
       'court_ruling_pending': r'ICJ|court.*(?:ruling|decision|judgment).*(\d{4})',
       'anniversary': r'(\d+)(?:th|st|nd|rd)?\s+anniversary',
       'news_hook': r'(?:2026|2027|recently|latest|current)'
   }

   def detect_urgency(topic_description):
       for pattern_name, regex in URGENCY_PATTERNS.items():
           if match := re.search(regex, topic_description, re.IGNORECASE):
               if pattern_name == 'news_hook':
                   return {'urgency': 'HIGH', 'reason': 'Current event connection'}
               elif pattern_name in ['treaty_expiring', 'court_ruling_pending']:
                   year = int(match.group(1))
                   if year <= 2027:
                       return {'urgency': 'CRITICAL', 'reason': f'Deadline: {year}'}

       return {'urgency': 'NORMAL', 'reason': 'Evergreen topic'}
   ```

4. **Prioritize by urgency × opportunity:**
   - `CRITICAL urgency + high opportunity = produce NOW`
   - `NORMAL urgency + high opportunity = queue for next cycle`
   - `CLOSING window + medium opportunity = skip, too late`

**Warning signs:**
- Topics marked "low competition" at discovery now have 10+ videos
- Published videos underperform despite "high opportunity" score at research time
- Competitor channels release similar videos 2-4 weeks before yours
- Search volume dropped 50%+ between research and publish

**Detection:**
- Weekly: Re-scrape competition count for queued topics, compare to original
- Monthly: Compare predicted vs. actual impressions for published videos
- If >30% of videos have "opportunity closed by publish time," data refresh cadence too slow

**Phase to address:**
- Phase 1 (Demand Research) — Add timestamp tracking
- Phase 2 (Competition Analysis) — Add competition growth monitoring
- Ongoing — Weekly refresh of queued opportunities

---

### Pitfall 3: Invisible Filtering Errors (False Negatives)

**What goes wrong:** Discovery tool misses perfect opportunities because filtering rules are too restrictive or pattern matching fails. Creator manually finds great topic that tool never surfaced.

**Why it happens:** Overly conservative filters ("MUST have 10K+ search volume") eliminate long-tail winners. Keyword pattern matching misses semantic variations ("Velvet Divorce" vs "Czechoslovakia split peacefully" vs "how Czech and Slovak separated"). Intent classification fails on ambiguous queries. Historical channel data shows Belize (23K views) came from territorial dispute category, but search query was "Guatemala claims Belize" — no "dispute" keyword.

**Consequences:**
- Tool develops reputation for "missing the good ones"
- Creator stops trusting tool, reverts to manual research
- Entire system becomes unused despite development investment
- No learning loop to improve filters (invisible failures)

**Prevention:**
1. **Log ALL candidates before filtering, track what was eliminated:**
   ```python
   def discover_opportunities(seed_topics):
       raw_candidates = []

       for seed in seed_topics:
           autocomplete_results = scrape_youtube_autocomplete(seed)
           raw_candidates.extend(autocomplete_results)

       # CRITICAL: Log before filtering
       db.log_raw_candidates(raw_candidates, source='autocomplete', timestamp=now())

       # Apply filters
       filtered = []
       eliminated = {'reasons': {}}

       for candidate in raw_candidates:
           filters_passed, failure_reason = apply_all_filters(candidate)

           if filters_passed:
               filtered.append(candidate)
           else:
               # Track WHY eliminated
               eliminated['reasons'][failure_reason] = eliminated['reasons'].get(failure_reason, 0) + 1
               db.log_eliminated_candidate(candidate, reason=failure_reason)

       # Alert if elimination rate >80%
       elimination_rate = len(eliminated) / len(raw_candidates)
       if elimination_rate > 0.8:
           log_warning(f'High elimination rate ({elimination_rate*100:.0f}%). Filters may be too restrictive.')

       return filtered, eliminated
   ```

2. **Implement "manual override" feedback loop:**
   ```python
   # When creator manually selects topic tool didn't surface
   def log_missed_opportunity(topic, actual_performance):
       # Find if topic was in raw candidates but filtered out
       elimination_record = db.get_elimination_record(topic)

       if elimination_record:
           # Tool saw it but filtered it
           db.log_filter_failure({
               'topic': topic,
               'eliminated_reason': elimination_record['reason'],
               'actual_performance': actual_performance,
               'should_have_surfaced': True
           })

           # Suggest filter adjustment
           if elimination_record['reason'] == 'search_volume_too_low':
               current_threshold = FILTERS['min_search_volume']
               topic_volume = elimination_record['search_volume']
               suggest_threshold_reduction(current_threshold, topic_volume)
       else:
           # Tool never saw it (autocomplete seed gap)
           db.log_autocomplete_gap({
               'topic': topic,
               'missing_seed': infer_seed_keyword(topic),
               'action': 'Add seed to discovery prompts'
           })
   ```

3. **Add semantic similarity matching, not just keyword exact match:**
   ```python
   # Don't just match "territorial dispute" keyword
   # Match semantic intent: border, claim, conflict, sovereignty, etc.

   SEMANTIC_CLUSTERS = {
       'territorial_dispute': ['border', 'claim', 'conflict', 'sovereignty', 'dispute',
                               'territory', 'demarcation', 'delimitation', 'frontier'],
       'myth_busting': ['myth', 'false', 'true', 'actually', 'fact check', 'misconception',
                        'debunk', 'really', 'truth about'],
       'primary_source': ['treaty', 'document', 'manuscript', 'archive', 'original',
                          'agreement', 'text', 'decree', 'proclamation']
   }

   def classify_intent_semantic(query):
       query_lower = query.lower()

       for intent, keywords in SEMANTIC_CLUSTERS.items():
           # Any keyword match triggers classification
           if any(kw in query_lower for kw in keywords):
               matched = [kw for kw in keywords if kw in query_lower]
               return {
                   'intent': intent,
                   'confidence': len(matched) / len(keywords),
                   'matched_terms': matched
               }

       return {'intent': 'UNKNOWN', 'confidence': 0.0}
   ```

4. **Run "smoke test" with known winners:**
   ```python
   # Topics that actually performed well
   KNOWN_WINNERS = [
       {'topic': 'Guatemala claims Belize', 'views': 23000, 'should_surface': True},
       {'topic': 'Somaliland independence', 'views': 8000, 'should_surface': True},
       {'topic': 'medieval flat earth myth', 'views': 5000, 'should_surface': True}
   ]

   def test_filter_false_negatives():
       missed = []

       for winner in KNOWN_WINNERS:
           # Run through current filters
           passes_filters = apply_all_filters(winner)

           if not passes_filters and winner['should_surface']:
               missed.append({
                   'topic': winner['topic'],
                   'actual_views': winner['views'],
                   'failed_filter': get_failure_reason(winner)
               })

       if missed:
           log_error(f'Filter false negatives: {len(missed)} known winners eliminated')
           for m in missed:
               log_error(f"  - {m['topic']} ({m['actual_views']} views) failed: {m['failed_filter']}")

           raise ValueError('Filters too restrictive. Adjust thresholds.')
   ```

**Warning signs:**
- Creator frequently says "I found a great topic manually that the tool missed"
- Elimination rate >80% in discovery runs
- Known high-performing topics fail filter smoke test
- Discovery tool output feels "generic" or "safe" (avoiding anything interesting)

**Detection:**
- Monthly: Run smoke test with known winners, ensure they pass current filters
- After each published video: Check if topic was in raw candidates, why it was/wasn't surfaced
- Track manual override frequency: if >30% of videos came from manual research, tool is underperforming

**Phase to address:**
- Phase 1 (Demand Research) — Add raw candidate logging
- Phase 2 (Competition Analysis) — Add semantic similarity matching
- Phase 3 (Format Filtering) — Implement smoke testing with known winners
- Ongoing — Manual override feedback loop after each video

---

## Moderate Pitfalls

### Pitfall 4: Competitor Analysis Without Context

**What goes wrong:** Tool shows "Kraut covered this topic, 2M views" and recommends skipping it. But Kraut's video was 2 hours long with countryball animation — different format, different angle. There's still an opening for 10-minute document-focused version.

**Why it happens:** Competitor analysis tracks "who covered what" but not "how they covered it" (format, angle, length, sources). A topic can be "covered" but still have gaps. Channel DNA shows competitive advantage is showing primary sources on screen, which most competitors don't do. Simply avoiding "covered topics" eliminates differentiation opportunities.

**Prevention:**
1. **Track competitor coverage attributes, not just binary covered/uncovered:**
   ```sql
   CREATE TABLE competitor_coverage (
       id INTEGER PRIMARY KEY,
       topic TEXT,
       competitor_channel TEXT,
       video_id TEXT,
       views INTEGER,
       video_length_minutes INTEGER,
       format TEXT,  -- 'animation', 'talking_head', 'documentary', 'lecture'
       primary_sources_shown BOOLEAN,  -- CRITICAL: your differentiator
       angle TEXT,   -- 'political', 'legal', 'economic', 'cultural'
       upload_date DATE
   );

   -- Find gap opportunities
   CREATE VIEW coverage_gaps AS
   SELECT
       topic,
       COUNT(*) as competitor_count,
       SUM(CASE WHEN primary_sources_shown = 1 THEN 1 ELSE 0 END) as source_focused_count,
       MAX(views) as top_views
   FROM competitor_coverage
   GROUP BY topic
   HAVING source_focused_count = 0  -- NO ONE showed primary sources
   ORDER BY competitor_count DESC;  -- Most interest but gap in YOUR approach
   ```

2. **Add differentiation scoring:**
   ```python
   def calculate_differentiation_score(topic, your_approach):
       competitors = db.get_competitor_coverage(topic)

       if not competitors:
           return 1.0  # No competition, full differentiation

       differentiation = 0.0

       for comp in competitors:
           # Same format = low differentiation
           if comp['format'] == your_approach['format']:
               differentiation -= 0.2

           # They showed primary sources = no differentiator
           if comp['primary_sources_shown'] == True:
               differentiation -= 0.3

           # Different angle = opportunity
           if comp['angle'] != your_approach['angle']:
               differentiation += 0.2

           # Much longer/shorter = different value prop
           length_ratio = abs(comp['video_length_minutes'] - your_approach['target_length']) / your_approach['target_length']
           if length_ratio > 0.5:  # 50%+ difference
               differentiation += 0.1

       return max(0.0, min(1.0, 0.5 + differentiation))

   YOUR_APPROACH = {
       'format': 'talking_head_with_broll',
       'primary_sources_shown': True,  # KEY DIFFERENTIATOR
       'angle': 'legal_documentary',
       'target_length': 12  # minutes
   }
   ```

3. **Ask "What angle is missing?" not just "Is it covered?":**
   - Topic: "Library of Alexandria burning"
   - Competitor 1: Animated timeline, 20 min, political angle
   - Competitor 2: Documentary, 40 min, cultural loss angle
   - **Your gap:** Legal/documentary angle, 10-12 min, show PRIMARY SOURCES about what was actually lost (show the evidence, not narratives)

**Warning signs:**
- Tool eliminates all "popular topics" due to competitor presence
- Discoveries feel niche/obscure but don't perform (no existing demand validation)
- Missing opportunities like "covered topic, but poorly" or "covered topic, different angle"

**Phase to address:** Phase 2 (Competition Analysis) — Add format/angle tracking to competitor coverage

---

### Pitfall 5: VidIQ Integration Without Accuracy Tracking

**What goes wrong:** VidIQ says "10K monthly searches," you build video expecting 5K impressions minimum, you get 200. Trust in tool erodes. No learning loop to calibrate VidIQ predictions to YOUR channel's actual performance.

**Why it happens:** VidIQ estimates search volume using proprietary models. They claim 85% accuracy overall, but accuracy varies by: channel size (small channels see different results), niche specificity (obscure history topics less accurate than mainstream), and keyword type (long-tail vs. head terms). Without tracking predictions vs. reality, you can't calibrate.

**Prevention:**
1. **Log VidIQ predictions at research time:**
   ```sql
   CREATE TABLE vidiq_predictions (
       id INTEGER PRIMARY KEY,
       topic TEXT,
       video_id TEXT,  -- NULL until published
       predicted_search_volume INTEGER,
       predicted_competition_score REAL,
       predicted_overall_score REAL,
       prediction_date DATE,
       -- Actual performance (filled post-publish)
       actual_impressions INTEGER,
       actual_views INTEGER,
       actual_ctr REAL,
       measured_at DATE,
       -- Accuracy metrics
       volume_accuracy REAL GENERATED ALWAYS AS (
           CASE
               WHEN actual_impressions IS NULL THEN NULL
               ELSE 1.0 - ABS(predicted_search_volume - actual_impressions) / predicted_search_volume
           END
       ) STORED
   );
   ```

2. **Calculate channel-specific calibration factors:**
   ```python
   def calibrate_vidiq_predictions():
       # After 10+ videos with VidIQ data
       predictions = db.get_vidiq_predictions_with_actuals()

       if len(predictions) < 10:
           return {'status': 'INSUFFICIENT_DATA', 'message': 'Need 10+ videos to calibrate'}

       # Calculate average variance
       volume_errors = []
       for pred in predictions:
           predicted = pred['predicted_search_volume']
           actual = pred['actual_impressions']
           error = (actual - predicted) / predicted  # Percentage error
           volume_errors.append(error)

       avg_error = sum(volume_errors) / len(volume_errors)

       # Generate calibration factor
       calibration = {
           'average_error': avg_error,
           'adjustment_factor': 1.0 + avg_error,
           'confidence_interval': calculate_ci(volume_errors),
           'recommendation': f'Multiply VidIQ volume by {1.0 + avg_error:.2f} for this channel'
       }

       # Apply to future predictions
       return calibration

   # Example: If VidIQ consistently OVER-predicts by 40%
   # avg_error = -0.4
   # adjustment_factor = 0.6
   # Future prediction: VidIQ says 10K → Calibrated: 6K
   ```

3. **Segment accuracy by topic category:**
   ```python
   # VidIQ might be accurate for territorial disputes, less for ideological myths

   def calculate_category_specific_accuracy():
       categories = ['territorial_dispute', 'myth_busting', 'primary_source', 'ideological_narrative']

       accuracy_by_category = {}

       for category in categories:
           preds = db.get_vidiq_predictions_by_intent(category)

           if len(preds) >= 3:  # Minimum for meaningful stats
               errors = [calc_error(p) for p in preds]
               accuracy_by_category[category] = {
                   'avg_accuracy': sum(errors) / len(errors),
                   'sample_size': len(preds),
                   'trust_level': 'HIGH' if len(preds) >= 5 else 'MEDIUM'
               }

       return accuracy_by_category

   # Use in filtering:
   # If myth_busting has low VidIQ accuracy, weight VidIQ score less for those topics
   ```

**Warning signs:**
- Consistent mismatch between VidIQ "high score" and actual impressions
- Creator stops checking VidIQ because "it's always wrong"
- No systematic tracking of prediction accuracy over time

**Phase to address:**
- Phase 1 (Demand Research) — Add VidIQ prediction logging
- Post-publish (ongoing) — Fill in actual performance, calculate accuracy
- After 10 videos — Generate calibration factors

---

### Pitfall 6: Discovery-Publish Workflow Disconnect

**What goes wrong:** Discovery tool runs separately from production workflow. Topics discovered in January sit in spreadsheet, forgotten by March. No connection between `/discover` command and `/research --new` command. No tracking of which discovered topics entered production vs. abandoned.

**Why it happens:** Building discovery as standalone tool instead of integrating into existing workflow. User must manually transfer data from discovery output to research input. No lifecycle tracking from "opportunity identified" → "research started" → "script written" → "published." Historical project data shows 30+ videos in production with no clear source tracking.

**Prevention:**
1. **Extend existing `/research --new` command to accept discovery data:**
   ```python
   # BEFORE (manual)
   # 1. Run: python tools/discovery/find_opportunities.py > topics.txt
   # 2. Read topics.txt
   # 3. Run: /research --new --topic "Velvet Divorce"
   # 4. No connection between discovery and research

   # AFTER (integrated)
   # /discover --seed "czechoslovakia"  # Generates opportunities with IDs
   # /research --new --from-discovery OPP_12345  # Starts research from opportunity record

   @command('/research')
   def research_command(args):
       if args.from_discovery:
           # Load opportunity data
           opp = db.get_opportunity(args.from_discovery)

           # Pre-fill research template
           project_dir = create_project_dir(opp['topic'])

           # Copy discovery metadata
           write_file(f'{project_dir}/00-DISCOVERY-DATA.md', {
               'discovered_at': opp['discovered_at'],
               'predicted_volume': opp['search_volume'],
               'competition_count': opp['competition_count'],
               'intent_category': opp['primary_intent'],
               'opportunity_score': opp['opportunity_score'],
               'keywords': opp['related_keywords']
           })

           # Mark opportunity as "in_research"
           db.update_opportunity_status(args.from_discovery, status='IN_RESEARCH')
       else:
           # Manual topic entry (existing flow)
           pass
   ```

2. **Add lifecycle tracking to opportunities table:**
   ```sql
   CREATE TABLE opportunities (
       id INTEGER PRIMARY KEY,
       topic TEXT,
       opportunity_score REAL,
       discovered_at TIMESTAMP,
       -- Lifecycle tracking
       status TEXT DEFAULT 'DISCOVERED',  -- DISCOVERED, IN_RESEARCH, SCRIPTED, PUBLISHED, ABANDONED
       project_folder TEXT,  -- Link to video-projects/...
       video_id TEXT,  -- YouTube video ID after publish
       status_updated_at TIMESTAMP,
       abandoned_reason TEXT,
       -- Performance tracking
       predicted_impressions INTEGER,
       actual_impressions INTEGER,
       prediction_accuracy REAL
   );

   -- View: Opportunities by lifecycle stage
   CREATE VIEW opportunity_funnel AS
   SELECT
       status,
       COUNT(*) as count,
       AVG(opportunity_score) as avg_score,
       AVG(JULIANDAY(status_updated_at) - JULIANDAY(discovered_at)) as avg_days_in_stage
   FROM opportunities
   GROUP BY status;
   ```

3. **Add conversion tracking to measure discovery ROI:**
   ```python
   def calculate_discovery_roi():
       funnel = db.query('SELECT * FROM opportunity_funnel')

       discovered = funnel['DISCOVERED']['count']
       published = funnel['PUBLISHED']['count']
       abandoned = funnel['ABANDONED']['count']

       conversion_rate = published / discovered if discovered > 0 else 0

       # Target: 20%+ of discovered topics should reach publish
       if conversion_rate < 0.2:
           alert = {
               'status': 'LOW_CONVERSION',
               'rate': conversion_rate,
               'issue': 'Too many discovered topics abandoned',
               'likely_causes': [
                   'Discovery filters too permissive (surfacing unproduceable topics)',
                   'Production constraints changed (tool not updated)',
                   'Opportunity window closing (staleness issue)',
                   'Duplicate discovery (same topic found multiple times)'
               ],
               'action': 'Review abandoned_reason column for patterns'
           }

           return alert

       return {'status': 'HEALTHY', 'conversion_rate': conversion_rate}
   ```

4. **Make discovery-to-research transition one command:**
   ```bash
   # Instead of multi-step manual process

   # One command creates project from opportunity
   /research --new --from-discovery OPP_12345

   # This should:
   # 1. Create video-projects/_IN_PRODUCTION/XX-topic-2026/
   # 2. Copy discovery metadata to 00-DISCOVERY-DATA.md
   # 3. Update opportunity status to IN_RESEARCH
   # 4. Pre-fill NOTEBOOKLM-SOURCE-LIST.md with competitor sources
   # 5. Generate initial keyword list for metadata
   ```

**Warning signs:**
- Discovery tool output sits in files/spreadsheets, not acted on
- No tracking of "what happened to discovered opportunities"
- Creator can't answer "which videos came from discovery tool?"
- Manual data transfer between discovery → research → script phases

**Phase to address:**
- Phase 1 (Demand Research) — Add lifecycle tracking to opportunities table
- Phase 5 (Opportunity Scoring) — Integrate with `/research --new` command
- Ongoing — Track conversion metrics, review abandonment reasons

---

### Pitfall 7: Format Filtering Based on Assumptions, Not Data

**What goes wrong:** Filter eliminates topics requiring "historical photos" assuming they're hard to find. Actually, many topics have rich public domain archives (Wikimedia Commons, Library of Congress, national archives). Filter is overly conservative based on incorrect assumption.

**Why it happens:** Production constraints defined based on past experience or guesses, not systematic audit of actual asset availability. "We can't do X" becomes filter rule without validating if X is truly impossible. Existing codebase shows B-roll download links for multiple videos — asset sourcing is solved for many topics.

**Prevention:**
1. **Test format constraints with sample topics before hardcoding:**
   ```python
   # DON'T: Hardcode assumptions
   ASSUMED_CONSTRAINTS = {
       'requires_historical_photos': False,  # "We can't get these"
       'requires_map_graphics': True,  # "We can make these"
   }

   # DO: Validate with sample topics
   def validate_format_constraints():
       test_topics = [
           'Sykes-Picot Agreement 1916',  # Requires: map, historical photo, treaty text
           'Library of Alexandria',  # Requires: historical illustration, manuscript photos
           'Chagos Islands dispute'  # Requires: modern map, treaty documents
       ]

       for topic in test_topics:
           asset_check = check_asset_availability(topic)

           print(f'\n{topic}:')
           print(f'  Historical photos: {asset_check["historical_photos"]["available"]} ({asset_check["historical_photos"]["source"]})')
           print(f'  Maps: {asset_check["maps"]["available"]} ({asset_check["maps"]["source"]})')
           print(f'  Documents: {asset_check["documents"]["available"]} ({asset_check["documents"]["source"]})')

   def check_asset_availability(topic):
       # Check common sources
       sources = {
           'historical_photos': check_wikimedia_commons(topic),
           'maps': check_david_rumsey_maps(topic),
           'documents': check_internet_archive(topic)
       }

       return sources
   ```

2. **Make format scoring graduated, not binary:**
   ```python
   # DON'T: Binary "can/can't produce"
   if topic['requires_animation']:
       return REJECT

   # DO: Graduated scoring
   def calculate_asset_difficulty_score(topic):
       difficulty = 0.0  # 0 = easy, 1 = very difficult

       asset_requirements = extract_asset_requirements(topic)

       for asset_type, required_count in asset_requirements.items():
           if asset_type == 'animation':
               difficulty += 0.5 * required_count  # High difficulty
           elif asset_type == 'historical_photos':
               # Check if public domain available
               if check_public_domain_availability(topic, asset_type):
                   difficulty += 0.1 * required_count  # Low difficulty
               else:
                   difficulty += 0.3 * required_count  # Medium difficulty
           elif asset_type == 'maps':
               difficulty += 0.1 * required_count  # Usually easy (can create or find)

       return min(1.0, difficulty)

   # Use in scoring: topics with difficulty <0.4 = green light, 0.4-0.7 = research further, >0.7 = likely too hard
   ```

3. **Build asset source database from past videos:**
   ```python
   # Mine existing B-ROLL-DOWNLOAD-LINKS.md files

   def build_asset_source_database():
       projects = glob('video-projects/_IN_PRODUCTION/*/B-ROLL-DOWNLOAD-LINKS.md')

       asset_sources = {}

       for project in projects:
           topic = extract_topic_from_path(project)
           links = parse_broll_links(project)

           for link in links:
               source_domain = extract_domain(link['url'])
               asset_type = link['type']  # 'map', 'photo', 'document', etc.

               if source_domain not in asset_sources:
                   asset_sources[source_domain] = {
                       'topics_used': [],
                       'asset_types': set(),
                       'reliability': 'HIGH'  # Proven by past usage
                   }

               asset_sources[source_domain]['topics_used'].append(topic)
               asset_sources[source_domain]['asset_types'].add(asset_type)

       # Generate reusable asset source checklist
       save_json('channel-data/proven-asset-sources.json', asset_sources)

   # Examples from existing videos:
   # - Wikimedia Commons: historical photos, maps (used in Bir Tawil, Belize, Somaliland)
   # - David Rumsey Historical Map Collection: detailed historical maps
   # - Internet Archive: treaty documents, government publications
   # - National Archives (UK, US): declassified documents
   ```

4. **Add asset pre-check to opportunity scoring:**
   ```python
   def score_asset_feasibility(topic):
       # Before eliminating topic due to "requires historical photos"
       # Actually check if photos exist

       asset_sources = load_json('channel-data/proven-asset-sources.json')

       required_assets = extract_asset_requirements(topic)

       feasibility = 1.0  # Start optimistic

       for asset_type in required_assets:
           # Check proven sources
           available_sources = [
               source for source, data in asset_sources.items()
               if asset_type in data['asset_types']
           ]

           if not available_sources:
               # Not found in proven sources, but doesn't mean impossible
               # Reduce feasibility but don't eliminate
               feasibility -= 0.2
           elif len(available_sources) >= 2:
               # Multiple proven sources = high confidence
               feasibility += 0.1

       return max(0.0, min(1.0, feasibility))
   ```

**Warning signs:**
- Filter eliminates topics that creator manually researches and finds produceable
- Asset sourcing "problems" that don't actually materialize in production
- Overly narrow topic selection (only very specific format types pass)

**Phase to address:**
- Phase 3 (Format Filtering) — Mine existing B-ROLL-DOWNLOAD-LINKS.md files
- Phase 3 (Format Filtering) — Validate constraints with sample topics
- Phase 5 (Opportunity Scoring) — Add asset feasibility checking

---

## Minor Pitfalls

### Pitfall 8: Search Intent Ambiguity Without Context

**What goes wrong:** Keyword "crusades" classified as MYTH_BUSTING intent, but searcher actually wants timeline. Video about "were crusades defensive myth" doesn't match what viewer wanted. High CTR, low retention, algorithm penalizes.

**Why it happens:** Single keywords are ambiguous. "Crusades" could be: myth-busting ("were crusades defensive?"), timeline ("when did crusades happen?"), territorial ("crusades impact on Middle East borders"), or ideological ("crusades in modern politics"). Without full query context, classification guesses.

**Prevention:**
- Require minimum query length (3+ words) for intent classification
- Support multi-intent (primary + secondary) for complex queries
- Use full autocomplete queries, not extracted single keywords
- Validate classification against video performance (does intent predict retention?)

**Phase to address:** Phase 1 (Demand Research) — Add query length requirements to intent classifier

---

### Pitfall 9: Not Tracking WHY Opportunities Were Abandoned

**What goes wrong:** 20 opportunities discovered, only 2 published, no record of why 18 were abandoned. Can't learn from failures, repeat same filtering mistakes.

**Why it happens:** No systematic logging of abandonment reasons. Creator moves on to next topic without documenting "why not this one?"

**Prevention:**
- Add `abandoned_reason` column to opportunities table
- Require reason selection when marking opportunity as abandoned: `ASSET_UNAVAILABLE`, `COMPETITION_GREW`, `SOURCE_INACCESSIBLE`, `SCOPE_TOO_LARGE`, `DUPLICATE`, `LOST_INTEREST`
- Monthly: Review abandonment patterns, adjust filters to reduce preventable abandonments

**Phase to address:** Phase 5 (Opportunity Scoring) — Add abandonment tracking

---

### Pitfall 10: Keyword Database Growth Without Maintenance

**What goes wrong:** After 6 months, keyword database has 10,000+ entries. Query performance degrades. Stale entries (discovered 6 months ago, never used) clutter results. No cleanup strategy.

**Why it happens:** Aggressive autocomplete scraping accumulates keywords fast. No expiration policy. No archival strategy for keywords that proved irrelevant.

**Prevention:**
- Add `status` field: `ACTIVE`, `ARCHIVED`, `INVALID`
- Monthly: Archive keywords discovered >90 days ago with no associated videos
- Add last_accessed timestamp, query from most-recently-used first
- Limit active keyword pool to most recent 6 months unless explicitly marked evergreen

**Phase to address:** Ongoing maintenance (document in Phase 5 implementation plan)

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|----------------|------------|
| Phase 1: Demand Research | VidIQ predictions treated as ground truth | Add prediction logging, calculate accuracy after 10 videos |
| Phase 1: Demand Research | Rate limiting from YouTube autocomplete | Implement exponential backoff, stealth browser automation |
| Phase 2: Competition Analysis | Binary "covered/uncovered" without format differentiation | Track competitor format, angle, primary source usage |
| Phase 3: Format Filtering | Overly restrictive assumptions about asset availability | Validate constraints with sample topics, mine existing B-roll links |
| Phase 4: Niche Scoring | Ignoring production timeline in opportunity ranking | Add urgency detection, flag closing windows |
| Phase 5: Opportunity Scoring | No connection to existing `/research` workflow | Integrate discovery into project creation, track lifecycle |
| Ongoing | No learning loop from published videos back to filters | Track predicted vs actual performance, calibrate filters quarterly |

---

## Quality Checklist

Before launching niche discovery tool, verify:

**Data Quality:**
- [ ] VidIQ predictions logged with timestamps for accuracy tracking
- [ ] Autocomplete scraper has rate limiting (2s+ delay, exponential backoff)
- [ ] Competition data refreshed weekly for queued opportunities
- [ ] Opportunity staleness detection (flag if >7 days old)

**Filtering Accuracy:**
- [ ] Production constraints documented in editable config file
- [ ] Fit scoring tested with known winners (smoke test passes)
- [ ] Raw candidates logged before filtering (track elimination reasons)
- [ ] Semantic similarity matching for intent (not just keyword exact match)

**Integration:**
- [ ] Discovery integrates with `/research --new` command (one-click project creation)
- [ ] Lifecycle tracking implemented (DISCOVERED → IN_RESEARCH → SCRIPTED → PUBLISHED)
- [ ] Abandonment reason required when marking opportunity skipped
- [ ] Conversion rate tracking (target: 20%+ discovered → published)

**Learning Loop:**
- [ ] Predicted vs. actual performance tracking after publish
- [ ] Monthly filter calibration based on accuracy data
- [ ] Quarterly review of abandoned opportunities for filter improvement
- [ ] Channel-specific VidIQ calibration factor after 10 videos

---

## Sources

**High Confidence (WebSearch + Official Documentation):**
- [YouTube Niche Discovery Mistakes 2026](https://packapop.com/blogs/youtube-success-blog/youtube-mistakes) - Common creator errors including starting trends too late, poor discovery elements
- [YouTube Keyword Research Pitfalls](https://outlierkit.com/blog/ahrefs-youtube-keyword-tool-alternative) - Accuracy issues with SEO tools, competition analysis errors
- [YouTube Automation Mistakes 2026](https://www.facelessyoutubechannelidea.com/p/the-harsh-truth-about-youtube-automation-no-one-talks-about-2026-update) - Quality control failures, zero oversight traps
- [Content Production Workflow Errors](https://www.podcastvideos.com/articles/outdated-content-workflows-2026/) - Lack of documentation, inconsistent strategy
- [YouTube Topic Discovery Best Practices](https://cscestudiodigital.com/blog/youtube-automation-with-ai-what-really-looks-like-in-2026/) - Topic selection errors, niche strategy failures
- [TubeLab Niche Finder Reviews](https://outlierkit.com/blog/tubelab-reviews-features-alternatives) - Tool accuracy issues, integration problems
- [YouTube Niche Finder Tools 2026](https://outlierkit.com/blog/best-niche-finder-tools-for-youtube) - Data quality issues, false positives

**Medium Confidence (Project Context):**
- Existing phase research documents (`.planning/phases/06-competitive-intelligence/06-RESEARCH.md`, `.planning/phases/13-discovery-tools/13-RESEARCH.md`)
- Channel performance data (`COMPETITOR-TITLE-DATABASE.md`, `OUTLIER-TOPIC-IDEAS.md`)
- Existing tools architecture (`tools/discovery/autocomplete.py`, `tools/script-checkers/`)

**Inferred from Requirements:**
- Production constraints from PROJECT.md ("no animation, academic sources required, solo creator")
- Channel DNA from CLAUDE.md ("documentary tone, primary sources on screen, history-first not geopolitics-first")
- Known winners from project context (Belize 23K views, territorial disputes perform well)

---

*Research completed: 2026-01-31*
*Confidence: HIGH (web-verified pitfalls + project-specific context)*
*Next step: Use in roadmap creation for Phase 14.1 niche discovery implementation*
