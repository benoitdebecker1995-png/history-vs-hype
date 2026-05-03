"""
Aggregate outlier vs loser thumbnail patterns across 8 close-match channels.

Date: 2026-04-26
Includes the 3 new channels added in Phase B:
- PolyMatter (closest format match)
- Asianometry (mechanism/HOW gap)
- Lindybeige (myth-busting + sources, smaller scale)

Plus the 5 original close-match channels (Knowing Better, Shaun, Three Arrows, Kraut, WonderWhy).

Outputs:
  tools/benchmark/_outlier_thumbs_3x_filtered_v2.json (8-channel close-match aggregate)
"""
import json
import re
from pathlib import Path

NON_CONTENT_PATTERNS = [
    r'\bQ\s*&\s*A\b',
    r'\bSubscriber\b.*\bQ', r'\bQ\b.*\bSubscriber\b',
    r'\b\d+k\b.*\bQ', r'\bQ\b.*\b\d+k\b',
    r'giveaway', r'merchandise',
    r'\bnotebook\b.*king', r'king.*\bnotebook\b',
    r'lore recap', r'mission archive',
    r'\bbonus\b',
    r'subscribers?!\b',
    r'youtube live',
    r'\bchannel update\b',
    r'thank you for', r'we hit',
    r'\bpatreon\b',  # patreon shoutout
]
NON_CONTENT_RE = re.compile('|'.join(NON_CONTENT_PATTERNS), re.IGNORECASE)


def is_non_content(title):
    return bool(NON_CONTENT_RE.search(title or ''))


# Original 5 + 3 new
CHANNEL_FOLDERS = {
    'knowing_better': 'Knowing_Better',
    'shaun': 'Shaun',
    'three_arrows': 'Three_Arrows',
    'kraut': 'Kraut',
    'wonderwhy': 'WonderWhy',
    'polymatter': 'PolyMatter',
    'asianometry': 'Asianometry',
    'lindybeige': 'Lindybeige',
}

OUTLIER_T = 3.0
LOSER_T = 0.5


def stats(group):
    n = len(group)
    if n == 0:
        return {'n': 0}
    keys = ['has_map', 'has_text', 'has_face', 'has_arrows', 'has_icons']
    out = {'n': n}
    for k in keys:
        pct = 100 * sum(1 for o in group if o.get(k)) / n
        out[k + '_pct'] = round(pct, 0)
    # Distributions
    for field in ['face_type', 'text_style', 'primary_visual', 'map_type']:
        dist = {}
        for o in group:
            v = o.get(field) or 'none'
            dist[v] = dist.get(v, 0) + 1
        out[field + '_dist'] = dist
    return out


def main():
    per_channel = {}
    all_outliers, all_losers, all_videos, dropped = [], [], [], []

    for ch_lower, ch_folder in CHANNEL_FOLDERS.items():
        raw_path = Path(f'tools/benchmark/raw_data/{ch_lower}.json')
        cls_path = Path(f'tools/benchmark/thumbnails/{ch_folder}/_classifications.json')
        if not raw_path.exists():
            print(f'MISSING raw_data: {ch_lower}')
            continue
        if not cls_path.exists():
            print(f'MISSING classifications: {ch_folder}')
            continue

        raw = json.loads(raw_path.read_text(encoding='utf-8'))
        cls = json.loads(cls_path.read_text(encoding='utf-8'))
        cls_list = cls.get('classifications') or cls.get('videos') or []
        cls_by_id = {(c.get('video_id') or c.get('id')): c for c in cls_list}
        median = raw['median_views']

        outliers, losers = [], []
        for v in raw['all_videos']:
            ratio = v['view_count'] / median if median else 0
            c = cls_by_id.get(v['id'])
            if not c:
                continue
            rec = {
                'channel': raw['name'], 'title': v['title'], 'views': v['view_count'],
                'ratio': round(ratio, 2),
                'has_map': c.get('has_map'), 'map_type': c.get('map_type'),
                'has_text': c.get('has_text'), 'text_content': c.get('text_content'),
                'text_style': c.get('text_style'),
                'has_face': c.get('has_face'), 'face_type': c.get('face_type'),
                'has_arrows': c.get('has_arrows'), 'has_icons': c.get('has_icons'),
                'primary_visual': c.get('primary_visual'),
            }
            all_videos.append(rec)
            if is_non_content(v['title']):
                dropped.append(rec)
                continue
            if ratio >= OUTLIER_T:
                outliers.append(rec)
            elif ratio < LOSER_T:
                losers.append(rec)

        all_outliers.extend(outliers)
        all_losers.extend(losers)
        per_channel[raw['name']] = {
            'median': median,
            'subscriber_count': raw.get('subscriber_count'),
            'total': len(raw['all_videos']),
            'outliers': outliers,
            'losers': losers,
            'outlier_stats': stats(outliers),
            'loser_stats': stats(losers),
        }

    agg = {
        'outlier_stats': stats(all_outliers),
        'loser_stats': stats(all_losers),
        'all_video_stats': stats(all_videos),
    }

    print('=== AGGREGATE 8-CHANNEL CLOSE-MATCH ===\n')
    o = agg['outlier_stats']; l = agg['loser_stats']
    print(f'Outliers (3x+) n={o["n"]} | Losers (<0.5x, content-only) n={l["n"]}')
    print(f'Dropped non-content: {len(dropped)}')
    print(f'\n{"signal":18s} {"outliers":>10s} {"losers":>8s} {"delta":>8s}')
    for k in ['has_map_pct', 'has_text_pct', 'has_face_pct', 'has_arrows_pct', 'has_icons_pct']:
        if k in o and k in l:
            print(f'{k:18s} {o[k]:9.0f}% {l[k]:7.0f}% {o[k]-l[k]:+7.0f}pp')

    print('\n=== PER-CHANNEL ===')
    for name, data in per_channel.items():
        os_, ls_ = data['outlier_stats'], data['loser_stats']
        print(f'\n{name} (median={data["median"]:,}, subs={data.get("subscriber_count") or "?"})')
        print(f'  outliers n={os_.get("n",0)} | losers n={ls_.get("n",0)}')
        if os_.get('n'):
            print(f'  OUT  map={os_["has_map_pct"]:.0f}% text={os_["has_text_pct"]:.0f}% face={os_["has_face_pct"]:.0f}% arr={os_["has_arrows_pct"]:.0f}% ico={os_["has_icons_pct"]:.0f}%')
        if ls_.get('n'):
            print(f'  LOSE map={ls_["has_map_pct"]:.0f}% text={ls_["has_text_pct"]:.0f}% face={ls_["has_face_pct"]:.0f}% arr={ls_["has_arrows_pct"]:.0f}% ico={ls_["has_icons_pct"]:.0f}%')

    out_path = Path('tools/benchmark/_outlier_thumbs_3x_filtered_v2.json')
    out_path.write_text(json.dumps({
        'per_channel': per_channel,
        'agg_outliers': all_outliers,
        'agg_losers': all_losers,
        'aggregate_stats': agg,
        'dropped_non_content': dropped,
        'outlier_threshold': OUTLIER_T,
        'loser_threshold': LOSER_T,
        'channels_included': list(CHANNEL_FOLDERS.values()),
    }, indent=2), encoding='utf-8')
    print(f'\n[saved] {out_path}')
    print(f'  total outliers: {len(all_outliers)}')
    print(f'  total losers: {len(all_losers)}')
    print(f'  total videos: {len(all_videos)}')


if __name__ == '__main__':
    main()
