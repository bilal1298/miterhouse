# Miter House — GATHER Editorial Redesign

**Date:** 2026-06-02
**Status:** Approved
**Reference:** `temp/blog-template-design.html` (GATHER HTML mockup) + `temp/blog-template/` (Astro template)
**Approach:** Full GATHER magazine aesthetic — paper grain, duotone photos, masthead, editorial typography

---

## 1. Design Direction

A print-magazine editorial aesthetic adapted from the GATHER design system. Warm paper tones, a single rust accent, three-font variable type system, and subtle texture. Designed for trust (E-E-A-T), readability, and natural ad monetization.

Constraints: pure CSS + Astro, zero JS frameworks, mobile-first, accessible. Three Google Font families (variable weights).

---

## 2. Color Palette (GATHER tokens)

| Token          | Hex       | Usage                            |
|----------------|-----------|----------------------------------|
| `--paper`      | `#F6F1E9` | Page background                  |
| `--paper-2`    | `#EFE8DC` | Panels, cards                    |
| `--paper-3`    | `#E7DECF` | Deeper panels                    |
| `--ink`        | `#1B1916` | Primary text                     |
| `--ink-soft`   | `#4B463E` | Secondary text                   |
| `--muted`      | `#908779` | Meta, captions                   |
| `--line`       | `#D8CFBF` | Hairlines, borders               |
| `--accent`     | `#BB4626` | Single accent (CTAs, kickers)    |
| `--accent-deep`| `#8F3318` | Accent hover                     |

---

## 3. Typography

- **Display:** `"Fraunces", Georgia, serif` — variable weight 300-900, optical sizing
- **Body:** `"Newsreader", Georgia, serif` — variable weight 300-600, optical sizing
- **UI/Labels:** `"Hanken Grotesk", system-ui, sans-serif` — 400-800
- **Body size:** 18px, line-height 1.6
- **Prose size:** 19.5px, line-height 1.72

Google Fonts URL:
```
https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,400..900&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&family=Hanken+Grotesk:wght@400;500;600;700;800&display=swap
```

---

## 4. Key Design Features

### Paper Grain Texture
SVG noise overlay on `body::after`, fixed, `pointer-events: none`, 5% opacity.

### Duotone Photo Treatment
All images wrapped in `.ph` container:
- Image: `filter: grayscale(1) contrast(1.06) brightness(1.02)`
- `::after` pseudo: accent color with `mix-blend-mode: multiply`, 32% opacity
- `::before` pseudo: paper color with `mix-blend-mode: screen`, 10% opacity
- Hover: `transform: scale(1.04)` with smooth cubic-bezier transition

### Load Reveal Animations
`.reveal` class: fade up from 16px, 0.9s cubic-bezier. Staggered delays (d1-d5).

---

## 5. Home Page

### 5.1 Top Bar
Thin bar with: left = date + issue number, right = Subscribe + Write for Us links.

### 5.2 Masthead
Centered: decorative rule line with tagline text, large Fraunces logo "Miter House", italic tagline below.

### 5.3 Sticky Nav
`position: sticky`, double border (top ink + bottom ink). Centered category links + search link. Horizontal scroll on mobile.

### 5.4 Hero (Asymmetric)
2-column grid (1.05fr / 0.95fr): text left (kicker, large Fraunces h1, dek paragraph, byline with avatar), image right (4:5 duotone photo). Stacks on mobile.

### 5.5 Feature Grid
Section header ("From the journal" + "All stories →"). 2-column: left = 3-column card grid, right = "Most read" numbered sidebar list (01-04).

### 5.6 Ad Slot
Striped background, centered, bordered.

### 5.7 Category Section
Section header + 3-column card grid of category-specific posts.

### 5.8 Newsletter Band
Dark (ink bg), 2-column: left = kicker + Fraunces heading + description, right = email form with underline input style.

---

## 6. Article Page

