# Daily Drop — Spec for Cowork

> **Purpose of this document:** A runbook telling Cowork exactly how to generate, format, and publish each day's Daily Drop entry to the AI Operations Accelerator archive site. Follow it top to bottom each day.

---

## 1. Mission

The Daily Drop is a short editorial briefing for professionals in **traditional operations, strategy & planning, project management, and administrative roles** who are AI-curious but cautious. The community goal is to **remove the fear of AI** and help members use AI to advance — not be replaced by it.

Every drop must leave the reader feeling **more capable, less afraid, and slightly more equipped** than when they opened the page.

**Audience weighting (most → least):** Strategy & Planning → Operations → Project Management → Administrative.

---

## 2. Daily Workflow

Run this every day at the scheduled time.

1. **Pull the latest version of the repo.**
2. **Research** today's three trends (see §5 for sources).
3. **Draft** the day's entry following the structure in §3 and the voice rules in §4.
4. **Insert** the new entry into `index.html` per §6.
5. **Validate** the file per §7 before committing.
6. **Commit** with the message: `Add drop: YYYY-MM-DD`
7. **Push** to the default branch. Netlify/Vercel will auto-deploy.

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
      challenge: "A short, security-safe action a community member can try and share back. Use <em>...</em> for any prompt text being suggested."
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
- The three trends should **cover different angles** when possible — e.g., one strategic shift, one workflow/tooling shift, one skills/cultural shift. Don't run three "new AI tool launched" trends in one day.
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
- Inside string values, use `\"` to escape double quotes (since the strings are wrapped in double quotes).
- HTML emphasis: use `<em>...</em>` for highlights. The CSS renders these with a soft accent background — use sparingly (1–2 per trend body, optional in slants/challenges).
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

## 7. Pre-publish Checklist

Before committing, verify:

- [ ] The JSON-like object structure is valid JavaScript (no missing commas, no unescaped quotes, no trailing commas before `}`).
- [ ] Date key is in `"YYYY-MM-DD"` format and matches today's date.
- [ ] Exactly 3 trends.
- [ ] Every trend has all 4 role slants and 1 challenge.
- [ ] Every stat or claim has a real source you could link to.
- [ ] No banned hype words (see §4).
- [ ] Challenges are security-safe (no proprietary data instructions).
- [ ] Homework prompt is personal, not work-related.
- [ ] HTML `<em>` tags are properly opened and closed.
- [ ] Opening `index.html` locally renders the new drop without breaking the page.

If any check fails, **fix before pushing.** A broken JS object will break the whole site, not just the new entry.

---

## 8. Full Worked Example

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

## 9. Common Pitfalls (avoid these)

1. **Fabricating stats.** If you can't link to the source, don't include the number. Re-shape the trend around something verifiable.
2. **Generic role slants.** "AI can help you work faster" is not a slant. Each line should reveal something only true of that role.
3. **Recommending tools the member's company has blocked.** Challenges should reference *the company-approved AI tool* generically, not name specific consumer apps.
4. **Three near-identical trends.** Variety in angle matters more than topical density. If two trends are essentially "AI is good at writing," replace one.
5. **Forgetting the comma when inserting above an existing entry.** This breaks the object literal and kills the site.
6. **Using `<em>` everywhere.** It's an accent, not a default. ~1–2 per trend body is plenty.
7. **Hype voice creeping in.** Re-read the draft. If it sounds like a vendor blog post, rewrite.
8. **Long-winded homework prompts.** The personal prompt is short by design. Members should be able to copy it and paste it into a chatbot without editing.

---

## 10. Tone Calibration — Quick Reference

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
