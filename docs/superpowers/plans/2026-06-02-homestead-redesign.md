# The Homestead Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the Miter House blog from a generic Bootstrap-era design into a warm, editorial, magazine-style experience ("The Homestead") with zero JavaScript.

**Architecture:** Full CSS rewrite with new earthy color palette (forest green / linen / terracotta), Playfair Display + Inter typography, image-forward post cards, sticky header with CSS-only mobile hamburger, 6-section home page, post pages with full-bleed hero header and auto-generated table of contents. All interactions (hamburger, accordions, ToC collapse) are CSS-only. No JS frameworks.

**Tech Stack:** Astro 5, pure CSS (custom properties), Google Fonts (Playfair Display, Inter), HTML `<details>`/`<summary>` for accordions.

**Spec:** `docs/superpowers/specs/2026-06-02-homestead-redesign-design.md`

---

## File Map

### Modified files
- `site.config.ts` — Update colors, add `categoryDescriptions`, `categoryGradients`
- `src/styles/global.css` — Full rewrite: new palette, typography, all component/section styles
- `src/layouts/BaseLayout.astro` — Add Google Fonts `<link>`, update structure
- `src/layouts/PostLayout.astro` — Rewrite: full-bleed hero header, overlapping content card, ToC, accordion FAQ
- `src/components/Header.astro` — Rewrite: sticky, backdrop-blur, CSS-only mobile hamburger
- `src/components/Footer.astro` — Rewrite: 3-column, forest green inverted palette
- `src/components/PostCard.astro` — Rewrite: image card with gradient fallback, hover lift
- `src/components/AuthorBio.astro` — Restyle: larger avatar, linen background, 12px radius
- `src/components/AdSlot.astro` — Restyle: linen treatment, "Advertisement" label
- `src/components/Breadcrumbs.astro` — Restyle: updated colors
- `src/components/SEO.astro` — Add Google Fonts preconnect
- `src/pages/index.astro` — Rewrite: 6-section home page
- `src/pages/blog/index.astro` — Update classes for new design
- `src/pages/category/[category].astro` — Add banner stripe, post count, description
- `src/pages/tag/[tag].astro` — Update classes
- `src/pages/author/[author].astro` — Restyle: centered, larger avatar, linen card
- `src/pages/about.astro` — Add CTA to Write for Us
- `src/pages/write-for-us.astro` — Landing page feel, terracotta CTA button
- `src/pages/search.astro` — Update input styles, focus ring
- `src/pages/contact.astro` — Linen card treatment
- `src/pages/404.astro` — Serif heading, styled links
- `src/pages/privacy-policy.astro` — No changes needed (uses `.prose`)
- `src/pages/terms.astro` — No changes needed
- `src/pages/disclosure.astro` — No changes needed

### New files
- `src/components/TableOfContents.astro` — Auto-generated from headings, CSS-only collapsible
- `src/components/HeroBanner.astro` — Full-width featured post hero
- `src/components/CategoryShowcase.astro` — Home page category cards section
- `src/components/EditorPicks.astro` — Numbered compact post row
- `src/components/NewsletterTeaser.astro` — CTA banner section
- `src/components/SectionHeading.astro` — Reusable small-caps section label
- `src/utils/category-gradients.ts` — Category-to-gradient mapping utility

---

## Task 1: Update site.config.ts and create category utilities

**Files:**
- Modify: `site.config.ts`
- Create: `src/utils/category-gradients.ts`

- [ ] **Step 1: Update site.config.ts colors**

```ts
// In site.config.ts, replace the colors block:
colors: {
  primary: "#2D4A3E",
  primaryLight: "#3D6B5A",
  accent: "#C1694F",
  accentLight: "#D4896F",
  background: "#FAF6F1",
  surface: "#FFFFFF",
  text: "#2C2C2C",
  heading: "#1A1A1A",
  muted: "#6B6B6B",
  border: "#E8E0D8",
},
```

Also add `categoryDescriptions` after the `categories` array:

```ts
categoryDescriptions: {
  "Kitchen & Bath Remodeling": "Real costs and step-by-step guides for your next kitchen or bathroom project.",
  "Flooring & Tile": "From subfloor prep to grout — practical flooring guides for every room.",
  "Painting & Walls": "Techniques, product picks, and honest advice for interior and exterior painting.",
  "Outdoor & Landscaping": "Decks, patios, gardens, and curb appeal projects you can tackle yourself.",
  "Plumbing & Electrical": "Know when to DIY and when to call a pro — plus the basics you can handle.",
  "Basement & Attic": "Finishing, waterproofing, insulation, and making unused space livable.",
  "Tools & Materials": "Honest reviews and comparisons of the tools and materials that matter.",
  "Budget & Planning": "Cost breakdowns, project planning, and how to get the most from your budget.",
} as Record<string, string>,
```

- [ ] **Step 2: Create category gradient utility**

Create `src/utils/category-gradients.ts`:

```ts
const categoryGradients: Record<string, string> = {
  "Kitchen & Bath Remodeling": "linear-gradient(135deg, #5B7B6A 0%, #C1694F 100%)",
  "Flooring & Tile": "linear-gradient(135deg, #8B7355 0%, #C4A882 100%)",
  "Painting & Walls": "linear-gradient(135deg, #7A8B6E 0%, #D4896F 100%)",
  "Outdoor & Landscaping": "linear-gradient(135deg, #2D4A3E 0%, #5B7B6A 100%)",
  "Plumbing & Electrical": "linear-gradient(135deg, #4A6670 0%, #8BA5A0 100%)",
  "Basement & Attic": "linear-gradient(135deg, #6B5B4E 0%, #A89080 100%)",
  "Tools & Materials": "linear-gradient(135deg, #5A5A5A 0%, #8B7355 100%)",
  "Budget & Planning": "linear-gradient(135deg, #C1694F 0%, #D4896F 100%)",
};

export function getCategoryGradient(category: string): string {
  return categoryGradients[category] || "linear-gradient(135deg, #2D4A3E 0%, #C1694F 100%)";
}

export function getCategoryColor(category: string): string {
  const colors: Record<string, string> = {
    "Kitchen & Bath Remodeling": "#5B7B6A",
    "Flooring & Tile": "#8B7355",
    "Painting & Walls": "#7A8B6E",
    "Outdoor & Landscaping": "#2D4A3E",
    "Plumbing & Electrical": "#4A6670",
    "Basement & Attic": "#6B5B4E",
    "Tools & Materials": "#5A5A5A",
    "Budget & Planning": "#C1694F",
  };
  return colors[category] || "#2D4A3E";
}
```

- [ ] **Step 3: Verify the build still passes**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds (colors are just config data, gradients are unused yet).

- [ ] **Step 4: Commit**

```bash
git add site.config.ts src/utils/category-gradients.ts
git commit -m "feat: update color palette and add category gradient utility"
```

---

## Task 2: Rewrite global.css — foundation layer

This is the largest single file change. The entire CSS is replaced.

**Files:**
- Modify: `src/styles/global.css`

- [ ] **Step 1: Replace the entire contents of global.css**

