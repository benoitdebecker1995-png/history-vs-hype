# Migration Guide: Moving History vs Hype to New PC

## Quick 3-Step Migration

### Step 1: On OLD PC (Current)
Everything is already committed and ready to transfer!

```bash
# Check everything is saved
git status
```

### Step 2: Transfer to NEW PC

**Option A: Using Git Remote (Recommended)**
```bash
# On old PC - push to GitHub/GitLab
git remote add origin YOUR_REPO_URL
git push -u origin master

# On new PC - clone
git clone YOUR_REPO_URL "C:\Users\YOUR_NEW_USERNAME\Documents\History vs Hype"
```

**Option B: Manual Transfer**
1. Copy entire folder: `C:\Users\benoi\Documents\History vs Hype`
2. Transfer via USB drive, network share, or cloud storage
3. Paste to: `C:\Users\YOUR_NEW_USERNAME\Documents\History vs Hype`

### Step 3: Configure NEW PC

**A. Update Claude Code Settings**

Edit `.claude\settings.local.json`:
- Find & Replace: `C:\\Users\\benoi\\` → `C:\\Users\\YOUR_NEW_USERNAME\\`
- Save the file

**B. Install Git**
```bash
# Download from git-scm.com
# Configure:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**C. Test Claude Code**
```bash
cd "C:\Users\YOUR_NEW_USERNAME\Documents\History vs Hype"

# Test a slash command
/notebooklm-prompts

# Check agents load
# Browse .claude/agents/ folder
```

## What's Included

✅ All video projects (1-13)
✅ All scripts and research
✅ Claude agents and commands
✅ Documentation and guides
✅ YouTube metadata and editing guides
✅ Fact-checking protocols

## What's NOT Included (Intentionally)

❌ Library PDFs (left on old PC for now)
❌ PDF organizer scripts (not needed)
❌ Video files (.mp4, .mov - too large for git)
❌ DaVinci Resolve projects (.drp files)
❌ Cache and temp files

## Quick Reference

**Claude Code Setup:**
- Agents: `.claude/agents/`
- Commands: `.claude/commands/`
- Settings: `.claude/settings.local.json`

**Video Projects:**
- Active work: `video-projects/_IN_PRODUCTION/`
- Ready to film: `video-projects/_READY_TO_FILM/`
- Completed: `video-projects/_ARCHIVED/`

**Documentation:**
- Main guide: `CLAUDE.md`
- Workflow: `guides/MASTER_WORKFLOW.md`
- Fact-checking: `guides/fact-checking-protocol.md`

## Troubleshooting

**If slash commands don't work:**
- Check `.claude/commands/` folder exists
- Verify you're in the correct directory

**If paths are broken:**
- Update `.claude/settings.local.json` with new username
- Use Find & Replace for all path references

**If git complains:**
- Run `git config` commands from Step 3B
- Check you're in the repository folder

## That's It!

Your entire YouTube production system is now portable. Just transfer, update the username in settings, and you're ready to continue work on the new PC.

---
Created: 2025-11-28
Last updated: Migration prep commit 6f7dd00