### 6.1 Breadcrumbs
Small uppercase Hanken Grotesk, muted color.

### 6.2 Centered Header
Category kicker, large Fraunces h1, italic dek (description), byline (avatar initials + name + date + reading time).

### 6.3 Hero Image
Wide aspect (21:9) duotone photo with caption below.

### 6.4 Body Grid (3-column)
Left: sticky sidebar ToC (label links, accent active state). Center: prose (680px max). Right: empty.
ToC hides on mobile (<1040px).

### 6.5 Prose Styling
- Drop cap on lead paragraph (Fraunces, 4.6em, accent color, floated)
- H2s with accent bar (`<span class="hr">`) above
- Blockquotes: centered, Fraunces italic, large
- List markers: accent color
- Internal links: accent-deep underline
- Figures with duotone treatment + caption

### 6.6 In-Content Ad Slot
Same style as home, max-width constrained.

### 6.7 FAQ Section
CSS-only `<details>/<summary>` accordions (preserved from current).

### 6.8 Tags
Pill style with accent color.

### 6.9 Author Box
Flex layout: initials avatar (accent bg) + eyebrow + name + bio + links (website + more articles).

### 6.10 Share Row
Horizontal: "Share" label + Email / Copy link / Bluesky / Pocket.

### 6.11 Keep Reading
Section header + 3-column related posts grid.

---

## 7. Header (Global)

Top bar + masthead (home only, condensed on articles) + sticky nav with double ink borders.

---

## 8. Footer

4-column grid: Brand (logo + description), Sections (top categories), About (nav links), Legal (policy links).
Colophon bar below: copyright + platform credits.

---

## 9. Archive Pages

Category/tag/author/blog archives use `.page-head` (centered: eyebrow + h1 + count/description) + card grid.

---

## 10. Static Pages

About, Write for Us, Contact, Legal, 404 — prose column with `.container`, clean typography. 404 uses eyebrow "404" + h1 + description + button.

---

## 11. Component Inventory

| Component | Status | Notes |
|-----------|--------|-------|
| `global.css` | Rewrite | Full GATHER CSS system |
| `site.config.ts` | Update | Add theme section with GATHER tokens |
| `BaseLayout.astro` | Rewrite | Theme variable injection, new structure |
| `SEO.astro` | Update | New Google Fonts URL |
| `Header.astro` | Rewrite | Top bar + masthead + sticky nav |
| `Footer.astro` | Rewrite | 4-column + colophon |
| `PostCard.astro` | Rewrite | GATHER card with duotone photos |
| `PostLayout.astro` | Rewrite | Centered header, ToC sidebar, prose |
| `AuthorBio.astro` | Rewrite | GATHER author box |
| `AdSlot.astro` | Rewrite | GATHER stripe style |
| `Breadcrumbs.astro` | Restyle | GATHER crumb style |
| `index.astro` | Rewrite | GATHER home (hero + grid + most-read + newsletter) |
| `src/utils/helpers.ts` | **New** | readingTime, formatDate, relatedPosts, slugify, path helpers |
| HeroBanner.astro | **Remove** | Replaced by inline hero in index.astro |
| CategoryShowcase.astro | **Remove** | Not in GATHER design |
| EditorPicks.astro | **Remove** | Replaced by most-read sidebar |
| NewsletterTeaser.astro | **Remove** | Replaced by newsletter band in index.astro |
| SectionHeading.astro | **Remove** | Replaced by .shead pattern |
| TableOfContents.astro | **Remove** | Replaced by sticky sidebar ToC in PostLayout |
| category-gradients.ts | **Remove** | Replaced by duotone treatment |

---

## 12. What's Preserved

- Content schema (faq, hero_image_prompt, date field names)
- JSON-LD (Article, BreadcrumbList, FAQPage, Organization, Person)
- Blog post content files
- n8n workflow compatibility
- AdSense config structure
- Canonical URLs, OG tags, sitemaps, RSS
- Legal pages content
