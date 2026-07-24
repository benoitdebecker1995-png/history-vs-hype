"""Generate retitle candidates for all underperforming titles.

Scores current titles and proposed alternatives using title_scorer.py,
then generates a ranked report with recommendations.

Script-based generation reads SRT/script openings, extracts the thesis
sentence (the core claim/tension), and restructures it into title format
using measured CTR patterns.

Usage:
    python -m tools.retitle_gen
    python -m tools.retitle_gen --script-only   # Only show script-generated titles
"""
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from tools.title_scorer import score_title


# Video ID → project folder slug (for finding SRT/script/research files)
VIDEO_PROJECT_MAP = {
    'LrthC_8Hb2Y': None,  # South China Sea — no project folder
    'n-CUSE4bDvg': None,  # Cyprus — no project folder
    'ZZz_g_Ov6Lg': '14-chagos-islands-2025',
    '71xY0Pt4T-M': None,  # Georgia — no project folder
    'L5ZIP24-36s': '24-iran-1953-coup-2025',
    'BNEEAD--Y3c': '3-fuentes-fact-check-2025',
    'l8abBf4aMv8': '23-christmas-origins-2025',
    'LuLZYZWMiU4': '19-flat-earth-medieval-2025',
    '6GybGd_q25w': '27-peru-2025',
    'xODFE2Pyubo': None,  # Thailand-Cambodia — no project folder
    'TYNaIu28LeU': '30-belavezha-accords-2025',
    'WZnCxVPNF7A': '35-gibraltar-treaty-utrecht-2026',
    '6SdfqTYPviQ': None,  # Ukraine — no project folder
    '_N_08zn95FY': None,  # Turkey-Greece — no project folder
    'Oc7oq292HkM': None,  # Armenian genocide — no project folder
    'Ac-k2p9Gvj4': None,  # Ancient hatreds — no project folder
    'XKAqt_ZLHGo': '6-bir-tawil-2025',
}

