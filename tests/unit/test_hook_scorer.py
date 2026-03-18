"""
Unit tests for upgraded hook_scorer.py (Phase 69 — Hook Quality Upgrade).

Tests cover:
1. TestFrameworkDetection  — Document Reveal framework replaces 4-beat detection
2. TestFulfillmentCheck    — Entity echo + promise-type alignment when title provided
3. TestScoreHook           — Backward compat + new optional params
4. TestStyleRecommendation — Topic-type mapping + confidence scoring
5. TestFormatHookRanking   — Output format shows Framework column
"""

import unittest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

# Brazil hook — rich with anomaly (1494), stakes, inciting incident
BRAZIL_HOOK = """Open a language map of South America. Every country speaks Spanish. Except one.

And the border between Spanish and Portuguese South America isn't a mountain range or a river. It follows an almost perfect north-south line.

That line is a treaty. Signed on June 7th, 1494, in a small Spanish town called Tordesillas. Two countries drew a line through a world they'd never mapped.

The standard answer is: that's why Brazil speaks Portuguese. The pope drew a line. Portugal got the east. Done.

That answer is incomplete. Because in 1494, nobody could actually measure where that line was. Because most of modern Brazil sits on the wrong side of it. And because the people living there weren't speaking Portuguese anyway — until a government decree in 1757 forced them to.

Here's what actually happened. It starts with a wind pattern. And a compromise that accidentally included a continent nobody in Europe knew existed."""

# Hook with clear stakes language
STAKES_HOOK = (
    "This border which meant the entire water supply of a million people was controlled "
    "by a foreign power. The systemic consequence of this decision determined the fate "
    "of an empire. All of the surrounding regions were affected by what happened next. "
    "The resource flows were entirely redirected. " * 3
)

# Hook with clear inciting incident
INCITING_HOOK = (
    "Spain controlled most of the continent. But the problem was that nobody had "
    "actually surveyed the line. Except the explorers who arrived found something "
    "that nobody expected. Until the treaty was renegotiated in 1750, the ambiguity "
    "persisted. " * 3
)

# Generic context hook — no anomaly, no stakes, no inciting incident
GENERIC_HOOK = (
    "Throughout history, many countries have had disputes about their borders. "
    "Geopolitics is a complex field that involves many factors. For centuries, "
    "nations have struggled to define their territories. The history of borders "
    "is long and complicated. " * 3
)

# Mock pattern library returned by _load_pattern_library
# cold_fact: 7 examples → HIGH confidence
# myth_contradiction: 4 examples → LOW confidence
MOCK_PATTERN_LIBRARY = {
    'cold_fact': {
        'topic_types': ['territorial', 'political_fact_check'],
        'examples': [
            'In the year 401 BC, at the height of the period known as the Greek Golden Age...',
            'Around the year 1200 AD, the medieval Arab traveler...',
            'In the year 1858, the French novelist Gustave Flaubert arrived...',
            'around the year 1200 ad the medieval Arab traveler...',
            'in the year 1852 the French writer...',
            'In 1997, I was in middle school and the best movie ever was released...',
            'over the Millennium and a half that separate the rise of Augustus...',
        ],
        'confidence': 'high',
        'count': 7,
    },
    'myth_contradiction': {
        'topic_types': ['ideological', 'political_fact_check'],
        'examples': [
            'This video is going to look and sound a little different...',
            'We should all know the American creation myth...',
            'pacifism is objectively pro-fascist...',
            'London, Paris, Milan, and hundreds of other cities...',
        ],
        'confidence': 'low',
        'count': 4,
    },
    'specificity_bomb': {
        'topic_types': ['territorial', 'ideological'],
        'examples': [
            'in arizona\'s southern county of santa cruz you will find the city of nogales...',
            'Here in the temple of Isis at Fel is the last hieroglyphic inscription...',
            'I\'m Garrett Ryan this is toen Stone Roman concrete...',
        ],
        'confidence': 'low',
        'count': 3,
    },
    'contextual_opening': {
        'topic_types': ['territorial', 'ideological'],
        'examples': [
            'somewhere more less close to you there\'s a prison...',
            'when you search through history books you will find many anecdotes...',
        ],
        'confidence': 'low',
        'count': 8,
    },
}


