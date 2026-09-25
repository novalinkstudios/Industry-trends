# Daily Drop — Routine Spec

> **Purpose:** A runbook for the Claude Code Remote Routine that generates, validates, and publishes each day’s Daily Drop entry to the Cisco AI Ops Accelerator archive site. Click each section’s `❯` chevron to expand it.

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>1. Mission</strong></summary>

<br>

The Daily Drop is a short editorial briefing for Cisco employees in **leadership, traditional operations, strategy & planning, project management, and administrative roles** who are AI-curious but cautious. The community goal is to **remove the fear of AI** and help members use AI to advance — not be replaced by it.

Every drop must leave the reader feeling **more capable, less afraid, and slightly more equipped** than when they opened the page.

**Audience weighting (most → least):** Strategy & Planning → Leaders → Operations → Project Management → Administrative.

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>2. Daily Workflow</strong></summary>

<br>

The routine runs once per day on Anthropic’s cloud (no local machine required). On each run:

1. **Fresh clone** of the default branch happens automatically.
1. **Idempotency check** (see §8) — if today’s drop already exists or is already in an open PR, exit cleanly without creating duplicates.
1. **Research** today’s three trends using web search (see §5 for sources).
1. **Draft** the day’s entry following the structure in §3 and the voice rules in §4.
1. **Insert** the new entry into `index.html` per §6.
1. **Sync `drops.json`** — run `python generate_drop.py --sync` so downstream consumers stay current.
1. **Validate** the file per §7.
1. **Commit** on a new branch: `claude/daily-drop-YYYY-MM-DD` (commit both `index.html` and `drops.json`).
1. **Open a Pull Request** following the format in §9.
1. **Exit.** A human reviews and merges the PR. Netlify/Vercel auto-deploys on merge.

The routine never pushes directly to `main`. Every drop is human-reviewed before going live.

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>3. Content Format</strong></summary>

<br>

Each daily entry is a JavaScript object keyed by ISO date (`"YYYY-MM-DD"`) inside the `DROPS` object in `index.html`. Its shape:

