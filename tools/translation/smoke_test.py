"""
Translation Pipeline Smoke Test (PIPE-03)

End-to-end validation of the full translation pipeline in a single command.
Makes real API calls (intentional) to validate actual connectivity.

Usage:
    python tools/translation/cli.py smoketest
    python tools/translation/smoke_test.py

Output format:
    [1/5] Step name........... PASS (details)
    [2/5] Step name........... FAIL (error + fix suggestion)

Exit code 0 if all steps pass, 1 if any step fails.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, Tuple

# Ensure tools/translation is on path when run directly
sys.path.insert(0, str(Path(__file__).parent))

from env_loader import load_api_key

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


def step1_credential_check() -> Tuple[bool, str, str]:
    """
    Step 1: Verify API key is available.

    Returns:
        (passed, detail_on_pass, error_on_fail)
    """
    result = load_api_key()

    if 'error' in result:
        error_msg = result['error']
        return False, '', error_msg

    key = result['key']
    # Show partial key for confirmation (first 10 chars + masked rest)
    if len(key) > 10:
        key_display = key[:10] + '...' + key[-4:]
    else:
        key_display = key[:4] + '...'

    source = 'env var'
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        source = '.env file'

    return True, f"API key loaded from {source} ({key_display})", ''


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


def step3_translation(sections: list) -> Tuple[bool, str, str, Any]:
    """
    Step 3: Translate the detected sections.

    Returns:
        (passed, detail, error, translated_sections)
    """
    try:
        from translator import Translator
    except ImportError as e:
        return False, '', f"Could not import Translator: {e}", None

    start = time.time()

    try:
        translator = Translator()

        if translator.error:
            return False, '', translator.error, None

        result = translator.translate_document(
            sections=sections,
            source_language='french',
            full_text=TEST_DOCUMENT
        )

        elapsed = time.time() - start

        if 'error' in result:
            return False, '', result['error'], None

        translated = result.get('sections', [])

        # Verify each section has a non-empty translation
        missing = [
            s.get('id', f'section-{i+1}')
            for i, s in enumerate(translated)
            if not s.get('translation', '').strip()
            and not s.get('error')  # allow sections that explicitly errored
        ]

        if missing:
            return (
                False,
                '',
                f"Sections missing translations: {', '.join(missing)}",
                None
            )

        clause_count = result.get('clause_count', len(translated))
        return True, f"{clause_count} clauses translated, {elapsed:.1f}s", '', translated

    except Exception as e:
        return False, '', f"Translation raised exception: {e}", None


def step4_formatting(translated_sections: list) -> Tuple[bool, str, str]:
    """
    Step 4: Format translated sections to markdown.

    Returns:
        (passed, detail, error)
    """
    try:
        from formatter import Formatter
    except ImportError as e:
        return False, '', f"Could not import Formatter: {e}"

    try:
        formatter = Formatter()
        output = formatter.format_paired(translated_sections, output_format='markdown')

        if not output or not output.strip():
            return False, '', "Formatter returned empty output"

        if '##' not in output:
            return (
                False,
                '',
                "Formatter output missing expected '##' markdown headers. "
                "Check formatter.format_paired() output."
            )

        line_count = len(output.strip().splitlines())
        return True, f"markdown output generated ({line_count} lines)", ''

    except Exception as e:
        return False, '', f"Formatting raised exception: {e}"


def step5_pipeline_integrity(
    sections: list,
    translated_sections: list
) -> Tuple[bool, str, str]:
    """
    Step 5: Verify pipeline data integrity end-to-end.

    Checks that input section IDs match output section IDs
    and translations are non-empty for non-preamble sections.

    Returns:
        (passed, detail, error)
    """
    if not sections or not translated_sections:
        return False, '', "No sections or translated sections to validate"

    input_ids = {s.get('id', f'section-{i+1}') for i, s in enumerate(sections)}
    output_ids = {s.get('id', f'section-{i+1}') for i, s in enumerate(translated_sections)}

    missing_in_output = input_ids - output_ids
    if missing_in_output:
        return (
            False,
            '',
            f"Section IDs in input not found in output: {missing_in_output}"
        )

    # Verify no translation is entirely the error placeholder
    error_sections = [
        s.get('id', 'unknown')
        for s in translated_sections
        if s.get('translation', '').startswith('[Translation failed:')
    ]

    if error_sections:
        return (
            False,
            '',
            f"Translation failed for sections: {', '.join(error_sections)}"
        )

    return True, f"all {len(translated_sections)} steps connected", ''


def run_smoke_test() -> int:
    """
    Run the full 5-step smoke test.

    Returns:
        Exit code: 0 (all pass) or 1 (any failure)
    """
    print("\n=== Translation Pipeline Smoke Test ===\n")

    total_steps = 5
    all_passed = True
    failures = []
    test_start = time.time()

    # Step 1: Credential check
    step_start = time.time()
    passed, detail, error = step1_credential_check()
    step_elapsed = time.time() - step_start

    if passed:
        _print_step(1, total_steps, "Credential check", "PASS", detail)
    else:
        _print_step(1, total_steps, "Credential check", "FAIL",
                    "see fix instructions below")
        all_passed = False
        failures.append({
            'step': 1,
            'name': 'Credential check',
            'error': error,
            'fix': (
                "Run: echo ANTHROPIC_API_KEY=sk-ant-... >> "
                "\"G:/History vs Hype/.env\"\n"
                "Or: export ANTHROPIC_API_KEY=sk-ant-..."
            )
        })
        # Cannot proceed without credentials
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

    # Step 3: Translation
    passed, detail, error, translated_sections = step3_translation(sections)

    if passed:
        _print_step(3, total_steps, "Translation", "PASS", detail)
    else:
        _print_step(3, total_steps, "Translation", "FAIL",
                    "see details below")
        all_passed = False
        failures.append({
            'step': 3,
            'name': 'Translation',
            'error': error,
            'fix': (
                "Check your API key is valid.\n"
                "Run: python -c \"from tools.translation.env_loader import load_api_key; "
                "print(load_api_key())\""
            )
        })
        _print_results(all_passed, failures, test_start)
        return 1

    # Step 4: Formatting
    passed, detail, error = step4_formatting(translated_sections)

    if passed:
        _print_step(4, total_steps, "Formatting", "PASS", detail)
    else:
        _print_step(4, total_steps, "Formatting", "FAIL",
                    "see details below")
        all_passed = False
        failures.append({
            'step': 4,
            'name': 'Formatting',
            'error': error,
            'fix': (
                "Check tools/translation/formatter.py format_paired() method."
            )
        })
        _print_results(all_passed, failures, test_start)
        return 1

    # Step 5: Pipeline integrity
    passed, detail, error = step5_pipeline_integrity(sections, translated_sections)

    if passed:
        _print_step(5, total_steps, "Pipeline integrity", "PASS", detail)
    else:
        _print_step(5, total_steps, "Pipeline integrity", "FAIL",
                    "see details below")
        all_passed = False
        failures.append({
            'step': 5,
            'name': 'Pipeline integrity',
            'error': error,
            'fix': (
                "Check that section IDs flow correctly through the pipeline:\n"
                "structure_detector -> translator -> formatter"
            )
        })

    _print_results(all_passed, failures, test_start)
    return 0 if all_passed else 1


def _print_results(all_passed: bool, failures: list, test_start: float) -> None:
    """Print final summary and any failure details."""
    total_elapsed = time.time() - test_start
    total_steps = 5
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