CANDIDATES = {
    'LrthC_8Hb2Y': {
        'current': 'The 1947 Map That Set the South China Sea on Fire',
        'views': 91, 'ret': 49.6, 'subs': 2, 'priority': 'URGENT',
        'reason': 'Best retention on channel (49.6%) but year penalty killing CTR',
        'options': [
            '6 Countries Claim the Same Sea. One Map Explains Why.',
            'China vs Everyone. The Map That Explains the South China Sea.',
            'China Drew a Line on a Map. Now 6 Countries Want War.',
        ]
    },
    'n-CUSE4bDvg': {
        'current': "Europe's Last Divided Capital: The Cyprus Problem",
        'views': 99, 'ret': 33.5, 'subs': 2, 'priority': 'HIGH',
        'reason': 'Colon penalty, strong retention',
        'options': [
            'Cyprus Is Still Divided. Both Sides Blame the Other.',
            'Turkey vs Greece. The Island They Split in Half.',
            'One City, Two Countries. Why Cyprus Is Still Divided.',
        ]
    },
    'ZZz_g_Ov6Lg': {
        'current': '"Leave or Starve": The Secret Memo That Emptied an Island',
        'views': 26, 'ret': 33.2, 'subs': 0, 'priority': 'HIGH',
        'reason': 'Colon penalty, strong retention (33.2%)',
        'options': [
            'Britain Expelled 2,000 Islanders. The Memo Proves It.',
            'A Secret British Memo Emptied an Entire Island.',
            'Britain vs Chagos. The Memo That Said "Leave or Starve."',
        ]
    },
    '71xY0Pt4T-M': {
        'current': 'The Georgia Playbook: How 2008 Predicted Ukraine',
        'views': 39, 'ret': 23.0, 'subs': 0, 'priority': 'HIGH',
        'reason': 'Year + colon = double penalty (score 5)',
        'options': [
            'Russia Tested Its Ukraine Strategy on Georgia First.',
            'Russia vs Georgia. The Rehearsal for Ukraine.',
            'Putin Invaded Georgia Before Ukraine. Nobody Stopped Him.',
        ]
    },
    'L5ZIP24-36s': {
        'current': 'The Iran Documents: 1953 Was The Second Coup',
        'views': 34, 'ret': 21.4, 'subs': 1, 'priority': 'HIGH',
        'reason': 'Year + colon = double penalty (score 5)',
        'options': [
            "Iran Had Two Coups. The CIA Only Admits to One.",
            "The CIA Destroyed Iran's Democracy. Twice.",
            'Iran vs the CIA. Two Coups the West Wants You to Forget.',
        ]
    },
    'BNEEAD--Y3c': {
        'current': 'Fact-Checking Nick Fuentes: Why His Claims Are Dangerous',
        'views': 168, 'ret': 25.6, 'subs': 0, 'priority': 'MEDIUM',
        'reason': 'Colon pattern',
        'options': [
            'Nick Fuentes Made 5 Claims. The Documents Prove Him Wrong.',
            'I Fact-Checked Nick Fuentes with Primary Sources.',
            'Nick Fuentes vs the Historical Record.',
        ]
    },
    'l8abBf4aMv8': {
        'current': 'Did Pagans Actually Copy Christmas?',
        'views': 193, 'ret': 22.9, 'subs': 6, 'priority': 'MEDIUM',
        'reason': 'Question pattern (2.4% CTR), too short',
        'options': [
            'Christians vs Pagans. Who Actually Invented Christmas?',
            'Christmas Was Never Pagan. The Evidence Proves It.',
            'The Pagan Origins of Christmas Are a Modern Myth.',
        ]
    },
    'LuLZYZWMiU4': {
        'current': "The Flat Earth Myth Was Invented in 1828. Here's Who Did It.",
        'views': 205, 'ret': 11.6, 'subs': 2, 'priority': 'MEDIUM',
        'reason': 'Year penalty; also deepest retention problems (11.6%)',
        'options': [
            'Medieval People Never Believed the Earth Was Flat.',
            "The Flat Earth Myth Was Fabricated. Here's Who Did It.",
            'Nobody in the Middle Ages Thought the Earth Was Flat.',
        ]
    },
    '6GybGd_q25w': {
        'current': 'Why Spain Didn\'t "Civilize" Peru: The 500-Year Lie',
        'views': 46, 'ret': 28.0, 'subs': 1, 'priority': 'MEDIUM',
        'reason': 'Colon pattern',
        'options': [
            'Spain Claimed It Civilized Peru. The Evidence Says Otherwise.',
            'Spain vs Peru. The Colony That Was Never "Civilized."',
            "Spain's \"Civilization\" of Peru Was a 500-Year Lie.",
        ]
    },
    'xODFE2Pyubo': {
        'current': 'Why a 1908 Map is Still Killing People: Thailand vs. Cambodia',
        'views': 27, 'ret': 26.2, 'subs': 0, 'priority': 'MEDIUM',
        'reason': 'Year + colon double penalty',
        'options': [
            'Thailand vs Cambodia. The Temple Dispute That Killed Soldiers.',
            'Thailand and Cambodia Almost Went to War Over a Temple.',
            'One Ancient Temple. Two Countries. Soldiers Died Over It.',
        ]
    },
    'TYNaIu28LeU': {
        'current': 'The 1922 Treaty Loophole That Ended the USSR',
        'views': 24, 'ret': 27.1, 'subs': 0, 'priority': 'MEDIUM',
        'reason': 'Year penalty',
        'options': [
            'A Legal Loophole Destroyed the Soviet Union.',
            'The Treaty Loophole That Ended the Soviet Union.',
            'The USSR Had a Self-Destruct Clause. Someone Found It.',
        ]
    },
    'WZnCxVPNF7A': {
        'current': "The 1713 Document That Still Controls Gibraltar's Borders",
        'views': 21, 'ret': 26.3, 'subs': 0, 'priority': 'MEDIUM',
        'reason': 'Year penalty',
        'options': [
            'Spain vs Britain. The Treaty Loophole Holding Gibraltar Hostage.',
            'Gibraltar Is British Because of One Treaty Clause.',
            'Britain Won Gibraltar With a Loophole. Spain Wants It Back.',
        ]
    },
    '6SdfqTYPviQ': {
        'current': '1,000 Years of Ukraine: The History Putin Erased',
        'views': 84, 'ret': 24.1, 'subs': 4, 'priority': 'MEDIUM',
        'reason': 'Colon pattern',
        'options': [
            "Putin Erased Ukraine's History. The Documents Prove It.",
            "Ukraine Existed Before Russia. Putin Doesn't Want You to Know.",
            'Putin vs Ukrainian History. The Evidence He Wants Erased.',
        ]
    },
    '_N_08zn95FY': {
        'current': "Why TURKEY and GREECE Can't Agree on these islands.",
        'views': 923, 'ret': 38.9, 'subs': 13, 'priority': 'LOW-RISK',
        'reason': 'Already performing well (923 views). Minor: needs active verb or number.',
        'options': [
            "Turkey vs Greece. The Islands They've Fought Over for Decades.",
            'Greece and Turkey Almost Went to War Over These Islands.',
            "Turkey Claims 152 Greek Islands. Here's Why.",
        ]
    },
    'Oc7oq292HkM': {
        'current': 'Why Trump Walked Back the Armenian Genocide',
        'views': 156, 'ret': 26.2, 'subs': 4, 'priority': 'MEDIUM',
        'reason': 'No active verb or number',
        'options': [
            'Trump Recognized the Armenian Genocide. Then He Reversed It.',
            'The Armenian Genocide Was Recognized. Then Erased.',
            'America Admitted the Armenian Genocide. Then Took It Back.',
        ]
    },
    'Ac-k2p9Gvj4': {
        'current': "The 'Ancient Hatreds' Narrative Is Completely Wrong About the Middle East",
        'views': 93, 'ret': 28.5, 'subs': 1, 'priority': 'MEDIUM',
        'reason': 'Too long (73 chars, truncated on mobile)',
        'options': [
            '"Ancient Hatreds" in the Middle East Are a Modern Invention.',
            "The Middle East's \"Ancient Hatreds\" Were Invented Recently.",
            "Middle East Conflicts Aren't Ancient. The Evidence Proves It.",
        ]
    },
    'XKAqt_ZLHGo': {
        'current': 'Why Egypt and Sudan Both Reject Bir Tawil',
        'views': 69, 'ret': 20.9, 'subs': 0, 'priority': 'MEDIUM',
        'reason': 'No active verb or number',
        'options': [
            "Two Countries Refuse to Claim This Land. Here's Why.",
            "Nobody Wants This 800-Square-Mile Desert. Here's Why.",
            'Egypt vs Sudan. The Land Neither Country Will Claim.',
        ]
    },
}


