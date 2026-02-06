# Phase 10: Performance Feedback Loop — Governance Specification

**Document Type:** System Governance
**Version:** 1.0
**Status:** Active
**Scope:** Defines when and how Phases 1–9 may be modified

---

## Purpose

Phase 10 is a constraint layer. It does not add capabilities. It defines the conditions under which the system is permitted to change and the conditions under which change is forbidden.

---

## Section 1: Baseline Calculation

### Definition

**Baseline** = median views of the last 10 published videos.

### Calculation Rules

| Condition | Baseline Method |
|-----------|-----------------|
| Fewer than 5 published videos | Absolute threshold: 1,000 views |
| 5–9 published videos | Median of all published videos |
| 10+ published videos | Median of last 10 published videos |

### Recalculation Timing

Baseline recalculates after each video publication. The new video is excluded from its own baseline calculation.

---

## Section 2: Measurement Time Horizons

### Primary Measurement

**30 days post-publication.**

No governance decision may reference a video's performance until 30 days have elapsed since publication.

### Secondary Measurement

**90 days post-publication.**

Used for evergreen confirmation. A video classified as underperforming at 30 days may be reclassified if it exceeds thresholds at 90 days. A video classified as successful at 30 days retains that classification regardless of 90-day performance.

### Prohibited Actions Before Measurement

| Action | Minimum Wait |
|--------|--------------|
| Classify video as success | 30 days |
| Classify video as failure | 30 days |
| Trigger training data graduation | 30 days |
| Trigger technique modification | 30 days × 3 videos |

---

## Section 3: Success Thresholds

### Quantitative Thresholds

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| Views | ≥3× baseline | Discoverability success |
| Retention | ≥35% average | Content success |

### Classification Matrix

| Views | Retention | Classification |
|-------|-----------|----------------|
| ≥3× baseline | ≥35% | SUCCESS — eligible for training data graduation |
| ≥3× baseline | <35% | PACKAGING SUCCESS / CONTENT FAILURE |
| <3× baseline | ≥35% | PACKAGING FAILURE / CONTENT SUCCESS |
| <3× baseline | <35% | FAILURE — no action until pattern confirmed |

### Training Data Graduation Requirements

A video qualifies for training data graduation only when ALL conditions are met:

1. Views ≥3× baseline at 30-day measurement
2. Retention ≥35% average
3. Confirmation video exists (same technique, different topic, also meets 1 and 2)

---

## Section 4: Attribution Isolation

### Metric Definitions

| Metric | Isolates | Governed By |
|--------|----------|-------------|
| Click-through rate (CTR) | Packaging quality (thumbnail, title) | Not governed by Phases 1–9 |
| Retention rate | Content quality (script, technique, execution) | Governed by Phases 1–9 |
| Views | Discoverability (algorithm, topic, timing) | Partially governed |

### Attribution Rules

The system shall not attribute success or failure to technique unless retention data supports the attribution.

| Observed Pattern | Attribution |
|------------------|-------------|
| High CTR, low retention | Packaging worked, content failed |
| Low CTR, high retention | Packaging failed, content worked |
| High CTR, high retention | Both worked |
| Low CTR, low retention | Insufficient data for technique attribution |

### Controlled Comparison Requirement

Technique modification requires pattern confirmation across 3+ videos with controlled packaging:

- Similar thumbnail style
- Similar title structure
- Different topics

If packaging varies significantly across the 3 videos, technique attribution is unreliable.

---

## Section 5: Topic-Technique Separation

### Coupling Risk

A technique that succeeds may have succeeded due to topic selection rather than technique quality. The system must distinguish between these causes.

### Classification

| Pattern | Classification |
|---------|----------------|
| Technique succeeds on Topic A only | Topic-coupled |
| Technique succeeds on Topics A and B | Technique-validated |

### Rules

1. Topic-coupled techniques remain available for use but are not promoted to author-style.md
2. Training data graduation requires a confirmation video on a different topic
3. If no confirmation video exists, the technique is logged as "pending validation"

---

## Section 6: Objective Triggers for System Modification

The system is permitted to modify Phases 1–9 only when one of the following conditions is met:

| Trigger | Threshold | Permitted Scope |
|---------|-----------|-----------------|
| Outlier success | 3× baseline AND ≥35% retention AND confirmation video | Extract techniques, promote to author-style.md |
| Pattern failure | 3+ videos underperform with same technique | Deprioritize technique, flag for review |
| Coverage gap | Coverage audit returns ❌ for planned video type | Add external creator analysis |
| Execution failure | 3+ videos show same filming/editing error | Modify Phase 9 checklist |
| Fact-check failure | Any verified error reaches publication | Modify Phases 1–6 verification gates |

---

## Section 7: Signals Insufficient to Justify Modification

