#!/bin/sh
# Install repo-tracked git hooks into .git/hooks/ (which is NOT version-controlled).
# Run once after clone:  sh tools/hooks/install.sh
# Idempotent — re-run any time to refresh.
set -e
ROOT=$(git rev-parse --show-toplevel)
cp "$ROOT/tools/hooks/pre-commit" "$ROOT/.git/hooks/pre-commit"
chmod +x "$ROOT/.git/hooks/pre-commit" 2>/dev/null || true
echo "Installed: .git/hooks/pre-commit (secret-guard)"
