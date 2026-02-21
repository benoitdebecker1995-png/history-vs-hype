"""
refresh.py — Full refresh orchestrator for the YouTube Intelligence Engine

Runs the complete 10-phase pipeline:
    Phase 1:  Scrape algorithm sources      (algo_scraper)
    Phase 2:  Synthesize algorithm knowledge (algo_synthesizer — text analysis mode)
    Phase 3:  Save algorithm snapshot        (KBStore)
    Phase 4:  Fetch all competitors          (competitor_tracker)
    Phase 5:  Purge old competitor videos    (KBStore — purge-and-replace)
    Phase 6:  Save new competitor videos     (KBStore)
    Phase 7:  Detect outliers                (pattern_analyzer)
    Phase 8:  Extract niche patterns + save  (pattern_analyzer + KBStore)
    Phase 9:  Export to Markdown             (kb_exporter)
    Phase 10: Update last_refresh timestamp  (KBStore)

Errors are collected and returned without stopping the pipeline (unless fatal).
Progress is printed to stdout for visibility when run interactively.

All public functions follow the error-dict pattern.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Module imports (all collected here for easy error surfacing)
# ---------------------------------------------------------------------------
from tools.intel.kb_store import KBStore
from tools.intel.algo_scraper import scrape_all_sources
from tools.intel.algo_synthesizer import synthesize_with_text_analysis
from tools.intel.competitor_tracker import fetch_all_competitors, load_channel_config
from tools.intel.pattern_analyzer import detect_outliers, extract_niche_patterns
from tools.intel.kb_exporter import export_kb_to_markdown

# Default paths
_INTEL_DIR = Path(__file__).parent
_DEFAULT_DB_PATH = str(_INTEL_DIR / "intel.db")
_DEFAULT_CONFIG_PATH = str(_INTEL_DIR / "competitor_channels.json")


def _now_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _print_phase(phase_num: int, description: str) -> None:
    """Print phase progress to stdout."""
    print(f"  [{phase_num}/10] {description}...")


# ---------------------------------------------------------------------------
# Bootstrap helper
# ---------------------------------------------------------------------------

def ensure_channels_loaded(store: KBStore) -> None:
    """
    Bootstrap the competitor_channels table from competitor_channels.json.

    Called at the start of refresh. If the table already has entries, this
    is a no-op (won't duplicate channels due to upsert in save_competitor_channel).

    For a completely empty table, loads all channels from the JSON config.
    """
    try:
        existing = store.get_active_channels()
        if existing and not isinstance(existing, dict):
            return  # Already loaded

        channels = load_channel_config(_DEFAULT_CONFIG_PATH)
        if isinstance(channels, dict) and "error" in channels:
            print(f"  [WARNING] Could not load channel config: {channels['error']}")
            return

        for channel in channels:
            channel_id = channel.get("id")
            channel_name = channel.get("name", channel_id)
            category = channel.get("category")
            if channel_id:
                store.save_competitor_channel(
                    channel_id=channel_id,
                    channel_name=channel_name,
                    niche_category=category,
                )
    except Exception as exc:
        # Non-fatal — proceed even if bootstrap fails
        print(f"  [WARNING] ensure_channels_loaded failed: {exc}")


# ---------------------------------------------------------------------------
# Summary helpers
# ---------------------------------------------------------------------------

def get_refresh_summary(refresh_result: dict) -> dict:
    """
    Return a concise summary from a run_refresh() result dict.

    Args:
        refresh_result: The dict returned by run_refresh(), containing keys like
            channels_fetched, videos_total, outliers_found, algo_sources_scraped,
            kb_exported_to, errors, refreshed, skipped, etc.

    Returns:
        {
            'channels_fetched':    int,
            'videos_total':        int,
            'outliers_found':      int,
            'algo_sources_scraped': int,
            'kb_exported_to':      str | None,
            'errors':              list,
            'refreshed':           bool,
        }
    """
    if not isinstance(refresh_result, dict):
        return {"error": f"get_refresh_summary expects a dict, got {type(refresh_result).__name__}"}

    if "error" in refresh_result:
        return refresh_result

    return {
        "channels_fetched":     refresh_result.get("channels_fetched", 0),
        "videos_total":         refresh_result.get("videos_total", 0),
        "outliers_found":       refresh_result.get("outliers_found", 0),
        "algo_sources_scraped": refresh_result.get("algo_sources_scraped", 0),
        "kb_exported_to":       refresh_result.get("kb_exported_to"),
        "errors":               refresh_result.get("errors", []),
        "refreshed":            refresh_result.get("refreshed", False),
    }


# ---------------------------------------------------------------------------
# Main refresh pipeline
# ---------------------------------------------------------------------------

def run_refresh(force: bool = False, db_path: str = None) -> dict:
    """
    Run the complete 10-phase intelligence refresh pipeline.

    Args:
        force:   If True, skip the staleness check and always refresh.
        db_path: Optional path to intel.db (defaults to tools/intel/intel.db).

    Returns:
        {
            'refreshed':             bool,
            'skipped':               bool,           # True if not stale and not forced
            'reason':                str,            # If skipped, why
            'last_refresh':          str,            # ISO timestamp
            'algo_sources_scraped':  int,
            'channels_fetched':      int,
            'videos_total':          int,
            'outliers_found':        int,
            'kb_exported_to':        str,
            'errors':                list[str],
        }
        or {'error': str}  # Fatal — store init failed
    """
    errors = []
    resolved_db = db_path or _DEFAULT_DB_PATH

    # Initialise store
    try:
        store = KBStore(resolved_db)
    except Exception as exc:
        return {"error": f"KBStore init failed: {exc}"}

    # Staleness check (skip if forced)
    if not force:
        is_stale = store.is_stale()
        if not is_stale:
            last = store.get_last_refresh()
            print("  KB is current — skipping refresh. Use force=True to override.")
            return {
                "refreshed":  False,
                "skipped":    True,
                "reason":     "KB is current",
                "last_refresh": last,
                "algo_sources_scraped": 0,
                "channels_fetched": 0,
                "videos_total": 0,
                "outliers_found": 0,
                "kb_exported_to": "",
                "errors": [],
            }

    print("Starting YouTube Intelligence Engine refresh...")

    # -----------------------------------------------------------------------
    # Phase 1: Scrape algorithm sources
    # -----------------------------------------------------------------------
    _print_phase(1, "Scraping algorithm sources")
    scraped_results = []
    try:
        scraped_results = scrape_all_sources()
        successful_scrapes = [r for r in scraped_results if "error" not in r]
        failed_scrapes = [r for r in scraped_results if "error" in r]
        for r in failed_scrapes:
            errors.append(f"Scrape failed: {r['error']}")
        print(f"     Scraped {len(successful_scrapes)}/{len(scraped_results)} sources")
    except Exception as exc:
        errors.append(f"Phase 1 (scrape) failed: {exc}")
        scraped_results = []

    algo_sources_scraped = len([r for r in scraped_results if "error" not in r])

    # -----------------------------------------------------------------------
    # Phase 2: Synthesize algorithm knowledge
    # -----------------------------------------------------------------------
    _print_phase(2, "Synthesizing algorithm knowledge (text-analysis mode)")
    synthesis_result = {}
    try:
        synthesis_result = synthesize_with_text_analysis(scraped_results)
        if "error" in synthesis_result:
            errors.append(f"Phase 2 (synthesize) failed: {synthesis_result['error']}")
            synthesis_result = {}
        else:
            print(f"     Confidence: {synthesis_result.get('confidence', 'unknown')}")
    except Exception as exc:
        errors.append(f"Phase 2 (synthesize) failed: {exc}")

    # -----------------------------------------------------------------------
    # Phase 3: Save algorithm snapshot
    # -----------------------------------------------------------------------
    _print_phase(3, "Saving algorithm snapshot")
    try:
        if synthesis_result and "algorithm_model" in synthesis_result:
            algo_model = synthesis_result["algorithm_model"]
            save_result = store.save_algo_snapshot(
                source_names=synthesis_result.get("sources_used", []),
                algorithm_model=algo_model,
                signal_weights=synthesis_result.get("signal_weights"),
                longform_insights=synthesis_result.get("longform_insights"),
                confidence=synthesis_result.get("confidence", "low"),
            )
            if "error" in save_result:
                errors.append(f"Phase 3 (save algo) failed: {save_result['error']}")
            else:
                print(f"     Snapshot id={save_result.get('id')}")
        else:
            errors.append("Phase 3 skipped: no synthesis result to save")
    except Exception as exc:
        errors.append(f"Phase 3 (save algo) failed: {exc}")

    # -----------------------------------------------------------------------
    # Phase 4: Bootstrap channels + fetch competitor feeds
    # -----------------------------------------------------------------------
    _print_phase(4, "Fetching competitor feeds")
    ensure_channels_loaded(store)

    competitor_result = {"channels_fetched": 0, "videos_total": 0, "videos": [], "errors": []}
    try:
        competitor_result = fetch_all_competitors()
        if isinstance(competitor_result, dict) and "error" in competitor_result:
            errors.append(f"Phase 4 (fetch competitors) failed: {competitor_result['error']}")
            competitor_result = {"channels_fetched": 0, "videos_total": 0, "videos": [], "errors": []}
        else:
            for err in competitor_result.get("errors", []):
                errors.append(f"Competitor fetch: {err}")
            print(f"     Fetched {competitor_result.get('channels_fetched', 0)} channels, "
                  f"{competitor_result.get('videos_total', 0)} videos")
    except Exception as exc:
        errors.append(f"Phase 4 (fetch competitors) failed: {exc}")

    channels_fetched = competitor_result.get("channels_fetched", 0)
    raw_videos = competitor_result.get("videos", [])

    # -----------------------------------------------------------------------
    # Phase 5: Purge old competitor videos (purge-and-replace)
    # -----------------------------------------------------------------------
    _print_phase(5, "Purging old competitor videos")
    try:
        purge_result = store.purge_competitor_videos()
        if "error" in purge_result:
            errors.append(f"Phase 5 (purge) failed: {purge_result['error']}")
        else:
            print(f"     Purged {purge_result.get('deleted', 0)} old videos")
    except Exception as exc:
        errors.append(f"Phase 5 (purge) failed: {exc}")

    # -----------------------------------------------------------------------
    # Phase 6: Save new competitor videos
    # -----------------------------------------------------------------------
    _print_phase(6, "Saving new competitor videos")
    try:
        if raw_videos:
            # Normalise videos for storage (is_outlier defaults to False before detection)
            videos_to_save = [
                {
                    "video_id":         v.get("video_id"),
                    "channel_id":       v.get("channel_id"),
                    "title":            v.get("title"),
                    "published_at":     v.get("published_at"),
                    "views":            v.get("views"),
                    "likes":            v.get("likes"),
                    "duration_seconds": v.get("duration_seconds"),
                    "description":      v.get("description"),
                    "is_outlier":       False,
                    "outlier_reason":   None,
                }
                for v in raw_videos
                if v.get("video_id") and v.get("title")
            ]
            save_result = store.save_competitor_videos(videos_to_save)
            if "error" in save_result:
                errors.append(f"Phase 6 (save videos) failed: {save_result['error']}")
            else:
                print(f"     Saved {save_result.get('saved', 0)} videos")
        else:
            print("     No videos to save")
    except Exception as exc:
        errors.append(f"Phase 6 (save videos) failed: {exc}")

    videos_total = len(raw_videos)

    # -----------------------------------------------------------------------
    # Phase 7: Detect outliers + update is_outlier flags in DB
    # -----------------------------------------------------------------------
    _print_phase(7, "Detecting outliers")
    outliers_found = 0
    try:
        stored_videos = store.get_competitor_videos(limit=1000)
        if isinstance(stored_videos, dict) and "error" in stored_videos:
            errors.append(f"Phase 7 (get videos for outliers) failed: {stored_videos['error']}")
            stored_videos = []

        if stored_videos:
            annotated = detect_outliers(stored_videos)
            if isinstance(annotated, dict) and "error" in annotated:
                errors.append(f"Phase 7 (detect outliers) failed: {annotated['error']}")
            else:
                # Update is_outlier flags in DB for outlier videos
                outlier_videos = [v for v in annotated if v.get("is_outlier")]
                outliers_found = len(outlier_videos)
                if outlier_videos:
                    # Re-save outlier videos with updated flags
                    for v in outlier_videos:
                        v["outlier_reason"] = f"Views={v.get('views')}, ratio={v.get('outlier_ratio', 0):.1f}x median"
                    store.save_competitor_videos(outlier_videos)
                print(f"     Found {outliers_found} outlier(s)")
    except Exception as exc:
        errors.append(f"Phase 7 (detect outliers) failed: {exc}")

    # -----------------------------------------------------------------------
    # Phase 8: Extract niche patterns + save snapshot
    # -----------------------------------------------------------------------
    _print_phase(8, "Extracting niche patterns")
    try:
        # Use the annotated video list if available, fall back to raw_videos
        pattern_input = raw_videos if raw_videos else []
        niche_patterns = extract_niche_patterns(pattern_input)
        if isinstance(niche_patterns, dict) and "error" in niche_patterns:
            errors.append(f"Phase 8 (extract patterns) failed: {niche_patterns['error']}")
        else:
            snap_result = store.save_niche_snapshot(
                format_patterns=niche_patterns.get("format_patterns"),
                hook_patterns=niche_patterns.get("hook_patterns"),
                trending_topics=niche_patterns.get("trending_topics"),
            )
            if "error" in snap_result:
                errors.append(f"Phase 8 (save niche) failed: {snap_result['error']}")
            else:
                fmt = niche_patterns.get("format_patterns", {})
                print(f"     Patterns from {fmt.get('video_count', 0)} videos")
    except Exception as exc:
        errors.append(f"Phase 8 (extract patterns) failed: {exc}")

    # -----------------------------------------------------------------------
    # Phase 9: Export to Markdown
    # -----------------------------------------------------------------------
    _print_phase(9, "Exporting to youtube-intelligence.md")
    kb_exported_to = ""
    try:
        export_result = export_kb_to_markdown(db_path=resolved_db)
        if "error" in export_result:
            errors.append(f"Phase 9 (export) failed: {export_result['error']}")
        else:
            kb_exported_to = export_result.get("written_to", "")
            print(f"     Written to {kb_exported_to} ({export_result.get('word_count', 0)} words)")
    except Exception as exc:
        errors.append(f"Phase 9 (export) failed: {exc}")

    # -----------------------------------------------------------------------
    # Phase 10: Update last_refresh timestamp
    # -----------------------------------------------------------------------
    _print_phase(10, "Updating last_refresh timestamp")
    try:
        ts_result = store.set_last_refresh()
        if "error" in ts_result:
            errors.append(f"Phase 10 (set refresh) failed: {ts_result['error']}")
        else:
            print(f"     Timestamp: {ts_result.get('last_refresh', '—')[:19]}")
    except Exception as exc:
        errors.append(f"Phase 10 (set refresh) failed: {exc}")

    print(f"Refresh complete. {len(errors)} error(s)." if errors else "Refresh complete.")

    return {
        "refreshed":             True,
        "skipped":               False,
        "reason":                "",
        "last_refresh":          store.get_last_refresh() or _now_iso(),
        "algo_sources_scraped":  algo_sources_scraped,
        "channels_fetched":      channels_fetched,
        "videos_total":          videos_total,
        "outliers_found":        outliers_found,
        "kb_exported_to":        kb_exported_to,
        "errors":                errors,
    }