# ============================================================================
# Thesis Extraction & Title Generation
# ============================================================================

def get_db_tags(video_id: str) -> list[str]:
    """Get tags from the analytics DB for a video."""
    db_path = Path('tools/youtube_analytics/analytics.db')
    if not db_path.exists():
        return []
    try:
        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()
        c.execute('SELECT tags FROM videos WHERE video_id = ?', (video_id,))
        row = c.fetchone()
        conn.close()
        if row and row[0]:
            return json.loads(row[0])
    except Exception:
        pass
    return []


def get_opening_text(video_id: str) -> str:
    """Extract first ~500 words from SRT, script, or fetched transcript."""

    # Source 1: Project folder SRT/script
    project_slug = VIDEO_PROJECT_MAP.get(video_id)
    if project_slug:
        # Resolve across all stages — a retitled video is usually published, so
        # it lives in _ARCHIVED/published/, not _IN_PRODUCTION/ (the old hardcoded
        # path never existed for published videos and silently fell through).
        from tools.video_projects import AmbiguousSlugError, VideoProjectRepo

        try:
            project = VideoProjectRepo().by_slug(project_slug)
        except AmbiguousSlugError:
            project = None
        base = project.path if project else None
        if base is not None and base.exists():
            # SRT transcript
            for srt_file in sorted(base.glob('*.srt')):
                if 'BACKUP' in srt_file.name or '_es' in srt_file.name or '_fr' in srt_file.name:
                    continue
                try:
                    raw = srt_file.read_text(encoding='utf-8')
                    lines = []
                    for line in raw.splitlines():
                        line = line.strip()
                        if not line or re.match(r'^\d+$', line) or re.match(r'\d{2}:\d{2}:\d{2}', line):
                            continue
                        line = re.sub(r'<[^>]+>', '', line)
                        lines.append(line)
                    text = ' '.join(lines)
                    words = text.split()[:500]
                    return ' '.join(words)
                except Exception:
                    pass

            # Script draft
            script = base / '02-SCRIPT-DRAFT.md'
            if script.exists():
                try:
                    text = script.read_text(encoding='utf-8')
                    text = re.sub(r'#+\s+', '', text)
                    text = re.sub(r'\*+', '', text)
                    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
                    words = text.split()[:500]
                    return ' '.join(words)
                except Exception:
                    pass

    # Source 2: Fetched transcript (for videos without project folders)
    transcript_dir = Path('transcripts/retitle')
    if transcript_dir.exists():
        for txt_file in transcript_dir.glob(f'*-{video_id}.txt'):
            try:
                text = txt_file.read_text(encoding='utf-8')
                words = text.split()[:500]
                return ' '.join(words)
            except Exception:
                pass

    return ''


