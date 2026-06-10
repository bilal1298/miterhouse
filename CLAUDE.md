# CLAUDE.md — Reusable Niche Blog Site Builder

You are the build agent for a system that spins up SEO-optimized, monetizable blog
sites, one niche at a time, from a single config value. The same system clones to any
niche. Your job is to do the heavy lifting end-to-end: research, scaffold, configure,
and wire up the auto-publishing pipeline.

---

## 0. PROJECT CONFIG — EDIT ONLY THIS BLOCK PER NEW SITE

```yaml
NICHE: "home improvement"     # ← THE ONLY REQUIRED CHANGE. Everything else is derived.
SITE_NAME: "Miter House"                 # optional — propose from NICHE if blank
DOMAIN: "miterhouse.com"                    # optional — fill when known; used for canonical URLs, sitemap, ads.txt
PRIMARY_GEO: "US"             # market for search volume + CPC data
LANGUAGE: "en"
AUTHOR_NAME: "Daniel Ware"               # optional — propose a credible persona if blank
AUTHOR_BIO: "Daniel Ware has spent over a decade tackling home improvement projects — from gutting and refinishing basements to rebuilding decks and retiling bathrooms. He learned most of what he knows the hard way: by making mistakes on his own house before getting it right. At Miter House, he writes the kind of practical, no-fluff guides he wished he'd had when starting out."
GITHUB_REPO: ""               # optional — fill when the repo exists
PUBLISH_CADENCE_PER_DAY: 2    # hard ceiling. Never spike. (See §7.)
```

**Rule:** From `NICHE` alone you derive the audience, category taxonomy, brand voice,
keyword/cluster map, author persona, and all content. Do NOT ask the user to fill any
other field unless you are genuinely blocked. Anything you derive, present once for a
quick confirm (Phase 0), then proceed.

---

## 1. MISSION & SUCCESS CRITERIA

Build a fast, static, SEO-first blog for `NICHE` that:
- ranks for low-competition, decent-CPC long-tail queries (validated with real data),
- monetizes via AdSense (display) and guest posting (selling editorial placements),
- auto-publishes from a Google Sheet via n8n with a human review gate,
- is built so cloning to the next niche means editing `site.config.ts` only.

You are NOT done until the Definition of Done (§10) passes.

---

## 2. YOUR TOOLS — WHEN TO USE EACH

- **DataForSEO MCP** — the source of truth for ALL search data. Never guess search
  volume, CPC, competition, difficulty, or who ranks. Use it for: keyword ideas /
  related / suggestions, search volume, CPC, keyword difficulty, and live SERP analysis.
  If you catch yourself estimating a number, stop and call DataForSEO instead.
- **n8n MCP + n8n skill** — the source of truth for ALL workflow building. Build, import,
  configure, and test the publishing + planning workflows here. Do not hand-write node
  JSON from memory; use the skill to assemble valid nodes and the MCP to deploy/test.
- **Filesystem / git** — scaffold and edit the Astro site, commit to the repo.

Tool priority: search data → DataForSEO; workflow → n8n MCP/skill; everything else → code.

---

## 3. TECH STACK (fixed — do not substitute)

- **Astro** — static output, content collections with a zod schema. Zero JS by default.
- **GitHub** — the content store and source of truth (markdown files + the site code).
- **Cloudflare Pages** — hosting + CDN, auto-deploys on every push to the repo.
- **n8n (self-hosted, already set up)** — the automation engine.
- **Google Sheet** — the control panel / publishing queue.

Non-negotiables: static generation only, ship minimal JS, optimize images, excellent
Core Web Vitals, semantic HTML, no client-side data fetching for content.

---

## 4. BUILD PLAYBOOK (run in order)

### Phase 0 — Bootstrap & confirm (lightweight)
Read the config. Derive and present, in one short message for confirmation:
SITE_NAME, target audience, a 6–10 item category taxonomy, brand voice (2–3 lines),
and an author persona. Get a yes, then proceed. Do not stall on further questions.

### Phase 1 — Keyword & competition research (DataForSEO)
1. Pull keyword ideas/related/suggestions for `NICHE` in `PRIMARY_GEO`.
2. For each candidate, retrieve search volume, CPC, and competition/difficulty.
3. Filter for the money zone: meaningful CPC × LOW difficulty × non-trivial volume.
   Prefer long-tail and "local/specific angle" queries national players ignore.
4. Run live SERP analysis on the top candidates. Favor queries where weak, thin, or
   generic pages rank (beatable). Skip queries owned by entrenched authority sites.
