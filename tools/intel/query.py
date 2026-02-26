"""
query.py — Query interface for the YouTube Intelligence Engine

Provides formatted Markdown output functions for the /intel slash command:

    get_full_report()         — Full youtube-intelligence.md contents
    get_algo_summary()        — Algorithm mechanics (signal weights, pipeline, longform)
    get_competitor_report()   — Competitor channel activity + recent uploads
    get_outlier_report()      — Outlier/viral videos with analysis
    get_niche_report()        — Duration stats, title formula distribution, trending topics
    get_staleness_status()    — Last refresh date, staleness status, next suggested refresh
    add_competitor_channel()  — Add channel to tracking list

All functions return formatted Markdown strings ready for display.
All functions follow the error-dict pattern internally; callers receive
human-readable strings even when data is missing.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from tools.logging_config import get_logger

logger = get_logger(__name__)

# Resolve paths relative to this file's location
_INTEL_DIR = Path(__file__).parent
_DEFAULT_DB_PATH = str(_INTEL_DIR / "intel.db")
_KB_MD_PATH = _INTEL_DIR.parent.parent / "channel-data" / "youtube-intelligence.md"


def _get_store(db_path: str | None = None):
    """Return a KBStore instance, using the default path if none supplied."""
    from tools.intel.kb_store import KBStore
    return KBStore(db_path or _DEFAULT_DB_PATH)


def _db_exists(db_path: str | None = None) -> bool:
    """Return True if intel.db exists at the given (or default) path."""
    path = Path(db_path) if db_path else Path(_DEFAULT_DB_PATH)
    return path.exists()


# ---------------------------------------------------------------------------
# Public query functions
# ---------------------------------------------------------------------------


def get_full_report(db_path: str | None = None) -> str:
    """
    Return the full contents of channel-data/youtube-intelligence.md.

    If the file does not exist, return a message suggesting /intel --refresh.

    Args:
        db_path: Optional path to intel.db (unused here, kept for API consistency)

    Returns:
        Formatted Markdown string ready for display
    """
    if not _KB_MD_PATH.exists():
        return (
            "# YouTube Intelligence Report\n\n"
            "**No intelligence data found.**\n\n"
            "Run `/intel --refresh` to build the knowledge base for the first time.\n"
        )
    try:
        content = _KB_MD_PATH.read_text(encoding="utf-8")
        staleness = get_staleness_status(db_path)
        return f"{content}\n---\n{staleness}\n"
    except Exception as exc:
        return f"Error reading intelligence report: {exc}\n\nRun `/intel --refresh` to rebuild."


def get_algo_summary(db_path: str | None = None) -> str:
    """
    Return a concise algorithm mechanics summary from the latest algo snapshot.

    Format: signal weights table, pipeline mechanics, longform insights.
    Target: under 500 words.

    Args:
        db_path: Optional path to intel.db

    Returns:
        Formatted Markdown string ready for display
    """
    if not _db_exists(db_path):
        return _no_data_message("Algorithm mechanics")

    try:
        store = _get_store(db_path)
        snapshot = store.get_latest_algo_snapshot()

        if snapshot is None or (isinstance(snapshot, dict) and "error" in snapshot):
            return _no_data_message("Algorithm mechanics")

        lines = ["## Algorithm Mechanics Summary\n"]

        # Signal weights table
        signal_weights = snapshot.get("signal_weights") or {}
        if signal_weights:
            lines.append("### Signal Weights\n")
            lines.append("| Signal | Weight |")
            lines.append("| ------ | ------ |")
            for signal, weight in signal_weights.items():
                lines.append(f"| {signal} | {weight} |")
            lines.append("")

        # Algorithm model details
        algo_model = snapshot.get("algorithm_model") or {}
        if isinstance(algo_model, dict):
            pipeline = algo_model.get("pipeline_mechanics", {})
            if pipeline:
                lines.append("### Pipeline Mechanics\n")
                for channel, desc in pipeline.items():
                    lines.append(f"- **{channel}:** {desc}")
                lines.append("")

            satisfaction = algo_model.get("satisfaction_signals", [])
            if satisfaction:
                lines.append("### Satisfaction Signals\n")
                for signal in satisfaction[:5]:  # Cap at 5 for conciseness
                    lines.append(f"- {signal}")
                lines.append("")

        # Longform insights
        longform = snapshot.get("longform_insights") or []
        if longform:
            lines.append("### Longform Insights\n")
            for insight in longform[:5]:  # Cap at 5 for conciseness
                lines.append(f"- {insight}")
            lines.append("")

        # Metadata footer
        confidence = snapshot.get("confidence", "medium")
        refreshed = snapshot.get("refreshed_at", "unknown")[:10]
        source_names = snapshot.get("source_names") or []
        sources_str = ", ".join(source_names) if source_names else "unknown sources"
        lines.append(f"*Confidence: {confidence} | Refreshed: {refreshed} | Sources: {sources_str}*\n")
        lines.append(get_staleness_status(db_path))

        return "\n".join(lines)

    except Exception as exc:
        return f"Error loading algorithm summary: {exc}"


def get_competitor_report(db_path: str | None = None) -> str:
    """
    Return competitor channel activity report.

    Format: channel summary table (name, category, subscribers) + recent uploads list.

    Args:
        db_path: Optional path to intel.db

    Returns:
        Formatted Markdown string ready for display
    """
    if not _db_exists(db_path):
        return _no_data_message("Competitor intelligence")

    try:
        store = _get_store(db_path)

        channels = store.get_active_channels()
        if isinstance(channels, dict) and "error" in channels:
            return f"Error reading competitor channels: {channels['error']}"

        videos = store.get_competitor_videos(limit=20)
        if isinstance(videos, dict) and "error" in videos:
            videos = []

        lines = ["## Competitor Landscape\n"]

        # Channels table
        if channels:
            lines.append("### Tracked Channels\n")
            lines.append("| Channel | Category | Subscribers |")
            lines.append("| ------- | -------- | ----------- |")
            for ch in channels:
                name = ch.get("channel_name", "Unknown")
                cat = ch.get("niche_category") or "—"
                subs = ch.get("subscriber_count")
                subs_str = f"{subs:,}" if subs else "—"
                lines.append(f"| {name} | {cat} | {subs_str} |")
            lines.append("")
        else:
            lines.append("*No competitor channels configured. Run `/intel --add-channel` to add channels.*\n")

        # Recent uploads table (capped at 15)
        recent = [v for v in videos if not v.get("is_outlier")][:15]
        if recent:
            lines.append("### Recent Uploads\n")
            lines.append("| Title | Channel | Published | Duration |")
            lines.append("| ----- | ------- | --------- | -------- |")
            # Build channel_id -> name lookup
            ch_map = {ch.get("channel_id"): ch.get("channel_name", ch.get("channel_id")) for ch in channels}
            for v in recent:
                title = _truncate(v.get("title", "Untitled"), 50)
                ch_name = ch_map.get(v.get("channel_id"), v.get("channel_id", "—"))
                published = (v.get("published_at") or "—")[:10]
                dur = _format_duration(v.get("duration_seconds"))
                lines.append(f"| {title} | {ch_name} | {published} | {dur} |")
            lines.append("")
        else:
            lines.append("*No competitor video data available. Run `/intel --refresh` to fetch.*\n")

        lines.append(get_staleness_status(db_path))
        return "\n".join(lines)

    except Exception as exc:
        return f"Error loading competitor report: {exc}"


def get_outlier_report(db_path: str | None = None) -> str:
    """
    Return outlier/viral video analysis report.

    Format: outlier table (title, channel, views, ratio) with heuristic analysis.

    Args:
        db_path: Optional path to intel.db

    Returns:
        Formatted Markdown string ready for display
    """
    if not _db_exists(db_path):
        return _no_data_message("Outlier analysis")

    try:
        store = _get_store(db_path)

        outliers = store.get_competitor_videos(outliers_only=True, limit=20)
        if isinstance(outliers, dict) and "error" in outliers:
            return f"Error reading outlier data: {outliers['error']}"

        channels = store.get_active_channels()
        if isinstance(channels, dict):
            channels = []
        ch_map = {ch.get("channel_id"): ch.get("channel_name", ch.get("channel_id")) for ch in channels}

        lines = ["## Outlier Video Analysis\n"]

        if not outliers:
            lines.append("*No outlier videos detected yet.*\n")
            lines.append("Outliers are detected at >= 3x the channel's median view count.")
            lines.append("Run `/intel --refresh` to scan for new outliers.\n")
        else:
            lines.append(f"*{len(outliers)} outlier video(s) detected (>= 3x channel median)*\n")
            lines.append("### Outlier Videos\n")
            lines.append("| Title | Channel | Views | Published | Possible Reasons |")
            lines.append("| ----- | ------- | ----- | --------- | ---------------- |")
            for v in outliers:
                title = _truncate(v.get("title", "Untitled"), 45)
                ch_name = ch_map.get(v.get("channel_id"), v.get("channel_id", "—"))
                views = f"{v.get('views', 0):,}" if v.get("views") else "—"
                published = (v.get("published_at") or "—")[:10]
                reasons = _truncate(v.get("outlier_reason") or "unknown", 60)
                lines.append(f"| {title} | {ch_name} | {views} | {published} | {reasons} |")
            lines.append("")

            # Aggregate insight: top reasons
            all_reasons = [v.get("outlier_reason", "") for v in outliers if v.get("outlier_reason")]
            if all_reasons:
                lines.append("### Pattern Observations\n")
                lines.append("Common outlier characteristics from current dataset:")
                # Simple dedup of reason text snippets
                seen = set()
                for reason in all_reasons:
                    for phrase in reason.split(";"):
                        phrase = phrase.strip()
                        if phrase and phrase not in seen:
                            lines.append(f"- {phrase}")
                            seen.add(phrase)
                lines.append("")

        lines.append(get_staleness_status(db_path))
        return "\n".join(lines)

    except Exception as exc:
        return f"Error loading outlier report: {exc}"


def get_niche_report(db_path: str | None = None) -> str:
    """
    Return niche format and pattern analysis.

    Format: duration stats, title formula distribution table, trending topics table.

    Args:
        db_path: Optional path to intel.db

    Returns:
        Formatted Markdown string ready for display
    """
    if not _db_exists(db_path):
        return _no_data_message("Niche pattern analysis")

    try:
        store = _get_store(db_path)
        snapshot = store.get_latest_niche_snapshot()

        if snapshot is None or (isinstance(snapshot, dict) and "error" in snapshot):
            return _no_data_message("Niche pattern analysis")

        lines = ["## Niche Pattern Analysis\n"]

        format_patterns = snapshot.get("format_patterns") or {}
        hook_patterns = snapshot.get("hook_patterns") or {}
        trending_topics = snapshot.get("trending_topics") or []
        refreshed = (snapshot.get("refreshed_at") or "unknown")[:10]

        # Format / duration stats
        if format_patterns:
            total = format_patterns.get("total_videos", 0)
            avg_dur = format_patterns.get("avg_duration_min")
            median_dur = format_patterns.get("median_duration_min")
            duration_dist = format_patterns.get("duration_distribution", {})

            lines.append("### Duration Stats\n")
            lines.append(f"- **Videos analysed:** {total}")
            lines.append(f"- **Avg duration:** {f'{avg_dur:.1f} min' if avg_dur else '—'}")
            lines.append(f"- **Median duration:** {f'{median_dur:.1f} min' if median_dur else '—'}")
            lines.append("")

            if duration_dist:
                lines.append("**Duration Distribution:**\n")
                lines.append("| Bucket | Count |")
                lines.append("| ------ | ----- |")
                bucket_order = ["0-10min", "10-20min", "20-30min", "30-45min", "45+min", "unknown"]
                for bucket in bucket_order:
                    count = duration_dist.get(bucket, 0)
                    if count > 0 or bucket != "unknown":
                        lines.append(f"| {bucket} | {count} |")
                lines.append("")

        # Title formulas
        if hook_patterns:
            title_formulas = hook_patterns.get("title_formula_counts", {})
            if title_formulas:
                total_vids = sum(title_formulas.values()) or 1
                lines.append("### Title Formulas\n")
                lines.append("| Formula | Count | % |")
                lines.append("| ------- | ----- | - |")
                sorted_formulas = sorted(title_formulas.items(), key=lambda x: x[1], reverse=True)
                for formula, count in sorted_formulas[:8]:
                    pct = (count / total_vids) * 100
                    lines.append(f"| {formula} | {count} | {pct:.1f}% |")
                lines.append("")

        # Trending topics
        if trending_topics:
            lines.append("### Trending Topics\n")
            lines.append("| Topic | Count | % |")
            lines.append("| ----- | ----- | - |")
            total_vids = format_patterns.get("total_videos") or 1
            for topic_entry in trending_topics[:10]:
                topic = topic_entry.get("topic", "unknown")
                count = topic_entry.get("count", 0)
                pct = (count / total_vids) * 100
                lines.append(f"| {topic} | {count} | {pct:.1f}% |")
            lines.append("")

        lines.append(f"*Refreshed: {refreshed}*\n")
        lines.append(get_staleness_status(db_path))
        return "\n".join(lines)

    except Exception as exc:
        return f"Error loading niche report: {exc}"


def get_staleness_status(db_path: str | None = None) -> str:
    """
    Return staleness status: last refresh date, days since refresh, next suggested refresh.

    Args:
        db_path: Optional path to intel.db

    Returns:
        Single-line Markdown string for display at bottom of reports
    """
    if not _db_exists(db_path):
        return "*Last refreshed: never — Run `/intel --refresh` to initialize.*"

    try:
        store = _get_store(db_path)
        last = store.get_last_refresh()

        if last is None or isinstance(last, dict):
            return "*Last refreshed: never — Run `/intel --refresh` to initialize.*"

        last_dt = datetime.fromisoformat(last)
        if last_dt.tzinfo is None:
            last_dt = last_dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        age_days = (now - last_dt).days
        last_str = last_dt.strftime("%Y-%m-%d")

        if age_days == 0:
            age_label = "today"
        elif age_days == 1:
            age_label = "1 day ago"
        else:
            age_label = f"{age_days} days ago"

        is_stale = store.is_stale()
        stale_flag = " *(STALE — run `/intel --refresh`)*" if is_stale else ""

        return f"*Last refreshed: {last_str} ({age_label}){stale_flag}*"

    except Exception as exc:
        return f"*Staleness check failed: {exc}*"


def add_competitor_channel(
    channel_id: str,
    channel_name: str,
    category: str = "broad-history",
    db_path: str | None = None,
) -> str:
    """
    Add a competitor channel to the tracking list.

    Updates both KBStore (competitor_channels table) and competitor_channels.json.

    Args:
        channel_id:   YouTube channel ID (e.g. UCxxxxxx)
        channel_name: Human-readable name
        category:     One of: style-match, broad-history, geopolitics
        db_path:      Optional path to intel.db

    Returns:
        Confirmation message string
    """
    import json as _json

    if not _db_exists(db_path):
        return "Error: intel.db not found. Run `/intel --refresh` first to initialize."

    # Validate category
    valid_categories = {"style-match", "broad-history", "geopolitics"}
    if category not in valid_categories:
        category = "broad-history"

    try:
        store = _get_store(db_path)
        result = store.save_competitor_channel(
            channel_id=channel_id,
            channel_name=channel_name,
            niche_category=category,
        )

        if isinstance(result, dict) and "error" in result:
            return f"Error adding channel to database: {result['error']}"

        # Also update competitor_channels.json
        config_path = _INTEL_DIR / "competitor_channels.json"
        if config_path.exists():
            try:
                channels = _json.loads(config_path.read_text(encoding="utf-8"))
                # Check for duplicates
                existing_ids = {ch.get("id") for ch in channels}
                if channel_id not in existing_ids:
                    channels.append({"id": channel_id, "name": channel_name, "category": category})
                    config_path.write_text(_json.dumps(channels, indent=2), encoding="utf-8")
                    json_msg = "Added to competitor_channels.json."
                else:
                    json_msg = "Already in competitor_channels.json (updated DB only)."
            except Exception as exc:
                json_msg = f"DB updated but could not update JSON: {exc}"
        else:
            json_msg = "competitor_channels.json not found; added to DB only."

        return (
            f"Added channel: **{channel_name}** (`{channel_id}`)\n"
            f"- Category: {category}\n"
            f"- {json_msg}\n"
            f"- Run `/intel --refresh` to fetch videos from this channel."
        )

    except Exception as exc:
        return f"Error adding channel: {exc}"


def get_pattern_report(db_path: str | None = None) -> str:
    """
    Return competitor pattern analysis report (topic clusters, formulas, gaps).

    Args:
        db_path: Optional path to intel.db

    Returns:
        Formatted Markdown string ready for display
    """
    if not _db_exists(db_path):
        return _no_data_message("Competitor pattern analysis")

    try:
        from tools.intel.competitor_patterns import get_pattern_report as _get_patterns
        resolved = db_path or _DEFAULT_DB_PATH
        report = _get_patterns(resolved)
        staleness = get_staleness_status(db_path)
        return f"{report}\n{staleness}\n"
    except Exception as exc:
        return f"Error loading pattern report: {exc}"


def get_topic_score(topic_text: str, db_path: str | None = None) -> str:
    """
    Score a topic idea and return formatted Markdown report.

    Args:
        topic_text: Topic title or description to score
        db_path:    Optional path to intel.db

    Returns:
        Formatted Markdown string with score breakdown
    """
    if not _db_exists(db_path):
        return _no_data_message("Topic scoring")

    try:
        from tools.intel.topic_scorer import score_topic, format_score_report
        resolved = db_path or _DEFAULT_DB_PATH
        result = score_topic(topic_text, resolved)
        report = format_score_report(result)
        staleness = get_staleness_status(db_path)
        return f"{report}\n{staleness}\n"
    except Exception as exc:
        return f"Error scoring topic: {exc}"


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _no_data_message(section: str) -> str:
    """Return a consistent 'no data' message with refresh suggestion."""
    return (
        f"## {section}\n\n"
        f"*No data available yet.*\n\n"
        f"Run `/intel --refresh` to build the intelligence knowledge base.\n"
    )


def _truncate(text: str, max_len: int) -> str:
    """Truncate text to max_len, appending '...' if cut."""
    if not text:
        return "—"
    text = str(text)
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def _format_duration(seconds: int | None) -> str:
    """Format duration seconds as mm:ss or return '—'."""
    if not seconds:
        return "—"
    try:
        seconds = int(seconds)
        mins, secs = divmod(seconds, 60)
        if mins >= 60:
            hours, mins = divmod(mins, 60)
            return f"{hours}h {mins}m"
        return f"{mins}m {secs:02d}s"
    except (ValueError, TypeError):
        return "—"


# ---------------------------------------------------------------------------
# Entrypoint for quick smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(get_staleness_status())