```javascript
"2026-06-15": {
  intro: "One-sentence framing for the day.",
  trends: [
    {
      title: "Trend headline — short and editorial",
      source_url: "https://example.com/the-source-article",
      body: "1–3 sentences. Use <em>...</em> to highlight a key phrase or statistic.",
      slants: {
        strategy:   "One line — how this lands for a strategy/planning person.",
        leaders:    "One line — how this lands for a people leader or senior manager.",
        operations: "One line — how this lands for an ops person.",
        pm:         "One line — how this lands for a project manager.",
        admin:      "One line — how this lands for an administrative pro."
      },
      challenge: {
        steps: [
          "Step 1 — short, concrete action (open a tool, find a doc, etc.)",
          "Step 2 — uses <em>...</em> to wrap any exact prompt text the member should paste.",
          "Step 3 — what to do with the AI's output (read, identify, mark, etc.)",
          "Step 4 — share back to the community."
        ]
      }
    }
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
- Every trend must have all **5 role slants** (`strategy`, `leaders`, `operations`, `pm`, `admin`).
- Every trend must have **one challenge** in the `{ steps: [...] }` shape.
- Every trend must have a **`source_url`** — the URL of the primary source cited in the trend body. This renders as a "Source" button at the bottom of the trend card, opening in a new window.
- Every drop must have **one homework block**.

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>4. Editorial Guidelines</strong></summary>

<br>

### Voice

- **Encouraging, plain-spoken, confident.** Tone of a smart friend, not a consultant.
- **Never fear-based.** “AI is coming for you” is banned. “AI is shifting what’s valuable in your work” is the move.
- **Active verbs.** “You’re shifting from writer to editor” not “Writers are being shifted.”
- **No hype words.** Avoid *revolutionary, game-changing, disrupt, unleash, supercharge, transformative*.
- **No empty hedging.** Avoid *might, could potentially, may possibly*. Pick a position.
- **Sentence-case headlines.** No Title Case headlines, no clickbait.

### Trend selection

- The three trends should **cover different angles** — e.g., one strategic shift, one workflow/tooling shift, one skills/cultural shift. Don’t run three “new AI tool launched” trends in one day.
- Lean into trends that **most strongly affect strategy & planning roles** (the primary audience), then ops, then PM, then admin.
- All sources **MUST be published within the last 72 hours** of the drop date. Freshness is non-negotiable — do not use older articles regardless of relevance.
- **Every stat or claim must come from a real, citable source.** If you can’t link it, don’t quote it. Never fabricate numbers.

### Role slants

- **Five slants per trend:** `strategy`, `leaders`, `operations`, `pm`, `admin`.
- **One sentence each.** Don’t pad.
- The **`leaders`** slant targets people managers and senior managers — those accountable for team performance, AI adoption decisions, and organizational change. Frame it around what they can do with their positional influence (set direction, fund enablement, model behavior, ask the hard question in the room).
- Slants should be **genuinely different** for each role — if the same line could apply to all five, the trend’s framing is too generic and needs reworking.
- If a trend honestly does not have a meaningful angle for one of the roles, write the most truthful version possible — don’t manufacture relevance.
- **Positive and empowering tone.** Every slant should leave the reader feeling more capable, not more anxious. Frame around opportunity, action, and what’s possible — not around gaps, threats, or what’s going wrong. Avoid language that warns, scolds, or highlights what someone is missing.
- **Frame from the hiring and team-building side.** The audience is building, managing, and developing teams — not marketing themselves to another employer. Write slants about how to hire for the right skills, develop people, structure teams, and make smarter organizational decisions. Never frame a slant in a way that encourages the reader to leave their current role or position themselves for the job market.
- **Positive-leaning headlines.** Trend headlines should emphasize what’s working, what’s emerging, or what organizations can do — not what’s broken, failing, or dividing. Reframe negative findings around the opportunity they reveal.

### Challenges

- **Step-by-step structure.** Every challenge is a numbered sequence of **3–6 short steps**, written for someone new to AI. Each step should be 1–2 sentences max — easy to follow, no jargon.
- **Each step is concrete.** “Open your company-approved AI tool,” “Paste the document in,” “Read the response.” Not: “Think about how AI could help” or “Consider the implications.”
- **Wrap exact prompt text in `<em>...</em>`.** Members should be able to copy/paste the prompt without retyping or paraphrasing. Example: `Add this prompt: <em>"Argue against this from the perspective of a skeptical executive."</em>`
- **Always end with a sharing step.** The last step should invite the member to share their result or insight in the community group.
- **Don’t pad with filler steps.** If a challenge is genuinely simple (a reflection prompt), 3 steps is fine. Don’t manufacture steps to hit a number.
- **Security-safe.** Default assumption: the community member works at a Cisco-approved AI environment. Never instruct them to paste proprietary documents, customer data, or internal information into a public AI tool.
- Safe framings: “using your company-approved AI tool,” “with a fictional or sanitized version,” “with a document you wrote that doesn’t contain confidential info.”
- **Doable in 10–15 minutes total.** No multi-day projects.
- **Progressive difficulty across the week.** Members are increasing their AI knowledge over time — early-week challenges can be lighter (single tool, single prompt), later-week can layer in more sophisticated techniques (chained prompts, comparison across tools, structured outputs).

### Homework (personal prompt)

- This is the **try-at-home, no-work-risk** moment of each drop. Critical for AI-anxious members.
- Always use a **personal-life scenario** (not a work scenario). Examples: planning a trip, writing a tough personal message, cooking with what’s on hand, decoding a bill, prepping for a hard conversation.
- The prompt should include a **prompting technique** the member learns by doing — e.g., “ask me 3 questions before you answer,” “give me 3 options ranked by [criterion],” “explain like I’m new to this.”
- Recommend free tools only: **ChatGPT, Claude, Gemini, Perplexity** (web versions).

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>5. Source Guidance</strong></summary>

<br>

Acceptable primary sources for trends:

- Stanford HAI AI Index
- Microsoft Work Trend Index
- Deloitte / PwC / McKinsey / Gartner / Forrester research reports
- MIT Sloan Management Review
- Harvard Business Review (AI/operations coverage)
- The Information, The Verge, Axios (for product/news trends)
- Anthropic, OpenAI, Google DeepMind, Microsoft official blog posts (for capability shifts)
- Substack / Medium pieces from credible operators (e.g., Lenny’s Newsletter, Every, Stratechery) — only when the underlying analysis is sound

**Do not source from:**

- LinkedIn influencer posts as primary sources (link through to what they’re citing)
- Vendor marketing pages
- AI-generated SEO content farms
- Anything without a clear author and date

When in doubt: **fewer, stronger sources > more, weaker ones.** One trend with a solid citation beats three with vague references.

**Capture every source URL** — they go in the PR description (§9).

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>6. Insertion Instructions</strong></summary>

<br>

### ⚠️ Scope of edits — read first

The routine modifies **one and only one thing in `index.html`**: the `DROPS` object inside the `<script>` block. **Do not edit any other part of the file.** That means:

- ❌ Do not change the `<style>` block (design tokens, fonts, layout, colors)
- ❌ Do not change the `<head>`, `<header>`, hero `<section>`, `<nav>`, `<footer>`, or any HTML structure
- ❌ Do not change any JavaScript function or event handler
- ❌ Do not add new HTML elements, scripts, stylesheets, or external dependencies
- ✅ Only add one new entry to the `DROPS` object per run

If the styling looks “off” or you think the design needs adjustment, **leave it alone**. Design changes are a separate workflow handled by a human. Your job is content, not design.

### Where to insert

Open `index.html`. Find the `DROPS` object inside the `<script>` block. Insert the new entry **above the most recent existing entry** so newest is always first.

### Format rules

- Use `"YYYY-MM-DD"` as the key, in quotes.
- **Add a comma** after the new entry’s closing brace if another entry follows it.
- Remove or add commas as needed so the object literal stays valid JavaScript.
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
        source_url: "https://example.com/source-article",
        body: "Example body with <em>a highlighted phrase</em> for emphasis.",
        slants: {
          strategy:   "Strategy slant line.",
          leaders:    "Leaders slant line.",
          operations: "Operations slant line.",
          pm:         "PM slant line.",
          admin:      "Admin slant line."
        },
        challenge: {
          steps: [
            "First concrete action.",
            "Paste this prompt: <em>\"Exact prompt text here.\"</em>",
            "Read the output and identify one insight.",
            "Share that insight in the group."
          ]
        }
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
    /* existing entry below */
  }
};
```

Note the trailing comma after `"2026-06-15"`’s closing brace.

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>7. Pre-commit Checklist</strong></summary>

<br>

