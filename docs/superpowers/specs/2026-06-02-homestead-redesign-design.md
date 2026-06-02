# The Homestead — Miter House Visual Redesign

**Date:** 2026-06-02
**Status:** Approved
**Approach:** Warm & Editorial, hero-image-forward, earthy palette

---

## 1. Design Direction

"The Homestead" — a Kinfolk-meets-Dwell editorial magazine aesthetic. Warm, grounded, and premium. Designed to build trust (E-E-A-T), keep visitors browsing (internal linking via categories and related posts), and monetize naturally (ad slots and guest-post funnel).

Constraints: pure CSS + Astro components, zero JS frameworks, mobile-first, fast loading, accessible. Google Fonts limited to two families, two weights each.

---

## 2. Color Palette

| Token                | Hex       | Usage                                      |
|----------------------|-----------|--------------------------------------------|
| `--color-primary`    | `#2D4A3E` | Forest green — headers, nav, logo, links   |
| `--color-primary-light` | `#3D6B5A` | Hover states, lighter green accents     |
| `--color-accent`     | `#C1694F` | Terracotta — CTAs, category highlights     |
| `--color-accent-light` | `#D4896F` | Hover variant                            |
| `--color-bg`         | `#FAF6F1` | Warm linen background (whole page)         |
| `--color-surface`    | `#FFFFFF` | Cards, content areas, elevated surfaces    |
| `--color-text`       | `#2C2C2C` | Body copy                                  |
| `--color-heading`    | `#1A1A1A` | Headlines (near-black)                     |
| `--color-muted`      | `#6B6B6B` | Meta text, dates, captions                 |
| `--color-border`     | `#E8E0D8` | Warm gray borders                          |

Update `site.config.ts` colors to match.

---

## 3. Typography

- **Headlines:** `"Playfair Display", Georgia, serif` — bold (700), editorial feel
- **Body:** `"Inter", system-ui, sans-serif` — regular (400) + semibold (600)
- **Scale (desktop):** H1 `2.75rem`, H2 `1.75rem`, H3 `1.35rem`, body `1.0625rem`
- **Scale (mobile):** H1 `2rem`, H2 `1.5rem`, H3 `1.2rem`, body `1rem`
- **Body line-height:** `1.8`
- **Google Fonts:** Load Playfair Display 700 and Inter 400/600 via `<link>` with `display=swap`

---

## 4. Home Page

Six sections, top to bottom:

### 4.1 Hero Banner (featured post)
- Full-width, ~60vh desktop / ~40vh mobile
- Latest post's hero image as background (`object-fit: cover`)
- Dark gradient overlay (transparent top → rgba(0,0,0,0.6) bottom)
- White text overlay: category pill, serif H1 title, date
- Entire banner is clickable (link to the post)
- Fallback when no hero image: earthy gradient (`#2D4A3E` → `#C1694F`)

### 4.2 Latest Articles
- Section heading: "LATEST ARTICLES" in small-caps tracked sans-serif
- 3-column grid (desktop), 2-column (tablet), 1-column (mobile)
- 6 posts
- Card design: hero image top (16:9, `object-fit: cover`), white body below
- Card body: category pill (terracotta, small caps), serif title (2-line clamp), date + author (muted), 2-line excerpt
- `border-radius: 12px`, subtle `box-shadow`, slight translateY lift on hover
- Image placeholder: warm gradient per category when no image exists

### 4.3 Category Showcase
- 2-4 categories displayed as wide horizontal cards
- Each card: category name (serif), short description, post count, link arrow
- Linen background section to break up the white card rhythm
- 2-column grid on desktop, stacked on mobile

### 4.4 Editor's Picks
- Horizontal row of 3 posts, compact card style
- Numbered 01 / 02 / 03 with large muted numbers
- Different visual rhythm from the standard card grid
- Used to surface evergreen pillar content

### 4.5 Newsletter / About Teaser
- Full-width warm-toned callout banner (forest green or linen)
- One-liner about the site + email signup input or "Read our story →" link
- Future email list hook

### 4.6 More Articles
- Same 3-column card grid, 6 more posts
- "View all articles →" terracotta link at the bottom

---

## 5. Post Page

### 5.1 Post Hero Header
- Full-width hero image, ~35vh, dark gradient overlay
- Overlaid: category pill, serif H1, author avatar (small circle) + name + date in white
- No image fallback: warm gradient matching category

### 5.2 Content Card
- White surface card, `max-width: 720px`, centered
- Negative top margin to overlap the hero image bottom (layered editorial effect)
- Padding: `2.5rem` sides, `3rem` top

### 5.3 Table of Contents
- Appears first inside the content card, before the prose
- CSS-only collapsible via `<details>` / `<summary>`
- Open by default on desktop, collapsed on mobile
- Linen background box, "In This Article" heading in small caps
- Lists H2s as forest green anchor links
- Subtle left border line connecting items
- `scroll-behavior: smooth` on `html`
- Auto-generated at build time by an Astro component parsing the rendered HTML headings

