#!/usr/bin/env python3
import json, os, re, sys
from datetime import date
import anthropic

TODAY = date.today().isoformat()
DROPS_PATH = "drops.json"
INDEX_PATH = "index.html"

BANNED_WORDS = [
    "revolutionary", "game-changing", "disrupt", "unleash",
    "supercharge", "transformative", "game changer", "disrupting",
]

SYSTEM_PROMPT = """You write a daily AI briefing called The Daily Drop.

## Audience

Business professionals in strategy & planning, operations, project management,
and administrative roles at a large enterprise. They are AI-curious but
sometimes apprehensive. Your job is to make them feel MORE CAPABLE, LESS AFRAID,
and slightly more equipped than when they opened the page.

Audience weighting (most → least): Strategy & Planning → Operations → Project Management → Administrative.

## Voice

- Encouraging, plain-spoken, confident. Tone of a smart friend, not a consultant.
- NEVER fear-based. "AI is coming for you" is banned. "AI is shifting what's valuable in your work" is the move.
- Active verbs. "You're shifting from writer to editor" not "Writers are being shifted."
- Sentence-case headlines. No Title Case, no clickbait.
- No hype words: revolutionary, game-changing, disrupt, unleash, supercharge, transformative.
- No empty hedging: might, could potentially, may possibly. Pick a position.

## Trend selection

- The three trends MUST cover different angles — e.g., one strategic shift, one workflow/tooling shift, one skills/cultural shift. Do NOT run three "new AI tool launched" stories.
- Lean into trends that most strongly affect strategy & planning roles.
- Prefer trends from the last 2–4 weeks. Every stat or claim must come from a real, citable source.
- Acceptable sources: Stanford HAI, Microsoft Work Trend Index, Deloitte, PwC, McKinsey, Gartner, Forrester, MIT Sloan, HBR, The Information, The Verge, Axios, Anthropic/OpenAI/Google official blogs, credible Substacks.
- Do NOT source from: LinkedIn influencer posts, vendor marketing pages, AI-generated SEO farms, anything without a clear author and date.

## Role slants

- One sentence each. Don't pad.
- Slants must be genuinely different for each role — if the same line could apply to all four, rework the trend framing.

## Challenges

- 3–6 numbered steps. Each step is 1–2 sentences, concrete, for someone new to AI.
- Wrap exact prompt text in <em>...</em> so members can copy-paste.
- ALWAYS end with a sharing step (share in the group).
- Security-safe: use "your company-approved AI tool" or "any AI assistant." Never instruct pasting proprietary/confidential data.
- Doable in 10–15 minutes.

## Homework

- Personal, not work-related. Examples: planning a trip, cooking, writing a tough message, decoding a bill.
- Must include a prompting technique the reader learns by doing (e.g., "ask me questions first", "give me ranked options", "explain like I'm new").
- Recommend free tools only: ChatGPT, Claude, Gemini, Perplexity.

## Formatting

- Use <em>...</em> sparingly for highlights (1–2 per trend body).
- Cite sources inline: <em>(Source Name, Month Year)</em> or (Source Name, Month Year).
- Do NOT reference the day of the week anywhere (no "Happy Friday", "this Monday")."""


def load_drops():
    if not os.path.exists(DROPS_PATH):
        return {}
    with open(DROPS_PATH, encoding="utf-8-sig") as f:
        return json.load(f)


def save_drops(drops):
    with open(DROPS_PATH, "w", encoding="utf-8") as f:
        json.dump(drops, f, indent=2, ensure_ascii=False)


def recent_titles(drops, n=5):
    keys = sorted(drops.keys(), reverse=True)[:n]
    titles = []
    for k in keys:
        for t in drops[k].get("trends", []):
            titles.append(t.get("title", ""))
    return titles


def validate(entry):
    errors = []
    if not entry.get("intro"):
        errors.append("Missing intro")
    trends = entry.get("trends", [])
    if len(trends) != 3:
        errors.append(f"Expected 3 trends, got {len(trends)}")
    for i, t in enumerate(trends, 1):
        if not t.get("title"):
            errors.append(f"Trend {i}: missing title")
        if not t.get("body"):
            errors.append(f"Trend {i}: missing body")
        slants = t.get("slants", {})
        for role in ("strategy", "operations", "pm", "admin"):
            if not slants.get(role):
                errors.append(f"Trend {i}: missing slant '{role}'")
        ch = t.get("challenge", {})
        steps = ch.get("steps", [])
        if not (3 <= len(steps) <= 6):
            errors.append(f"Trend {i}: {len(steps)} steps (need 3-6)")
        if steps:
            last = steps[-1].lower()
            if "share" not in last and "group" not in last and "colleague" not in last and "team" not in last:
                errors.append(f"Trend {i}: last step doesn't mention sharing")
    hw = entry.get("homework", {})
    if not hw.get("title") or not hw.get("body") or not hw.get("prompt"):
        errors.append("Homework incomplete")
    full_text = json.dumps(entry).lower()
    for word in BANNED_WORDS:
        if word in full_text:
            errors.append(f"Banned word found: '{word}'")
    em_opens = full_text.count("<em>")
    em_closes = full_text.count("</em>")
    if em_opens != em_closes:
        errors.append(f"Unbalanced <em> tags: {em_opens} opens, {em_closes} closes")
    return errors