Before committing, verify:

- [ ] The JSON-like object structure is valid JavaScript (no missing commas, no unescaped quotes, no trailing commas before `}`).
- [ ] Date key is `"YYYY-MM-DD"` and matches today’s date in **Eastern Time**.
- [ ] Exactly 3 trends.
- [ ] Every trend has all 5 role slants (`strategy`, `leaders`, `operations`, `pm`, `admin`) and 1 challenge.
- [ ] Every challenge has 3–6 concrete steps and ends with a sharing action.
- [ ] Every trend has a `source_url` pointing to the primary source.
- [ ] Every stat or claim has a real source you could link to (URL captured for the PR body).
- [ ] No banned hype words (see §4).
- [ ] Challenges are security-safe (no proprietary data instructions).
- [ ] Homework prompt is personal, not work-related.
- [ ] HTML `<em>` tags are properly opened and closed.

If any check fails, **fix before committing.** A broken JS object will break the whole site, not just the new entry.

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>8. Idempotency Rules</strong></summary>

<br>

The routine may occasionally run more than once for the same date. To prevent duplicates:

1. **Before drafting**, check `index.html` for today’s date key. If it already exists in `DROPS`, **exit cleanly** with the message: *“Today’s drop already published — no action taken.”* Do not commit, do not open a PR.
1. **Before opening a PR**, check open PRs for any with `Daily Drop: [today's date]` in the title. If one exists, **exit cleanly** — do not open a second.
1. If the routine is partway through a run and the network drops, it should be safe to restart from step 1; any prior partial work would have been on a separate branch that can be discarded.

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>9. Branch and Pull Request Conventions</strong></summary>

<br>

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
- [x] 3 trends, 5 role slants each
- [x] Each challenge is 3–6 concrete steps ending with a share action
- [x] Every claim sourced
- [x] No banned hype words
- [x] Security-safe challenges
- [x] Personal homework prompt
- [x] HTML tags balanced