def extract_thesis(opening_text: str) -> list[str]:
    """Extract thesis/claim sentences from the opening.

    Strategy: The script hook works like this:
      1. Setup sentence (context)
      2. Pivot marker ("But...", "Here's what...")
      3. THE ACTUAL CLAIM (1-2 sentences after the pivot)

    We want #3, not #2. The pivot is a teaser; the claim is the title material.

    Returns list of claim sentences, ordered by strength.
    """
    if not opening_text:
        return []

    # Split into sentences
    raw_sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"])', opening_text)

    sentences = []
    for s in raw_sentences:
        s = s.strip()
        if len(s) < 10:
            continue
        sentences.append(s)

    if not sentences:
        return []

    # Phase 1: Find pivot indices (the "but" / "here's what" moments)
    pivot_indices = []
    for i, sent in enumerate(sentences[:20]):
        lower = sent.lower()
        if (re.search(r'\bbut\b', lower)
                or "here's what" in lower
                or "here's the" in lower
                or 'however' in lower):
            pivot_indices.append(i)

    # Phase 2: Collect claim sentences (sentences AFTER pivots + standalone claims)
    claims = []

    # Claims that follow a pivot (the actual thesis)
    for pi in pivot_indices:
        # Check if the pivot sentence ITSELF contains the claim after "but"
        sent = sentences[pi]
        lower = sent.lower()
        for marker in ['but ', 'however, ', 'however ']:
            if marker in lower:
                idx = lower.index(marker) + len(marker)
                after = sent[idx:].strip()
                if len(after) > 20:
                    after = after[0].upper() + after[1:]
                    claims.append((after, 5))  # High score — claim after pivot

        # Also grab 1-2 sentences AFTER the pivot
        for offset in [1, 2]:
            j = pi + offset
            if j < len(sentences):
                next_sent = sentences[j]
                # Skip if this is another teaser/pivot
                nl = next_sent.lower()
                if "here's" in nl or nl.startswith('but '):
                    continue
                claims.append((next_sent, 4 - offset))

    # Phase 3: Also score standalone claim sentences (not tied to a pivot)
    for i, sent in enumerate(sentences[:20]):
        lower = sent.lower()
        score = 0

        # Strong standalone claim markers
        if 'destroyed' in lower or 'invented' in lower or 'fabricated' in lower:
            score += 3
        if 'never' in lower or "didn't" in lower or "wasn't" in lower:
            score += 2
        if 'proves' in lower or 'reveals' in lower:
            score += 2
        if 'twice' in lower or 'again' in lower:
            score += 2
        if 'still' in lower and ('today' in lower or 'now' in lower):
            score += 2

        # Skip pure teasers and context
        if "here's" in lower or lower.startswith('but '):
            continue
        if score == 0:
            continue

        # Bonus for punchy short claims
        if len(sent.split()) <= 8:
            score += 1

        claims.append((sent, score))

    # Deduplicate and sort
    seen = set()
    unique_claims = []
    for claim, score in sorted(claims, key=lambda x: -x[1]):
        cl = claim.lower()
        if cl in seen:
            continue
        seen.add(cl)
        unique_claims.append(claim)

    return unique_claims[:6]


# Proven title patterns (measured CTR from 33 videos)
# versus=4.0%, declarative=3.8%, how_why=3.3%, question=2.4%, colon=2.3%

# Actors: countries/orgs/people that can serve as title subjects
KNOWN_ACTORS = {
    'britain', 'british', 'china', 'chinese', 'russia', 'russian',
    'turkey', 'turkish', 'greece', 'greek', 'cyprus', 'iran', 'iranian',
    'america', 'american', 'united states', 'france', 'french',
    'spain', 'spanish', 'peru', 'peruvian', 'thailand', 'thai',
    'cambodia', 'cambodian', 'georgia', 'georgian', 'ukraine', 'ukrainian',
    'egypt', 'egyptian', 'sudan', 'sudanese', 'israel', 'israeli',
    'germany', 'german', 'mexico', 'mexican', 'mauritius',
    'somalia', 'somaliland', 'ethiopia', 'ethiopian', 'italy', 'italian',
    'philippines', 'vietnam', 'taiwan', 'armenia', 'armenian',
    'ottoman', 'soviet', 'ussr', 'cia', 'nato', 'eu', 'icj',
    'putin', 'trump', 'fuentes',
}

