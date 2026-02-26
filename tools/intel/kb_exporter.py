"""
kb_exporter.py — Generate agent-readable Markdown from SQLite intelligence KB

Reads the latest data from all intel.db tables via KBStore and produces
channel-data/youtube-intelligence.md — a scannable, concise Markdown file
optimised for agent context window consumption (target: under 3,000 words).

Format principles (from RESEARCH.md Pitfall 5):
    - Tables for data, bullets for insights — not prose
    - Sections that can be partially loaded by agents
    - Concise headings so agents can navigate by section name

All public functions follow the error-dict pattern: return {'error': msg}
on failure, never raise.
"""

from datetime import datetime, timezone
from pathlib import Path

# Resolve paths relative to this file's location
_INTEL_DIR = Path(__file__).parent
_DEFAULT_DB_PATH = str(_INTEL_DIR / "intel.db")
_DEFAULT_OUTPUT_PATH = str(Path(__file__).parent.parent.parent / "channel-data" / "youtube-intelligence.md")


def _now_utc_str() -> str:
    """Return current UTC time as a readable string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _fmt_duration(seconds: int | None) -> str:
    """Convert seconds to mm:ss or hh:mm:ss string."""
    if not seconds:
        return "—"
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}h {m:02d}m"
    return f"{m}m {s:02d}s"


def _fmt_views(views: int | None) -> str:
    """Format view count with K/M abbreviation."""
    if views is None:
        return "—"
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    if views >= 1_000:
        return f"{views / 1_000:.1f}K"
    return str(views)


def _count_words(text: str) -> int:
    """Rough word count for the output text."""
    return len(text.split())


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def _render_algo_section(snapshot: dict | None) -> str:
    """Render the Algorithm Mechanics section from a snapshot dict."""
    if not snapshot:
        return "## Algorithm Mechanics\n\n*No algorithm data yet. Run `/intel --refresh` to populate.*\n\n"

    lines = ["## Algorithm Mechanics\n"]
    lines.append(f"*Source confidence: {snapshot.get('confidence', 'unknown')} "
                 f"| Refreshed: {snapshot.get('refreshed_at', '—')[:10]}*\n")

    # Signal weights table
    signal_weights = snapshot.get("signal_weights") or {}
    if signal_weights:
        lines.append("\n### Signal Weights\n")
        lines.append("| Signal | Weight |")
        lines.append("| ------ | ------ |")
        signal_labels = {
            "satisfaction":          "Viewer Satisfaction",
            "ctr":                   "Click-Through Rate (CTR)",
            "avd":                   "Average View Duration (AVD)",
            "session_continuation":  "Session Continuation",
            "upload_consistency":    "Upload Consistency",
        }
        for key, label in signal_labels.items():
            weight = signal_weights.get(key, "—")
            lines.append(f"| {label} | {weight} |")

    # Algorithm model blob
    algo_model = snapshot.get("algorithm_model") or {}
    if isinstance(algo_model, str):
        # Handle case where it's stored as JSON string (shouldn't happen but be safe)
        import json
        try:
            algo_model = json.loads(algo_model)
        except (json.JSONDecodeError, TypeError):
            algo_model = {}

    # Pipeline mechanics
    pipeline = algo_model.get("pipeline_mechanics") or {}
    if pipeline:
        lines.append("\n### Pipeline Mechanics\n")
        for name, desc in [
            ("Browse Feed", pipeline.get("browse_feed")),
            ("Search",      pipeline.get("search")),
            ("Suggested",   pipeline.get("suggested")),
        ]:
            if desc:
                lines.append(f"- **{name}:** {desc}")

    # Longform-specific insights
    longform = algo_model.get("longform_specific") or snapshot.get("longform_insights") or []
    if isinstance(longform, list) and longform:
        lines.append("\n### Longform-Specific\n")
        for insight in longform[:5]:  # Limit to 5 to control word count
            lines.append(f"- {insight}")

    # Satisfaction signals
    satisfaction = algo_model.get("satisfaction_signals") or []
    if isinstance(satisfaction, list) and satisfaction:
        lines.append("\n### Satisfaction Signals\n")
        for sig in satisfaction[:4]:
            lines.append(f"- {sig}")

    # Thresholds
    avd_t = algo_model.get("avd_thresholds")
    ctr_t = algo_model.get("ctr_thresholds")
    if avd_t or ctr_t:
        lines.append("\n### Reported Thresholds\n")
        if avd_t:
            lines.append(f"- **AVD:** {avd_t}")
        if ctr_t:
            lines.append(f"- **CTR:** {ctr_t}")

    # Small channel notes
    small = algo_model.get("small_channel_notes")
    if small:
        lines.append("\n### Small Channel Notes\n")
        lines.append(f"- {small}")

    # Sources used
    sources = algo_model.get("sources_used") or snapshot.get("source_names") or []
    if isinstance(sources, list) and sources:
        lines.append(f"\n*Sources: {', '.join(sources)}*")

    lines.append("")
    return "\n".join(lines) + "\n"


def _render_competitor_section(channels: list, videos: list) -> str:
    """Render the Competitor Landscape section."""
    lines = ["## Competitor Landscape\n"]

    if not channels:
        lines.append("*No channels loaded. Run `/intel --refresh` to populate.*\n")
        return "\n".join(lines) + "\n"

    # Channel summary table
    lines.append("### Tracked Channels\n")
    lines.append("| Channel | Category | Subscribers |")
    lines.append("| ------- | -------- | ----------- |")
    for ch in channels[:10]:
        name = ch.get("channel_name", "—")
        cat = ch.get("niche_category", "—")
        subs = _fmt_views(ch.get("subscriber_count"))
        lines.append(f"| {name} | {cat} | {subs} |")

    if not videos:
        lines.append("\n*No video data yet. Run `/intel --refresh` to populate.*\n")
        return "\n".join(lines) + "\n"

    # Recent outlier videos table
    outliers = [v for v in videos if v.get("is_outlier")]
    if outliers:
        lines.append("\n### Outlier Videos (3x+ channel median)\n")
        lines.append("| Title | Channel | Views | Ratio | Duration |")
        lines.append("| ----- | ------- | ----- | ----- | -------- |")
        for vid in outliers[:10]:
            title = (vid.get("title") or "—")[:50]
            channel = vid.get("channel_id", "—")
            views = _fmt_views(vid.get("views"))
            ratio = f"{vid.get('outlier_ratio', 0):.1f}x"
            dur = _fmt_duration(vid.get("duration_seconds"))
            lines.append(f"| {title} | {channel} | {views} | {ratio} | {dur} |")
    else:
        lines.append("\n*No outliers detected in current data.*\n")

    # Recent uploads summary
    recent = sorted(
        [v for v in videos if v.get("published_at")],
        key=lambda v: v.get("published_at", ""),
        reverse=True,
    )[:5]
    if recent:
        lines.append("\n### Most Recent Uploads\n")
        lines.append("| Title | Channel | Published | Duration |")
        lines.append("| ----- | ------- | --------- | -------- |")
        for vid in recent:
            title = (vid.get("title") or "—")[:50]
            channel = vid.get("channel_id", "—")
            pub = (vid.get("published_at") or "—")[:10]
            dur = _fmt_duration(vid.get("duration_seconds"))
            lines.append(f"| {title} | {channel} | {pub} | {dur} |")

    lines.append("")
    return "\n".join(lines) + "\n"


def _render_niche_section(snapshot: dict | None) -> str:
    """Render the Niche Patterns section from a niche_snapshot dict."""
    lines = ["## Niche Patterns\n"]

    if not snapshot:
        lines.append("*No niche data yet. Run `/intel --refresh` to populate.*\n")
        return "\n".join(lines) + "\n"

    format_pat = snapshot.get("format_patterns") or {}
    hook_pat = snapshot.get("hook_patterns") or {}
    trending = snapshot.get("trending_topics") or []

    if format_pat:
        lines.append("### Format Stats\n")
        avg_s = format_pat.get("avg_duration_seconds", 0)
        med_s = format_pat.get("median_duration_seconds", 0)
        count = format_pat.get("video_count", 0)
        lines.append(f"- **Videos analysed:** {count}")
        lines.append(f"- **Avg duration:** {_fmt_duration(int(avg_s))}")
        lines.append(f"- **Median duration:** {_fmt_duration(int(med_s))}")

        dist = format_pat.get("duration_distribution") or {}
        if dist:
            lines.append("\n**Duration Distribution:**\n")
            lines.append("| Bucket | Count |")
            lines.append("| ------ | ----- |")
            bucket_order = ["0-10min", "10-20min", "20-30min", "30-45min", "45+min", "unknown"]
            for bucket in bucket_order:
                if bucket in dist:
                    lines.append(f"| {bucket} | {dist[bucket]} |")

    if hook_pat:
        formula_counts = hook_pat.get("title_formula_counts") or {}
        formula_pct = hook_pat.get("title_formula_pct") or {}
        if formula_counts:
            lines.append("\n### Title Formulas\n")
            lines.append("| Formula | Count | % |")
            lines.append("| ------- | ----- | - |")
            for formula, count in sorted(formula_counts.items(), key=lambda x: -x[1])[:8]:
                pct = formula_pct.get(formula, "—")
                lines.append(f"| {formula} | {count} | {pct} |")

    if trending:
        lines.append("\n### Trending Topics\n")
        lines.append("| Topic | Count | % |")
        lines.append("| ----- | ----- | - |")
        for item in trending[:10]:
            topic = item.get("topic", "—")
            count = item.get("count", 0)
            pct = item.get("pct", "—")
            lines.append(f"| {topic} | {count} | {pct} |")

    lines.append("")
    return "\n".join(lines) + "\n"


def _render_outlier_section(outlier_analysis: list) -> str:
    """Render the Outlier Analysis section from generate_outlier_analysis() output."""
    lines = ["## Outlier Analysis\n"]

    if not outlier_analysis:
        lines.append("*No outlier analysis available.*\n")
        return "\n".join(lines) + "\n"

    for item in outlier_analysis[:8]:  # Cap at 8 to control word count
        title = item.get("title", "—")[:70]
        channel = item.get("channel", "—")
        views = _fmt_views(item.get("views"))
        ratio = f"{item.get('outlier_ratio', 0):.1f}x"
        dur = _fmt_duration(item.get("duration_seconds"))
        reasons = item.get("possible_reasons") or []

        lines.append(f"### {title}\n")
        lines.append(f"- **Channel:** {channel} | **Views:** {views} ({ratio} median) | **Duration:** {dur}")
        if reasons:
            lines.append(f"- **Possible reasons:** {'; '.join(reasons)}")
        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def export_kb_to_markdown(db_path: str = None, output_path: str = None) -> dict:
    """
    Generate youtube-intelligence.md from the latest intel.db data.

    Reads all tables via KBStore, renders 5 sections, writes Markdown file.
    Targets under 3,000 words total (RESEARCH.md Pitfall 5).

    Args:
        db_path:     Path to intel.db. Defaults to tools/intel/intel.db.
        output_path: Path for output Markdown. Defaults to
                     channel-data/youtube-intelligence.md.

    Returns:
        {
            'written_to': str,    # Absolute path of written file
            'sections': list,     # Section names included
            'word_count': int,    # Approximate word count of output
        }
        or {'error': str}
    """
    try:
        from tools.intel.kb_store import KBStore
        from tools.intel.pattern_analyzer import generate_outlier_analysis

        resolved_db = db_path or _DEFAULT_DB_PATH
        resolved_out = output_path or _DEFAULT_OUTPUT_PATH

        store = KBStore(resolved_db)

        # Load data from all tables
        algo_snapshot = store.get_latest_algo_snapshot()
        channels = store.get_active_channels() or []
        if isinstance(channels, dict):
            channels = []  # Error from get_active_channels — treat as empty

        videos = store.get_competitor_videos(limit=200) or []
        if isinstance(videos, dict):
            videos = []

        niche_snapshot = store.get_latest_niche_snapshot()

        # Build outlier analysis
        outliers = [v for v in videos if v.get("is_outlier")]
        outlier_analysis = generate_outlier_analysis(outliers) if outliers else []
        if isinstance(outlier_analysis, dict):  # error dict
            outlier_analysis = []

        # Render sections
        header = (
            f"# YouTube Intelligence KB\n\n"
            f"> Last refreshed: {_now_utc_str()}\n"
            f"> This file is auto-generated by `tools/intel/kb_exporter.py`. Do not edit manually.\n\n"
        )

        algo_section = _render_algo_section(algo_snapshot)
        competitor_section = _render_competitor_section(channels, videos)
        niche_section = _render_niche_section(niche_snapshot)
        outlier_section = _render_outlier_section(outlier_analysis)

        full_content = header + algo_section + competitor_section + niche_section + outlier_section
        word_count = _count_words(full_content)

        # Write output
        out_path = Path(resolved_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(full_content, encoding="utf-8")

        sections = ["algorithm_mechanics", "competitor_landscape", "niche_patterns", "outlier_analysis"]
        return {
            "written_to": str(out_path.resolve()),
            "sections": sections,
            "word_count": word_count,
        }

    except Exception as exc:
        return {"error": f"export_kb_to_markdown failed: {exc}"}