Merge to publish. Netlify/Vercel will auto-deploy.
```

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>10. Full Worked Example</strong></summary>

<br>

This is the seed entry already in the file. Use it as a reference for tone, length, and structure.

```javascript
"2026-06-14": {
  intro: "Three things worth thinking about today — and one for you to try at home.",
  trends: [
    {
      title: "The strategic memo is being rebuilt — fast",
      source_url: "https://www.microsoft.com/en-us/worklab/work-trend-index/2026",
      body: "Microsoft's 2026 Work Trend Index just landed. <em>49% of Copilot conversations now support cognitive work</em> — analysis, problem-solving, strategic thinking — and 58% of AI users say they're producing work they couldn't have done a year ago. The work isn't disappearing. It's being promoted.",
      slants: {
        strategy:   "You're shifting from <em>writer</em> to <em>editor + pressure-tester</em>.",
        leaders:    "Your team's strategic output can improve overnight — if you invest the time to show them how to pressure-test with AI.",
        operations: "Synthesis across systems is now a 30-min job, not a 3-day one.",
        pm:         "Status reports get auto-drafted; framing the right questions is the new value-add.",
        admin:      "Your judgment on tone, context, and 'what the exec actually meant' becomes the premium skill."
      },
      challenge: {
        steps: [
          "Pick a document you wrote last quarter — a recommendation, memo, or proposal. Make sure it doesn't contain confidential client or customer information.",
          "Open your company-approved AI tool (Copilot, Gemini Enterprise, Claude for Work — whatever's blessed at Cisco).",
          "Paste the document in, then add this prompt: <em>\"Argue against this from the perspective of a skeptical executive. Be specific about the weakest assumptions.\"</em>",
          "Read the response carefully and identify one point you hadn't considered before.",
          "Share that insight in the group — what surprised you most?"
        ]
      }
    },
    {
      title: "The Transformation Paradox",
      source_url: "https://www.deloitte.com/global/en/issues/generative-ai/state-of-ai-in-enterprise.html",
      body: "Deloitte's 2026 enterprise report puts it plainly: <em>companies are layering AI onto legacy processes instead of redesigning work holistically</em>. The investment isn't compounding because the workflow underneath is still pre-AI.",
      slants: {
        strategy:   "The QBR was built for a pre-AI world. Rethink the inputs and outputs.",
        leaders:    "Give one team permission to redesign a workflow from scratch — the results will make the case for doing it everywhere else.",
        operations: "Your SOPs probably encode 2019 assumptions.",
        pm:         "\"Weekly check-ins\" exist because info moved slowly. Does it still?",
        admin:      "Calendar-and-email triage workflows are ripe for a clean-slate redesign."
      },
      challenge: {
        steps: [
          "Pick ONE recurring meeting or process you own — the QBR, a weekly check-in, a status report.",
          "Open a notes app or grab a piece of paper.",
          "Write at the top: <em>\"If AI were a teammate from minute one, this would [...]\"</em>",
          "Finish the sentence. Don't overthink it — the first instinct is usually the most honest one.",
          "Share your one-sentence answer in the group."
        ]
      }
    },
    {
      title: "AI fluency is the new literacy",
      body: "Stanford HAI's 2026 AI Index: AI-related skills now appear in <em>2.5% of all U.S. job postings — a 297% increase over a decade</em>. This isn't \"learn to code.\" It's <em>learn to direct, evaluate, and trust-but-verify</em> AI output.",
      slants: {
        strategy:   "Prompting is problem-framing. The clearer your ask, the sharper your strategy.",
        leaders:    "The leaders who invest in AI fluency now are building the teams that will set the pace for everyone else.",
        operations: "Knowing when AI is wrong saves more time than AI being right.",
        pm:         "Agent orchestration is the next PM specialty.",
        admin:      "You already know how things actually work here. AI doesn't."
      },
      challenge: {
        steps: [
          "Open a blank document or note.",
          "List your top 3 weekly recurring tasks — the things you do every week without fail.",
          "Next to each task, write one of three labels: <em>\"AI could draft this\"</em>, <em>\"AI could review my work on this\"</em>, or <em>\"Only I can do this.\"</em>",
          "Look at your split. Pick one task you didn't realize AI could help with.",
          "Share your split in the group, and call out that one surprise task."
        ]
      }
    }
  ],
  homework: {
    title: "Brand new to AI? Start with something personal tonight.",
    body: "The fastest way to lose the fear: use AI on something where there's no security policy and no judgment. Try one of these in your free tool of choice (ChatGPT, Claude, Gemini, or Perplexity all have free web versions):",
    prompt: "\"I'm trying to [plan a weekend / write a tough message / figure out a recipe from what's in my fridge / understand a confusing bill]. Ask me 3 questions before you help, so your answer actually fits.\"<br><br>That last line — <em>ask me questions first</em> — is the single most useful prompting habit you'll ever learn."
  }
}
```

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>11. Common Pitfalls</strong></summary>

<br>

1. **Fabricating stats.** If you can’t link to the source, don’t include the number. Re-shape the trend around something verifiable.
1. **Generic role slants.** “AI can help you work faster” is not a slant. Each line should reveal something only true of that role.
1. **Recommending tools the member’s company has blocked.** Challenges should reference *the company-approved AI tool* generically.
1. **Three near-identical trends.** Variety in angle matters more than topical density.
1. **Forgetting the comma when inserting above an existing entry.** This breaks the object literal and kills the site.
1. **Using `<em>` everywhere.** It’s an accent, not a default. ~1–2 per trend body is plenty.
1. **Hype voice creeping in.** Re-read the draft. If it sounds like a vendor blog post, rewrite.
1. **Long-winded homework prompts.** The personal prompt is short by design.
1. **Skipping the idempotency check.** Double drops are confusing and noisy in the PR list.
1. **Pushing to `main` directly.** Never. Always PR.
1. **Padding challenge steps with filler.** 3 honest steps beats 6 padded ones.
1. **Vague challenge steps.** “Use AI to think about your strategy” is bad. “Open [tool], paste [content], add the prompt: <em>’…’</em>” is good. Always tell the member exactly what to do.

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>12. Tone Calibration — Quick Reference</strong></summary>

<br>

|❌ Avoid                          |✅ Use instead                                     |
|---------------------------------|--------------------------------------------------|
|“AI will revolutionize your role”|“AI is changing what’s most valuable in your role”|
|“Don’t get left behind”          |“Here’s one way to stay ahead”                    |
|“Unleash productivity”           |“Cut the busywork”                                |
|“Game-changing tool”             |“A practical tool worth 10 minutes tonight”       |
|“Studies show…” (no link)        |“Microsoft’s 2026 Work Trend Index found…”        |
|“You should consider…”           |“Try this:”                                       |

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>13. Design Tokens &amp; Brand</strong></summary>

<br>

The host `index.html` uses Cisco’s brand system. The routine does NOT need to edit these — they live in the host file’s `<style>` block. This section is documented here so the brand language stays consistent if the page is ever extended.

### Color tokens

```css
--navy:    #0D2340;   /* primary dark / text */
--blue:    #00BCEB;   /* primary accent — links, highlights, dots, italic year */
--gold:    #FBAB18;   /* secondary accent — trend numbers, "today" ring, homework left border */
--magenta: #E20074;   /* tertiary accent — challenge call-to-action label */
--white:   #FFFFFF;   /* card backgrounds */
--light:   #F0F6FA;   /* page background */
--muted:   #6B7A8D;   /* secondary text */
--text:    #0D2340;   /* body text */
```

### Typography

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,300&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
```

- **DM Serif Display** — display type for hero title, date hero, trend titles, homework title, intro line. Used at large sizes with italic variants for emphasis.
- **DM Sans** — body text, navigation labels, role tags, eyebrows. Multiple weights (300/400/500/700).

### Component → token map

|Element                                      |Token usage                    |
|---------------------------------------------|-------------------------------|
|Hero background                              |`--navy`                       |
|Hero “Accelerator” italic                    |`--blue`                       |
|Sticky navbar background                     |`--white` (translucent + blur) |
|Calendar “today” ring                        |`--gold`                       |
|Calendar “has-drop” dot                      |`--blue`                       |
|Calendar selected day                        |`--navy` fill, `--blue` dot    |
|Today button                                 |`--navy` bg → `--blue` on hover|
|Trend number (italic)                        |`--gold`                       |
|Trend title                                  |`--navy`                       |
|Trend body `<em>` highlight                  |`--blue` tint background       |
|Role slants left border                      |`--blue`                       |
|Role tag                                     |`--navy` text on `--blue` tint |
|Challenge label “Try this with the community”|`--magenta`                    |
|Challenge step circles                       |`--white` text on `--blue`     |
|Homework prompt left border                  |`--gold`                       |
|Footer                                       |`--navy`                       |

