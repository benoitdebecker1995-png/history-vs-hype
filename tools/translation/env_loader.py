"""
Environment Loader for Translation Pipeline (PIPE-01)

Handles .env file loading and credential resolution without external dependencies.
Parses KEY=value lines, skips comments, strips quotes. Falls back to os.environ.

Usage:
    from env_loader import load_api_key, wrap_api_error

    result = load_api_key()
    if 'error' in result:
        print(result['error'])
        sys.exit(1)
    api_key = result['key']
"""

import os
from pathlib import Path
from typing import Dict, Any

# Project root: two levels up from this file (tools/translation/ -> tools/ -> project root)
_PROJECT_ROOT = Path(__file__).parent.parent.parent


def _parse_env_file(env_path: Path) -> Dict[str, str]:
    """
    Parse a .env file into a dict of key-value pairs.

    - Skips blank lines and lines starting with #
    - Strips surrounding quotes (" or ') from values
    - Handles KEY=value and KEY="value" formats

    Args:
        env_path: Path to the .env file

    Returns:
        Dict of {key: value} pairs
    """
    env_vars = {}

    try:
        content = env_path.read_text(encoding='utf-8')
    except Exception:
        return {}

    for line in content.splitlines():
        line = line.strip()

        # Skip blank lines and comments
        if not line or line.startswith('#'):
            continue

        # Must contain '='
        if '=' not in line:
            continue

        key, _, value = line.partition('=')
        key = key.strip()
        value = value.strip()

        # Strip surrounding quotes
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]

        if key:
            env_vars[key] = value

    return env_vars


def load_api_key() -> Dict[str, Any]:
    """
    Load ANTHROPIC_API_KEY from .env file (project root) or environment variable.

    Resolution order:
    1. .env file at project root (G:/History vs Hype/.env)
    2. os.environ['ANTHROPIC_API_KEY']

    Returns:
        {'key': str} on success
        {'error': str} on failure with step-by-step fix instructions
    """
    env_path = _PROJECT_ROOT / '.env'

    # Try .env file first
    if env_path.exists():
        env_vars = _parse_env_file(env_path)
        key = env_vars.get('ANTHROPIC_API_KEY', '').strip()
        if key:
            return {'key': key}

    # Fall back to environment variable
    key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    if key:
        return {'key': key}

    # Neither source found - return actionable error
    env_file_path = str(env_path).replace('\\', '/')
    error_msg = (
        "Missing ANTHROPIC_API_KEY.\n\n"
        "To fix:\n"
        "1. Get your API key from https://console.anthropic.com/settings/keys\n"
        "2. Add it to .env file:\n"
        f'   echo ANTHROPIC_API_KEY=sk-ant-... >> "{env_file_path}"\n\n'
        "Or set it as environment variable:\n"
        "   export ANTHROPIC_API_KEY=sk-ant-..."
    )
    return {'error': error_msg}


def ensure_env_example() -> None:
    """
    Create .env.example at project root if it does not already exist.

    The template contains a commented placeholder for ANTHROPIC_API_KEY.
    Safe to call on every import — no-ops if the file already exists.
    """
    env_example_path = _PROJECT_ROOT / '.env.example'

    if env_example_path.exists():
        return

    template = (
        "# Anthropic API Key (required for translation pipeline)\n"
        "# Get yours at: https://console.anthropic.com/settings/keys\n"
        "# ANTHROPIC_API_KEY=sk-ant-...\n"
    )

    try:
        env_example_path.write_text(template, encoding='utf-8')
    except Exception:
        # Non-fatal: if we can't write the example, don't crash
        pass


def wrap_api_error(exception: Exception) -> str:
    """
    Convert common Anthropic API exceptions into actionable error messages.

    Handles:
    - anthropic.AuthenticationError
    - anthropic.RateLimitError
    - anthropic.APIConnectionError
    - All others (generic fallback)

    Args:
        exception: The caught exception

    Returns:
        Human-readable error string with remediation steps
    """
    # Get exception class name for duck-typing (avoids importing anthropic here)
    exc_type = type(exception).__name__
    exc_module = getattr(type(exception), '__module__', '')

    # Check for anthropic-specific exceptions by class name
    if 'AuthenticationError' in exc_type or 'Authentication' in exc_type:
        return (
            "Invalid API key. "
            "Check your key at https://console.anthropic.com/settings/keys\n\n"
            "To fix:\n"
            "1. Verify your key starts with 'sk-ant-'\n"
            "2. Update ANTHROPIC_API_KEY in your .env file"
        )

    if 'RateLimitError' in exc_type or 'RateLimit' in exc_type:
        return (
            "Rate limit hit. "
            "Wait 60 seconds and retry, or check your plan at "
            "https://console.anthropic.com/settings/plans\n\n"
            "To fix:\n"
            "1. Wait 60 seconds before retrying\n"
            "2. For higher limits, upgrade your Anthropic plan"
        )

    if ('APIConnectionError' in exc_type or 'ConnectionError' in exc_type
            or 'ConnectTimeout' in exc_type or 'NetworkError' in exc_type
            or 'TimeoutError' in exc_type):
        return (
            "Network error: Could not reach Anthropic API. "
            "Check your internet connection and try again.\n\n"
            "To fix:\n"
            "1. Verify internet connectivity\n"
            "2. Check https://status.anthropic.com for outages\n"
            "3. Retry in 30 seconds"
        )

    # Generic fallback
    return (
        f"API error: {str(exception)}. "
        "If this persists, check https://status.anthropic.com"
    )


# Ensure .env.example exists on first import (non-fatal side effect)
ensure_env_example()
