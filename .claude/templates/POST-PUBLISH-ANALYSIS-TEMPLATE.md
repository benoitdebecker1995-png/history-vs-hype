<!-- Canonical template for POST-PUBLISH-ANALYSIS files. Parser expects these exact section headers. -->

# Post-Publish Analysis: {title}

**Video ID:** {video_id}
**Analyzed:** {timestamp}
**Saved to:** {file_path}

---

## Quick Summary

**Above average:** {metrics_above}
**Below average:** {metrics_below}

## Performance vs Benchmarks

| Metric | This Video | Channel Avg | vs Avg |
|--------|-----------|-------------|--------|
| Views | {views} | {avg_views} | {delta}% |
| Watch Time (min) | {watch_time} | {avg_watch} | {delta}% |
| Likes | {likes} | {avg_likes} | {delta}% |
| Comments | {comments} | {avg_comments} | {delta}% |
| Subscribers | +{subs} | +{avg_subs} | {delta}% |

*Channel averages based on last {N} videos*

## Click-Through Rate

**CTR:** {ctr}%
**Impressions:** {impressions}

*Check YouTube Studio > Analytics > Reach tab for CTR data*

## Retention Analysis

**Average retention:** {avg_retention}%
**Final retention:** {final_retention}%

### Retention Curve

*Run `python retention.py VIDEO_ID` for full curve visualization*

### Drop-off Points

*Sorted by impact (biggest drops first)*

| Position | Viewers Lost | Location |
|----------|--------------|----------|
| {position}% | {lost}% dropped | {location} |

## Comments Analysis

**Total fetched:** {total}

### Questions ({count})

{question_list}

### Objections ({count})

{objection_list}

### Content Requests ({count})

{request_list}

## Lessons

### Observations

- {observation_1}
- {observation_2}

### Actionable Items

- [ ] {action_1}
- [ ] {action_2}

## Discovery Diagnostics

**Diagnosis:** {summary}
**Primary Issue:** {issue} (Severity: {severity})

## Variant Tracking

**Thumbnail variants:** {thumb_count}
**Title variants:** {title_count}
**CTR snapshots:** {snapshot_count}

### Active Thumbnail: Variant {letter}

| Variant | Visual Pattern | Hash | Active Since |
|---------|----------------|------|--------------|
| {letter} | {pattern} | {hash} | {date} |

### Active Title: Variant {letter}

| Variant | Title | Length | Active Since |
|---------|-------|--------|--------------|
| {letter} | {title} | {length} chars | {date} |

### CTR History

| Date | CTR | Impressions | Active Thumbnail | Active Title |
|------|-----|-------------|------------------|--------------|
| {date} | {ctr}% | {impressions} | {thumb_variant} | {title_variant} |

## CTR Analysis

### Thumbnail Performance

**Active:** Variant {letter}
**Status:** {status_badge}
**Impression tier:** {tier}
**Channel avg CTR:** {overall_avg}% | Category avg: {category_avg}%

{verdict_details}

### Title Performance

**Active:** Variant {letter}
**Status:** {status_badge}
**Impression tier:** {tier}
**Channel avg CTR:** {overall_avg}% | Category avg: {category_avg}%

{verdict_details}

## Errors

- **{component}:** {error_message}