### Brand voice in UI

- Calendar trigger label: shows the currently selected date (e.g., “Jun 14, 2026”)
- Empty-state prev/next at top: “No earlier drops” / “Latest drop” (warmer than dashes)
- Today button: short, action-only — never “Go to Today”

</details>

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>14. Homework Category Rotation (200 categories)</strong></summary>

<br>

### Rule

**Do not repeat the same category within 250 days.** Track which categories have been used and when. Each category below includes 2–3 example prompt angles — vary the specific prompt each time the category comes back into rotation. When all 200 have been used, restart from the least recently used.

### Categories

**Personal Life & Logistics (1–15)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 1 | Trip/travel planning | Weekend getaway, day trip, bucket-list destination research |
| 2 | Meal planning from what's on hand | Fridge inventory dinner, leftover transformation, pantry-only meals |
| 3 | Home maintenance troubleshooting | Diagnose an appliance issue, fix a running toilet, patch a wall |
| 4 | Personal budgeting | Build a monthly budget, track spending categories, find savings |
| 5 | Moving/relocation planning | Neighborhood comparison, moving timeline, packing strategy |
| 6 | Event planning | Birthday party, reunion, holiday gathering, potluck coordination |
| 7 | Home organization | Closet declutter plan, garage organization, digital + physical filing |
| 8 | Car decisions | Maintenance schedule, purchase comparison, insurance shopping |
| 9 | Subscription/recurring cost audit | Identify what to cancel, compare alternatives, negotiate renewals |
| 10 | Emergency preparedness | Build a go-bag list, family communication plan, insurance review |
| 11 | Apartment/house hunting | Compare two listings, generate questions for a landlord, red flag checklist |
| 12 | Wardrobe/closet audit | Capsule wardrobe plan, seasonal rotation, outfit planning |
| 13 | Commute optimization | Route comparison, podcast/audiobook queue, productive transit time |
| 14 | Seasonal home prep | Winterizing, spring cleaning checklist, storm prep |
| 15 | Daily routine redesign | Morning routine, evening wind-down, weekend structure |

**Health & Wellness (16–30)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 16 | Workout plan design | Beginner plan, 3-day/week schedule, bodyweight-only routine |
| 17 | Understanding lab results | Blood work, cholesterol panel, vitamin levels |
| 18 | Sleep improvement | Bedtime routine, sleep hygiene audit, wind-down sequence |
| 19 | Meal prep for health goals | High-protein week, low-sodium menu, anti-inflammatory meals |
| 20 | Stress management | Identify triggers, build a toolkit, 5-minute reset techniques |
| 21 | Walking/running plan | Couch-to-5K, step goal strategy, route planning |
| 22 | Ergonomic workspace setup | Desk audit, posture check, eye strain reduction |
| 23 | Hydration/nutrition tracking | Daily targets, meal timing, snack swaps |
| 24 | Meditation/mindfulness | Beginner practice, breathing techniques, gratitude journaling |
| 25 | Understanding a health condition | Research a diagnosis, generate doctor questions, treatment comparison |
| 26 | Stretching/mobility routine | Morning stretch, desk break sequence, recovery day plan |
| 27 | Dental/vision/preventive care | Appointment prep, questions for the provider, insurance maximization |
| 28 | Mental health check-in | Weekly reflection prompts, mood patterns, when to seek support |
| 29 | First aid refresher | Kit inventory, skill review, household safety audit |
| 30 | Healthy habit stacking | Pair new habits with existing ones, 30-day challenge design |

**Relationships & Communication (31–45)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 31 | Drafting a tough personal message | Saying no, delivering bad news, following up on something awkward |
| 32 | Rehearsing a difficult conversation | Role-play both sides, anticipate objections, find the opening line |
| 33 | Writing a heartfelt letter or card | Thank-you note, congratulations, sympathy, encouragement |
| 34 | Planning a meaningful date or outing | Anniversary, reconnection, budget-friendly surprise |
| 35 | Reconnecting with an old friend | Icebreaker message, shared memory prompt, no-pressure invitation |
| 36 | Setting a personal boundary | Script the language, practice delivery, plan for pushback |
| 37 | Writing a toast or speech | Wedding, birthday, retirement, team celebration |
| 38 | Resolving a neighbor/roommate issue | Noise, shared space, cost-splitting, polite escalation |
| 39 | Expressing gratitude | Specific thank-you, public acknowledgment draft, gratitude inventory |
| 40 | Navigating family dynamics | Holiday logistics, caregiving decisions, diffusing old conflicts |
| 41 | Apologizing well | Structure an honest apology, avoid common mistakes, follow up |
| 42 | Asking for help | Framing the ask, choosing who, making it easy to say yes |
| 43 | Giving personal feedback | To a friend, a partner, a family member — honestly and kindly |
| 44 | Supporting someone going through a hard time | What to say, what not to say, practical offers |
| 45 | Teaching something you know to someone else | Explain your expertise, break it into steps, check understanding |