The system shall not modify based on:

| Signal | Reason Insufficient |
|--------|---------------------|
| Anxiety | Not measurable |
| Novelty | Not performance-validated |
| Single video success | May be noise or topic-driven |
| Single video failure | May be noise or packaging-driven |
| External opinion | Not controlled for channel context |
| Comparison to other creators | Not controlled for audience overlap |
| VidIQ or tool recommendations | Not validated against channel DNA |

---

## Section 8: Explicit Prohibitions

### Prohibition 1: Trend-Chasing

The system shall not recommend topics based on recency, news cycle, or trending status unless the topic independently qualifies under established channel DNA criteria (history-first, documentary evidence, modern relevance through mechanism).

### Prohibition 2: Frequency Over Quality

The system shall not recommend increasing publication frequency as a growth strategy. Quality gates in Phases 1–9 remain fixed regardless of schedule pressure. No phase may be abbreviated or skipped to meet a publication deadline.

### Prohibition 3: Single-Video Pivot

The system shall not recommend strategic pivots based on any single video's performance, regardless of magnitude. A video at 10× baseline does not justify pivot. A video at 0.1× baseline does not justify pivot. Patterns require 3+ videos.

### Prohibition 4: Clone Production

The system shall not recommend replicating a successful video's topic. Only techniques may be extracted and reapplied. Producing "Topic X Part 2" or "More on Topic X" based on success of Topic X is forbidden unless independently justified by channel DNA criteria.

### Prohibition 5: Preemptive Gap-Filling

The system shall not acquire new creator transcripts or fill coverage gaps for video types that are not actively planned. Gaps are addressed when triggered by production decisions, not speculatively.

---

## Section 9: System Freeze Rules

### Freeze Duration

After any modification to Phases 1–9, the system enters freeze state.

| Rule | Specification |
|------|---------------|
| Minimum videos before next modification | 3 |
| Minimum time before next modification | 90 days OR 3 videos, whichever comes later |
| Freeze applies to | All of Phases 1–9 |
| Freeze does not apply to | Data collection, performance logging |

### Freeze Override

Freeze may be broken only by:

- Fact-check failure reaching publication (immediate safety concern)

All other triggers must wait for freeze expiration.

---

## Section 10: Author Signal Detection

### Detection Mechanism

When a video achieves training data graduation, analyze its script for technique divergence:

1. Compare techniques used against creator-techniques.md
2. Flag any technique not mapped to documented creator technique
3. Log as "candidate author-original"

### Promotion Criteria

A candidate author-original is promoted to confirmed author-signal when:

1. It appears in a second successful video
2. The second video covers a different topic
3. The technique does not appear in any creator transcript

### Scaffolding Displacement

Track frequency of creator technique usage across successful videos. If a creator technique stops appearing—replaced by author-style.md technique achieving equivalent function—flag as "displaced."

Displaced techniques are not removed. They are deprioritized in future script generation.

---

## Section 11: Coverage Gap Protocol

### Gap Classification

| Status | Definition | Action |
|--------|------------|--------|
| ✅ Sufficient | ≥2 transcripts for video type | None |
| ⚠️ Marginal | 1 transcript for video type | Monitor for overgeneralization |
| ❌ Underspecified | 0 transcripts for video type | Blocked if video planned |

### Trigger Conditions

Coverage gap action is permitted only when:

1. A video of that type is actively in production pipeline
2. Coverage audit returns ⚠️ or ❌
3. A specific creator is identified who demonstrably succeeds in that video type
4. A full transcript is obtainable

### Acquisition Rules

- Minimum 1 full transcript required
- Transcript must be from a video of the same type (not just same creator)
- Surface analysis (reputation, topic overlap) is insufficient justification

---

## How to Use This

Before making any modification to Phases 1–9, consult this document. Identify which trigger condition applies. Verify all thresholds are met using 30-day measurement data. Confirm freeze period has expired. If all conditions pass, proceed with narrowly scoped modification and re-enter freeze. If any condition fails, the modification is not permitted. Data collection and performance logging continue during freeze but do not constitute modification. When in doubt, the answer is: wait for more data.

## What This Forbids You From Doing

You may not modify the system because a video underperformed, because you discovered an exciting new creator, because you feel something is missing, because VidIQ suggested a change, because one video succeeded beyond expectations, because you want to post more frequently, because a topic is trending, or because you are anxious about growth. You may not replicate successful topics. You may not skip quality gates. You may not measure performance before 30 days. You may not promote techniques without confirmation videos. You may not acquire transcripts for video types you have not committed to producing. You may not break freeze for any reason other than fact-check failure reaching publication. The system changes when objective thresholds are met, measured with sufficient data, after sufficient time. Until then, the system is frozen and you execute against it.