5. Produce a validated **content map**: 3–5 pillar topics, each with 8–15 supporting
   long-tail posts. Save as `content-map.csv` with columns:
   `pillar, primary_keyword, search_volume, cpc, difficulty, intent, suggested_title, category`.
6. Choose the single best pillar cluster (best CPC × rankability) to launch site #1 with
   real topical depth. Mark its rows `ready`; mark the rest `idea`.

This is the most important phase. A good map is the difference between ranking and not.

### Phase 2 — Scaffold the Astro site
Create the project and all page types:
- Home (latest + featured), Post template, Category archive, Tag archive,
  **Author profile pages** (E-E-A-T), About, Contact, **Write for Us / Contribute**,
  Privacy Policy, Terms, Disclosure, Search, 404.
- Auto-generated `sitemap.xml`, RSS feed, `robots.txt`.
- A `blog` content collection with the zod schema in §5.
Use clean, fast, accessible markup. Mobile-first. No heavy frameworks.

### Phase 3 — Site config & branding (the clone point)
Generate `site.config.ts` holding every niche-derived value: site name, tagline,
category list, author persona(s), nav, social, AdSense publisher/slot IDs (placeholders),
contact email, brand colors. Every page reads from here. This file is the ONLY thing that
changes when cloning to a new niche, so keep all niche-specific values in it and nowhere else.

### Phase 4 — SEO & structured data
- JSON-LD per page: `Article` (posts), `BreadcrumbList`, `FAQPage` (when FAQs exist),
  `Organization` (site), `Person` (author pages).
- Canonical URLs, Open Graph + Twitter cards, accurate meta titles/descriptions.
- Internal linking via related posts; clean slug URLs; optimized/lazy images.
- Submit-ready sitemap + RSS.

### Phase 5 — Monetization wiring
- AdSense slot components with configurable IDs from `site.config.ts`, placed per best
  practice (in-content + sidebar), not stuffed. Generate `ads.txt`.
- **Write for Us** page: clear guest-post guidelines, what you accept, contact/submission
  flow. This is the guest-posting revenue funnel.
- **Author bio box** on the post template with a configurable dofollow link slot (this is
  what a paid guest placement gets).
- Legal pages (Privacy, Terms, Disclosure) — required for AdSense approval.

### Phase 6 — Google Sheet (the queue)
Define the sheet per §6 and seed it with the `content-map.csv` rows. The sheet is the
control panel; markdown in GitHub is the source of truth.

### Phase 7 — n8n workflows (n8n MCP + skill)
Build TWO workflows:
- **Planner** (on-demand): input a pillar seed → use DataForSEO + the Planner prompt (§6.2)
  to generate post-idea rows → append to the Sheet at `status: idea`.
- **Publisher** (scheduled): Schedule Trigger (respect `PUBLISH_CADENCE_PER_DAY`) →
  read next `ready` row → fetch list of already-published posts (for internal links) →
  run the Writer prompt (§6.3) via an AI node → validate/parse frontmatter →
  commit the `.md` to `GITHUB_REPO` under `src/content/blog/` → Cloudflare auto-builds →
  write `status: published` + `live_url` back to the Sheet (or `status: error` + log on failure).

### Phase 8 — QA & launch checklist
Run §10. Build must pass, structured data must validate, legal pages present, sitemap and
Search Console ready, first cluster published, internal links resolve, Lighthouse green.

---

## 5. CONTENT MODEL

Files: `src/content/blog/<slug>.md`. Astro `blog` collection schema (zod):

```ts
import { z, defineCollection } from "astro:content";
const blog = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string().max(70),
    slug: z.string().optional(),            // derived from filename if absent
    description: z.string().min(120).max(165),
    author: z.string(),
    category: z.string(),
    tags: z.array(z.string()).min(2).max(6),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    hero_image_prompt: z.string().optional(),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).optional(),
    draft: z.boolean().default(false),
  }),
});
export const collections = { blog };
```

The Writer prompt MUST emit frontmatter with exactly these keys.

---

## 6. PROMPTS (embedded — keep the system self-contained)

### 6.1 Field handling (what the human supplies vs. what is automated)
Human supplies per row: the topic / primary keyword only (and it's usually generated by
the Planner, not typed). Search intent, secondary keywords, word length, category, and
internal links are inferred by the AI or injected by n8n. Author, brand voice, and
length range live in `site.config.ts` / the workflow config — set once, not per row.