**Learning & Curiosity (46–60)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 46 | Understanding a complex topic from scratch | Economics, climate, law, medicine — pick one you've always wondered about |
| 47 | Language learning practice | Conversational phrases, travel basics, daily 5-minute habit |
| 48 | Book/reading list curation | By mood, by goal, by genre — with rationale for each pick |
| 49 | Exploring a historical period or event | Deep dive, "what really happened," connecting it to today |
| 50 | Understanding a scientific concept | Quantum basics, how vaccines work, why the sky is blue — ELI5 |
| 51 | Learning about a different culture | Food, customs, holidays, etiquette for travel or conversation |
| 52 | Photography basics | Composition rules, phone camera tips, editing a specific shot |
| 53 | Understanding economic/political concepts | Inflation, tariffs, electoral systems — neutral explainer |
| 54 | Exploring philosophy or ethics | Trolley problem variants, stoicism basics, applied ethics in daily life |
| 55 | Music appreciation | Genre history, ear training, building a playlist by era |
| 56 | Learning to read a chart or data viz | Interpreting a graph, spotting misleading data, basic statistics |
| 57 | Understanding how something is made | A product, a building, a dish — the process from raw to finished |
| 58 | Current events deep dive | Pick one headline, get the full context and competing perspectives |
| 59 | Exploring a career or skill you're curious about | What does a [job] actually do? What would month one look like? |
| 60 | Fact-checking something you've always believed | Urban legends, common misconceptions, "is this actually true?" |

**Creative & Fun (61–75)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 61 | Writing a short story or poem | Flash fiction, limerick, personal narrative, fan fiction premise |
| 62 | Creating a trivia game for friends/family | Custom categories, difficulty tiers, themed rounds |
| 63 | Designing a themed movie/TV marathon | By mood, by decade, by actor, hidden gems in a genre |
| 64 | Building a custom playlist | Workout, dinner party, road trip, focus — with AI curation logic |
| 65 | Planning a themed dinner party | Country cuisine night, decade theme, mystery dinner |
| 66 | Writing a family newsletter or update | Seasonal recap, milestone announcements, humorous spin |
| 67 | Creating a personal challenge | 30-day drawing, photo-a-day, gratitude jar, learn one new thing daily |
| 68 | Brainstorming a side project or hobby | What fits your schedule, budget, and interests? |
| 69 | Designing a scavenger hunt | For kids, for friends, for a date, for a neighborhood walk |
| 70 | Building a "bucket list" with structure | Categorized, prioritized, with first steps for the top 3 |
| 71 | Writing humor | Roast jokes for a friend, comedic rewrite of a boring story, puns |
| 72 | Creating a custom crossword or puzzle | Themed clues, personal inside jokes, printable format |
| 73 | Reimagining your space | What would this room look like in a different style? Mood board prompts |
| 74 | Planning a game night | Game selection by group size, rule summaries, snack pairings |
| 75 | Collaborative storytelling | Start a story, let AI continue, then take it somewhere unexpected |

**Food & Cooking (76–85)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 76 | Cuisine exploration | Pick a country, build a 3-course menu, learn one technique |
| 77 | Baking something new | Bread, pastry, cookies — with technique focus and substitution tips |
| 78 | Cocktail/mocktail creation | By flavor profile, by occasion, by what's in the liquor cabinet |
| 79 | Meal prep for the week | Batch cooking strategy, variety within a budget, container plan |
| 80 | Understanding food labels | Decode a nutrition panel, compare two products, spot marketing tricks |
| 81 | Coffee or tea appreciation | Brewing methods, flavor profiles, tasting notes, gear on a budget |
| 82 | Recreating a restaurant dish at home | Reverse-engineer a favorite, find the technique, simplify |
| 83 | Cooking for dietary restrictions | Allergen-free, vegan swap, low-FODMAP — without sacrificing flavor |
| 84 | Fermentation/preservation project | Pickles, sourdough starter, jam — beginner walkthrough |
| 85 | Planning a potluck contribution | Crowd-pleaser that travels well, dietary-inclusive, make-ahead |

**Home & Garden (86–92)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 86 | Container garden planning | Herbs, vegetables, flowers — by sunlight, space, and season |
| 87 | DIY home repair walkthrough | Patch drywall, fix a squeaky door, replace a faucet |
| 88 | Room redesign on a budget | Rearrange what you have, one new piece, paint color strategy |
| 89 | Energy efficiency audit | Lower the electric bill, seal drafts, upgrade lighting |
| 90 | Pet care optimization | Routine, enrichment, vet prep questions, behavior troubleshooting |
| 91 | Lawn/yard seasonal plan | Month-by-month care, low-maintenance alternatives, curb appeal |
| 92 | Painting a room | Color selection psychology, prep steps, common mistakes to avoid |

**Personal Finance (93–100)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 93 | Savings plan for a specific goal | Vacation fund, down payment, big purchase — reverse-engineer the timeline |
| 94 | Understanding investment basics | Index funds, compound interest, risk tolerance — plain language |
| 95 | Comparing two major purchases | Appliances, electronics, cars — build a weighted decision matrix |
| 96 | Debt payoff strategy | Snowball vs. avalanche, visualization, milestone rewards |
| 97 | Negotiating a recurring bill | Cable, insurance, rent — script the call, anticipate counter-offers |
| 98 | Tax preparation checklist | Deductions to look for, documents to gather, timeline |
| 99 | Understanding retirement basics | 401k, IRA, employer match — what to do first |
| 100 | Decoding a confusing bill or statement | Medical bill, utility bill, insurance EOB — line by line |

