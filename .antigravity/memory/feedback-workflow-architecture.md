---
name: Workflow Architecture Preferences
description: Core architectural preferences for how the workflow should operate — agent-heavy, conversational, token-lean. Drives all /gsd work and command/agent design decisions.
type: feedback
originSessionId: 665caf6c-b014-4ddf-b05b-7e66f62087fa
---
**Rule:** Prefer MORE agent delegation + LESS main-context verbosity + conversational orchestrator flow + explicit token-saving measures. Keep only what earns its keep; improve what needs improving; end goal is always better videos.

**Why:** User hit rate limits repeatedly, felt workflow was not streamlined, had to doubletake often, and felt commands ran like scripts instead of dialogues. User explicitly stated preference for "more agents and conversational flow with clear token saving measures" (2026-04-21). Agent sub-contexts don't return to main — only summaries do — which is the cheapest way to handle heavy reference loads.

**How to apply:**
- **Main context = orchestrator only.** Keep responses tight, delegate heavy reads/reasoning to agents.
- **Default to spawning agents** for anything that requires loading multiple reference files, reading many source files, or long reasoning chains. Do NOT read 5 files in main context when a sub-agent can do it and return a 200-word summary.
- **Conversational flow:** commands should check in with user at natural decision points (not silent autopilot). Mid-flow AskUserQuestion is better than wrong end-state.
- **Cut surface area:** when building/editing commands, agents, refs — delete what's redundant, keep what's actively used. Overlap is waste.
- **Explicit token measures:** state token-saving choices out loud ("spawning agent so main context stays lean", "skipping parallel scan — one agent can do both"). Never vague.
- **Output bar = better videos.** Every workflow change must answer "does this improve retention/CTR/scripting quality?" If unclear — cut it.
- **Improve before replace.** When something partially works, iterate; don't demolish.