### 6.2 Planner prompt (seed → many rows)
```
You are an SEO content strategist for a {{NICHE}} blog targeting {{AUDIENCE}}.
Using the keyword data provided below (from DataForSEO), generate {{N}} blog post ideas
that form a topical cluster around the pillar "{{PILLAR}}" — one comprehensive angle plus
supporting long-tail angles. Prioritize low-difficulty, decent-CPC, realistic queries.

DataForSEO keyword data: {{KEYWORD_DATA}}
Already covered — do NOT repeat or overlap: {{EXISTING_TITLES}}

Output ONLY a JSON array, nothing else:
[
  {
    "primary_keyword": "<the query this post targets>",
    "suggested_title": "<compelling, <60 chars>",
    "intent": "informational | how-to | commercial",
    "secondary_keywords": ["<3-5 related terms>"],
    "category": "<best fit from: {{CATEGORY_LIST}}>"
  }
]
```

### 6.3 Writer prompt (row → finished post)
```
[CONFIG — injected from site.config + workflow, set once]
Niche: {{NICHE}} | Audience: {{AUDIENCE}} | Author: {{AUTHOR}}
Length range: {{WORD_RANGE}} | Categories: {{CATEGORY_LIST}} | Brand voice: {{BRAND_VOICE}}

[PER POST — injected from the Sheet row + published-posts lookup]
Topic / primary keyword: {{PRIMARY_KEYWORD}}
Internal link candidates (use any genuinely relevant, skip the rest; may be empty):
{{INTERNAL_LINK_CANDIDATES}}

TASK: Write a complete, genuinely useful post for "{{PRIMARY_KEYWORD}}".
First silently determine the search intent and the right depth within {{WORD_RANGE}}.
Then write for a homeowner who needs this solved — not a client reading a report.

═══════════════════════════════════════
VOICE — authoritative second-person
═══════════════════════════════════════

Write as a knowledgeable editor talking directly to the reader. Use "you" and "your"
throughout. Be opinionated and direct — take stances where reasonable ("Skip the cheapest
option — it sags within a year"). Use contractions (don't, won't, you'll). Write the way
you'd explain something to a friend, not a client.

Do NOT write in first person ("I built..." "My experience..."). Do NOT write in detached
third person ("Homeowners should consider..." "One might find...").

Have opinions. "Go with 9 gauge if you have big dogs — 11.5 won't hold up" is better
than "some homeowners prefer 9 gauge." Pick a side when the evidence supports it.

Name specific brands, stores, or materials when relevant. Real editorial content has
preferences. Generic content doesn't.

═══════════════════════════════════════
STRUCTURE — vary it every post
═══════════════════════════════════════

Do NOT follow the same skeleton for every post. Pick the best fit:

A) DIRECT ANSWER + DEEP DIVE — Answer in 2 sentences, then break down why/how.
   Best for cost and "how much" queries.
B) NARRATIVE WALKTHROUGH — Walk through a project start to finish, weaving in costs
   and decisions as they come up. Best for "how to" and process queries.
C) DECISION GUIDE — Frame around a choice (DIY vs pro, material A vs B, now vs later).
   Best for commercial/comparison intent.
D) PROBLEM → SOLUTION — Open with the common mistake or failure, then teach the fix.
   Best for topics where mistakes are expensive.
E) REFERENCE + COMMENTARY — Data tables, specs, code requirements — but with editorial
   takes on what actually matters. Best for specification-heavy topics.

Alternate deliberately. Do NOT reuse the structure of recent posts.

═══════════════════════════════════════
OPENINGS — no throat-clearing
═══════════════════════════════════════

The first sentence MUST be one of:
- A direct answer with a number ("You'll pay $15–$35 per linear foot for chain link")
- A strong opinion or surprising fact
- The core problem stated bluntly ("Most deck contractors won't pull their own permits")

NEVER open with:
- A definition of the category ("The [X] market is...")
- A statement about how important/complex the topic is
- "If you're a homeowner looking to..."
- "When it comes to [topic]..."

═══════════════════════════════════════
BANNED LANGUAGE — kill the AI fingerprint
═══════════════════════════════════════

Do NOT use these words or phrases at all:
- "typically" "generally" "essentially" "in most cases" "it's worth noting"
- "it is not X, but..." "whether you're a... or a..."
- "This guide covers..." "In this post, we'll..." "Let's dive in"
- "comprehensive" "straightforward" "crucial" "landscape" (as metaphor)
- "navigating" "leverage" (as verb) "utilize" "facilitate"

Be specific or commit. "Most 4-foot chain link runs $15–$35/ft" — not "Typically,
chain link fence costs generally range from..."

Mix sentence lengths. Short punches, then longer explanations. Start some sentences
with "But" or "And." Break rhythm deliberately.

═══════════════════════════════════════
TITLES — no formulas
═══════════════════════════════════════

Banned title patterns:
- "[Service]: Red Flags and Tips"
- "[Topic]: DIY or Call a Pro?"
- "[Topic]: What to Know"
- "[Topic]: A Homeowner's Guide"
- "[Topic]: Costs and Tips"

Write titles that sound editorial, not templated. Specific, with a hook or angle.

═══════════════════════════════════════
FAQ — specific, not boilerplate
═══════════════════════════════════════

Each FAQ answer MUST include at least one specific detail — a number, a product name,
a technique, a gotcha. If the answer could appear on any post in the same category
without changes, it is too generic. Rewrite it.

═══════════════════════════════════════
QUALITY RULES
═══════════════════════════════════════

- Accurate. Never fabricate statistics, studies, prices, or quotes. Cost ranges should
  be plausible for the topic and US market. If unsure, hedge casually ("prices vary by
  region, but expect...") rather than inventing specifics.
- Use the primary keyword and natural related terms without stuffing.
- Weave in relevant internal links where they genuinely help. Use varied anchor text —
  don't link the same page twice with identical words.
- Include at least one insight a generic AI summary would miss: a trade-off most guides
  skip, a counterintuitive finding, a common mistake that costs money.
- At least 3 internal links per post when candidates are available.

OUTPUT EXACTLY THIS FORMAT, NOTHING ELSE:
---
title: "<specific, <60 chars, keyword natural, NOT a formula>"
slug: "<url-safe-lowercase-hyphenated>"
description: "<120-160 char meta description that earns the click>"
author: "{{AUTHOR}}"
category: "<best fit from {{CATEGORY_LIST}}>"
tags: ["<3-6 tags>"]
date: "{{PUBLISH_DATE}}"
hero_image_prompt: "<one-sentence header image description>"
faq:
  - q: "<question>"
    a: "<1-3 sentence answer with at least one specific detail>"
---

<full Markdown body, starting with the intro — do NOT repeat the H1; Astro renders it>
```