**Technology & Digital Life (101–115)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 101 | Phone cleanup & optimization | Delete unused apps, organize home screen, free up storage |
| 102 | Password & account security audit | Set up a password manager, enable 2FA, review saved passwords |
| 103 | Smart home setup or troubleshooting | Compare smart speakers, automate lighting, fix connectivity issues |
| 104 | Digital decluttering | Inbox zero strategy, clean up cloud storage, unsubscribe from email lists |
| 105 | Screen time audit & reduction plan | Review usage stats, set app limits, design phone-free windows |
| 106 | Backup & data protection strategy | Set up automatic backups, 3-2-1 rule, test a restore |
| 107 | Understanding privacy settings | Social media privacy walkthrough, app permissions review, location sharing audit |
| 108 | Comparing streaming & digital services | Music, video, news — feature/price matrix for your household |
| 109 | Building a personal website or portfolio | Platform comparison, domain selection, content planning |
| 110 | Digital legacy & end-of-life planning | Password inheritance, account memorialization, digital executor setup |
| 111 | Home Wi-Fi optimization | Dead-zone diagnosis, router placement, mesh network comparison |
| 112 | Learning a new app or tool | Master keyboard shortcuts, hidden features, workflow templates |
| 113 | Online reputation & search results | Google yourself, clean up old profiles, manage what others see |
| 114 | AI tool exploration for personal use | Compare chatbots for a task, try image generation, automate a chore |
| 115 | E-waste & old device disposition | Trade-in value check, secure data wipe, responsible recycling options |

**Career & Professional Development (116–130)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 116 | Interview preparation & practice | Behavioral question rehearsal, STAR method practice, company research |
| 117 | Salary & compensation research | Market rate lookup, total comp calculation, cost-of-living comparison |
| 118 | LinkedIn profile refresh | Headline rewrite, summary overhaul, featured section strategy |
| 119 | Building a professional portfolio | Select your best work, write case study narratives, choose a format |
| 120 | Negotiating a raise or promotion | Build your case with evidence, script the conversation, anticipate objections |
| 121 | Writing a professional bio | Conference bio, website about page, 50-word vs. 200-word versions |
| 122 | Exploring a career pivot | Transferable skills inventory, informational interview questions, 90-day plan |
| 123 | Understanding your benefits package | HSA vs. FSA, equity vesting, disability insurance — decode what you have |
| 124 | Professional development plan | Skill gap analysis, course selection, quarterly learning goals |
| 125 | Networking without awkwardness | Craft a warm intro, follow up after an event, maintain dormant ties |
| 126 | Personal SWOT analysis | Identify strengths, weaknesses, opportunities, and threats in your career |
| 127 | Side hustle feasibility study | Time audit, market sizing, revenue model, minimum viable test |
| 128 | Public speaking improvement | Structure a talk, manage nerves, practice with AI feedback |
| 129 | Professional email & writing polish | Rewrite a wordy email, format a proposal, tone-check a sensitive message |
| 130 | Freelance or consulting basics | Rate setting, contract essentials, finding first clients |

**Parenting & Family (131–145)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 131 | Age-appropriate chore chart design | Toddler tasks, tween responsibilities, reward system structure |
| 132 | Explaining complex topics to kids | Where babies come from, why people die, how money works — age-calibrated |
| 133 | Family activity & game night planning | Rainy day ideas, multi-age games, outdoor adventure list by season |
| 134 | Homework help strategies | Math approaches, research skills, teaching without doing it for them |
| 135 | Screen time rules & digital parenting | Age-based guidelines, content filters, contract template for teens |
| 136 | College savings & education planning | 529 overview, savings timeline, financial aid basics |
| 137 | Teaching kids about money | Allowance structure, savings jars, first bank account, investing for teens |
| 138 | Family meeting framework | Agenda template, conflict resolution rules, shared decision-making |
| 139 | Babysitter or childcare search | Interview questions, emergency info sheet, trial run checklist |
| 140 | Multigenerational household planning | Shared space design, caregiving schedules, boundary setting |
| 141 | Kids' birthday party on a budget | Theme ideas, DIY decorations, activity timeline, allergy-safe treats |
| 142 | Building family traditions | Weekly rituals, holiday customs, milestone celebrations to start now |
| 143 | School communication & advocacy | Email the teacher, request accommodations, navigate a report card |
| 144 | Sibling conflict mediation | Fair-fighting rules, sharing frameworks, when to intervene |
| 145 | Summer or school break planning | Camp research, at-home schedule, skill-building projects, boredom jar |

**Travel & Adventure (146–160)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 146 | Packing optimization | Capsule packing list, carry-on only strategy, packing cube system |
| 147 | Travel hacking & points strategy | Credit card comparison, loyalty program basics, award booking walkthrough |
| 148 | Learning local customs & etiquette | Tipping norms, greeting styles, taboos to avoid at your destination |
| 149 | Road trip route building | Scenic detours, kid-friendly stops, EV charging plan, overnight pacing |
| 150 | Destination comparison & decision | Beach vs. mountain, two cities head-to-head, off-season value analysis |
| 151 | Solo travel planning | Safety checklist, meeting people on the road, itinerary for one |
| 152 | Day trip discovery | Hidden gems within 2 hours, themed day trips, seasonal picks |
| 153 | Travel journal & memory capture | Prompts for each day, photo organization plan, scrapbook layout |
| 154 | Budget travel planning | Hostel vs. hotel, free walking tours, eat-like-a-local strategy |
| 155 | International travel logistics | Visa requirements, phone plan options, currency exchange tips |
| 156 | Camping & outdoor adventure prep | Gear checklist, campsite comparison, beginner backpacking plan |
| 157 | Travel safety & health prep | Vaccination checklist, travel insurance comparison, embassy registration |
| 158 | Foodie travel itinerary | Build a trip around restaurants, markets, and food tours |
| 159 | Accessible travel planning | Wheelchair-friendly destinations, sensory considerations, accommodation requests |
| 160 | Post-trip organization | Photo culling workflow, expense reconciliation, trip review for next time |