```css
/* ── Reset ─────────────────────────────────────────────────── */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --color-primary: #2D4A3E;
  --color-primary-light: #3D6B5A;
  --color-accent: #C1694F;
  --color-accent-light: #D4896F;
  --color-bg: #FAF6F1;
  --color-surface: #FFFFFF;
  --color-text: #2C2C2C;
  --color-heading: #1A1A1A;
  --color-muted: #6B6B6B;
  --color-border: #E8E0D8;
  --font-serif: "Playfair Display", Georgia, serif;
  --font-sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --max-width: 1200px;
  --content-width: 720px;
  --radius: 12px;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 30px rgba(0, 0, 0, 0.1);
}

html {
  font-family: var(--font-sans);
  font-size: 106.25%; /* 17px base */
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.8;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  scroll-behavior: smooth;
}

body {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.2s;
}
a:hover {
  color: var(--color-primary-light);
}

/* ── Typography ────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-serif);
  line-height: 1.25;
  font-weight: 700;
  color: var(--color-heading);
}
h1 { font-size: 2.75rem; margin-bottom: 0.75rem; }
h2 { font-size: 1.75rem; margin-top: 2.5rem; margin-bottom: 0.75rem; }
h3 { font-size: 1.35rem; margin-top: 2rem; margin-bottom: 0.5rem; }

/* ── Layout helpers ────────────────────────────────────────── */
.container {
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 1.5rem;
}

.content-column {
  max-width: var(--content-width);
  margin: 0 auto;
}

/* ── Section heading (small caps, tracked) ─────────────────── */
.section-heading {
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-muted);
  margin-bottom: 1.75rem;
}

/* ── Prose (markdown content) ──────────────────────────────── */
.prose {
  font-size: 1rem;
  line-height: 1.8;
}
.prose p {
  margin-bottom: 1.5rem;
}
.prose ul, .prose ol {
  margin-bottom: 1.5rem;
  padding-left: 1.5rem;
}
.prose li {
  margin-bottom: 0.4rem;
}
.prose li::marker {
  color: var(--color-accent);
}
.prose h2, .prose h3 {
  font-family: var(--font-serif);
}
.prose h2 {
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}
.prose blockquote {
  border-left: 4px solid var(--color-accent);
  padding: 1rem 1.25rem;
  margin: 2rem 0;
  background: var(--color-bg);
  color: var(--color-muted);
  border-radius: 0 var(--radius) var(--radius) 0;
  font-style: italic;
}
.prose table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  border-radius: var(--radius);
  overflow: hidden;
}
.prose th, .prose td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}
.prose th {
  background: var(--color-primary);
  color: var(--color-surface);
  font-weight: 600;
  font-size: 0.9rem;
}
.prose tr:nth-child(even) td {
  background: var(--color-bg);
}
.prose code {
  background: var(--color-bg);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-size: 0.88em;
  color: var(--color-accent);
}
.prose pre {
  background: var(--color-heading);
  color: #e8e0d8;
  padding: 1.25rem;
  border-radius: var(--radius);
  overflow-x: auto;
  margin: 2rem 0;
}
.prose pre code {
  background: none;
  padding: 0;
  color: inherit;
}
.prose a {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-color: var(--color-border);
  transition: text-decoration-color 0.2s;
}
.prose a:hover {
  text-decoration-color: var(--color-primary);
}
.prose strong {
  color: var(--color-heading);
}

/* ── Post card grid ────────────────────────────────────────── */
.post-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.post-card {
  background: var(--color-surface);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.post-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
.post-card__image {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}
.post-card__image img,
.post-card__image-placeholder {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.post-card__image-placeholder {
  display: flex;
  align-items: flex-end;
  padding: 1rem;
}
.post-card__body {
  padding: 1.25rem 1.5rem 1.5rem;
}
.post-card__category {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-accent);
}
.post-card__category a {
  color: var(--color-accent);
}
.post-card__category a:hover {
  color: var(--color-accent-light);
}
.post-card__title {
  font-family: var(--font-serif);
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1.35;
  margin: 0.5rem 0 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.post-card__title a {
  color: var(--color-heading);
}
.post-card__title a:hover {
  color: var(--color-primary);
  text-decoration: none;
}
.post-card__meta {
  font-size: 0.82rem;
  color: var(--color-muted);
}
.post-card__excerpt {
  font-size: 0.9rem;
  color: var(--color-muted);
  margin-top: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.6;
}

/* ── Hero banner ───────────────────────────────────────────── */
.hero-banner {
  position: relative;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  height: 60vh;
  min-height: 400px;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
}
.hero-banner__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hero-banner__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 30%, rgba(0, 0, 0, 0.65) 100%);
}
.hero-banner__content {
  position: relative;
  z-index: 1;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2rem 1.5rem 2.5rem;
  width: 100%;
  color: #fff;
}
.hero-banner__pill {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: var(--color-accent);
  color: #fff;
  padding: 0.3rem 0.75rem;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}
.hero-banner__title {
  font-family: var(--font-serif);
  font-size: 2.75rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.15;
  max-width: 700px;
  margin-bottom: 0.75rem;
}
.hero-banner__meta {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.85);
}
.hero-banner a {
  color: inherit;
}
.hero-banner a:hover {
  color: inherit;
}

/* ── Category showcase ─────────────────────────────────────── */
.category-showcase {
  background: var(--color-bg);
  padding: 4rem 0;
}
.category-showcase__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}
.category-card {
  background: var(--color-surface);
  border-radius: var(--radius);
  padding: 1.75rem 2rem;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
  border-left: 4px solid var(--color-accent);
}
.category-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  text-decoration: none;
}
.category-card__name {
  font-family: var(--font-serif);
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.35rem;
}
.category-card__desc {
  font-size: 0.88rem;
  color: var(--color-muted);
  line-height: 1.5;
}
.category-card__count {
  font-size: 0.8rem;
  color: var(--color-muted);
  margin-top: 0.35rem;
}
.category-card__arrow {
  font-size: 1.5rem;
  color: var(--color-accent);
  flex-shrink: 0;
}

/* ── Editor picks ──────────────────────────────────────────── */
.editor-picks {
  padding: 4rem 0;
}
.editor-picks__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}
.pick-card {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  text-decoration: none;
}
.pick-card:hover {
  text-decoration: none;
}
.pick-card__number {
  font-family: var(--font-serif);
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-border);
  line-height: 1;
  flex-shrink: 0;
}
.pick-card:hover .pick-card__number {
  color: var(--color-accent);
}
.pick-card__title {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-heading);
  line-height: 1.35;
  margin-bottom: 0.25rem;
}
.pick-card__meta {
  font-size: 0.82rem;
  color: var(--color-muted);
}

/* ── Newsletter teaser ─────────────────────────────────────── */
.newsletter-teaser {
  background: var(--color-primary);
  color: var(--color-bg);
  padding: 3.5rem 0;
  text-align: center;
}
.newsletter-teaser__title {
  font-family: var(--font-serif);
  font-size: 1.75rem;
  color: var(--color-bg);
  margin-bottom: 0.75rem;
}
.newsletter-teaser__desc {
  font-size: 1rem;
  color: rgba(250, 246, 241, 0.85);
  max-width: 500px;
  margin: 0 auto 1.5rem;
}
.newsletter-teaser__form {
  display: flex;
  gap: 0.5rem;
  max-width: 420px;
  margin: 0 auto;
}
.newsletter-teaser__input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid rgba(250, 246, 241, 0.3);
  border-radius: 8px;
  background: rgba(250, 246, 241, 0.1);
  color: var(--color-bg);
  font-family: var(--font-sans);
  font-size: 0.95rem;
}
.newsletter-teaser__input::placeholder {
  color: rgba(250, 246, 241, 0.5);
}
.newsletter-teaser__input:focus {
  outline: none;
  border-color: var(--color-accent);
}
.newsletter-teaser__link {
  display: inline-block;
  background: var(--color-accent);
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background 0.2s;
  text-decoration: none;
}
.newsletter-teaser__link:hover {
  background: var(--color-accent-light);
  color: #fff;
}

/* ── Author bio box ────────────────────────────────────────── */
.author-bio {
  display: flex;
  gap: 1.25rem;
  padding: 1.75rem;
  background: var(--color-bg);
  border-radius: var(--radius);
  margin: 2.5rem 0;
}
.author-bio__avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}
.author-bio__name {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--color-heading);
}
.author-bio__name a {
  color: var(--color-heading);
}
.author-bio__name a:hover {
  color: var(--color-primary);
}
.author-bio__text {
  font-size: 0.9rem;
  color: var(--color-muted);
  margin-top: 0.35rem;
  line-height: 1.6;
}

/* ── FAQ section ───────────────────────────────────────────── */
.faq-list {
  margin: 2.5rem 0;
}
.faq-item {
  border-bottom: 1px solid var(--color-border);
}
.faq-item summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 1rem 0;
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--color-primary);
  list-style: none;
}
.faq-item summary::-webkit-details-marker {
  display: none;
}
.faq-item summary::after {
  content: "+";
  font-size: 1.3rem;
  color: var(--color-accent);
  font-weight: 400;
  transition: transform 0.2s;
  flex-shrink: 0;
  margin-left: 1rem;
}
.faq-item[open] summary::after {
  content: "−";
}
.faq-item__answer {
  padding: 0 0 1rem;
  color: var(--color-muted);
  font-size: 0.95rem;
  line-height: 1.7;
}

/* ── Ad slot ───────────────────────────────────────────────── */
.ad-slot {
  text-align: center;
  margin: 2rem 0;
  padding: 1.25rem;
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
  font-size: 0.7rem;
  color: var(--color-muted);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ── Breadcrumbs ───────────────────────────────────────────── */
.breadcrumbs {
  font-size: 0.82rem;
  color: var(--color-muted);
  margin-bottom: 1.25rem;
}
.breadcrumbs a {
  color: var(--color-muted);
  transition: color 0.2s;
}
.breadcrumbs a:hover {
  color: var(--color-primary);
}
.breadcrumbs__sep {
  margin: 0 0.4rem;
  color: var(--color-border);
}

/* ── Tags ──────────────────────────────────────────────────── */
.tag {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: 0.8rem;
  background: var(--color-bg);
  color: var(--color-primary);
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  margin: 0.2rem;
  transition: all 0.2s;
}
.tag:hover {
  background: var(--color-accent);
  color: #fff;
  text-decoration: none;
}

/* ── Table of contents ─────────────────────────────────────── */
.toc {
  background: var(--color-bg);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
}
.toc summary {
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-muted);
  cursor: pointer;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.toc summary::-webkit-details-marker {
  display: none;
}
.toc summary::after {
  content: "▾";
  transition: transform 0.2s;
}
.toc[open] summary::after {
  transform: rotate(180deg);
}
.toc__list {
  list-style: none;
  margin-top: 0.75rem;
  padding-left: 1rem;
  border-left: 2px solid var(--color-border);
}
.toc__list li {
  margin-bottom: 0.4rem;
}
.toc__list a {
  font-size: 0.9rem;
  color: var(--color-primary);
  text-decoration: none;
}
.toc__list a:hover {
  color: var(--color-accent);
}

/* ── Post hero (full-bleed on post pages) ──────────────────── */
.post-hero {
  position: relative;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  height: 35vh;
  min-height: 280px;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
}
.post-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.post-hero__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 20%, rgba(0, 0, 0, 0.6) 100%);
}
.post-hero__content {
  position: relative;
  z-index: 1;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2rem 1.5rem;
  width: 100%;
  color: #fff;
}
.post-hero__pill {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: var(--color-accent);
  color: #fff;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  margin-bottom: 0.6rem;
}
.post-hero__title {
  font-family: var(--font-serif);
  font-size: 2.25rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.2;
  max-width: 650px;
  margin-bottom: 0.5rem;
}
.post-hero__meta {
  font-size: 0.88rem;
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.post-hero__avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

/* ── Post content card (overlapping hero) ──────────────────── */
.post-content-card {
  background: var(--color-surface);
  max-width: var(--content-width);
  margin: -3rem auto 0;
  padding: 2.5rem 2.5rem 2rem;
  border-radius: var(--radius) var(--radius) 0 0;
  position: relative;
  z-index: 2;
  box-shadow: var(--shadow-md);
}

/* ── Site header ───────────────────────────────────────────── */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(250, 246, 241, 0.92);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  padding: 0;
}
.site-header__inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0.85rem 1.5rem;
}
.site-header__logo {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
  text-decoration: none;
}
.site-header__logo:hover {
  color: var(--color-primary-light);
  text-decoration: none;
}
.site-nav {
  display: flex;
  gap: 1.75rem;
  list-style: none;
  align-items: center;
}
.site-nav a {
  font-family: var(--font-sans);
  font-size: 0.9rem;
  color: var(--color-primary);
  font-weight: 500;
  text-decoration: none;
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}
.site-nav a:hover,
.site-nav a[aria-current="page"] {
  color: var(--color-accent);
  border-bottom-color: var(--color-accent);
  text-decoration: none;
}

/* Hamburger (CSS-only) */
.hamburger-toggle {
  display: none;
}
.hamburger-label {
  display: none;
  cursor: pointer;
  width: 28px;
  height: 20px;
  position: relative;
  z-index: 101;
}
.hamburger-label span,
.hamburger-label span::before,
.hamburger-label span::after {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--color-primary);
  border-radius: 2px;
  position: absolute;
  transition: all 0.3s;
}
.hamburger-label span {
  top: 9px;
}
.hamburger-label span::before {
  content: "";
  top: -7px;
}
.hamburger-label span::after {
  content: "";
  top: 7px;
}
.hamburger-toggle:checked + .hamburger-label span {
  background: transparent;
}
.hamburger-toggle:checked + .hamburger-label span::before {
  top: 0;
  transform: rotate(45deg);
}
.hamburger-toggle:checked + .hamburger-label span::after {
  top: 0;
  transform: rotate(-45deg);
}
.mobile-nav {
  display: none;
}
.hamburger-toggle:checked ~ .mobile-nav {
  display: block;
}

/* ── Footer ────────────────────────────────────────────────── */
.site-footer {
  margin-top: auto;
  background: var(--color-primary);
  color: var(--color-bg);
  padding: 3.5rem 0 0;
}
.site-footer a {
  color: rgba(250, 246, 241, 0.75);
  transition: color 0.2s;
}
.site-footer a:hover {
  color: #fff;
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 3rem;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 1.5rem;
}
.footer-brand__name {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
}
.footer-brand__tagline {
  font-size: 0.9rem;
  color: rgba(250, 246, 241, 0.7);
  line-height: 1.5;
  max-width: 300px;
}
.footer-col__title {
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(250, 246, 241, 0.5);
  margin-bottom: 1rem;
}
.footer-col__list {
  list-style: none;
}
.footer-col__list li {
  margin-bottom: 0.5rem;
}
.footer-col__list a {
  font-size: 0.9rem;
}
.footer-bottom {
  border-top: 1px solid rgba(250, 246, 241, 0.15);
  margin-top: 2.5rem;
  padding: 1.25rem 1.5rem;
  max-width: var(--max-width);
  margin-left: auto;
  margin-right: auto;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.8rem;
  color: rgba(250, 246, 241, 0.5);
}
.footer-bottom__links {
  display: flex;
  gap: 1rem;
  list-style: none;
}
.footer-bottom__links a {
  font-size: 0.8rem;
  color: rgba(250, 246, 241, 0.5);
}
.footer-bottom__links a:hover {
  color: #fff;
}

/* ── Page header (archives, etc.) ──────────────────────────── */
.page-header {
  padding: 3rem 0 2rem;
  text-align: center;
}
.page-header__title {
  font-family: var(--font-serif);
  font-size: 2.25rem;
}
.page-header__desc {
  color: var(--color-muted);
  margin-top: 0.5rem;
  max-width: 550px;
  margin-left: auto;
  margin-right: auto;
}
.page-header__count {
  font-size: 0.85rem;
  color: var(--color-muted);
  margin-top: 0.35rem;
}

/* ── Category banner stripe ────────────────────────────────── */
.category-banner {
  height: 6px;
  border-radius: 3px;
  max-width: 80px;
  margin: 0.75rem auto 0;
}

/* ── Author profile ────────────────────────────────────────── */
.author-profile {
  text-align: center;
  padding: 3rem 0 2rem;
}
.author-profile__avatar {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto 1rem;
  box-shadow: var(--shadow-md);
}
.author-profile__name {
  font-family: var(--font-serif);
  font-size: 2rem;
  margin-bottom: 0.75rem;
}
.author-profile__bio {
  max-width: 600px;
  margin: 0 auto;
  color: var(--color-muted);
  line-height: 1.7;
  background: var(--color-bg);
  padding: 1.5rem 2rem;
  border-radius: var(--radius);
}

/* ── Buttons ───────────────────────────────────────────────── */
.btn {
  display: inline-block;
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 0.95rem;
  padding: 0.8rem 1.75rem;
  border-radius: 8px;
  transition: all 0.2s;
  text-decoration: none;
  cursor: pointer;
  border: none;
}
.btn--accent {
  background: var(--color-accent);
  color: #fff;
}
.btn--accent:hover {
  background: var(--color-accent-light);
  color: #fff;
  text-decoration: none;
}
.btn--outline {
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-border);
}
.btn--outline:hover {
  border-color: var(--color-primary);
  text-decoration: none;
}

/* ── View all link ─────────────────────────────────────────── */
.view-all {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 600;
  color: var(--color-accent);
  font-size: 0.95rem;
  margin-top: 2rem;
}
.view-all:hover {
  color: var(--color-accent-light);
  text-decoration: none;
}

/* ── Search input ──────────────────────────────────────────── */
.search-input {
  width: 100%;
  padding: 0.85rem 1.25rem;
  font-family: var(--font-sans);
  font-size: 1rem;
  border: 2px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-surface);
  color: var(--color-text);
  transition: border-color 0.2s;
  margin: 1rem 0;
}
.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

/* ── 404 page ──────────────────────────────────────────────── */
.page-404 {
  text-align: center;
  padding: 5rem 0;
}
.page-404__code {
  font-family: var(--font-serif);
  font-size: 6rem;
  font-weight: 700;
  color: var(--color-border);
  line-height: 1;
  margin-bottom: 1rem;
}
.page-404__message {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  color: var(--color-heading);
  margin-bottom: 1rem;
}
.page-404__links {
  color: var(--color-muted);
}
.page-404__links a {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 3px;
}

/* ── Content page card (contact, about, etc.) ──────────────── */
.content-card {
  background: var(--color-surface);
  padding: 2.5rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
}

/* ── Write for us CTA ──────────────────────────────────────── */
.cta-box {
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: var(--radius);
  padding: 2rem;
  text-align: center;
  margin: 2.5rem 0;
}
.cta-box__title {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}
.cta-box__desc {
  color: var(--color-muted);
  margin-bottom: 1.25rem;
}

/* ── Home page sections spacing ────────────────────────────── */
.home-section {
  padding: 4rem 0;
}
.home-section--surface {
  background: var(--color-surface);
}
.home-section__center {
  text-align: center;
  margin-top: 2rem;
}

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .post-grid { grid-template-columns: repeat(2, 1fr); }
  .editor-picks__grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 768px) {
  h1 { font-size: 2rem; }
  h2 { font-size: 1.5rem; }

  .hero-banner {
    height: 40vh;
    min-height: 300px;
  }
  .hero-banner__title {
    font-size: 1.75rem;
  }

  .post-hero {
    height: 30vh;
    min-height: 240px;
  }
  .post-hero__title {
    font-size: 1.6rem;
  }
  .post-content-card {
    padding: 1.5rem 1.25rem 1.5rem;
    margin-top: -2rem;
  }

  .post-grid { grid-template-columns: 1fr; }
  .category-showcase__grid { grid-template-columns: 1fr; }
  .editor-picks__grid { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr; gap: 2rem; }

  /* Mobile nav */
  .site-nav { display: none; }
  .hamburger-label { display: block; }
  .mobile-nav {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--color-bg);
    padding: 1rem 1.5rem 1.5rem;
    box-shadow: var(--shadow-md);
  }
  .mobile-nav ul {
    list-style: none;
  }
  .mobile-nav li {
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--color-border);
  }
  .mobile-nav a {
    font-size: 1rem;
    color: var(--color-primary);
    font-weight: 500;
  }

  .newsletter-teaser__form {
    flex-direction: column;
  }

  .author-bio {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }

  .pick-card__number {
    font-size: 2.25rem;
  }

  .home-section {
    padding: 2.5rem 0;
  }
}

@media (max-width: 480px) {
  .site-header__inner {
    padding: 0.75rem 1rem;
  }
  .container {
    padding: 0 1rem;
  }
  .hero-banner__title {
    font-size: 1.5rem;
  }
  .post-content-card {
    padding: 1.25rem 1rem;
    border-radius: 8px 8px 0 0;
  }
}
```

