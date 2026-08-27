# History vs Hype — Claude adapter

Read `AGENTS.md` as the active shared operating contract. It replaces the former command-driven
Claude workflow.

Start with `CHANNEL.md` for channel-level work. Resolve `ACTIVE_PROJECT` and use that project's
`PROJECT.md`, `RESEARCH.md`, and `SCRIPT.md` for current-video work. Keep those two levels separate.

Benoit talks normally. Infer what he wants and operate retrieval, tools, databases, and files
internally. Do not require slash commands, modes, named agents, research stages, percentage gates, or
manual handoffs. Do not load `.claude/` during normal work; it is preserved only as migration history.

Use the smallest relevant packet, surface uncertainty, make a supported recommendation, and ask only
when a missing choice would materially change the outcome or when external/irreversible action needs
approval.