# Normalize to canonical display names
ACTOR_DISPLAY = {
    'british': 'Britain', 'chinese': 'China', 'russian': 'Russia',
    'turkish': 'Turkey', 'greek': 'Greece', 'iranian': 'Iran',
    'american': 'America', 'french': 'France', 'spanish': 'Spain',
    'peruvian': 'Peru', 'thai': 'Thailand', 'cambodian': 'Cambodia',
    'georgian': 'Georgia', 'ukrainian': 'Ukraine', 'egyptian': 'Egypt',
    'sudanese': 'Sudan', 'israeli': 'Israel', 'german': 'Germany',
    'mexican': 'Mexico', 'ethiopian': 'Ethiopia', 'italian': 'Italy',
    'armenian': 'Armenia',
    'ottoman': 'Ottoman Empire', 'soviet': 'The Soviet Union',
    'ussr': 'The Soviet Union',
    'cia': 'The CIA', 'nato': 'NATO', 'eu': 'The EU', 'icj': 'The ICJ',
    'putin': 'Putin', 'trump': 'Trump', 'fuentes': 'Nick Fuentes',
}

# Topic-specific actor overrides: some videos have a clear primary matchup
# that shouldn't be overridden by actors mentioned in passing in the transcript
VIDEO_ACTOR_OVERRIDES = {
    'Oc7oq292HkM': ['Trump', 'Armenia'],       # Armenian genocide recognition
    '71xY0Pt4T-M': ['Russia', 'Georgia'],       # Georgia 2008 (not "Georgia vs Ukraine")
    'Ac-k2p9Gvj4': ['Colonial Powers', 'The Middle East'],  # Ancient hatreds myth
    '6SdfqTYPviQ': ['Putin', 'Ukraine'],         # Ukraine history
    'xODFE2Pyubo': ['Thailand', 'Cambodia'],     # Temple dispute
}

# Strong verbs that work in titles (create tension + specificity)
# Tier 1: dramatic action verbs (best for titles)
TITLE_VERBS_T1 = {
    'destroyed', 'erased', 'divided', 'invaded', 'expelled',
    'stole', 'annexed', 'fabricated', 'invented', 'conquered',
    'deleted', 'carved', 'partitioned', 'rewrote', 'betrayed',
    'emptied', 'deported', 'coerced', 'occupied', 'abolished',
    'overthrew', 'toppled', 'rigged', 'forged', 'faked', 'weaponized',
}
# Tier 2: informational verbs (ok for titles, less dramatic)
TITLE_VERBS_T2 = {
    'signed', 'wrote', 'created', 'drew', 'claimed', 'proved',
    'built', 'broke', 'split', 'blocked', 'denied', 'rejected',
    'refused', 'ignored', 'hid', 'buried', 'lost', 'ceased',
    'collapsed', 'failed', 'survived', 'existed', 'appeared',
    'recognized', 'reversed', 'backed', 'abandoned', 'admitted',
}
TITLE_VERBS = TITLE_VERBS_T1 | TITLE_VERBS_T2


