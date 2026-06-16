# Daily Drop — Routine Spec

> **Purpose:** A runbook for the Claude Code Remote Routine that generates, validates, and publishes each day's Daily Drop entry to the AI Operations Accelerator archive site. The routine fires daily, clones this repo, runs the workflow below, and opens a PR for human review.

---

## 1. Mission

The Daily Drop is a short editorial briefing for professionals in **traditional operations, strategy & planning, project management, and administrative roles** who are AI-curious but cautious. The community goal is to **remove the fear of AI** and help members use AI to advance — not be replaced by it.

Every drop must leave the reader feeling **more capable, less afraid, and slightly more equipped** than when they opened the page.

**Audience weighting (most → least):** Strategy & Planning → Operations → Project Management → Administrative.

---

## 2. Daily Workflow

The routine runs once per day on Anthropic's cloud (no local machine required). On each run:

1. **Fresh clone** of the default branch happens automatically.
2. **Idempotency check** (see §8) — if today's drop already exists or is already in an open PR, exit cleanly without creating duplicates.
3. **Research** today's three trends using web search (see §5 for sources).
4. **Draft** the day's entry following the structure in §3 and the voice rules in §4.
5. **Insert** the new entry into `index.html` per §6.
6. **Validate** the file per §7.
7. **Commit** on a new branch: `claude/daily-drop-YYYY-MM-DD`
8. **Open a Pull Request** following the format in §9.
9. **Exit.** A human reviews and merges the PR. Netlify/Vercel auto-deploys on merge.

The routine never pushes directly to `main`. Every drop is human-reviewed before going live.

---

## 3. Content Format

Each daily entry is a JavaScript object keyed by ISO date (`"YYYY-MM-DD"`) inside the `DROPS` object in `index.html`. Its shape:

```javascript
"2026-06-15": {
  intro: "One-sentence framing for the day.",
  trends: [
    {
      title: "Trend headline — short and editorial",
      body: "1–3 sentences. Use <em>...</em> to highlight a key phrase or statistic.",
      slants: {
        strategy:   "One line — how this lands for a strategy/planning person.",
        operations: "One line — how this lands for an ops person.",
        pm:         "One line — how this lands for a project manager.",
        admin:      "One line — how this lands for an administrative pro."
      },
      challenge: "A short, security-safe action a community member can try and share back."
    },
    // … exactly 3 trend objects total
  ],
  homework: {
    title: "Italic, one-line invitation for the personal try-at-home moment.",
    body: "1–2 sentences. The body sets up the prompt.",
    prompt: "The actual prompt or instruction in quotes, formatted to feel personal and low-stakes."
  }
}
```

**Hard requirements:**
- Exactly **3 trends** per day.
- Every trend must have all **4 role slants** (`strategy`, `operations`, `pm`, `admin`).
- Every trend must have **one challenge**.
- Every drop must have **one homework block**.

---

## 4. Editorial Guidelines

### Voice
- **Encouraging, plain-spoken, confident.** Tone of a smart friend, not a consultant.
- **Never fear-based.** "AI is coming for you" is banned. "AI is shifting what's valuable in your work" is the move.
- **Active verbs.** "You're shifting from writer to editor" not "Writers are being shifted."
- **No hype words.** Avoid *revolutionary, game-changing, disrupt, unleash, supercharge, transformative*.
- **No empty hedging.** Avoid *might, could potentially, may possibly*. Pick a position.
- **Sentence-case headlines.** No Title Case headlines, no clickbait.

### Trend selection
- The three trends should **cover different angles** — e.g., one strategic shift, one workflow/tooling shift, one skills/cultural shift. Don't run three "new AI tool launched" trends in one day.
- Lean into trends that **most strongly affect strategy & planning roles** (the primary audience), then ops, then PM, then admin.
- Prefer trends from the **last 2–4 weeks**. Avoid recycling stories the community has likely seen.
- **Every stat or claim must come from a real, citable source.** If you can't link it, don't quote it. Never fabricate numbers.

### Role slants
- **One sentence each.** Don't pad.
- Slants should be **genuinely different** for each role — if the same line could apply to all four, the trend's framing is too generic and needs reworking.
- If a trend honestly does not have a meaningful angle for one of the roles, write the most truthful version possible — don't manufacture relevance.