### 5.4 Prose Styling
- Serif H2/H3 headings, sans-serif body
- Blockquotes: terracotta left border + linen background
- Tables: alternating linen row shading
- Internal links: forest green, underline on hover
- `<code>`: linen background, rounded

### 5.5 In-Content Ad Slot
- Thin top/bottom borders, linen background, small "Advertisement" label in muted text

### 5.6 FAQ Section
- CSS-only expandable accordions using `<details>` / `<summary>`
- Forest green question text, terracotta chevron/marker
- Replaces the current flat list

### 5.7 Tags
- Pill-shaped: linen background + forest green text
- Terracotta background + white text on hover

### 5.8 Author Bio Box
- Full content-column width, linen background, `border-radius: 12px`
- 96px avatar, serif name link, bio text, external dofollow link slot

---

## 6. Header

- `position: sticky; top: 0`, with `backdrop-filter: blur(8px)` and a permanent subtle `box-shadow` (the shadow is always visible — no JS scroll detection needed)
- Linen/cream background at ~95% opacity (so the blur is visible through it)
- Logo: "Miter House" in Playfair Display, forest green
- Nav links: Inter medium weight, forest green. Active = terracotta underline. Hover = terracotta color
- Mobile: CSS-only hamburger (hidden checkbox + label). Full-width dropdown, stacked nav links on linen background

---

## 7. Footer

- Forest green (`#2D4A3E`) background, cream/linen text (palette inversion)
- Three columns: Brand (logo + tagline), Quick Links (nav + legal), Categories (top 4-5)
- Bottom bar: copyright + legal links in smaller muted text
- Substantial and trustworthy, not a thin afterthought

---

## 8. Category Archive

- Large serif category name, description line, post count
- Subtle banner stripe in a category-specific warm tone
- 3-column card grid, same as home page
- Numbered pagination (not infinite scroll)

---

## 9. Tag Archive

- Simpler: small serif heading, muted description, card grid
- No banner stripe

---

## 10. Author Profile

- Centered layout: 128px rounded avatar, serif name, bio paragraph
- Linen card background behind the bio section
- "Articles by [name]" heading + card grid below
- Person JSON-LD preserved

---

## 11. Other Pages

- **About:** Centered prose column, editorial brand story, CTA to Write for Us
- **Write for Us:** Landing page feel. Value prop, numbered guidelines, terracotta CTA button
- **Search:** Clean rounded input, forest green focus ring, results as simplified list
- **Legal (Privacy, Terms, Disclosure):** Centered prose column, no special styling
- **404:** Friendly serif message, brand logo, links to home + search
- **Contact:** Simple info layout, linen card treatment

---

## 12. Component Inventory

New or significantly changed components:

| Component | Status | Notes |
|-----------|--------|-------|
| `global.css` | Rewrite | New palette, typography, all section styles |
| `Header.astro` | Rewrite | Sticky, mobile hamburger, active state |
| `Footer.astro` | Rewrite | 3-column, inverted palette |
| `PostCard.astro` | Rewrite | Image card with hover effects |
| `AuthorBio.astro` | Restyle | Larger avatar, linen background |
| `Breadcrumbs.astro` | Restyle | Updated colors |
| `AdSlot.astro` | Restyle | Linen treatment, "Advertisement" label |
| `TableOfContents.astro` | **New** | Auto-generated from H2s, CSS-only collapsible |
| `HeroBanner.astro` | **New** | Full-width featured post hero |
| `CategoryShowcase.astro` | **New** | Home page category cards section |
| `EditorPicks.astro` | **New** | Numbered compact post row |
| `NewsletterTeaser.astro` | **New** | CTA banner section |
| `SectionHeading.astro` | **New** | Reusable small-caps section label |
| `PostLayout.astro` | Rewrite | Hero header, ToC, overlapping card |
| `BaseLayout.astro` | Update | Google Fonts link, updated meta |
| `index.astro` | Rewrite | 6-section home page |

Pages with minor template updates (palette/class changes only):
- Category archive, tag archive, author profile, about, write-for-us, search, contact, legal pages, 404

---

## 13. Image Strategy

- `hero_image_prompt` already exists in the content schema
- For now: CSS gradient fallback per category (no broken images)
- Category gradient map defined in a utility (e.g., Outdoor = green→sage, Kitchen = warm→copper)
- When real images are added, they slot in via a `hero_image` frontmatter field (future enhancement)
- All images: `loading="lazy"`, explicit `width`/`height` for CLS, `object-fit: cover`

---

## 14. Performance Budget

- Google Fonts: 2 families, 2 weights each (~40KB)
- Zero JS (all interactions are CSS-only: hamburger, accordions, ToC collapse)
- No image dependencies for initial render (gradient fallbacks)
- Target: Lighthouse 95+ on all metrics
