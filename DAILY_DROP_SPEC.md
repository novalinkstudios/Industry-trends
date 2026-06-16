# Daily Drop — Routine Spec

> **Purpose:** A runbook for the Claude Code Remote Routine that generates, validates, and publishes each day’s Daily Drop entry to the Cisco AI Ops Accelerator archive site. Click each section’s `❯` chevron to expand it.

-----

<details>
<summary>❯&nbsp;&nbsp;<strong>1. Mission</strong></summary>

<br>

The Daily Drop is a short editorial briefing for Cisco employees in **traditional operations, strategy & planning, project management, and administrative roles** who are AI-curious but cautious. The community goal is to **remove the fear of AI** and help members use AI to advance — not be replaced by it.

Every drop must leave the reader feeling **more capable, less afraid, and slightly more equipped** than when they opened the page.

**Audience weighting (most → least):** Strategy & Planning → Operations → Project Management → Administrative.

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
1. **Validate** the file per §7.
1. **Commit** on a new branch: `claude/daily-drop-YYYY-MM-DD`
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
      body: "1–3 sentences. Use <em>...</em> to highlight a key phrase or statistic.",
      slants: {
        strategy:   "One line — how this lands for a strategy/planning person.",
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
- Every trend must have all **4 role slants** (`strategy`, `operations`, `pm`, `admin`).
- Every trend must have **one challenge** in the `{ steps: [...] }` shape.
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
- Prefer trends from the **last 2–4 weeks**. Avoid recycling stories the community has likely seen.
- **Every stat or claim must come from a real, citable source.** If you can’t link it, don’t quote it. Never fabricate numbers.

### Role slants

- **One sentence each.** Don’t pad.
- Slants should be **genuinely different** for each role — if the same line could apply to all four, the trend’s framing is too generic and needs reworking.
- If a trend honestly does not have a meaningful angle for one of the roles, write the most truthful version possible — don’t manufacture relevance.

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
        body: "Example body with <em>a highlighted phrase</em> for emphasis.",
        slants: {
          strategy:   "Strategy slant line.",
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
- [ ] Every trend has all 4 role slants and 1 challenge.
- [ ] Every challenge has 3–6 concrete steps and ends with a sharing action.
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
- [x] 3 trends, 4 role slants each
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
      body: "Microsoft's 2026 Work Trend Index just landed. <em>49% of Copilot conversations now support cognitive work</em> — analysis, problem-solving, strategic thinking — and 58% of AI users say they're producing work they couldn't have done a year ago. The work isn't disappearing. It's being promoted.",
      slants: {
        strategy:   "You're shifting from <em>writer</em> to <em>editor + pressure-tester</em>.",
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
      body: "Deloitte's 2026 enterprise report puts it plainly: <em>companies are layering AI onto legacy processes instead of redesigning work holistically</em>. The investment isn't compounding because the workflow underneath is still pre-AI.",
      slants: {
        strategy:   "The QBR was built for a pre-AI world. Rethink the inputs and outputs.",
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

**End of spec.** When in doubt, optimize for: *Did this leave the reader more confident and less afraid?* If yes, ship it.