def _clean_claim(text: str) -> str:
    """Strip years, colons, HTML, and normalize whitespace."""
    s = re.sub(r'<[^>]+>', '', text)
    # Strip years but also handle "in 1828," → "" and "from 1713" → ""
    s = re.sub(r'\b(in|on|by|from|of|after)\s+(1[0-9]{3}|20[0-2][0-9])\b,?\s*',
               '', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b,?\s*', '', s)
    s = s.replace(':', '.')
    s = re.sub(r'\s+', ' ', s).strip()
    # Fix orphaned leading prepositions from year removal
    s = re.sub(r'^(In|On|By|From)\s+(?=[a-z,.])', '', s)
    # Fix orphaned commas/periods at start
    s = re.sub(r'^[,.\s]+', '', s)
    # Fix "September 22nd, ." type artifacts
    s = re.sub(r',\s*\.', '.', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def extract_actors_from_text(text: str) -> list[str]:
    """Find actor names in text, return as display names ordered by position."""
    found = []
    lower = text.lower()
    seen = set()
    for actor in KNOWN_ACTORS:
        if re.search(r'\b' + re.escape(actor) + r'\b', lower):
            display = ACTOR_DISPLAY.get(actor, actor.title())
            if display not in seen:
                # Use position in text for ordering (earlier = more important)
                pos = lower.index(actor)
                found.append((pos, display))
                seen.add(display)
    found.sort()
    return [name for _, name in found]


def extract_verb_from_claim(claim: str) -> str | None:
    """Find the strongest verb in a claim sentence."""
    lower = claim.lower()
    for verb in TITLE_VERBS:
        if verb in lower:
            return verb
    return None


def extract_object_phrase(claim: str, verb: str) -> str | None:
    """Extract what comes after the verb (the object of the action)."""
    # Find verb in claim and grab what follows
    match = re.search(r'\b' + re.escape(verb) + r'\b\s+(.+)', claim, re.IGNORECASE)
    if match:
        obj = match.group(1).strip().rstrip('.')
        # Limit length
        words = obj.split()[:6]
        return ' '.join(words)
    return None


def thesis_to_titles(claims: list[str], tags: list[str],
                     current_title: str, video_id: str = '') -> list[str]:
    """Convert thesis claims into browse-page-ready titles.

    Pipeline:
    1. Extract WHO (actors from title/tags/claims)
    2. Extract WHAT (verb + object from claims)
    3. Slot into proven patterns (versus at 4.0% CTR, declarative at 3.8%)

    Titles must work for a channel with no audience:
    - Tell you WHAT the video is about (no assumed context)
    - Create TENSION (why click?)
    - Be SEARCHABLE (contain topic keywords)
    """
    if not claims:
        return []

    # Step 1: Get actors — use overrides if available, else extract
    override = VIDEO_ACTOR_OVERRIDES.get(video_id)
    if override:
        all_actors = list(override)
    else:
        title_actors = extract_actors_from_text(current_title)
        tag_text = ' '.join(tags)
        tag_actors = extract_actors_from_text(tag_text)

        # Merge: title actors first, then tag actors (deduped)
        all_actors = list(title_actors)
        for a in tag_actors:
            if a not in all_actors:
                all_actors.append(a)

        # Also check claims for actors not in title/tags
        for claim in claims:
            for a in extract_actors_from_text(claim):
                if a not in all_actors:
                    all_actors.append(a)

    # Step 2: Extract action insights from claims
    insights = []  # list of (verb, object_phrase, full_claim)
    for claim in claims:
        clean = _clean_claim(claim)
        verb = extract_verb_from_claim(clean)
        if verb:
            obj = extract_object_phrase(clean, verb)
            insights.append((verb, obj, clean))

    # Step 3: Generate titles using proven patterns
    generated = []
    actors = all_actors[:4]  # Top 4 actors

    # --- VERSUS pattern (4.0% CTR, best performer) ---
    if len(actors) >= 2:
        a, b = actors[0], actors[1]
        # In "X vs Y" position, strip leading "The " for cleaner titles
        if b.startswith('The '):
            b = b[4:]
        # Versus + insight from script (only dramatic verbs for "Who Really X?")
        for verb, obj, _ in insights[:2]:
            if obj and verb in TITLE_VERBS_T1:
                short_obj = obj.split(',')[0].strip()
                # Only use if object is meaningful (3+ chars, not a pronoun)
                if len(short_obj) > 5 and short_obj.lower() not in {
                    'it', 'them', 'this', 'that', 'a memo', 'to exist',
                }:
                    t = f'{a} vs {b}. Who Really {verb.title()} {short_obj}?'
                    generated.append(t)

        # Versus + claim-as-subtitle (preferred over generic kicker)
        for _, _, claim in insights[:2]:
            # Compress claim to fit after "A vs B."
            short = _compress_phrase(claim, 40)
            if short and len(short) > 15:
                t = f'{a} vs {b}. {short}.'
                generated.append(t)

        # Versus + varied kickers (only if no verb/claim titles generated above)
        versus_kickers = [
            'The Documents Tell a Different Story.',
            'One Side Is Lying.',
            'The Evidence Picks a Side.',
        ]
        # Only add 1 generic kicker, and only as last resort
        if not any(f'{a} vs {b}' in g for g in generated):
            generated.append(f'{a} vs {b}. {versus_kickers[0]}')

    # --- DECLARATIVE + ACTIVE VERB (3.8% CTR) ---
    decl_kickers = [
        'The Documents Prove It.',
        'And Nobody Stopped Them.',
        "Here's the Evidence.",
        'And Got Away With It.',
    ]
    for i, (verb, obj, _) in enumerate(insights[:3]):
        if not obj:
            continue
        # Actor + verb + object + kicker
        if actors:
            obj_clean = obj.rstrip('.').strip()
            # Rotate kickers to avoid repetition
            kicker = decl_kickers[i % len(decl_kickers)]
            t = f'{actors[0]} {verb.title()} {obj_clean}. {kicker}'
            generated.append(t)

    # --- DECLARATIVE from full claims (rewritten for browse page) ---
    for _, _, claim in insights[:3]:
        clean = _clean_claim(claim)
        # Only use if it contains enough context (has an actor + verb)
        has_actor = any(a.lower() in clean.lower() for a in actors[:2]) if actors else False
        if has_actor and 35 <= len(clean) <= 70:
            generated.append(clean.rstrip('.') + '.')

    # --- CLAIM PAIRS: short punchy claim + evidence kicker ---
    kickers = [
        'The Documents Prove It.',
        'The Evidence Says Otherwise.',
        "Here's the Proof.",
        'Nobody Talks About This.',
    ]
    for _, _, claim in insights[:2]:
        core = _compress_phrase(_clean_claim(claim), 35)
        if core and len(core) > 15:
            for kicker in kickers[:2]:
                t = f'{core}. {kicker}'
                if 40 <= len(t) <= 70:
                    generated.append(t)

    # --- FALLBACK: No verb-based insights? Use strongest claims directly ---
    if not insights:
        for claim in claims[:3]:
            clean = _clean_claim(claim)
            if len(clean) < 15:
                continue
            # Only use if it contains a topic-relevant actor
            has_actor = any(a.lower() in clean.lower()
                           for a in actors[:3]) if actors else False
            if has_actor and 35 <= len(clean) <= 70:
                generated.append(clean.rstrip('.') + '.')
            # Try versus + claim
            if len(actors) >= 2 and len(clean) <= 40:
                t = f'{actors[0]} vs {actors[1]}. {clean}.'
                t = t.replace('..', '.')
                if len(t) <= 72:
                    generated.append(t)

    # --- NUMBER + TOPIC (specificity bonus) ---
    # Extract numbers from claims
    for claim in claims:
        numbers = re.findall(r'\b(\d[\d,]*)\b', claim)
        for num_str in numbers:
            num = int(num_str.replace(',', ''))
            if 1000 <= num <= 2099:  # Skip years
                continue
            if num < 2:
                continue
            if actors:
                t = f'{actors[0]} Made {num_str} Mistakes. The Documents Prove It.'
                if 40 <= len(t) <= 70:
                    generated.append(t)
            break  # Only use first good number

    # Deduplicate, filter, clean
    seen = set()
    unique = []
    current_lower = current_title.lower()
    for t in generated:
        t = t.strip()
        t = re.sub(r'\s+', ' ', t)
        t = t.replace('..', '.')
        if t and t[0].islower():
            t = t[0].upper() + t[1:]
        # Strip any remaining years
        t = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b,?\s*', '', t).strip()
        t_lower = t.lower()
        if t_lower in seen or t_lower == current_lower:
            continue
        if len(t) < 35 or len(t) > 72:
            continue
        if ':' in t:
            continue
        # Reject broken/nonsensical titles
        if t.startswith('And then ') or t.startswith('In '):
            continue
        # Reject titles with sentence fragments (end with function words before period)
        fragment_endings = [
            # Function words
            r'\bthe\b$', r'\bthat\b$', r'\bwho\b$', r'\bwhich\b$',
            r'\ba\b$', r'\ban\b$', r'\bof\b$', r'\bfor\b$', r'\bto\b$',
            r'\bwith\b$', r'\bfrom\b$', r'\bnever\b$', r'\bhe\b$',
            r'\bsaid\b$', r'\bwas\b$', r'\bbut\b$', r'\band\b$',
            r'\bin\b$', r'\bon\b$', r'\bby\b$', r'\bis\b$', r'\bare\b$',
            r'\balso\b$', r'\beven\b$', r'\bjust\b$', r'\bown\b$',
            r'\bhas\b$', r'\bhad\b$', r'\bhave\b$', r'\bwere\b$',
            # Transitive verbs left hanging (clearly expects an object)
            r'that \w+ed$',  # "that started", "that documented", "that created"
            # Common trailing adverbs
            r'\bactually\b$', r'\bparticularly\b$', r'\bcompletely\b$',
        ]
        is_fragment = False
        # Check each sentence in the title (split on ". ")
        for part in t.rstrip('.').split('. '):
            part_clean = part.strip().rstrip('.').strip()
            for pat in fragment_endings:
                if re.search(pat, part_clean):
                    is_fragment = True
                    break
            if is_fragment:
                break
        if is_fragment:
            continue
        # Reject script narration (pronouns as objects)
        if re.search(r'\b(it|them|this|him|her)\b[.!?]', t_lower):
            continue
        seen.add(t_lower)
        unique.append(t)

    return unique


def _compress_phrase(text: str, max_len: int) -> str:
    """Compress a phrase to max_len chars at a word boundary."""
    s = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b,?\s*', '', text).strip()
    s = re.sub(r'\s+', ' ', s)
    if len(s) <= max_len:
        return s
    truncated = s[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > max_len // 2:
        return truncated[:last_space]
    return truncated


def generate_script_titles(video_id: str, current_title: str) -> list[str]:
    """Generate title candidates from script thesis extraction.

    Pipeline:
    1. Get opening text (SRT/script)
    2. Extract thesis sentences (contrast markers, revelation language)
    3. Convert thesis → title candidates (compress, strip years/colons)
    4. Score and return best candidates
    """
    opening = get_opening_text(video_id)
    tags = get_db_tags(video_id)

    if not opening:
        return []

    # Extract thesis
    thesis = extract_thesis(opening)
    if not thesis:
        return []

    # Convert to titles
    candidates = thesis_to_titles(thesis, tags, current_title, video_id)

    # Score and rank
    current_score = score_title(current_title)['score']
    scored = [(t, score_title(t)['score']) for t in candidates]
    scored.sort(key=lambda x: -x[1])

    # Return top 5 that beat current, or top 3 regardless
    better = [t for t, s in scored if s > current_score][:5]
    if not better and scored:
        better = [t for t, _ in scored[:3]]

    return better


# ============================================================================
# Report Generation
# ============================================================================

def main():
    script_only = '--script-only' in sys.argv

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    lines = [
        '# Retitle Recommendations',
        '',
        f'**Generated:** {now}',
        '**Method:** title_scorer.py v2 (measured CTR) + thesis extraction from scripts',
        '**Rule:** No colons (-37% CTR), no years (-44% CTR), '
        'prefer versus/declarative patterns',
        '',
        '---',
        '',
    ]

    # Sort by priority
    priority_order = {'URGENT': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW-RISK': 3}
    sorted_items = sorted(
        CANDIDATES.items(),
        key=lambda x: (priority_order.get(x[1]['priority'], 9), -x[1].get('ret', 0))
    )

    for vid_id, data in sorted_items:
        current = score_title(data['current'])

        # Generate script-based titles
        script_titles = generate_script_titles(vid_id, data['current'])

        # Combine manual + script-generated options
        if script_only:
            all_options = script_titles
        else:
            all_options = data['options'] + script_titles

        if not all_options:
            all_options = data['options']

        lines.append(f"## {data['current']}")
        lines.append(f"**ID:** `{vid_id}` | **Views:** {data['views']} | "
                      f"**Retention:** {data['ret']}% | **Subs:** +{data['subs']} | "
                      f"**Priority:** {data['priority']}")
        lines.append(f"**Current score:** {current['score']}/100 ({current['grade']}) | "
                      f"Pattern: {current['pattern']}")
        lines.append(f"**Problem:** {data['reason']}")
        if script_titles:
            lines.append(f'**Script-generated:** {len(script_titles)} additional '
                         f'candidates from thesis extraction')
        lines.append('')
        lines.append('| # | Candidate | Score | Grade | Delta | Pattern | Source |')
        lines.append('|---|-----------|-------|-------|-------|---------|--------|')

        scored = []
        manual_set = set(data['options'])
        for opt in all_options:
            s = score_title(opt)
            delta = s['score'] - current['score']
            source = 'manual' if opt in manual_set else 'script'
            scored.append((opt, s['score'], s['grade'], s['pattern'], delta, source))

        for i, (opt, sc, grade, pattern, delta, source) in enumerate(
                sorted(scored, key=lambda x: -x[1]), 1):
            delta_str = f'+{delta}' if delta >= 0 else str(delta)
            lines.append(f'| {i} | {opt} | {sc} | {grade} | '
                         f'{delta_str} | {pattern} | {source} |')

        lines.append('')
        best = sorted(scored, key=lambda x: -x[1])[0]
        lines.append(f"**Recommended:** {best[0]} ({best[1]}/100, {best[5]})")
        lines.append('')
        lines.append('---')
        lines.append('')

    output = '\n'.join(lines)
    outpath = 'channel-data/RETITLE-RECOMMENDATIONS.md'
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f'Saved to {outpath}')
    print()

    # Print summary table
    print('SUMMARY')
    print('=' * 115)
    fmt = '{:50s} | {:>4s} | {:50s} | {:>4s} | {:6s}'
    print(fmt.format('Current Title', 'Old', 'Best New', 'New', 'Src'))
    print('-' * 115)
    for vid_id, data in sorted_items:
        cur = score_title(data['current'])
        script_titles = generate_script_titles(vid_id, data['current'])
        if script_only:
            all_opts = script_titles or data['options']
        else:
            all_opts = data['options'] + script_titles
        manual_set = set(data['options'])
        scored = [(opt, score_title(opt), 'manual' if opt in manual_set else 'script')
                  for opt in all_opts]
        best = max(scored, key=lambda x: x[1]['score'])
        print(fmt.format(
            data['current'][:50], str(cur['score']),
            best[0][:50], str(best[1]['score']), best[2],
        ))


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        pass
    sys.exit(0)