- [ ] **Step 2: Verify the build still passes**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds. Pages still render (class names changed but templates haven't been updated yet — visual will be off until templates are updated).

- [ ] **Step 3: Commit**

```bash
git add src/styles/global.css
git commit -m "feat: rewrite global.css with Homestead design system"
```

---

## Task 3: Update BaseLayout and SEO with Google Fonts

**Files:**
- Modify: `src/layouts/BaseLayout.astro`
- Modify: `src/components/SEO.astro`

- [ ] **Step 1: Update SEO.astro to add Google Fonts preconnect**

Add after the existing `<link rel="sitemap" ...>` line at the end:

```astro
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet" />
```

- [ ] **Step 2: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/components/SEO.astro
git commit -m "feat: add Google Fonts preconnect and stylesheet links"
```

---

## Task 4: Rewrite Header with sticky nav and CSS-only hamburger

**Files:**
- Modify: `src/components/Header.astro`

- [ ] **Step 1: Replace the entire contents of Header.astro**

```astro
---
import { siteConfig } from "../../site.config";

const currentPath = Astro.url.pathname;
---

<header class="site-header">
  <div class="site-header__inner">
    <a href="/" class="site-header__logo">{siteConfig.name}</a>

    <nav>
      <ul class="site-nav">
        {siteConfig.nav.map((item) => (
          <li>
            <a
              href={item.href}
              aria-current={currentPath === item.href || currentPath.startsWith(item.href + "/") ? "page" : undefined}
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>

    <input type="checkbox" id="hamburger-toggle" class="hamburger-toggle" aria-hidden="true" />
    <label for="hamburger-toggle" class="hamburger-label" aria-label="Toggle menu">
      <span></span>
    </label>

    <div class="mobile-nav">
      <ul>
        {siteConfig.nav.map((item) => (
          <li>
            <a
              href={item.href}
              aria-current={currentPath === item.href || currentPath.startsWith(item.href + "/") ? "page" : undefined}
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  </div>
</header>
```

- [ ] **Step 2: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/components/Header.astro
git commit -m "feat: rewrite Header with sticky nav and CSS-only hamburger"
```

---

## Task 5: Rewrite Footer with 3-column inverted layout

**Files:**
- Modify: `src/components/Footer.astro`

- [ ] **Step 1: Replace the entire contents of Footer.astro**

```astro
---
import { siteConfig } from "../../site.config";
const year = new Date().getFullYear();
const topCategories = siteConfig.categories.slice(0, 5);
---

<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <p class="footer-brand__name">{siteConfig.name}</p>
      <p class="footer-brand__tagline">{siteConfig.tagline}</p>
    </div>

    <div>
      <p class="footer-col__title">Quick Links</p>
      <ul class="footer-col__list">
        {siteConfig.nav.map((item) => (
          <li><a href={item.href}>{item.label}</a></li>
        ))}
        <li><a href="/search/">Search</a></li>
      </ul>
    </div>

    <div>
      <p class="footer-col__title">Categories</p>
      <ul class="footer-col__list">
        {topCategories.map((cat) => (
          <li>
            <a href={`/category/${cat.toLowerCase().replace(/[&\s]+/g, "-").replace(/-+/g, "-")}/`}>
              {cat}
            </a>
          </li>
        ))}
      </ul>
    </div>
  </div>

  <div class="footer-bottom">
    <p>&copy; {year} {siteConfig.name}. All rights reserved.</p>
    <ul class="footer-bottom__links">
      <li><a href="/privacy-policy/">Privacy Policy</a></li>
      <li><a href="/terms/">Terms</a></li>
      <li><a href="/disclosure/">Disclosure</a></li>
    </ul>
  </div>
</footer>
```

- [ ] **Step 2: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/components/Footer.astro
git commit -m "feat: rewrite Footer with 3-column inverted layout"
```

---

## Task 6: Create new shared components (SectionHeading)

**Files:**
- Create: `src/components/SectionHeading.astro`

- [ ] **Step 1: Create SectionHeading.astro**

```astro
---
interface Props {
  text: string;
}
const { text } = Astro.props;
---

<h2 class="section-heading">{text}</h2>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/SectionHeading.astro
git commit -m "feat: add SectionHeading component"
```

---

## Task 7: Rewrite PostCard with image and gradient fallback

**Files:**
- Modify: `src/components/PostCard.astro`

- [ ] **Step 1: Replace the entire contents of PostCard.astro**

```astro
---
import { getCategoryGradient } from "../utils/category-gradients";

interface Props {
  title: string;
  slug: string;
  description: string;
  category: string;
  date: Date;
  author: string;
  heroImage?: string;
}
const { title, slug, description, category, date, author, heroImage } = Astro.props;
const dateStr = date.toLocaleDateString("en-US", {
  year: "numeric",
  month: "short",
  day: "numeric",
});
const categorySlug = category.toLowerCase().replace(/[&\s]+/g, "-").replace(/-+/g, "-");
const gradient = getCategoryGradient(category);
---

<article class="post-card">
  <div class="post-card__image">
    {heroImage ? (
      <img src={heroImage} alt={title} loading="lazy" width="400" height="225" />
    ) : (
      <div class="post-card__image-placeholder" style={`background: ${gradient};`}></div>
    )}
  </div>
  <div class="post-card__body">
    <span class="post-card__category">
      <a href={`/category/${categorySlug}/`}>{category}</a>
    </span>
    <h2 class="post-card__title">
      <a href={`/blog/${slug}/`}>{title}</a>
    </h2>
    <p class="post-card__meta">
      <time datetime={date.toISOString()}>{dateStr}</time> &middot; {author}
    </p>
    <p class="post-card__excerpt">{description}</p>
  </div>
</article>
```

- [ ] **Step 2: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/components/PostCard.astro
git commit -m "feat: rewrite PostCard with image and gradient fallback"
```

---

## Task 8: Create HeroBanner component

**Files:**
- Create: `src/components/HeroBanner.astro`

- [ ] **Step 1: Create HeroBanner.astro**

```astro
---
import { getCategoryGradient } from "../utils/category-gradients";

interface Props {
  title: string;
  slug: string;
  category: string;
  date: Date;
  heroImage?: string;
}
const { title, slug, category, date, heroImage } = Astro.props;
const dateStr = date.toLocaleDateString("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
});
const categorySlug = category.toLowerCase().replace(/[&\s]+/g, "-").replace(/-+/g, "-");
const gradient = getCategoryGradient(category);
---

<a href={`/blog/${slug}/`} class="hero-banner" style={!heroImage ? `background: ${gradient};` : undefined}>
  {heroImage && <img src={heroImage} alt={title} class="hero-banner__bg" />}
  <div class="hero-banner__overlay"></div>
  <div class="hero-banner__content">
    <span class="hero-banner__pill">
      {category}
    </span>
    <h1 class="hero-banner__title">{title}</h1>
    <p class="hero-banner__meta">
      <time datetime={date.toISOString()}>{dateStr}</time>
    </p>
  </div>
</a>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/HeroBanner.astro
git commit -m "feat: add HeroBanner component"
```

---

## Task 9: Create CategoryShowcase component

**Files:**
- Create: `src/components/CategoryShowcase.astro`

- [ ] **Step 1: Create CategoryShowcase.astro**

```astro
---
import SectionHeading from "./SectionHeading.astro";
import { siteConfig } from "../../site.config";
import { getCollection } from "astro:content";

const allPosts = await getCollection("blog", ({ data }) => !data.draft);

const categoriesToShow = siteConfig.categories.slice(0, 4);

const categoryData = categoriesToShow.map((cat) => {
  const count = allPosts.filter((p) => p.data.category === cat).length;
  const slug = cat.toLowerCase().replace(/[&\s]+/g, "-").replace(/-+/g, "-");
  const description = (siteConfig as any).categoryDescriptions?.[cat] || "";
  return { name: cat, slug, count, description };
});
---

<section class="category-showcase">
  <div class="container">
    <SectionHeading text="Browse by Topic" />
    <div class="category-showcase__grid">
      {categoryData.map((cat) => (
        <a href={`/category/${cat.slug}/`} class="category-card">
          <div>
            <p class="category-card__name">{cat.name}</p>
            <p class="category-card__desc">{cat.description}</p>
            <p class="category-card__count">{cat.count} {cat.count === 1 ? "article" : "articles"}</p>
          </div>
          <span class="category-card__arrow">&rarr;</span>
        </a>
      ))}
    </div>
  </div>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/CategoryShowcase.astro
git commit -m "feat: add CategoryShowcase component"
```

---

## Task 10: Create EditorPicks component

**Files:**
- Create: `src/components/EditorPicks.astro`

- [ ] **Step 1: Create EditorPicks.astro**

```astro
---
import SectionHeading from "./SectionHeading.astro";

interface Post {
  title: string;
  slug: string;
  category: string;
  date: Date;
}
interface Props {
  posts: Post[];
}
const { posts } = Astro.props;
const picks = posts.slice(0, 3);
---

{picks.length > 0 && (
  <section class="editor-picks">
    <div class="container">
      <SectionHeading text="Editor's Picks" />
      <div class="editor-picks__grid">
        {picks.map((post, i) => (
          <a href={`/blog/${post.slug}/`} class="pick-card">
            <span class="pick-card__number">{String(i + 1).padStart(2, "0")}</span>
            <div>
              <p class="pick-card__title">{post.title}</p>
              <p class="pick-card__meta">
                <time datetime={post.date.toISOString()}>
                  {post.date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
                </time>
              </p>
            </div>
          </a>
        ))}
      </div>
    </div>
  </section>
)}
```

- [ ] **Step 2: Commit**

```bash
git add src/components/EditorPicks.astro
git commit -m "feat: add EditorPicks component"
```

---

## Task 11: Create NewsletterTeaser component

**Files:**
- Create: `src/components/NewsletterTeaser.astro`

- [ ] **Step 1: Create NewsletterTeaser.astro**

```astro
---
import { siteConfig } from "../../site.config";
---

<section class="newsletter-teaser">
  <div class="container">
    <h2 class="newsletter-teaser__title">Honest home improvement advice, no filler.</h2>
    <p class="newsletter-teaser__desc">{siteConfig.tagline}</p>
    <a href="/about/" class="newsletter-teaser__link">Read our story &rarr;</a>
  </div>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/NewsletterTeaser.astro
git commit -m "feat: add NewsletterTeaser component"
```

---

## Task 12: Create TableOfContents component

**Files:**
- Create: `src/components/TableOfContents.astro`

- [ ] **Step 1: Create TableOfContents.astro**

```astro
---
interface Heading {
  depth: number;
  slug: string;
  text: string;
}
interface Props {
  headings: Heading[];
}
const { headings } = Astro.props;
const h2s = headings.filter((h) => h.depth === 2);
---

{h2s.length > 2 && (
  <details class="toc" open>
    <summary>In This Article</summary>
    <ol class="toc__list">
      {h2s.map((h) => (
        <li><a href={`#${h.slug}`}>{h.text}</a></li>
      ))}
    </ol>
  </details>
)}
```

- [ ] **Step 2: Commit**

```bash
git add src/components/TableOfContents.astro
git commit -m "feat: add TableOfContents component"
```

---

## Task 13: Restyle AuthorBio and AdSlot components

**Files:**
- Modify: `src/components/AuthorBio.astro`
- Modify: `src/components/AdSlot.astro`

- [ ] **Step 1: Update AuthorBio.astro**

Replace the entire file:

```astro
---
import { siteConfig } from "../../site.config";

interface Props {
  authorId: string;
}
const { authorId } = Astro.props;
const author = siteConfig.authors[authorId as keyof typeof siteConfig.authors];
if (!author) return;

const hasExternalLink = author.externalUrl && author.externalUrl.length > 0;
---

<aside class="author-bio">
  <img
    src={author.avatar}
    alt={author.name}
    class="author-bio__avatar"
    width="96"
    height="96"
    loading="lazy"
  />
  <div>
    <p class="author-bio__name">
      <a href={`/author/${author.slug}/`}>{author.name}</a>
      {hasExternalLink && (
        <> &middot; <a href={author.externalUrl} rel="author">Website</a></>
      )}
    </p>
    <p class="author-bio__text">{author.bio}</p>
  </div>
</aside>
```

- [ ] **Step 2: Update AdSlot.astro**

Replace the entire file:

```astro
---
import { siteConfig } from "../../site.config";

interface Props {
  slot: "inContent" | "sidebar" | "belowHeader";
}
const { slot } = Astro.props;
const slotId = siteConfig.adsense.slots[slot];
const pubId = siteConfig.adsense.publisherId;
const isPlaceholder = pubId.includes("XXXX");
---

{isPlaceholder ? (
  <div class="ad-slot" aria-hidden="true">Advertisement</div>
) : (
  <div class="ad-slot">
    <ins
      class="adsbygoogle"
      style="display:block"
      data-ad-client={pubId}
      data-ad-slot={slotId}
      data-ad-format="auto"
      data-full-width-responsive="true"
    />
  </div>
)}
```

- [ ] **Step 3: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 4: Commit**

```bash
git add src/components/AuthorBio.astro src/components/AdSlot.astro
git commit -m "feat: restyle AuthorBio and AdSlot components"
```

---

## Task 14: Rewrite PostLayout with hero header, ToC, and accordion FAQ

**Files:**
- Modify: `src/layouts/PostLayout.astro`

- [ ] **Step 1: Replace the entire contents of PostLayout.astro**

```astro
---
import BaseLayout from "./BaseLayout.astro";
import Breadcrumbs from "../components/Breadcrumbs.astro";
import AuthorBio from "../components/AuthorBio.astro";
import TableOfContents from "../components/TableOfContents.astro";
import AdSlot from "../components/AdSlot.astro";
import JsonLd from "../components/JsonLd.astro";
import { getCategoryGradient } from "../utils/category-gradients";
import { siteConfig } from "../../site.config";

interface Props {
  title: string;
  description: string;
  author: string;
  category: string;
  tags: string[];
  date: Date;
  updated?: Date;
  faq?: { q: string; a: string }[];
  slug: string;
  headings?: { depth: number; slug: string; text: string }[];
}

const { title, description, author, category, tags, date, updated, faq, slug, headings = [] } = Astro.props;

const dateStr = date.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
const categorySlug = category.toLowerCase().replace(/[&\s]+/g, "-").replace(/-+/g, "-");

const authorId = Object.keys(siteConfig.authors).find(
  (id) => siteConfig.authors[id as keyof typeof siteConfig.authors].name === author
) || siteConfig.defaultAuthor;
const authorData = siteConfig.authors[authorId as keyof typeof siteConfig.authors];

const canonicalUrl = `${siteConfig.siteUrl}/blog/${slug}/`;
const gradient = getCategoryGradient(category);

const articleJsonLd = {
  "@context": "https://schema.org",
  "@type": "Article",
  headline: title,
  description,
  url: canonicalUrl,
  datePublished: date.toISOString(),
  ...(updated ? { dateModified: updated.toISOString() } : {}),
  author: {
    "@type": "Person",
    name: authorData.name,
    url: `${siteConfig.siteUrl}/author/${authorData.slug}/`,
  },
  publisher: {
    "@type": "Organization",
    name: siteConfig.name,
    url: siteConfig.siteUrl,
  },
};

const faqJsonLd = faq && faq.length > 0 ? {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faq.map((item) => ({
    "@type": "Question",
    name: item.q,
    acceptedAnswer: { "@type": "Answer", text: item.a },
  })),
} : null;
---

<BaseLayout title={title} description={description} ogType="article" canonical={canonicalUrl}>
  <JsonLd data={articleJsonLd} />
  {faqJsonLd && <JsonLd data={faqJsonLd} />}

  <div class="post-hero" style={`background: ${gradient};`}>
    <div class="post-hero__overlay"></div>
    <div class="post-hero__content">
      <span class="post-hero__pill">
        <a href={`/category/${categorySlug}/`}>{category}</a>
      </span>
      <h1 class="post-hero__title">{title}</h1>
      <div class="post-hero__meta">
        <img src={authorData.avatar} alt={authorData.name} class="post-hero__avatar" width="32" height="32" loading="lazy" />
        <span>
          <a href={`/author/${authorData.slug}/`}>{authorData.name}</a>
          &middot; <time datetime={date.toISOString()}>{dateStr}</time>
        </span>
      </div>
    </div>
  </div>

  <article class="post-content-card">
    <Breadcrumbs items={[
      { label: "Blog", href: "/blog/" },
      { label: category, href: `/category/${categorySlug}/` },
      { label: title },
    ]} />

    <TableOfContents headings={headings} />

    <AdSlot slot="belowHeader" />

    <div class="prose">
      <slot />
    </div>

    <AdSlot slot="inContent" />

    {faq && faq.length > 0 && (
      <section class="faq-list">
        <h2>Frequently Asked Questions</h2>
        {faq.map((item) => (
          <details class="faq-item">
            <summary>{item.q}</summary>
            <p class="faq-item__answer">{item.a}</p>
          </details>
        ))}
      </section>
    )}

    <div style="margin:2rem 0;">
      {tags.map((tag) => (
        <a class="tag" href={`/tag/${tag.toLowerCase().replace(/\s+/g, "-")}/`}>{tag}</a>
      ))}
    </div>

    <AuthorBio authorId={authorId} />
  </article>
</BaseLayout>
```

- [ ] **Step 2: Update blog/[...slug].astro to pass headings**

Replace the entire file:

```astro
---
import PostLayout from "../../layouts/PostLayout.astro";
import { getCollection, render } from "astro:content";

export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  return posts.map((post) => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content, headings } = await render(post);
---

<PostLayout
  title={post.data.title}
  description={post.data.description}
  author={post.data.author}
  category={post.data.category}
  tags={post.data.tags}
  date={post.data.date}
  updated={post.data.updated}
  faq={post.data.faq}
  slug={post.id}
  headings={headings}
>
  <Content />
</PostLayout>
```

- [ ] **Step 3: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 4: Commit**

```bash
git add src/layouts/PostLayout.astro src/pages/blog/\[...slug\].astro
git commit -m "feat: rewrite PostLayout with hero header, ToC, and accordion FAQ"
```

---

## Task 15: Rewrite index.astro with 6-section home page

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1: Replace the entire contents of index.astro**

```astro
---
import BaseLayout from "../layouts/BaseLayout.astro";
import HeroBanner from "../components/HeroBanner.astro";
import PostCard from "../components/PostCard.astro";
import CategoryShowcase from "../components/CategoryShowcase.astro";
import EditorPicks from "../components/EditorPicks.astro";
import NewsletterTeaser from "../components/NewsletterTeaser.astro";
import SectionHeading from "../components/SectionHeading.astro";
import JsonLd from "../components/JsonLd.astro";
import { getCollection } from "astro:content";
import { siteConfig } from "../../site.config";

const allPosts = await getCollection("blog", ({ data }) => !data.draft);
const posts = allPosts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

const featuredPost = posts[0];
const latestPosts = posts.slice(1, 7);
const morePosts = posts.slice(7, 13);
const editorPicks = posts.slice(0, 3).map((p) => ({
  title: p.data.title,
  slug: p.id,
  category: p.data.category,
  date: p.data.date,
}));

const webSiteJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: siteConfig.name,
  url: siteConfig.siteUrl,
  description: siteConfig.description,
};
---

<BaseLayout title={siteConfig.name} description={siteConfig.description}>
  <JsonLd data={webSiteJsonLd} />

  {/* Section 1: Hero Banner */}
  {featuredPost && (
    <HeroBanner
      title={featuredPost.data.title}
      slug={featuredPost.id}
      category={featuredPost.data.category}
      date={featuredPost.data.date}
    />
  )}

  {/* Section 2: Latest Articles */}
  {latestPosts.length > 0 && (
    <section class="home-section home-section--surface">
      <div class="container">
        <SectionHeading text="Latest Articles" />
        <div class="post-grid">
          {latestPosts.map((post) => (
            <PostCard
              title={post.data.title}
              slug={post.id}
              description={post.data.description}
              category={post.data.category}
              date={post.data.date}
              author={post.data.author}
            />
          ))}
        </div>
      </div>
    </section>
  )}

  {/* Section 3: Category Showcase */}
  <CategoryShowcase />

  {/* Section 4: Editor's Picks */}
  <EditorPicks posts={editorPicks} />

  {/* Section 5: Newsletter / About Teaser */}
  <NewsletterTeaser />

  {/* Section 6: More Articles */}
  {morePosts.length > 0 && (
    <section class="home-section home-section--surface">
      <div class="container">
        <SectionHeading text="More Articles" />
        <div class="post-grid">
          {morePosts.map((post) => (
            <PostCard
              title={post.data.title}
              slug={post.id}
              description={post.data.description}
              category={post.data.category}
              date={post.data.date}
              author={post.data.author}
            />
          ))}
        </div>
        <div class="home-section__center">
          <a href="/blog/" class="view-all">View all articles &rarr;</a>
        </div>
      </div>
    </section>
  )}
</BaseLayout>
```

- [ ] **Step 2: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: rewrite home page with 6-section editorial layout"
```

---

## Task 16: Update archive and listing pages

**Files:**
- Modify: `src/pages/blog/index.astro`
- Modify: `src/pages/category/[category].astro`
- Modify: `src/pages/tag/[tag].astro`
- Modify: `src/pages/author/[author].astro`

- [ ] **Step 1: Update blog/index.astro**

Replace the entire file:

```astro
---
import BaseLayout from "../../layouts/BaseLayout.astro";
import PostCard from "../../components/PostCard.astro";
import Breadcrumbs from "../../components/Breadcrumbs.astro";
import { getCollection } from "astro:content";
import { siteConfig } from "../../../site.config";

const allPosts = await getCollection("blog", ({ data }) => !data.draft);
const posts = allPosts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
---

<BaseLayout title="Blog" description={`All ${siteConfig.niche} articles from ${siteConfig.name}.`}>
  <Breadcrumbs items={[{ label: "Blog" }]} />

  <section class="page-header">
    <h1 class="page-header__title">All Articles</h1>
    <p class="page-header__desc">Practical {siteConfig.niche} guides — costs, steps, and honest trade-offs.</p>
  </section>

  {posts.length > 0 ? (
    <div class="post-grid">
      {posts.map((post) => (
        <PostCard
          title={post.data.title}
          slug={post.id}
          description={post.data.description}
          category={post.data.category}
          date={post.data.date}
          author={post.data.author}
        />
      ))}
    </div>
  ) : (
    <p style="color:var(--color-muted);text-align:center;padding:3rem 0;">Posts are on the way. Check back soon.</p>
  )}
</BaseLayout>
```

- [ ] **Step 2: Update category/[category].astro**

Replace the entire file:

```astro
---
import BaseLayout from "../../layouts/BaseLayout.astro";
import PostCard from "../../components/PostCard.astro";
import Breadcrumbs from "../../components/Breadcrumbs.astro";
import { getCategoryColor } from "../../utils/category-gradients";
import { getCollection } from "astro:content";
import { siteConfig } from "../../../site.config";

export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  const categories = [...new Set(posts.map((p) => p.data.category))];
  return categories.map((cat) => ({
    params: { category: cat.toLowerCase().replace(/[&\s]+/g, "-").replace(/-+/g, "-") },
    props: {
      category: cat,
      posts: posts
        .filter((p) => p.data.category === cat)
        .sort((a, b) => b.data.date.getTime() - a.data.date.getTime()),
    },
  }));
}

const { category, posts } = Astro.props;
const catColor = getCategoryColor(category);
const description = (siteConfig as any).categoryDescriptions?.[category] || `Browse all ${category.toLowerCase()} guides.`;
---

<BaseLayout
  title={`${category} Articles`}
  description={`Browse all ${category.toLowerCase()} guides on ${siteConfig.name}.`}
>
  <Breadcrumbs items={[{ label: "Blog", href: "/blog/" }, { label: category }]} />

  <section class="page-header">
    <h1 class="page-header__title">{category}</h1>
    <p class="page-header__desc">{description}</p>
    <p class="page-header__count">{posts.length} {posts.length === 1 ? "article" : "articles"}</p>
    <div class="category-banner" style={`background: ${catColor};`}></div>
  </section>

  <div class="post-grid">
    {posts.map((post: any) => (
      <PostCard
        title={post.data.title}
        slug={post.id}
        description={post.data.description}
        category={post.data.category}
        date={post.data.date}
        author={post.data.author}
      />
    ))}
  </div>
</BaseLayout>
```

- [ ] **Step 3: Update tag/[tag].astro**

Replace the entire file:

```astro
---
import BaseLayout from "../../layouts/BaseLayout.astro";
import PostCard from "../../components/PostCard.astro";
import Breadcrumbs from "../../components/Breadcrumbs.astro";
import { getCollection } from "astro:content";
import { siteConfig } from "../../../site.config";

export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  const tagMap = new Map<string, { original: string; posts: typeof posts }>();

  for (const post of posts) {
    for (const tag of post.data.tags) {
      const slug = tag.toLowerCase().replace(/\s+/g, "-");
      if (!tagMap.has(slug)) tagMap.set(slug, { original: tag, posts: [] });
      tagMap.get(slug)!.posts.push(post);
    }
  }

  return [...tagMap.entries()].map(([slug, { original, posts }]) => ({
    params: { tag: slug },
    props: {
      tag: original,
      posts: posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime()),
    },
  }));
}

const { tag, posts } = Astro.props;
---

<BaseLayout
  title={`Posts tagged "${tag}"`}
  description={`All ${siteConfig.name} articles tagged with ${tag}.`}
>
  <Breadcrumbs items={[{ label: "Blog", href: "/blog/" }, { label: `Tag: ${tag}` }]} />

  <section class="page-header">
    <h1 class="page-header__title">Tag: {tag}</h1>
    <p class="page-header__count">{posts.length} {posts.length === 1 ? "article" : "articles"}</p>
  </section>

  <div class="post-grid">
    {posts.map((post: any) => (
      <PostCard
        title={post.data.title}
        slug={post.id}
        description={post.data.description}
        category={post.data.category}
        date={post.data.date}
        author={post.data.author}
      />
    ))}
  </div>
</BaseLayout>
```

- [ ] **Step 4: Update author/[author].astro**

Replace the entire file:

```astro
---
import BaseLayout from "../../layouts/BaseLayout.astro";
import PostCard from "../../components/PostCard.astro";
import JsonLd from "../../components/JsonLd.astro";
import SectionHeading from "../../components/SectionHeading.astro";
import { getCollection } from "astro:content";
import { siteConfig } from "../../../site.config";

export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);

  return Object.entries(siteConfig.authors).map(([id, author]) => ({
    params: { author: author.slug },
    props: {
      authorId: id,
      author,
      posts: posts
        .filter((p) => p.data.author === author.name)
        .sort((a, b) => b.data.date.getTime() - a.data.date.getTime()),
    },
  }));
}

const { author, posts } = Astro.props;

const personJsonLd = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: author.name,
  url: `${siteConfig.siteUrl}/author/${author.slug}/`,
  description: author.bio,
  ...(author.externalUrl ? { sameAs: [author.externalUrl] } : {}),
};
---

<BaseLayout title={author.name} description={author.bio.slice(0, 160)}>
  <JsonLd data={personJsonLd} />

  <section class="author-profile">
    <img
      src={author.avatar}
      alt={author.name}
      class="author-profile__avatar"
      width="128"
      height="128"
      loading="lazy"
    />
    <h1 class="author-profile__name">{author.name}</h1>
    <p class="author-profile__bio">{author.bio}</p>
  </section>

  {posts.length > 0 ? (
    <div>
      <SectionHeading text={`Articles by ${author.name}`} />
      <div class="post-grid">
        {posts.map((post: any) => (
          <PostCard
            title={post.data.title}
            slug={post.id}
            description={post.data.description}
            category={post.data.category}
            date={post.data.date}
            author={post.data.author}
          />
        ))}
      </div>
    </div>
  ) : (
    <p style="color:var(--color-muted);text-align:center;padding:2rem 0;">Articles by {author.name} coming soon.</p>
  )}
</BaseLayout>
```

- [ ] **Step 5: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds.

- [ ] **Step 6: Commit**

```bash
git add src/pages/blog/index.astro src/pages/category/\[category\].astro src/pages/tag/\[tag\].astro src/pages/author/\[author\].astro
git commit -m "feat: update archive and listing pages with Homestead design"
```

---

## Task 17: Update remaining static pages

**Files:**
- Modify: `src/pages/about.astro`
- Modify: `src/pages/write-for-us.astro`
- Modify: `src/pages/search.astro`
- Modify: `src/pages/contact.astro`
- Modify: `src/pages/404.astro`

- [ ] **Step 1: Update about.astro — add CTA box at the end**

After the existing `<h2>Contact</h2>` section and its `<p>` block, before the closing `</article>`, add:

```astro
    <div class="cta-box">
      <p class="cta-box__title">Share Your Expertise</p>
      <p class="cta-box__desc">Have hands-on experience with home improvement? We accept guest contributions.</p>
      <a href="/write-for-us/" class="btn btn--accent">Write for Us &rarr;</a>
    </div>
```

Also wrap the article content in a `content-card`:

Change `<article class="content-column prose">` to `<article class="content-column prose content-card">`.

- [ ] **Step 2: Update write-for-us.astro — add CTA button**

Change `<article class="content-column prose">` to `<article class="content-column prose content-card">`.

After the closing `</ol>` and the final `<p>` about not sending completed articles, add:

```astro
    <div class="cta-box" style="margin-top:2.5rem;">
      <p class="cta-box__title">Ready to Pitch?</p>
      <p class="cta-box__desc">Send your topic ideas and writing samples to get started.</p>
      <a href={`mailto:${siteConfig.email}?subject=Guest Post Pitch`} class="btn btn--accent">Email Your Pitch &rarr;</a>
    </div>
```

- [ ] **Step 3: Update search.astro**

Replace the `<input>` tag `style` attribute with `class="search-input"` and remove the inline style:

Change:
```html
<input
  type="search"
  id="search-input"
  placeholder="Search articles..."
  autocomplete="off"
  style="width:100%;padding:0.75rem 1rem;font-size:1rem;border:1px solid var(--color-border);border-radius:6px;margin:1rem 0;"
/>
```

To:
```html
<input
  type="search"
  id="search-input"
  placeholder="Search articles..."
  autocomplete="off"
  class="search-input"
/>
```

- [ ] **Step 4: Update contact.astro**

Change `<article class="content-column prose">` to `<article class="content-column prose content-card">`.

- [ ] **Step 5: Update 404.astro**

Replace the entire file:

```astro
---
import BaseLayout from "../layouts/BaseLayout.astro";
import { siteConfig } from "../../site.config";
---

<BaseLayout title="Page Not Found" description="The page you're looking for doesn't exist." noindex>
  <section class="page-404">
    <p class="page-404__code">404</p>
    <p class="page-404__message">Page not found</p>
    <p class="page-404__links">
      <a href="/">Go home</a> &middot; <a href="/blog/">Browse articles</a> &middot; <a href="/search/">Search</a>
    </p>
  </section>
</BaseLayout>
```

- [ ] **Step 6: Verify build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds with all pages rendering.

- [ ] **Step 7: Commit**

```bash
git add src/pages/about.astro src/pages/write-for-us.astro src/pages/search.astro src/pages/contact.astro src/pages/404.astro
git commit -m "feat: update static pages with Homestead design"
```

---

## Task 18: Final build verification and visual check

- [ ] **Step 1: Run full build**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro build`
Expected: Build succeeds with 0 errors.

- [ ] **Step 2: Start dev server and visually verify**

Run: `cd /Users/bilalshaikh/Documents/GP/home-improvement && npx astro dev`

Check each page type in the browser:
- Home page: hero banner, latest articles grid, category showcase, editor's picks, newsletter teaser, more articles
- Blog post (`/blog/diy-bathroom-remodel-cost/`): hero header with gradient, overlapping content card, table of contents, accordion FAQ, author bio, tags
- Blog index (`/blog/`)
- Category archive (`/category/budget-planning/`)
- Tag archive (`/tag/bathroom-remodel/`)
- Author page (`/author/daniel-ware/`)
- About, Contact, Write for Us, Search, 404, Privacy Policy, Terms, Disclosure

- [ ] **Step 3: Check mobile hamburger**

Resize browser to mobile width. Verify:
- Hamburger icon appears
- Clicking toggles the mobile nav dropdown
- Nav links are stacked and tappable

- [ ] **Step 4: Fix any visual issues found during review**

Address anything that doesn't match the design spec.

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "fix: visual polish from design review"
```