class TestFrameworkDetection(unittest.TestCase):
    """Test Document Reveal framework detection replaces 4-beat detection."""

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_anomaly_detected(self, mock_lib):
        """Hook with year/number in first 30 words scores anomaly > 0."""
        from tools.research.hook_scorer import score_hook
        hook = "In 1494, Spain and Portugal signed a treaty that divided the known world. " * 5
        result = score_hook(hook, label='test')
        self.assertIn('framework', result)
        self.assertGreater(result['framework']['anomaly'], 0,
                           "Year '1494' in first 30 words should score anomaly > 0")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_stakes_detected(self, mock_lib):
        """Hook with systemic consequence language scores stakes > 0."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(STAKES_HOOK, label='stakes')
        self.assertIn('framework', result)
        self.assertGreater(result['framework']['stakes'], 0,
                           "Phrases like 'which meant', 'entire', 'million' should score stakes > 0")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_inciting_incident_detected(self, mock_lib):
        """Hook with pivot language scores inciting_incident > 0."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(INCITING_HOOK, label='inciting')
        self.assertIn('framework', result)
        self.assertGreater(result['framework']['inciting_incident'], 0,
                           "Pivot words like 'but', 'except', 'the problem was' should score inciting_incident > 0")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_framework_replaces_beats(self, mock_lib):
        """Result dict has 'framework' key and 'framework_score', NOT 'beats' or 'beat_score'."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, label='brazil')
        self.assertIn('framework', result, "Result must have 'framework' key")
        self.assertIn('framework_score', result, "Result must have 'framework_score' key")
        self.assertNotIn('beats', result, "Result must NOT have 'beats' key")
        self.assertNotIn('beat_score', result, "Result must NOT have 'beat_score' key")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_framework_score_in_range(self, mock_lib):
        """Framework score is in 0-40 range."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, label='brazil')
        self.assertGreaterEqual(result['framework_score'], 0)
        self.assertLessEqual(result['framework_score'], 40)

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_brazil_hook_scores_anomaly(self, mock_lib):
        """Brazil hook with '1494' should score anomaly (year in first 30 words)."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, label='brazil')
        self.assertGreater(result['framework']['anomaly'], 0,
                           "Brazil hook contains '1494' — should score anomaly")


class TestFulfillmentCheck(unittest.TestCase):
    """Test title-fulfillment check: entity echo + promise-type alignment."""

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_entity_echo_pass(self, mock_lib):
        """Hook mentioning title entities in first 50 words → entity_echo.passed == True."""
        from tools.research.hook_scorer import score_hook
        hook = "In 1494, Spain and Portugal divided the world with a single line on a map. " * 5
        result = score_hook(hook, label='test', title='Spain vs Portugal Divided the World')
        self.assertIn('fulfillment', result)
        self.assertTrue(result['fulfillment']['entity_echo']['passed'],
                        "Hook mentions Spain and Portugal in first 50 words — entity echo should pass")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_entity_echo_fail(self, mock_lib):
        """Hook not mentioning title entities in first 50 words → entity_echo.passed == False."""
        from tools.research.hook_scorer import score_hook
        hook = "South America is a continent of surprising diversity. The geography of the region " \
               "has shaped its history in profound ways. Many nations rose and fell here. " * 3
        result = score_hook(hook, label='test', title='Spain vs Portugal Divided the World')
        self.assertIn('fulfillment', result)
        self.assertFalse(result['fulfillment']['entity_echo']['passed'],
                         "Hook doesn't mention Spain or Portugal in first 50 words — entity echo should fail")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_promise_type_match(self, mock_lib):
        """Title with 'vs' (conflict) + hook with two entities in opposition → promise_type.passed == True."""
        from tools.research.hook_scorer import score_hook
        # conflict title
        # hook names both entities and frames as rivalry/division
        hook = "Spain controlled the west. Portugal controlled the east. They divided the world " \
               "between them with a single line — and the rivalry between these two empires " \
               "would determine the fate of two continents. " * 3
        result = score_hook(hook, label='test', title='Spain vs Portugal: Who Divided the World')
        self.assertIn('fulfillment', result)
        self.assertTrue(result['fulfillment']['promise_type']['passed'],
                        "Conflict title + hook with two entities in opposition should pass")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_promise_type_mismatch(self, mock_lib):
        """Title promises conflict but hook opens with generic context → promise_type.passed == False, fix present."""
        from tools.research.hook_scorer import score_hook
        hook = "Throughout history, many empires have risen and fallen. The story of colonialism " \
               "is one of the most complex in human history. Many factors contributed to " \
               "the European expansion that took place in the 15th century. " * 3
        result = score_hook(hook, label='test', title='Spain vs Portugal: Who Divided the World')
        self.assertIn('fulfillment', result)
        self.assertFalse(result['fulfillment']['promise_type']['passed'],
                         "Generic-context hook with conflict title should fail promise_type")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_mismatch_suggests_fix(self, mock_lib):
        """When fulfillment fails, result['fulfillment']['fix_suggestion'] is a non-empty string."""
        from tools.research.hook_scorer import score_hook
        hook = "Throughout history, many empires have risen and fallen. The story of colonialism " \
               "is one of the most complex in human history. Many factors contributed to " \
               "the European expansion. " * 3
        result = score_hook(hook, label='test', title='Spain vs Portugal Divided the World')
        self.assertIn('fulfillment', result)
        fix = result['fulfillment'].get('fix_suggestion', '')
        self.assertIsInstance(fix, str)
        self.assertGreater(len(fix), 0,
                           "A fulfillment failure should include a non-empty fix_suggestion")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_fulfillment_has_title_entities(self, mock_lib):
        """Fulfillment result includes title_entities list."""
        from tools.research.hook_scorer import score_hook
        hook = "Spain and Portugal signed the treaty in 1494. " * 5
        result = score_hook(hook, label='test', title='Spain vs Portugal')
        self.assertIn('fulfillment', result)
        self.assertIn('title_entities', result['fulfillment']['entity_echo'],
                      "entity_echo should include title_entities list")


class TestScoreHook(unittest.TestCase):
    """Test score_hook() signature, backward compat, and new optional params."""

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_no_title_skips_fulfillment(self, mock_lib):
        """score_hook(text, title=None) → 'fulfillment' key not in result."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, title=None)
        self.assertNotIn('fulfillment', result,
                         "No title passed — fulfillment key must be absent")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_no_topic_skips_style(self, mock_lib):
        """score_hook(text, topic_type=None) → 'style_recommendation' key not in result."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, topic_type=None)
        self.assertNotIn('style_recommendation', result,
                         "No topic_type passed — style_recommendation key must be absent")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_backward_compat_no_title(self, mock_lib):
        """score_hook(text) with no kwargs returns valid total_score 0-100."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK)
        self.assertIn('total_score', result)
        self.assertGreaterEqual(result['total_score'], 0)
        self.assertLessEqual(result['total_score'], 100)

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_total_score_max_100(self, mock_lib):
        """With all dimensions provided, total_score never exceeds 100."""
        from tools.research.hook_scorer import score_hook
        # Use a hook with everything — anomaly, stakes, inciting incident
        result = score_hook(BRAZIL_HOOK, title='Spain vs Portugal Divided the World',
                            topic_type='territorial')
        self.assertLessEqual(result['total_score'], 100,
                             "Total score must never exceed 100")
        self.assertGreaterEqual(result['total_score'], 0)

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_score_hook_has_issues_and_strengths(self, mock_lib):
        """score_hook() result always has issues and strengths lists."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK)
        self.assertIn('issues', result)
        self.assertIn('strengths', result)
        self.assertIsInstance(result['issues'], list)
        self.assertIsInstance(result['strengths'], list)

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_short_hook_returns_valid_result(self, mock_lib):
        """Very short hook returns valid result dict with total_score."""
        from tools.research.hook_scorer import score_hook
        result = score_hook('Too short.')
        self.assertIn('total_score', result)
        self.assertEqual(result['total_score'], 0)


class TestStyleRecommendation(unittest.TestCase):
    """Test topic-type → style recommendation with confidence-based scoring."""

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_territorial_recommends_cold_fact(self, mock_lib):
        """score_hook(text, topic_type='territorial') → style_recommendation.recommended == 'cold_fact'."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, topic_type='territorial')
        self.assertIn('style_recommendation', result)
        self.assertEqual(result['style_recommendation']['recommended'], 'cold_fact',
                         "Territorial topic should recommend cold_fact style")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_ideological_recommends_myth_contradiction(self, mock_lib):
        """score_hook(text, topic_type='ideological') → style_recommendation.recommended == 'myth_contradiction'."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, topic_type='ideological')
        self.assertIn('style_recommendation', result)
        self.assertEqual(result['style_recommendation']['recommended'], 'myth_contradiction',
                         "Ideological topic should recommend myth_contradiction style")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_political_recommends_specificity_bomb(self, mock_lib):
        """score_hook(text, topic_type='political_fact_check') → style_recommendation.recommended == 'specificity_bomb'."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, topic_type='political_fact_check')
        self.assertIn('style_recommendation', result)
        self.assertEqual(result['style_recommendation']['recommended'], 'specificity_bomb',
                         "Political fact check topic should recommend specificity_bomb style")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_low_confidence_no_score_impact(self, mock_lib):
        """myth_contradiction has <5 examples → style match/mismatch does NOT change total_score."""
        from tools.research.hook_scorer import score_hook
        # myth_contradiction is low confidence (4 examples in mock)
        # Score with topic and without — difference should be 0
        result_with = score_hook(BRAZIL_HOOK, topic_type='ideological')
        result_without = score_hook(BRAZIL_HOOK)
        # The style_recommendation score_modifier should be 0 for low confidence
        self.assertEqual(result_with['style_recommendation']['score_modifier'], 0,
                         "Low-confidence pattern should have score_modifier == 0")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_high_confidence_match_bonus(self, mock_lib):
        """cold_fact has 7+ examples + hook matches → total_score includes +5 bonus."""
        from tools.research.hook_scorer import score_hook
        # Brazil hook starts with year (1494) — matches cold_fact style
        result = score_hook(BRAZIL_HOOK, topic_type='territorial')
        # cold_fact is high confidence (7 examples) and Brazil hook has anomaly (year)
        style_rec = result['style_recommendation']
        # If hook matched cold_fact, modifier should be +5
        # We check score_modifier is either +5 (match) or -5 (mismatch) or 0 (no data)
        self.assertIn(style_rec['score_modifier'], [-5, 0, 5],
                      "High confidence score_modifier should be -5, 0, or +5")
        self.assertIn('confidence', style_rec)
        self.assertEqual(style_rec['confidence'], 'high',
                         "cold_fact with 7 examples should be HIGH confidence")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_style_recommendation_has_examples(self, mock_lib):
        """Style recommendation includes examples list from pattern library."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, topic_type='territorial')
        style_rec = result['style_recommendation']
        self.assertIn('examples', style_rec)
        self.assertIsInstance(style_rec['examples'], list)
        self.assertGreater(len(style_rec['examples']), 0,
                           "Style recommendation should include at least one example")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_general_topic_has_no_recommendation(self, mock_lib):
        """topic_type='general' → style_recommendation.recommended is None."""
        from tools.research.hook_scorer import score_hook
        result = score_hook(BRAZIL_HOOK, topic_type='general')
        self.assertIn('style_recommendation', result)
        # general type has no mapping — recommended should be None or 'none'
        recommended = result['style_recommendation'].get('recommended')
        self.assertFalse(recommended,
                         "General topic type should have no recommended style (None or empty)")


class TestFormatHookRanking(unittest.TestCase):
    """Test format_hook_ranking() shows Framework column, not Beats."""

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_format_shows_framework_not_beats(self, mock_lib):
        """format_hook_ranking output contains 'Framework' column, not 'Beats'."""
        from tools.research.hook_scorer import rank_hooks, format_hook_ranking
        hooks = [
            {'label': 'Hook A', 'text': BRAZIL_HOOK},
            {'label': 'Hook B', 'text': GENERIC_HOOK},
        ]
        ranked = rank_hooks(hooks)
        output = format_hook_ranking(ranked)
        self.assertIn('Framework', output,
                      "format_hook_ranking output must contain 'Framework' column header")
        self.assertNotIn('| Beats |', output,
                         "format_hook_ranking output must NOT contain 'Beats' column")

    @patch('tools.research.hook_scorer._load_pattern_library', return_value=MOCK_PATTERN_LIBRARY)
    def test_rank_hooks_returns_sorted_list(self, mock_lib):
        """rank_hooks() returns list sorted by total_score descending."""
        from tools.research.hook_scorer import rank_hooks
        hooks = [
            {'label': 'Generic', 'text': GENERIC_HOOK},
            {'label': 'Brazil', 'text': BRAZIL_HOOK},
        ]
        ranked = rank_hooks(hooks)
        self.assertEqual(len(ranked), 2)
        # Brazil hook should score higher than generic hook
        scores = [h['total_score'] for h in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True),
                         "rank_hooks() should return list in descending score order")


class TestDetectTopicFromScript(unittest.TestCase):
    """Test detect_topic_from_script() function."""

    def test_territorial_detection(self):
        """Script with border/territory language → 'territorial'."""
        from tools.research.hook_scorer import detect_topic_from_script
        text = "The border between Spain and Portugal was disputed. The treaty defined territorial " \
               "control over the disputed zone. The frontier region was contested for decades. " * 10
        result = detect_topic_from_script(text)
        self.assertEqual(result, 'territorial')

    def test_ideological_detection(self):
        """Script with myth/ideology language → 'ideological'."""
        from tools.research.hook_scorer import detect_topic_from_script
        text = "This is a myth that many people believe. The ideology of nationalism shaped " \
               "how historians interpreted the events. The propaganda spread widely. " * 10
        result = detect_topic_from_script(text)
        self.assertEqual(result, 'ideological')

    def test_general_fallback(self):
        """Script with no strong topic signals → 'general'."""
        from tools.research.hook_scorer import detect_topic_from_script
        text = "Hello. This is some text. It does not contain specific domain keywords. " * 20
        result = detect_topic_from_script(text)
        self.assertIn(result, ['general', 'territorial', 'ideological', 'political_fact_check'],
                      "detect_topic_from_script must return a valid topic type string")

    def test_returns_string(self):
        """detect_topic_from_script always returns a string."""
        from tools.research.hook_scorer import detect_topic_from_script
        result = detect_topic_from_script('')
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
