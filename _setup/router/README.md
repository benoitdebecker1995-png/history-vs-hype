# Router setup — two lanes

Written 23 August 2026.

The point of this is **not** to replace the assistant you already pay for. It is to give you a second,
cheap lane for bulk mechanical work, without touching the first one.

| Lane | Command | Runs on | Use it for |
|---|---|---|---|
| **Main** | `claude` | Your Claude subscription | Script voice, historiography, claim checking, packaging, next-video judgment — everything where being wrong costs a video |
| **Bulk** | `ccr code` | OpenRouter, pay-per-token | Comment classification, transcript cleanup, subtitle passes, bulk tagging — anything where volume matters and quality does not |

They do not interfere. Installing the router does not change what `claude` does.

## Why the split

If you route everything through OpenRouter you stop using the subscription you are already paying for
and start paying per token on top of it, at API rates — which for heavy agentic work is usually more
expensive, not less. And OpenRouter's own documentation says plainly that *"Claude Code is optimized
for Anthropic models and may not work correctly with other providers."* So the cheap lane is for jobs
where a wrong answer is cheap.

The first real job for the bulk lane is the one thing this channel has never done: reading its own
comments. There are 381 on the Belize video alone, and roughly 33,000 were pulled in an earlier
comment sweep. Classifying those is exactly the shape of work a cheap model should do.

## Setup, in order

**1. Make sure the main lane works first.** Claude Code is already on your machine from 13 August.

```powershell
& "$env:USERPROFILE\.local\bin\claude.exe" --version
cd "G:\History vs Hype"
& "$env:USERPROFILE\.local\bin\claude.exe"
```

Sign in with your existing account. If that works, you may not need the rest of this at all — decide
after you've used it.

**2. Get an OpenRouter key.** openrouter.ai/settings/keys. Add a small amount of credit; you are
buying tokens, not a subscription.

**3. Set the key yourself.** I have deliberately not put it anywhere — no file here contains it, and
`config.json` reads it from the environment.

```powershell
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY","<your-key>","User")
```

Then open a new terminal so it takes effect.

**4. Install the router.**

```powershell
powershell -ExecutionPolicy Bypass -File "G:\History vs Hype\_setup\router\install.ps1"
```

This installs `@musistudio/claude-code-router` from npm — third-party software, not Anthropic's — and
copies `config.json` to `%USERPROFILE%\.claude-code-router\config.json`, backing up anything already
there. You have that directory already, so something has been set up before; the backup is why.

**5. Run it.**

```powershell
ccr start
ccr code
```

`ccr start` runs a local service on `127.0.0.1:3456`. `ccr code` opens Claude Code pointed at it.

## Choosing models

`config.json` currently points every route at `openai/gpt-oss-120b:free`, which is the example in the
current documentation. It is a safe first test because it costs nothing — use it to confirm the
plumbing works end to end, then change it.

I have deliberately not filled in a list of specific paid model IDs and prices. They change often
enough that anything I wrote today would be stale and would fail with a confusing error. Pick from
openrouter.ai/models against these criteria instead:

- **background** — the cheapest thing that can follow instructions. This is where the volume goes.
- **default** — mid-tier. Only matters if you use the bulk lane for anything with judgment in it.
- **think / longContext** — leave these pointed at whatever you set as default. If you find yourself
  wanting a strong model here, that is the signal to do the job in the main lane instead.

`longContextThreshold` is 60,000 tokens. Requests above it take the `longContext` route.

## Cost discipline

You have a €2,000/month target against €0 revenue, and you have said you do not want to spend before
knowing. So:

- Load a small amount of credit, not a large one. OpenRouter will simply stop rather than bill you.
- Check spend after the first real bulk job. If comment classification costs more than a euro or two,
  something is routed wrong — probably a frontier model on `background`.
- If the bulk lane sits unused for a month, you did not need it. Delete the config and stop.

## What this does not fix

The router is a cost and access tool. It is not the reason the channel is where it is, and setting it
up is not progress on the channel. Volhynia is recorded and in the edit; that is the work.
