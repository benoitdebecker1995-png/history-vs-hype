"""
Translation Pipeline Smoke Test (PIPE-03)

Validates the translation pipeline Python modules (pure data processing layer).
No API calls. No credentials needed. Tests module imports and data flow.

Usage:
    python tools/translation/cli.py smoketest
    python tools/translation/smoke_test.py

Output format:
    [1/4] Step name........... PASS (details)
    [2/4] Step name........... FAIL (error + fix suggestion)

Exit code 0 if all steps pass, 1 if any step fails.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

# Ensure tools/translation is on path when run directly
sys.path.insert(0, str(Path(__file__).parent))

# Test document: short 3-clause French legal snippet (fabricated, realistic)
TEST_DOCUMENT = """DECRET portant organisation des services publics

Préambule

Le Gouvernement de la République, considérant la nécessité d'organiser les services publics afin d'assurer le bon fonctionnement de l'administration et la protection des intérêts des citoyens, décrète ce qui suit.

Article 1

Tout fonctionnaire exerçant une fonction publique est tenu de respecter les dispositions du présent décret et de se conformer aux instructions de ses supérieurs hiérarchiques, sous peine de sanctions disciplinaires prévues par la loi.

Article 2

Les droits et obligations des agents de l'État sont définis conformément aux principes généraux du droit administratif. Aucune mesure portant atteinte aux droits fondamentaux des agents ne peut être prise sans consultation préalable des représentants du personnel.

Article 3

Le présent décret entre en vigueur à compter de sa publication au Journal Officiel. Les décrets antérieurs contraires aux dispositions du présent texte sont abrogés de plein droit."""


def _pad_step(step_name: str, total_width: int = 40) -> str:
    """Pad step name with dots to fixed width for aligned output."""
    dots_needed = total_width - len(step_name)
    if dots_needed < 3:
        dots_needed = 3
    return step_name + ('.' * dots_needed)


def _print_step(step_num: int, total: int, name: str, status: str, detail: str) -> None:
    """Print a formatted step result line."""
    padded = _pad_step(name)
    print(f"[{step_num}/{total}] {padded} {status} ({detail})")


def step1_module_health_check() -> Tuple[bool, str, str]:
    """
    Step 1: Verify all pipeline modules import correctly.

    Checks that TranslationDataBuilder, StructureDetector, and Formatter
    all import successfully — validating the pure Python data processing layer.

    Returns:
        (passed, detail_on_pass, error_on_fail)
    """
    modules_checked = []
    errors = []

    # Check TranslationDataBuilder
    try:
        from translator import TranslationDataBuilder
        builder = TranslationDataBuilder()
        modules_checked.append('TranslationDataBuilder')
    except ImportError as e:
        errors.append(f"translator.TranslationDataBuilder: {e}")
    except Exception as e:
        errors.append(f"translator.TranslationDataBuilder (init): {e}")

    # Check StructureDetector
    try:
        from structure_detector import StructureDetector
        _ = StructureDetector()
        modules_checked.append('StructureDetector')
    except ImportError as e:
        errors.append(f"structure_detector.StructureDetector: {e}")
    except Exception as e:
        errors.append(f"structure_detector.StructureDetector (init): {e}")

    # Check Formatter
    try:
        from formatter import Formatter
        _ = Formatter()
        modules_checked.append('Formatter')
    except ImportError as e:
        errors.append(f"formatter.Formatter: {e}")
    except Exception as e:
        errors.append(f"formatter.Formatter (init): {e}")

    if errors:
        error_msg = '; '.join(errors)
        return False, '', error_msg

    detail = f"{', '.join(modules_checked)} imported OK"
    return True, detail, ''


def step2_structure_detection() -> Tuple[bool, str, str, Any]:
    """
    Step 2: Run structure detection on the test document.

    Returns:
        (passed, detail, error, sections_for_next_step)
    """
    try:
        from structure_detector import StructureDetector
    except ImportError as e:
        return False, '', f"Could not import StructureDetector: {e}", None

    try:
        detector = StructureDetector()
        result = detector.detect_structure(TEST_DOCUMENT)

        if 'error' in result:
            return False, '', f"Structure detection failed: {result['error']}", None

        section_count = result.get('section_count', 0)
        if section_count < 2:
            return (
                False,
                '',
                f"Expected >= 2 sections, got {section_count}. "
                "Check structure_detector.py patterns.",
                None
            )

        sections = result.get('sections', [])
        return True, f"{section_count} sections detected", '', sections

    except Exception as e:
        return False, '', f"Structure detection raised exception: {e}", None


def step3_payload_builder(sections: list) -> Tuple[bool, str, str, Any]:
    """
    Step 3: Verify TranslationDataBuilder builds valid payloads (no LLM calls).

    Returns:
        (passed, detail, error, sample_payload)
    """
    try:
        from translator import TranslationDataBuilder
    except ImportError as e:
        return False, '', f"Could not import TranslationDataBuilder: {e}", None

    try:
        builder = TranslationDataBuilder()

        # Use first non-empty section
        test_section = None
        for section in sections:
            if section.get('body', '').strip():
                test_section = section
                break

        if test_section is None:
            return False, '', "No non-empty sections found in test document", None

        payload = builder.build_translation_payload(
            clause_text=test_section['body'],
            full_document=TEST_DOCUMENT,
            source_language='french',
            clause_id=test_section.get('id', 'section-1')
        )

        if 'error' in payload:
            return False, '', f"build_translation_payload returned error: {payload['error']}", None

        # Validate payload structure
        required_keys = ['clause_id', 'original', 'system_prompt', 'user_prompt']
        missing = [k for k in required_keys if k not in payload]
        if missing:
            return False, '', f"Payload missing required keys: {missing}", None

        if not payload['system_prompt']:
            return False, '', "system_prompt is empty", None

        if not payload['user_prompt']:
            return False, '', "user_prompt is empty", None

        detail = f"payload built for {payload['clause_id']} ({len(payload['user_prompt'])} chars)"
        return True, detail, '', payload

    except Exception as e:
        return False, '', f"Payload builder raised exception: {e}", None


def step4_response_parser() -> Tuple[bool, str, str]:
    """
    Step 4: Verify parse_response() handles formatted LLM output correctly.

    Returns:
        (passed, detail, error)
    """
    try:
        from translator import TranslationDataBuilder
    except ImportError as e:
        return False, '', f"Could not import TranslationDataBuilder: {e}"

    try:
        builder = TranslationDataBuilder()

        # Simulate a well-formed Claude response
        mock_response = """TRANSLATION:
The Government of the Republic, considering the necessity of organizing public services in order to ensure the proper functioning of administration and the protection of citizens' interests, decrees the following.

NOTES:
- "décrète ce qui suit" is a standard French administrative formula ("decrees the following")
- "bon fonctionnement" literally "good functioning" — "proper functioning" preserves register"""

        result = builder.parse_response(
            response_text=mock_response,
            clause_id='preamble',
            original_text='Le Gouvernement de la République...'
        )

        required_keys = ['clause_id', 'original', 'translation', 'notes']
        missing = [k for k in required_keys if k not in result]
        if missing:
            return False, '', f"parse_response result missing keys: {missing}"

        if not result['translation']:
            return False, '', "parse_response returned empty translation"

        if not isinstance(result['notes'], list):
            return False, '', f"notes should be a list, got {type(result['notes'])}"

        note_count = len(result['notes'])
        return True, f"translation extracted, {note_count} notes parsed", ''

    except Exception as e:
        return False, '', f"Response parser raised exception: {e}"


def run_smoke_test() -> int:
    """
    Run the full 4-step smoke test.

    Returns:
        Exit code: 0 (all pass) or 1 (any failure)
    """
    print("\n=== Translation Pipeline Smoke Test ===\n")

    total_steps = 4
    all_passed = True
    failures = []
    test_start = time.time()

    # Step 1: Module health check
    passed, detail, error = step1_module_health_check()

    if passed:
        _print_step(1, total_steps, "Module health check", "PASS", detail)
    else:
        _print_step(1, total_steps, "Module health check", "FAIL",
                    "see details below")
        all_passed = False
        failures.append({
            'step': 1,
            'name': 'Module health check',
            'error': error,
            'fix': (
                "Verify all translation modules are present:\n"
                "  tools/translation/translator.py\n"
                "  tools/translation/structure_detector.py\n"
                "  tools/translation/formatter.py"
            )
        })
        _print_results(all_passed, failures, test_start)
        return 1

    # Step 2: Structure detection
    passed, detail, error, sections = step2_structure_detection()

    if passed:
        _print_step(2, total_steps, "Structure detection", "PASS", detail)
    else:
        _print_step(2, total_steps, "Structure detection", "FAIL",
                    "see details below")
        all_passed = False
        failures.append({
            'step': 2,
            'name': 'Structure detection',
            'error': error,
            'fix': (
                "Check tools/translation/structure_detector.py\n"
                "Ensure ARTICLE_PATTERNS includes French article patterns."
            )
        })
        _print_results(all_passed, failures, test_start)
        return 1

    # Step 3: Payload builder
    passed, detail, error, payload = step3_payload_builder(sections)

    if passed:
        _print_step(3, total_steps, "Payload builder", "PASS", detail)
    else:
        _print_step(3, total_steps, "Payload builder", "FAIL",
                    "see details below")
        all_passed = False
        failures.append({
            'step': 3,
            'name': 'Payload builder',
            'error': error,
            'fix': (
                "Check tools/translation/translator.py\n"
                "Verify TranslationDataBuilder.build_translation_payload() returns\n"
                "dict with keys: clause_id, original, system_prompt, user_prompt"
            )
        })
        _print_results(all_passed, failures, test_start)
        return 1

    # Step 4: Response parser
    passed, detail, error = step4_response_parser()

    if passed:
        _print_step(4, total_steps, "Response parser", "PASS", detail)
    else:
        _print_step(4, total_steps, "Response parser", "FAIL",
                    "see details below")
        all_passed = False
        failures.append({
            'step': 4,
            'name': 'Response parser',
            'error': error,
            'fix': (
                "Check tools/translation/translator.py\n"
                "Verify TranslationDataBuilder.parse_response() handles\n"
                "TRANSLATION: and NOTES: markers correctly."
            )
        })

    _print_results(all_passed, failures, test_start)
    return 0 if all_passed else 1


def _print_results(all_passed: bool, failures: list, test_start: float) -> None:
    """Print final summary and any failure details."""
    total_elapsed = time.time() - test_start
    total_steps = 4
    passed_count = total_steps - len(failures)

    print()

    if all_passed:
        print(f"Result: ALL PASSED ({total_steps}/{total_steps})")
    else:
        print(f"Result: {len(failures)} FAILED ({passed_count}/{total_steps} passed)")

    print(f"Total time: {total_elapsed:.1f}s")

    if failures:
        print()
        print("=== Failure Details ===")
        for failure in failures:
            print(f"\n[Step {failure['step']}] {failure['name']}:")
            print(f"  Error: {failure['error']}")
            if failure.get('fix'):
                print(f"  Fix:\n    {failure['fix'].replace(chr(10), chr(10) + '    ')}")


if __name__ == '__main__':
    sys.exit(run_smoke_test())
