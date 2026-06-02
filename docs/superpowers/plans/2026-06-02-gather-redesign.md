# GATHER Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Replace the current "Homestead" design with the full GATHER editorial magazine aesthetic.

**Architecture:** Rewrite CSS + components to match GATHER design. Theme tokens injected from site.config via CSS variables in BaseLayout. Remove old Homestead components. Add utility helpers.

**Reference:** `temp/blog-template-design.html` (visual spec), `temp/blog-template/` (Astro patterns), `docs/superpowers/specs/2026-06-02-gather-redesign-design.md`

---

### Task 1: Foundation — site.config theme + global.css + SEO fonts + utils

**Files:**
- Modify: `site.config.ts`
- Rewrite: `src/styles/global.css`
- Modify: `src/components/SEO.astro`
- Create: `src/utils/helpers.ts`
- Remove: `src/utils/category-gradients.ts`

Add `theme` section to site.config.ts with all GATHER tokens (colors, fonts, radii, widths, Google Fonts URL).

Rewrite global.css with the full GATHER CSS system from `temp/blog-template-design.html` lines 11-312, using CSS custom properties that will be injected by BaseLayout.

Update SEO.astro to use the new Google Fonts URL from config.

Create `src/utils/helpers.ts` with: `slugify`, `categoryPath`, `tagPath`, `authorPath`, `formatDate`, `readingTime`, `getSortedPosts`, `relatedPosts`, `uniqueCategories`, `uniqueTags`.

Remove `src/utils/category-gradients.ts` (replaced by duotone treatment).

---

### Task 2: BaseLayout + Header + Footer

**Files:**
- Rewrite: `src/layouts/BaseLayout.astro`
- Rewrite: `src/components/Header.astro`
- Rewrite: `src/components/Footer.astro`

BaseLayout: Inject CSS variables from site.config.theme as inline `:root` style (like blog-template pattern). Add paper grain texture pseudo-element via body. Include skip link.

Header: GATHER-style with three sections:
1. Top bar (date + Subscribe / Write for Us links)
2. Masthead (decorative rule + large logo + tagline) — shown on home only, condensed on other pages
3. Sticky nav with double ink borders, centered category links + search

Footer: GATHER 4-column grid (brand, sections/categories, about links, legal links) + colophon bar.

---

### Task 3: PostCard + Home Page

**Files:**
- Rewrite: `src/components/PostCard.astro`
- Rewrite: `src/pages/index.astro`

PostCard: GATHER card with duotone `.ph` image wrapper, kicker label, Fraunces h3 with underline-on-hover, excerpt, meta line.

Home page (index.astro): Full GATHER layout:
1. Hero section (asymmetric 2-col: text left, duotone image right)
2. Section header ("From the journal" / "All stories →")
3. Feature grid (2-col: 3-col card grid left, numbered "Most read" sidebar right)
4. Ad slot
5. Category section (section header + 3-col cards)
6. Newsletter band (dark bg, 2-col: heading left, email form right)

---

### Task 4: PostLayout + Article Components

**Files:**
- Rewrite: `src/layouts/PostLayout.astro`
- Rewrite: `src/components/AuthorBio.astro`
- Rewrite: `src/components/AdSlot.astro`
- Rewrite: `src/components/Breadcrumbs.astro`

PostLayout: GATHER article layout:
- Breadcrumbs (GATHER style)
- Centered article header (kicker, Fraunces h1, italic dek, byline with avatar initials)
- Hero image area (duotone, 21:9, caption)
- 3-column body grid: sticky ToC sidebar left, prose center (680px), empty right
- Drop cap on first paragraph
- H2s with accent bar spans
- In-content ad slot
- FAQ section (details/summary preserved)
- Tags as pills
- Author box (GATHER style with initials)
- Share row
- "Keep reading" related posts section

AuthorBio: GATHER author box with initials avatar, eyebrow, name, bio, links.

AdSlot: GATHER style with diagonal stripe background, dashed border placeholder.

Breadcrumbs: GATHER style — small uppercase, muted, arrow separators.

---

### Task 5: Archive + Static Pages

**Files:**
- Rewrite: `src/pages/blog/index.astro`
- Rewrite: `src/pages/category/[category].astro`
- Rewrite: `src/pages/tag/[tag].astro`
- Rewrite: `src/pages/author/[author].astro`
- Rewrite: `src/pages/about.astro`
- Rewrite: `src/pages/write-for-us.astro`
- Rewrite: `src/pages/search.astro`
- Rewrite: `src/pages/contact.astro`
- Rewrite: `src/pages/404.astro`
- Update: `src/pages/privacy-policy.astro`
- Update: `src/pages/terms.astro`
- Update: `src/pages/disclosure.astro`

All archives: GATHER `.page-head` (centered: eyebrow + h1 + description) + card-grid. Category page adds eyebrow "Category", tag page adds eyebrow "Tag", author page adds centered avatar + bio.

Static pages: Clean prose column. About = prose + CTA. Write-for-us = prose + pitch form/email. Contact = prose + contact info. Legal = prose. 404 = eyebrow "404" + message + home button. Search = centered input.

---

### Task 6: Cleanup + Build Verification

**Files:**
- Remove: `src/components/HeroBanner.astro`
- Remove: `src/components/CategoryShowcase.astro`
- Remove: `src/components/EditorPicks.astro`
- Remove: `src/components/NewsletterTeaser.astro`
- Remove: `src/components/SectionHeading.astro`
- Remove: `src/components/TableOfContents.astro`

Remove all old Homestead-specific components. Run `npm run build` to verify clean build. Check all pages render.