def generate(drops):
    client = anthropic.Anthropic()
    titles = recent_titles(drops)
    dedup_block = ""
    if titles:
        title_list = "\n".join(f"  - {t}" for t in titles)
        dedup_block = f"""

IMPORTANT — Do NOT repeat these recent topics. Choose genuinely different stories:
{title_list}
"""

    prompt = f"""Today is {TODAY}. Research and write The Daily Drop for this date.

Use web search to find 3 real, diverse AI trends from the past 2-4 weeks.
Each trend needs a different angle — e.g., one strategic shift, one workflow/tooling change, one skills/cultural shift. Do NOT pick three "new AI tool launched" stories.
{dedup_block}
For each trend provide: a sentence-case editorial headline, 1-3 sentence body with one highlighted stat in <em>, four genuinely different role slants (strategy/operations/pm/admin — one sentence each), and a challenge with 3-6 concrete steps ending with a sharing action. Wrap exact prompt text in <em>"..."</em>.

Add a homework section — personal, fun, not work-related. Include a prompting technique the reader learns by doing.

Return ONLY valid JSON, no markdown, no code fences:
{{
  "intro": "One sentence framing the day's themes.",
  "trends": [
    {{
      "title": "Sentence-case editorial headline",
      "body": "1-3 sentences. Highlight one key stat or phrase in <em>...</em>. Cite the source inline.",
      "slants": {{
        "strategy": "One sentence — genuinely specific to strategy/planning roles.",
        "operations": "One sentence — genuinely specific to ops roles.",
        "pm": "One sentence — genuinely specific to project managers.",
        "admin": "One sentence — genuinely specific to admin professionals."
      }},
      "challenge": {{
        "steps": [
          "Concrete step 1.",
          "Step with prompt: <em>\\"Exact prompt text here.\\"</em>",
          "Step reviewing the output.",
          "Share your result in the group."
        ]
      }}
    }}
  ],
  "homework": {{
    "title": "Short personal invitation — not work-related.",
    "body": "1-2 sentences setting up the exercise. Mention free tools (ChatGPT, Claude, Gemini, Perplexity).",
    "prompt": "The actual prompt in quotes. Include a prompting technique the reader learns by doing."
  }}
}}"""

    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]
    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=6000,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if hasattr(b, "text"))
    m = re.search(r'\{[\s\S]*\}', text)
    if not m:
        raise ValueError(f"No JSON found in response: {text[:500]}")
    return json.loads(m.group())


def to_js(d, e):
    lines = [f'"{d}": {{', f'    intro: {json.dumps(e["intro"])},', '    trends: [']
    for i, t in enumerate(e.get("trends", [])):
        c = "," if i < len(e["trends"]) - 1 else ""
        lines += ['      {', f'        title: {json.dumps(t["title"])},',
                  f'        body: {json.dumps(t["body"])},']
        if "slants" in t:
            lines.append('        slants: {')
            sk = list(t["slants"].items())
            for j, (k, v) in enumerate(sk):
                lines.append(f'          {k}: {json.dumps(v)}{"," if j < len(sk)-1 else ""}')
            lines.append('        },')
        if "challenge" in t:
            ch = t["challenge"]
            if isinstance(ch, dict) and "steps" in ch:
                lines += ['        challenge: {', '          steps: [']
                for si, s in enumerate(ch["steps"]):
                    lines.append(f'            {json.dumps(s)}{"," if si < len(ch["steps"])-1 else ""}')
                lines += ['          ]', '        }']
        lines.append(f'      }}{c}')
    lines.append('    ],')
    if "homework" in e:
        hw = e["homework"]
        lines += ['    homework: {',
                  f'      title: {json.dumps(hw.get("title", ""))},',
                  f'      body: {json.dumps(hw.get("body", ""))},',
                  f'      prompt: {json.dumps(hw.get("prompt", ""))}',
                  '    }']
    lines.append('  }')
    return '\n  '.join(lines)


def inject_html(entry):
    with open(INDEX_PATH, encoding="utf-8") as f:
        html = f.read()
    if f'"{TODAY}"' in html:
        print("index.html already up to date.")
        return
    start = html.find("const DROPS = {")
    if start < 0:
        return
    after = start + len("const DROPS = {")
    m = re.search(r'"(\d{4}-\d{2}-\d{2})":', html[after:])
    if not m:
        return
    pos = after + m.start()
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html[:pos] + to_js(TODAY, entry) + ",\n  " + html[pos:])
    print("index.html updated.")


def main():
    drops = load_drops()
    with open(INDEX_PATH, encoding="utf-8") as f:
        html = f.read()

    if TODAY in drops and f'"{TODAY}"' in html:
        print(f"{TODAY} already published.")
        sys.exit(0)

    if TODAY not in drops:
        print(f"Generating {TODAY}...")
        entry = generate(drops)

        errors = validate(entry)
        if errors:
            print("Validation errors:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)

        drops[TODAY] = entry
        save_drops(drops)
        print("Validation passed.")
    else:
        entry = drops[TODAY]

    inject_html(entry)
    print("Done.")


if __name__ == "__main__":
    main()
