"""
Ollama title brainstorming — generates raw candidates for title_scorer.py to filter.
Uses local gemma3:4b. Zero Pro quota cost.

Usage:
    python tools/ollama_brainstorm.py "falklands malvinas dispute" --topic territorial
    python tools/ollama_brainstorm.py "viking myths" --topic ideological --count 15
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"

SYSTEM_PROMPT = """You are a YouTube title writer for a history channel called History vs Hype.
The channel debunks historical myths and exposes overlooked mechanisms in colonial, geopolitical, and ideological history.

CRITICAL FORMATTING RULE: NEVER USE A COLON. Not ever. Use a period between sentences instead.

GOOD examples (copy this structure):
- "Argentina and Britain Both Claim the Falklands. Neither Can Prove It Legally."
- "France Charged Haiti for Its Own Freedom. Haiti Paid for 122 Years."
- "Two Countries Signed the Same Treaty. They Each Read It Differently."
- "Britain Expelled Argentina from the Falklands. The Legal Basis Does Not Exist."

BAD examples (never do this):
- "Falklands Dispute: The Real Story" — COLON, banned
- "Malvinas Claim: What You Were Not Told" — COLON, banned
- "The Truth About the Falklands" — vague, no mechanism

Additional rules:
1. No years in the title
2. Two short declarative sentences separated by a period (not a colon)
3. Include a mechanism word (partition, expulsion, forgery, extension, claim, loophole)
4. Front-load the main search keyword
5. Be specific — name the parties or the mechanism. No vague words.
6. Under 70 characters total

Output one title per line. No numbering. No explanation. No preamble."""


def clean_colon(title: str) -> str:
    """Replace 'Word Word: Rest' pattern with 'Word Word. Rest' — Gemma training bias fix."""
    if ":" in title:
        title = title.replace(": ", ". ", 1)
    return title


def brainstorm(topic: str, count: int = 10) -> list[str]:
    prompt = f"{SYSTEM_PROMPT}\n\nTopic: {topic}\nGenerate {count} title candidates."

    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.8, "top_p": 0.9}
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            raw = result.get("response", "").strip()
            lines = [clean_colon(l.strip()) for l in raw.splitlines() if l.strip()]
            return lines
    except urllib.error.URLError:
        print("ERROR: Ollama not running. Start it with: ollama serve", file=sys.stderr)
        return []
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description="Brainstorm YouTube titles using local Ollama")
    parser.add_argument("topic", help="Video topic")
    parser.add_argument("--topic-type", "--topic", default="general",
                        choices=["territorial", "ideological", "colonial", "general"],
                        help="Topic type (for title_scorer.py passthrough)")
    parser.add_argument("--count", type=int, default=10, help="Number of candidates")
    parser.add_argument("--score", action="store_true",
                        help="Pipe output directly through title_scorer.py")
    args = parser.parse_args()

    candidates = brainstorm(args.topic, args.count)

    if not candidates:
        sys.exit(1)

    if args.score:
        # Pass through title_scorer
        import subprocess
        cmd = ["python", "tools/title_scorer.py"] + candidates + ["--topic", args.topic_type]
        subprocess.run(cmd)
    else:
        print(f"# Ollama brainstorm — {args.topic}")
        print(f"# Model: {MODEL} | Count: {len(candidates)}\n")
        for t in candidates:
            print(t)
        print(f"\n# Run with --score to pipe through title_scorer.py")


if __name__ == "__main__":
    main()