**Arts & Culture (161–175)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 161 | Museum or gallery visit prep | Research the collection, plan a route, build a discussion guide |
| 162 | Understanding an art movement | Impressionism, Bauhaus, Afrofuturism — key works, context, why it matters |
| 163 | Local events & hidden culture | Find what's happening this weekend, explore a neighborhood, cultural calendar |
| 164 | Songwriting or lyric drafting | Write a verse, study song structure, remix a genre |
| 165 | Logo or personal brand design for fun | Design principles, color psychology, sketch a concept |
| 166 | Theater & live show discovery | What to see, how to get cheap tickets, pre-show context |
| 167 | Art journaling & visual expression | Prompt-a-day ideas, supply list for beginners, mixed media techniques |
| 168 | Film appreciation deep dive | Analyze a scene, explore a director's filmography, compare adaptations |
| 169 | Creative writing workshop | Character development, dialogue practice, world-building exercises |
| 170 | Learning a musical instrument | Practice routine, free resources, 30-day beginner plan |
| 171 | Crafting & maker project planning | Knitting, woodworking, pottery — pick a first project, source materials |
| 172 | Podcast or video creation basics | Topic selection, episode structure, recording setup on a budget |
| 173 | Dance or movement exploration | Learn a style's basics, find local classes, practice routine at home |
| 174 | Understanding architecture around you | Identify building styles, take a self-guided walking tour, learn the history |
| 175 | Book club hosting & facilitation | Pick a book, write discussion questions, plan snacks and logistics |

**Community & Civic (176–185)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 176 | Understanding local government | Who represents you, how decisions get made, where to show up |
| 177 | Volunteering match & planning | Find opportunities by interest, time commitment, and skill set |
| 178 | HOA or condo board participation | Understand governing docs, prepare for a meeting, run for the board |
| 179 | Understanding ballot measures & elections | Break down propositions, research candidates, build a voter guide |
| 180 | Community garden participation | Plot planning, shared rules, what to grow in your zone and season |
| 181 | Block party or neighborhood event planning | Permits, logistics, activities, invite template, potluck coordination |
| 182 | Local school board & education advocacy | Understand the budget, attend a meeting, advocate for a policy |
| 183 | Charitable giving strategy | Evaluate nonprofits, donor-advised fund basics, giving budget allocation |
| 184 | Neighborhood safety & mutual aid | Start a communication network, emergency contact list, resource sharing |
| 185 | Civic skill building | Write a letter to an elected official, public comment prep, petition basics |

**Seasonal & Holiday (186–195)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 186 | Holiday gift strategy & budgeting | Gift list organizer, price tracking, handmade vs. bought decision tree |
| 187 | New Year goal setting & reflection | Year-in-review framework, SMART goal drafting, theme-of-the-year |
| 188 | Spring garden & outdoor kickoff | Planting calendar, garden bed prep, seed starting schedule |
| 189 | Summer reading challenge | Build a list by genre or goal, tracking method, discussion prompts |
| 190 | Fall bucket list creation | Seasonal activities by region, weekend planning, cozy home prep |
| 191 | Winter comfort & hygge planning | Indoor projects, comfort food rotation, self-care during dark months |
| 192 | Holiday card & letter writing | Annual family update draft, card list management, design ideas |
| 193 | Back-to-school preparation | Supply list optimization, routine reset, teacher communication setup |
| 194 | Tax season organization sprint | Document gathering checklist, deduction tracker, deadline calendar |
| 195 | End-of-year financial review | Net worth snapshot, goal check-in, next-year budget draft |

**Miscellaneous & Quirky (196–200)**

| # | Category | Example prompt angles |
|---|----------|----------------------|
| 196 | AI debate partner | Pick a controversial opinion, argue both sides, stress-test your reasoning |
| 197 | Dream house or space design | Floor plan wishlist, style inspiration, feature priority ranking |
| 198 | Explain your job to a 10-year-old | Simplify what you do, why it matters, what a day looks like |
| 199 | Time capsule list creation | What to include, letter to future self, predictions for 10 years out |
| 200 | Personal motto or mission statement | Draft it, test it against your values, refine it to one sentence |

### Usage notes

- **Variety across the week**: Don't cluster similar categories in the same week (e.g., three food categories in a row). Aim for thematic diversity across any 5-day span.
- **Seasonal awareness**: Prefer seasonally relevant categories when applicable (e.g., "Seasonal home prep" in October, "Trip planning" before summer/holidays).
- **Progressive technique teaching**: Each homework prompt should teach a prompting technique by doing — e.g., "ask me questions first," "give me options ranked by [criterion]," "argue against your own recommendation." Don't repeat the same technique within 14 days.
- **Free tools only**: Always recommend ChatGPT, Claude, Gemini, or Perplexity (web versions).

</details>

-----

**End of spec.** When in doubt, optimize for: *Did this leave the reader more confident and less afraid?* If yes, ship it.
