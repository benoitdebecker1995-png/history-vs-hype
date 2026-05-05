"""CheckerRegistry — programmatic interface for script quality checkers.

Provides a unified registry that replaces the direct checker imports in cli.py.
Each checker is adapted to the Checker protocol via _BaseCheckerAdapter.

Usage:
    from tools.script_checkers.registry import build_default_registry

    registry = build_default_registry()
    result = registry.run("stumble", script_text)
    print(registry.list_all())  # ['flow', 'pacing', 'repetition', 'scaffolding', 'stumble']
"""

from typing import Dict, Any, List, runtime_checkable, Protocol


@runtime_checkable
class Checker(Protocol):
    """Protocol that all registered checkers must implement."""

    @property
    def name(self) -> str:
        """Unique lowercase identifier used as CLI flag and registry key."""
        ...

    @property
    def description(self) -> str:
        """One-line description of what this checker detects."""
        ...

    def run(self, text: str) -> Dict[str, Any]:
        """Run the checker against script text.

        Args:
            text: Script text to analyze.

        Returns:
            Dict with at minimum: {'issues': list, 'stats': dict}
        """
        ...


class _BaseCheckerAdapter:
    """Adapts existing BaseChecker subclasses to the Checker protocol.

    Bridges the BaseChecker.check() interface to Checker.run() without
    modifying the underlying checker implementations.
    """

    def __init__(self, checker, description: str) -> None:
        self._checker = checker
        self._description = description

    @property
    def name(self) -> str:
        checker_name = self._checker.name
        return checker_name.lower() if isinstance(checker_name, str) else checker_name

    @property
    def description(self) -> str:
        return self._description

    def run(self, text: str) -> Dict[str, Any]:
        return self._checker.check(text)


class CheckerRegistry:
    """Registry that manages and dispatches to script quality checkers.

    Checkers are registered by name and can be invoked individually via run()
    or discovered via list_all().
    """

    def __init__(self) -> None:
        self._checkers: Dict[str, Checker] = {}

    def register(self, checker: Checker) -> None:
        """Register a checker.

        Args:
            checker: An object implementing the Checker protocol.
        """
        self._checkers[checker.name] = checker

    def get(self, name: str) -> Checker:
        """Retrieve a checker by name.

        Args:
            name: The checker's name (lowercase, e.g. 'stumble').

        Returns:
            The registered Checker.

        Raises:
            KeyError: If no checker is registered under that name.
        """
        return self._checkers[name]

    def list_all(self) -> List[str]:
        """Return sorted list of all registered checker names."""
        return sorted(self._checkers.keys())

    def run(self, name: str, script_text: str) -> Dict[str, Any]:
        """Run a named checker against script text.

        Args:
            name: Checker name (e.g. 'stumble', 'flow').
            script_text: Raw script text to analyze.

        Returns:
            Checker result dict (shape: {'issues': list, 'stats': dict}).

        Raises:
            KeyError: If no checker is registered under that name.
        """
        return self._checkers[name].run(script_text)


def build_default_registry() -> CheckerRegistry:
    """Build a CheckerRegistry populated with all available checkers.

    Imports and registers adapters for each checker. Lazy imports avoid
    spaCy/textstat dependency failures at module load time.

    Returns:
        CheckerRegistry with flow, pacing, repetition, scaffolding, stumble registered.
    """
    from .config import Config
    from .checkers.flow import FlowChecker
    from .checkers.pacing import PacingChecker
    from .checkers.repetition import RepetitionChecker
    from .checkers.scaffolding import ScaffoldingChecker
    from .checkers.stumble import StumbleChecker

    config = Config()
    registry = CheckerRegistry()

    registry.register(_BaseCheckerAdapter(
        FlowChecker(config),
        "Analyze script flow: undefined terms used before definition, missing transitions."
    ))
    registry.register(_BaseCheckerAdapter(
        PacingChecker(config),
        "Analyze pacing: sentence variance, readability, entity density by section."
    ))
    registry.register(_BaseCheckerAdapter(
        RepetitionChecker(config),
        "Detect repeated phrases (3+) while distinguishing rhetorical from redundant."
    ))
    registry.register(_BaseCheckerAdapter(
        ScaffoldingChecker(config),
        "Count scaffolding phrases (here's, let me, so,) against proportion threshold."
    ))
    registry.register(_BaseCheckerAdapter(
        StumbleChecker(config),
        "Detect teleprompter stumble risks: long sentences, nested subordinate clauses."
    ))

    return registry