### Challenges
- **Must be security-safe.** Default assumption: the community member works at a company with AI guardrails. Never instruct them to paste proprietary documents, customer data, or internal information into a public AI tool.
- Safe framings: "using your company-approved AI tool," "with a fictional or sanitized version," "with a document you wrote that doesn't contain confidential info."
- **Doable in 10–15 minutes.** No multi-day projects.
- **Shareable.** Should produce something the member can post in the community group.

### Homework (personal prompt)
- This is the **try-at-home, no-work-risk** moment of each drop. Critical for AI-anxious members.
- Always use a **personal-life scenario** (not a work scenario). Examples: planning a trip, writing a tough personal message, cooking with what's on hand, decoding a bill, prepping for a hard conversation.
- The prompt should include a **prompting technique** the member learns by doing — e.g., "ask me 3 questions before you answer," "give me 3 options ranked by [criterion]," "explain like I'm new to this."
- Recommend free tools only: **ChatGPT, Claude, Gemini, Perplexity** (web versions).

---

## 5. Source Guidance

Acceptable primary sources for trends:
- Stanford HAI AI Index
- Microsoft Work Trend Index
- Deloitte / PwC / McKinsey / Gartner / Forrester research reports
- MIT Sloan Management Review
- Harvard Business Review (AI/operations coverage)
- The Information, The Verge, Axios (for product/news trends)
- Anthropic, OpenAI, Google DeepMind, Microsoft official blog posts (for capability shifts)
- Substack / Medium pieces from credible operators (e.g., Lenny's Newsletter, Every, Stratechery) — only when the underlying analysis is sound

**Do not source from:**
- LinkedIn influencer posts as primary sources (link through to what they're citing)
- Vendor marketing pages
- AI-generated SEO content farms
- Anything without a clear author and date

When in doubt: **fewer, stronger sources > more, weaker ones.** One trend with a solid citation beats three with vague references.

**Capture every source URL** — they go in the PR description (§9).

---

## 6. Insertion Instructions

### Where to insert
Open `index.html`. Find the `DROPS` object inside the `<script>` block. It looks like this:

```javascript
const DROPS = {
  "2026-06-14": {
    // … existing entry
  }

  /* ── Add new entries above this line. Example template: */
};
```

**Insert the new entry ABOVE the most recent existing entry** (so newest is always first in the file).

### Format rules
- Use `"YYYY-MM-DD"` as the key, in quotes.
- **Add a comma** after the new entry's closing brace if another entry follows it.
- **Remove or add commas as needed** so the object literal stays valid JavaScript.
- Inside string values, use `\"` to escape double quotes.
- HTML emphasis: use `<em>...</em>` for highlights — sparingly (1–2 per trend body, optional in slants/challenges).
- **Line breaks inside a string:** use `<br><br>` for paragraph breaks (used in the homework `prompt` field when needed).

### Example of a properly formatted insertion

```javascript
const DROPS = {
  "2026-06-15": {
    intro: "Three things worth thinking about today — and one for you to try at home.",
    trends: [
      {
        title: "Example trend title",
        body: "Example body with <em>a highlighted phrase</em> for emphasis.",
        slants: {
          strategy:   "Strategy slant line.",
          operations: "Operations slant line.",
          pm:         "PM slant line.",
          admin:      "Admin slant line."
        },
        challenge: "A safe, shareable action prompt."
      },
      { /* trend 2 */ },
      { /* trend 3 */ }
    ],
    homework: {
      title: "Personal prompt title in italic voice.",
      body: "Setup sentence for the personal prompt.",
      prompt: "\"The actual prompt text in quotes.\"<br><br>One follow-up sentence about why this technique works."
    }
  },

  "2026-06-14": {
    // … existing entry below
  }
};
```

Note the trailing comma after `"2026-06-15"`'s closing brace.

---

## 6a. Site Design System

The site's visual identity matches the **AI Operations Accelerator** landing page (`why-join-aoa.netlify.app`). The routine **only touches the `DROPS` data object** — never modify the HTML structure, CSS, or JavaScript rendering logic below. This section is a reference so you understand the context your content renders into.

### Color palette (CSS custom properties)

```css
:root {
  --navy:    #0D2340;
  --blue:    #00BCEB;
  --gold:    #FBAB18;
  --magenta: #E20074;
  --white:   #FFFFFF;
  --light:   #F0F6FA;
  --muted:   #6B7A8D;
  --text:    #0D2340;
}
```

Derived aliases used throughout the page:

| Alias | Maps to | Used for |
|---|---|---|
| `--paper` | `var(--light)` | Page background |
| `--paper-soft` | `#E2ECF4` | Card/challenge backgrounds |
| `--ink` | `var(--navy)` | Primary text |
| `--ink-soft` | `var(--muted)` | Secondary text |
| `--ink-faint` | `#94A3B4` | Tertiary text, labels |
| `--accent` | `var(--blue)` | Links, highlights, chevrons |
| `--accent-soft` | `#D6F3FC` | `<em>` highlight background |
| `--tag-bg` | `#DDE6EE` | Role slant badges |
| `--rule` | `#D0DAE4` | Borders, dividers |

### Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,300&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
```

| Usage | Font family |
|---|---|
| Body text, labels, UI | `'DM Sans', sans-serif` |
| Headings, date display, hero title, trend titles, homework title | `'DM Serif Display', serif` |

### Hero section

The page opens with an AOA-branded hero matching the landing page:

```css
/* ── HERO ── */
.hero{background:var(--navy);color:var(--white);padding:56px 64px 48px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-120px;right:-80px;width:480px;height:480px;background:radial-gradient(circle,rgba(0,188,235,0.14) 0%,transparent 70%);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:-60px;left:30%;width:300px;height:300px;background:radial-gradient(circle,rgba(251,171,24,0.07) 0%,transparent 70%);pointer-events:none}
.hero-top{display:flex;align-items:flex-start;justify-content:space-between;gap:32px;position:relative;z-index:1}
.hero-left{flex:1}
.hero-eyebrow{font-size:10px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--blue);margin-bottom:16px}
.hero-title{font-family:'DM Serif Display',serif;font-size:52px;line-height:1.08;margin-bottom:12px}
.hero-title em{font-style:italic;color:var(--blue)}
.hero-tagline{font-size:18px;font-weight:400;color:var(--white);margin-bottom:10px;font-style:italic;font-family:'DM Serif Display',serif}
.hero-sub{font-size:13.5px;font-weight:300;color:rgba(255,255,255,0.55);max-width:520px;line-height:1.75;margin-bottom:0}
.hero-badge{background:rgba(0,188,235,0.12);border:1px solid rgba(0,188,235,0.25);border-radius:8px;padding:20px 24px;flex-shrink:0;text-align:center;min-width:180px}
.hero-badge-date{font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px}
.hero-badge-event{font-family:'DM Serif Display',serif;font-size:22px;color:var(--white);line-height:1.2;margin-bottom:4px}
.hero-badge-sub{font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase}
```

Hero HTML structure:

```html
<section class="hero">
  <div class="hero-top">
    <div class="hero-left">
      <div class="hero-eyebrow">AI Ops Accelerator · Daily Drop</div>
      <h1 class="hero-title">Daily<br><em>Drop</em></h1>
      <p class="hero-tagline">Come curious. Leave with something you can use on Monday.</p>
      <p class="hero-sub">A short daily briefing for operators, strategists, project managers, and admins navigating AI — built by the AI Operations Accelerator community.</p>
    </div>
    <div class="hero-badge" id="hero-badge">
      <div class="hero-badge-date" id="hero-badge-date"><!-- weekday, set by JS --></div>
      <div class="hero-badge-event" id="hero-badge-event"><!-- month + day, set by JS --></div>
      <div class="hero-badge-sub">Daily briefing</div>
    </div>
  </div>
</section>
```

### Navigation bar

Below the hero, a centered nav bar provides **Prev / Calendar / Today / Next** controls:

```html
<nav class="nav-bar">
  <button class="nav-btn" id="prev-btn" aria-label="Previous drop">‹ Prev</button>
  <!-- calendar picker here -->
  <button class="today-btn" id="today-btn">Today</button>
  <button class="nav-btn" id="next-btn" aria-label="Next drop">Next ›</button>
</nav>
```

Prev/Next buttons auto-disable when there is no adjacent drop. The calendar popover lets users jump to any date with a published drop.

### Collapsible sections

Trends and the homework block render inside `<details>` elements — **collapsed by default** (no `open` attribute). Each section header has a **CSS-drawn chevron** in the accent color (`var(--accent)` / `--blue`) that rotates on expand:

```css
.trend summary::after {
  content: "";
  position: absolute;
  top: 8px;
  right: 4px;
  width: 10px;
  height: 10px;
  border-right: 2.5px solid var(--accent);
  border-bottom: 2.5px solid var(--accent);
  transform: rotate(45deg);           /* points down when collapsed */
  transition: transform 0.25s ease;
}
.trend[open] summary::after {
  transform: rotate(-135deg);          /* points up when expanded */
}
```

The homework section uses the same chevron pattern. The `renderTrend()` and `renderDrop()` functions in `index.html` emit `<details class="trend">` (no `open`) and `<details class="homework">` (no `open`).

### Section styles (AOA pattern)

For reference, the AOA landing page uses these section classes (not currently used in the Daily Drop but available if the layout expands):

```css
.section{padding:48px 64px}
.section-white{background:var(--white)}
.section-light{background:var(--light)}
.section-navy{background:var(--navy);color:var(--white)}
.section-label{font-size:10px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--blue);margin-bottom:10px}
.section-label-light{color:rgba(255,255,255,0.45)}
.section-title{font-family:'DM Serif Display',serif;font-size:32px;line-height:1.15;margin-bottom:6px}
.section-title-white{color:var(--white)}
.section-body{font-size:13.5px;font-weight:300;color:var(--muted);line-height:1.8}
```

---

## 7. Pre-commit Checklist

Before committing, verify:

- [ ] The JSON-like object structure is valid JavaScript (no missing commas, no unescaped quotes, no trailing commas before `}`).
- [ ] Date key is `"YYYY-MM-DD"` and matches today's date in **Eastern Time** (the community's home timezone).
- [ ] Exactly 3 trends.
- [ ] Every trend has all 4 role slants and 1 challenge.
- [ ] Every stat or claim has a real source you could link to (and the URL is captured for the PR body).
- [ ] No banned hype words (see §4).
- [ ] Challenges are security-safe (no proprietary data instructions).
- [ ] Homework prompt is personal, not work-related.
- [ ] HTML `<em>` tags are properly opened and closed.

If any check fails, **fix before committing.** A broken JS object will break the whole site, not just the new entry.

---

## 8. Idempotency Rules

The routine may occasionally run more than once for the same date (catch-up runs, manual re-fires, etc.). To prevent duplicates:

1. **Before drafting**, check `index.html` for today's date key (`"YYYY-MM-DD"`). If it already exists in `DROPS`, **exit cleanly** with the message: *"Today's drop already published — no action taken."* Do not commit, do not open a PR.
2. **Before opening a PR**, check open PRs for any with `Daily Drop: [today's date]` in the title. If one exists, **exit cleanly** — do not open a second.
3. If the routine is partway through a run and the network drops, it should be safe to restart from step 1; any prior partial work would have been on a separate branch that can be discarded.

---

## 9. Branch and Pull Request Conventions

### Branch name
`claude/daily-drop-YYYY-MM-DD`

Example: `claude/daily-drop-2026-06-15`

### Commit message
`Add drop: YYYY-MM-DD`

### Pull Request title
`Daily Drop: [Weekday], [Month] [Day]`

Example: `Daily Drop: Sunday, June 15`

### Pull Request body — use this template

```markdown
## Today's Drop · [Weekday], [Month Day], [Year]

**Intro:** [the intro line]

### Trends
1. **[Trend 1 title]**
2. **[Trend 2 title]**
3. **[Trend 3 title]**

### Homework
*[Homework title]*

---

### Sources cited
- [URL 1] — [what it supports]
- [URL 2] — [what it supports]
- [URL 3] — [what it supports]

### Pre-commit checklist
- [x] Valid JS object structure
- [x] Date matches today (ET)
- [x] 3 trends, 4 role slants each, 1 challenge each
- [x] Every claim sourced
- [x] No banned hype words
- [x] Security-safe challenges
- [x] Personal homework prompt
- [x] HTML tags balanced

Merge to publish. Netlify/Vercel will auto-deploy.
```

---

## 10. Full Worked Example

This is the seed entry already in the file. Use it as a reference for tone, length, and structure.

```javascript
"2026-06-14": {
  intro: "Three things worth thinking about today — and one for you to try at home.",
  trends: [
    {
      title: "The strategic memo is being rebuilt — fast",
      body: "Microsoft's 2026 Work Trend Index just landed. <em>49% of Copilot conversations now support cognitive work</em> — analysis, problem-solving, strategic thinking — and 58% of AI users say they're producing work they couldn't have done a year ago. The work isn't disappearing. It's being promoted.",
      slants: {
        strategy:   "You're shifting from <em>writer</em> to <em>editor + pressure-tester</em>.",
        operations: "Synthesis across systems is now a 30-min job, not a 3-day one.",
        pm:         "Status reports get auto-drafted; framing the right questions is the new value-add.",
        admin:      "Your judgment on tone, context, and 'what the exec actually meant' becomes the premium skill."
      },
      challenge: "Find one document you wrote last quarter. Using your company-approved AI tool, ask: <em>\"Argue against this from the perspective of a skeptical executive.\"</em> Share what surprised you in the group."
    },
    {
      title: "The Transformation Paradox",
      body: "Deloitte's 2026 enterprise report puts it plainly: <em>companies are layering AI onto legacy processes instead of redesigning work holistically</em>. The investment isn't compounding because the workflow underneath is still pre-AI.",
      slants: {
        strategy:   "The QBR was built for a pre-AI world. Rethink the inputs and outputs.",
        operations: "Your SOPs probably encode 2019 assumptions.",
        pm:         "\"Weekly check-ins\" exist because info moved slowly. Does it still?",
        admin:      "Calendar-and-email triage workflows are ripe for a clean-slate redesign."
      },
      challenge: "Pick ONE recurring meeting or process you own. In one sentence: if AI were a teammate from minute one, what changes? Drop your answer in the group."
    },
    {
      title: "AI fluency is the new literacy",
      body: "Stanford HAI's 2026 AI Index: AI-related skills now appear in <em>2.5% of all U.S. job postings — a 297% increase over a decade</em>. This isn't \"learn to code.\" It's <em>learn to direct, evaluate, and trust-but-verify</em> AI output.",
      slants: {
        strategy:   "Prompting is problem-framing. The clearer your ask, the sharper your strategy.",
        operations: "Knowing when AI is wrong saves more time than AI being right.",
        pm:         "Agent orchestration is the next PM specialty.",
        admin:      "You already know how things actually work here. AI doesn't."
      },
      challenge: "Write down your top 3 weekly recurring tasks. Next to each, mark: <em>AI could draft this / AI could review my work on this / Only I can do this.</em> Share your split."
    }
  ],
  homework: {
    title: "Brand new to AI? Start with something personal tonight.",
    body: "The fastest way to lose the fear: use AI on something where there's no security policy and no judgment. Try one of these in your free tool of choice (ChatGPT, Claude, Gemini, or Perplexity all have free web versions):",
    prompt: "\"I'm trying to [plan a weekend / write a tough message / figure out a recipe from what's in my fridge / understand a confusing bill]. Ask me 3 questions before you help, so your answer actually fits.\"<br><br>That last line — <em>ask me questions first</em> — is the single most useful prompting habit you'll ever learn."
  }
}
```

---

## 11. Common Pitfalls (avoid these)

1. **Fabricating stats.** If you can't link to the source, don't include the number. Re-shape the trend around something verifiable.
2. **Generic role slants.** "AI can help you work faster" is not a slant. Each line should reveal something only true of that role.
3. **Recommending tools the member's company has blocked.** Challenges should reference *the company-approved AI tool* generically, not name specific consumer apps.
4. **Three near-identical trends.** Variety in angle matters more than topical density. If two trends are essentially "AI is good at writing," replace one.
5. **Forgetting the comma when inserting above an existing entry.** This breaks the object literal and kills the site.
6. **Using `<em>` everywhere.** It's an accent, not a default. ~1–2 per trend body is plenty.
7. **Hype voice creeping in.** Re-read the draft. If it sounds like a vendor blog post, rewrite.
8. **Long-winded homework prompts.** The personal prompt is short by design.
9. **Skipping the idempotency check.** Double drops are confusing and noisy in the PR list.
10. **Pushing to `main` directly.** Never. Always PR.

---

## 12. Tone Calibration — Quick Reference

| ❌ Avoid | ✅ Use instead |
|---|---|
| "AI will revolutionize your role" | "AI is changing what's most valuable in your role" |
| "Don't get left behind" | "Here's one way to stay ahead" |
| "Unleash productivity" | "Cut the busywork" |
| "Game-changing tool" | "A practical tool worth 10 minutes tonight" |
| "Studies show…" (no link) | "Microsoft's 2026 Work Trend Index found…" |
| "You should consider…" | "Try this:" |

---

**End of spec.** When in doubt, optimize for: *Did this leave the reader more confident and less afraid?* If yes, ship it.