---

## 7. QUALITY GUARDRAILS (these protect the monetization)

The whole business model dies if the content gets hit by a core update. Enforce:
- **Human review gate.** The Publisher parks new posts for review (`status: review`) before
  they go live; only a human flip to `ready`/`published` publishes. Never full auto-publish raw.
- **Steady cadence.** Never exceed `PUBLISH_CADENCE_PER_DAY`. Publishing-velocity spikes are
  a scaled-content-abuse flag. Ramp gradually.
- **Depth over volume.** Ship complete clusters (pillar + supporting), interlinked. Topical
  authority comes from going deep, not wide.
- **E-E-A-T surfaces.** Real author profiles with bios, bylines linking to author pages,
  Person + Organization schema, About/Contact present.
- **No fabrication.** No invented stats, studies, prices, or quotes anywhere.
- **Fingerprint variance.** Rotate structure, openings, and formats across posts.

---

## 8. MONETIZATION SETUP DETAIL

- **AdSense:** needs the legal pages, clean nav, and a real content base to get approved.
  Start with AdSense (no traffic minimum), graduate to Ezoic, then Mediavine/Raptive as
  traffic scales. Keep ad density reasonable — UX affects rankings.
- **Guest posting (your editorial-placement revenue):** the Write-for-Us page + author bio
  dofollow slot are the product. Buyers are abundant in home-services, but they only pay
  once the site has some domain authority and real traffic — so build traffic first.

---

## 9. REPO CONVENTIONS

- All niche-specific values live in `site.config.ts` only.
- Posts: `src/content/blog/<slug>.md`. Authors: `src/content/authors/<id>.md`.
- Keep components niche-agnostic; never hardcode niche text in templates.
- Commit messages from the Publisher: `post: <slug>`.

---

## 10. DEFINITION OF DONE

- [ ] `content-map.csv` produced from real DataForSEO data; first cluster marked `ready`.
- [ ] Astro site builds clean; all page types render.
- [ ] `site.config.ts` holds 100% of niche-specific values (clone test: changing it + niche is enough).
- [ ] JSON-LD validates (Article, Breadcrumb, FAQ, Organization, Person).
- [ ] Sitemap, RSS, robots.txt, ads.txt present; legal pages present.
- [ ] AdSense slots + author bio dofollow slot + Write-for-Us page in place.
- [ ] Google Sheet created and seeded with the content map.
- [ ] n8n Planner + Publisher workflows built, tested with one row, and writing status back.
- [ ] Review gate enforced; cadence ceiling respected.
- [ ] First cluster published; internal links resolve; Lighthouse green; Search Console ready.
```
