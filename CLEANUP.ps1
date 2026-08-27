# WITHDRAWN 23 August 2026 — this script must not run.
#
# It was written on 22 August before the August 2026 Codex audit and rebuild had been read.
# Running it would move into the attic:
#
#   tools\                  front_room.py (invoked by name in AGENTS.md and the module the
#                           entire August architecture depends on), pdf_source.py,
#                           preflight\citation_check.py, production\exhibits.py,
#                           youtube_analytics\, discovery\schema_manager.py and
#                           performance_tracker.py (the package_versions store).
#                           Every one of these is KEEP in the design accepted on 13 August.
#
#   _migration-snapshots\   The 824 MB SHA-256-verified pre-migration archive. Git health is
#                           unrepaired (44 unpushed commits, 4 GB pack, 546 MB garbage, the
#                           whole migration uncommitted), so this is the only safe rollback.
#
#   tests\, pyproject.toml  The suite validating all of the above.
#
# Codex's cleanup gate: "After three videos completed through the new workflow."
# Videos shipped through the new workflow so far: zero.
#
# Plan: https://claude.ai/code/artifact/a26e8a56-57ee-49eb-a676-6c11265f090d

Write-Host ""
Write-Host "CLEANUP.ps1 is withdrawn and will not run." -ForegroundColor Yellow
Write-Host "See the comments at the top of this file, or the plan artifact." -ForegroundColor Yellow
Write-Host ""
exit 1
