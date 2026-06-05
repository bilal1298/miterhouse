#!/usr/bin/env python3
"""
Build a 365-post content calendar from keyword research data + existing posts.
Outputs a complete CSV ready for Google Sheets import.

Steps:
1. Load keywords, further deduplicate synonym clusters
2. Categorize each keyword into one of 8 site categories
3. Organize into pillar clusters
4. Merge with existing 20 posts
5. Select best 345 new keywords
6. Sequence depth-first by pillar cluster
7. Assign publish dates (2/day starting after last existing post)
8. Build internal link candidates (chronological only)
9. Generate titles, slugs, descriptions, tags, FAQ seeds, image prompts
10. Output CSV
"""

import csv
import re
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# ── Config ──────────────────────────────────────────────────────────

CATEGORIES = [
    "Kitchen & Bath Remodeling",
    "Budget & Planning",
    "Flooring & Tile",
    "Painting & Walls",
    "Outdoor & Landscaping",
    "Plumbing & Electrical",
    "Basement & Attic",
    "Tools & Materials",
]

AUTHOR = "Daniel Ware"
POSTS_PER_DAY = 2
TOTAL_POSTS = 365
START_DATE = datetime(2026, 5, 10)  # first existing post date

# ── Category keyword patterns ───────────────────────────────────────

CATEGORY_PATTERNS = {
    "Kitchen & Bath Remodeling": [
        r'\bbathroom\b', r'\bbath\b', r'\bshower\b', r'\btub\b', r'\bvanity\b',
        r'\bkitchen\b', r'\bcabinet\b', r'\bcountertop\b', r'\bgranite\b',
        r'\bquartz\b', r'\bmarble\b', r'\bbacksplash\b', r'\bsink\b',
        r'\bfaucet\b', r'\btile.*wall\b', r'\bwall.*tile\b', r'\bremodel\b',
        r'\brenovati', r'\btoilet\b', r'\bbathtub\b',
    ],
    "Budget & Planning": [
        r'\bcost\b', r'\bprice\b', r'\bbudget\b', r'\bfinanc', r'\bestimate\b',
        r'\broi\b', r'\bvalue\b', r'\bworth\b', r'\bsave\b', r'\bcheap\b',
        r'\baffordab', r'\binvestment\b', r'\bplanning\b', r'\bpermit\b',
        r'\bcontract', r'\bhire\b', r'\bquote\b', r'\bbid\b',
    ],
    "Flooring & Tile": [
        r'\bfloor', r'\btile\b', r'\btiling\b', r'\bhardwood\b', r'\blaminate\b',
        r'\bvinyl\b', r'\blvp\b', r'\bcarpet\b', r'\bgrout\b', r'\bsubfloor\b',
        r'\bepoxy\b', r'\bconcrete.*floor\b', r'\bfloor.*concrete\b',
    ],
    "Painting & Walls": [
        r'\bpaint', r'\bwall\b', r'\bwalls\b', r'\bdrywall\b', r'\bplaster\b',
        r'\bwallpaper\b', r'\bstucco\b', r'\bprimer\b', r'\bspackle\b',
        r'\bsheetrock\b', r'\btextur', r'\bstain\b(?!less)', r'\bvarnish\b',
    ],
    "Outdoor & Landscaping": [
        r'\bdeck\b', r'\bpatio\b', r'\bfence\b', r'\blandscap', r'\bgarden\b',
        r'\blawn\b', r'\boutdoor\b', r'\bpergola\b', r'\bgazebo\b',
        r'\bshed\b', r'\bcurb\b', r'\bdriveway\b', r'\bsidewalk\b',
        r'\bporch\b', r'\bpaver\b', r'\bretaining.*wall\b', r'\byard\b',
        r'\birrigat', r'\bsprinkler\b', r'\bgutter\b', r'\broof\b',
        r'\bsiding\b', r'\bexterior\b', r'\bwindow\b(?!.*interior)',
        r'\bdoor\b(?!.*interior)', r'\bpool\b', r'\bcompost\b',
    ],
    "Plumbing & Electrical": [
        r'\bplumb', r'\bpipe\b', r'\bpipes\b', r'\bdrain\b', r'\bsewer\b',
        r'\bwater\s*heat', r'\belectric', r'\bwiring\b', r'\bcircuit\b',
        r'\boutlet\b', r'\bswitch\b(?!.*light)', r'\bpanel\b', r'\bbolt\b',
        r'\bamp\b', r'\bvolt', r'\bcable\b', r'\bfixture\b', r'\bleak\b',
        r'\bfaucet\b', r'\bwater\b(?!.*proof)', r'\bhvac\b', r'\bheat.*pump\b',
        r'\bboiler\b', r'\bfurnace\b', r'\bac\s*repair\b', r'\bther\w*stat\b',
    ],
    "Basement & Attic": [
        r'\bbasement\b', r'\battic\b', r'\bcrawl\s*space\b', r'\bwaterproof',
        r'\binsulat', r'\bmoisture\b', r'\bmold\b', r'\bfinish.*basement\b',
        r'\bbasement.*finish', r'\bsump\b', r'\bradon\b', r'\bfoundat',
    ],
    "Tools & Materials": [
        r'\btool\b', r'\btools\b', r'\bdrill\b', r'\bsaw\b', r'\bhammer\b',
        r'\blevel\b', r'\btape\s*measure\b', r'\bsander\b', r'\bscrew\b',
        r'\bnail\b', r'\bbolt\b(?!.*electrical)', r'\badhesive\b', r'\bcaulk\b',
        r'\bsealant\b', r'\bsafety\s*gear\b', r'\bppe\b', r'\bladder\b',
        r'\bscaffold', r'\bpower\s*tool\b',
    ],
}

# ── Pillar cluster seed topics ──────────────────────────────────────

PILLAR_SEEDS = {
    # Kitchen & Bath
    "bathroom-remodel": (r'\bbathroom\b.*\bremodel', "Kitchen & Bath Remodeling"),
    "kitchen-remodel": (r'\bkitchen\b.*\bremodel', "Kitchen & Bath Remodeling"),
    "shower-remodel": (r'\bshower\b', "Kitchen & Bath Remodeling"),
    "vanity-cabinet": (r'\bvanity\b|\bcabinet\b', "Kitchen & Bath Remodeling"),
    "countertop": (r'\bcountertop\b|\bgranite\b|\bquartz\b|\bmarble\b', "Kitchen & Bath Remodeling"),
    "backsplash-sink": (r'\bbacksplash\b|\bsink\b|\bfaucet\b', "Kitchen & Bath Remodeling"),

    # Budget & Planning
    "remodel-cost": (r'\bcost\b.*\bremodel|\bremodel.*\bcost\b', "Budget & Planning"),
    "home-value-roi": (r'\bvalue\b|\broi\b|\bworth\b|\binvestment\b', "Budget & Planning"),
    "financing-budget": (r'\bfinanc|\bbudget\b|\baffordab|\bsave\b|\bcheap\b', "Budget & Planning"),
    "hiring-permits": (r'\bcontract|\bhire\b|\bpermit\b|\bquote\b|\bbid\b', "Budget & Planning"),

    # Flooring
    "hardwood-floor": (r'\bhardwood\b', "Flooring & Tile"),
    "laminate-vinyl-floor": (r'\blaminate\b|\bvinyl\b|\blvp\b', "Flooring & Tile"),
    "tile-floor": (r'\btile\b.*\bfloor|\bfloor.*\btile|\btiling\b|\bgrout\b', "Flooring & Tile"),
    "carpet-floor": (r'\bcarpet\b|\bfloor.*install|\bsubfloor\b', "Flooring & Tile"),

    # Painting & Walls
    "interior-paint": (r'\bpaint\b.*\broom|\bpaint\b.*\binterior|\bpaint\b.*\bwall', "Painting & Walls"),
    "exterior-paint": (r'\bpaint\b.*\bexterior|\bpaint\b.*\bhouse|\bstain\b', "Painting & Walls"),
    "drywall-plaster": (r'\bdrywall\b|\bplaster\b|\bspackle\b|\bsheetrock\b', "Painting & Walls"),
    "wallpaper-texture": (r'\bwallpaper\b|\btextur|\bstucco\b', "Painting & Walls"),

    # Outdoor
    "deck-build": (r'\bdeck\b', "Outdoor & Landscaping"),
    "fence-build": (r'\bfence\b', "Outdoor & Landscaping"),
    "patio-paver": (r'\bpatio\b|\bpaver\b|\bconcrete\b.*\boutdoor', "Outdoor & Landscaping"),
    "landscape-garden": (r'\blandscap|\bgarden\b|\blawn\b|\byard\b', "Outdoor & Landscaping"),
    "roof-siding": (r'\broof\b|\bsiding\b|\bgutter\b', "Outdoor & Landscaping"),
    "window-door": (r'\bwindow\b|\bdoor\b', "Outdoor & Landscaping"),
    "driveway-porch": (r'\bdriveway\b|\bporch\b|\bsidewalk\b|\bpergola\b', "Outdoor & Landscaping"),

    # Plumbing & Electrical
    "water-heater": (r'\bwater\s*heat', "Plumbing & Electrical"),
    "plumbing-repair": (r'\bplumb|\bpipe\b|\bdrain\b|\bleak\b|\bsewer\b', "Plumbing & Electrical"),
    "electrical-wiring": (r'\belectric|\bwiring\b|\bcircuit\b|\boutlet\b|\bcable\b', "Plumbing & Electrical"),
    "hvac-heating": (r'\bhvac\b|\bheat.*pump\b|\bboiler\b|\bfurnace\b|\bac\b.*\brepair|\bthermostat\b', "Plumbing & Electrical"),
    "water-damage": (r'\bwater\s*damage|\bflood|\bwater\s*proof|\bmoisture\b.*\bdamage', "Plumbing & Electrical"),

    # Basement & Attic
    "basement-finish": (r'\bbasement\b', "Basement & Attic"),
    "attic-insulation": (r'\battic\b|\binsulat', "Basement & Attic"),
    "crawlspace-foundation": (r'\bcrawl\s*space\b|\bfoundat|\bsump\b|\bradon\b', "Basement & Attic"),
    "waterproofing": (r'\bwaterproof|\bmold\b', "Basement & Attic"),

    # Tools & Materials
    "power-tools": (r'\btool\b|\btools\b|\bdrill\b|\bsaw\b', "Tools & Materials"),
    "materials-supplies": (r'\badhesive\b|\bcaulk\b|\bsealant\b|\bscrew\b|\bnail\b', "Tools & Materials"),
}


def categorize_keyword(kw):
    """Assign keyword to best-fit category based on pattern matching."""
    kw_lower = kw.lower()
    scores = defaultdict(int)

    for cat, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, kw_lower):
                scores[cat] += 1

    if not scores:
        # Fallback heuristics
        if any(w in kw_lower for w in ['cost', 'price', 'how much', 'estimate', 'budget']):
            return "Budget & Planning"
        if any(w in kw_lower for w in ['install', 'replace', 'repair', 'fix']):
            return "Tools & Materials"
        return "Budget & Planning"  # safe default

    # If Budget & Planning ties with a specific category, prefer the specific one
    max_score = max(scores.values())
    top_cats = [c for c, s in scores.items() if s == max_score]
    if len(top_cats) > 1 and "Budget & Planning" in top_cats:
        top_cats.remove("Budget & Planning")
    return top_cats[0]


def assign_pillar(kw, category):
    """Assign keyword to a pillar cluster."""
    kw_lower = kw.lower()
    best_pillar = None
    best_score = 0

    for pillar, (pattern, pillar_cat) in PILLAR_SEEDS.items():
        if re.search(pattern, kw_lower):
            score = 2 if pillar_cat == category else 1
            if score > best_score:
                best_score = score
                best_pillar = pillar

    if not best_pillar:
        # Assign to generic pillar for category
        cat_pillars = {
            "Kitchen & Bath Remodeling": "bathroom-remodel",
            "Budget & Planning": "remodel-cost",
            "Flooring & Tile": "tile-floor",
            "Painting & Walls": "interior-paint",
            "Outdoor & Landscaping": "landscape-garden",
            "Plumbing & Electrical": "plumbing-repair",
            "Basement & Attic": "basement-finish",
            "Tools & Materials": "power-tools",
        }
        best_pillar = cat_pillars.get(category, "remodel-cost")

    return best_pillar


def generate_slug(title):
    """Generate URL-safe slug from title."""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return slug[:80]


def generate_title(keyword):
    """Generate a compelling blog post title from a keyword with variety."""
    title = _generate_title_raw(keyword)
    if len(title) > 65:
        # Truncate smartly at word boundary
        truncated = title[:62]
        if ' ' in truncated:
            truncated = truncated[:truncated.rfind(' ')]
        title = truncated.rstrip(':- ') + "..."
    return title


def _generate_title_raw(keyword):
    """Inner title generation — may produce titles over 65 chars."""
    import hashlib
    kw = keyword.strip()
    kw_lower = kw.lower()
    # Use hash for deterministic variety
    h = int(hashlib.md5(keyword.encode()).hexdigest(), 16)

    def titlecase(s):
        small = {'a','an','the','of','to','for','in','on','and','or','but','is','vs','at','by','with'}
        words = s.split()
        return ' '.join(w.capitalize() if i == 0 or w.lower() not in small else w.lower() for i, w in enumerate(words))

    def clean_subject(s, extra_remove=None):
        removes = [r'\bof\b', r'\bto\b', r'\bfor\b', r'\ba\b', r'\bthe\b', r'\bmy\b', r'\byour\b',
                    r'\bcalculate\b', r'\bcalculator\b', r'\bestimate\b', r'\bestimator\b',
                    r'\baverage\b', r'\btypical\b', r'\bnormal\b']
        if extra_remove:
            removes.extend(extra_remove)
        for r in removes:
            s = re.sub(r, '', s, flags=re.IGNORECASE)
        s = re.sub(r'\s+', ' ', s).strip()
        # Remove leading connectives
        s = re.sub(r'^(and|or|but|the|a|an)\s+', '', s, flags=re.IGNORECASE).strip()
        return s

    # Cost/price queries — 4 templates
    if re.search(r'\bcost\b|\bprice\b|\bhow\s+much\b', kw_lower):
        subject = re.sub(r'\bcost\b|\bprice\b|\bhow\s+much\b', '', kw_lower)
        subject = clean_subject(subject)
        st = titlecase(subject)
        templates = [
            f"{st} Cost: What to Expect in 2026",
            f"How Much Does {st} Really Cost?",
            f"{st} Cost Breakdown: Real Numbers",
            f"{st} Pricing Guide for Homeowners",
        ]
        return templates[h % len(templates)]

    # How-to queries — 3 templates
    if re.search(r'^how\s+to\b', kw_lower):
        rest = re.sub(r'^how\s+to\s+', '', kw_lower)
        rt = titlecase(rest)
        templates = [
            f"How to {rt}: Step-by-Step Guide",
            f"How to {rt} the Right Way",
            f"How to {rt} (Without Wrecking Anything)",
        ]
        return templates[h % len(templates)]

    # "Best" queries
    if re.search(r'^best\b', kw_lower):
        rest = re.sub(r'^best\s+', '', kw_lower)
        rt = titlecase(rest)
        templates = [
            f"Best {rt} for 2026: Honest Picks",
            f"Best {rt} Worth Your Money in 2026",
            f"The Best {rt} We've Actually Tested",
        ]
        return templates[h % len(templates)]

    # DIY queries
    if re.search(r'\bdiy\b', kw_lower):
        rest = re.sub(r'\bdiy\b', '', kw_lower).strip()
        rt = titlecase(rest)
        templates = [
            f"DIY {rt}: A Homeowner's Honest Guide",
            f"DIY {rt}: What It Really Takes",
            f"Can You DIY {rt}? Here's the Truth",
        ]
        return templates[h % len(templates)]

    # Install/installation queries — 3 templates
    if re.search(r'\binstall', kw_lower):
        subject = re.sub(r'\binstall\w*\b', '', kw_lower)
        subject = clean_subject(subject, [r'\bcost\b'])
        st = titlecase(subject)
        templates = [
            f"{st} Installation: Costs and Tips",
            f"Installing {st}: What to Know First",
            f"{st} Installation Guide: DIY or Hire Out?",
        ]
        return templates[h % len(templates)]

    # Repair queries — 3 templates
    if re.search(r'\brepair\b', kw_lower):
        subject = re.sub(r'\brepair\w*\b', '', kw_lower)
        subject = clean_subject(subject, [r'\bcost\b', r'\bservice\b', r'\bcosts\b'])
        st = titlecase(subject)
        templates = [
            f"{st} Repair: DIY or Call a Pro?",
            f"{st} Repairs: A Homeowner's Guide",
            f"{st} Repair Guide: What to Know",
        ]
        return templates[h % len(templates)]

    # Replace queries
    if re.search(r'\breplace', kw_lower):
        subject = re.sub(r'\breplace\w*\b', '', kw_lower)
        subject = clean_subject(subject, [r'\bcost\b'])
        st = titlecase(subject)
        templates = [
            f"When to Replace {st}: Signs and Costs",
            f"{st} Replacement: Full Planning Guide",
            f"Replacing {st}: What It Costs and Takes",
        ]
        return templates[h % len(templates)]

    # vs. comparisons
    if re.search(r'\bvs\.?\b|\bversus\b', kw_lower):
        return f"{titlecase(kw)}: Which Is Right for Your Home?"

    # Service queries
    if re.search(r'\bservice\b|\bcompan', kw_lower):
        subject = re.sub(r'\bservice\w*\b|\bcompan\w*\b', '', kw_lower)
        subject = clean_subject(subject)
        st = titlecase(subject)
        templates = [
            f"Hiring {st} Pros: What to Look For",
            f"{st}: When to Hire and What to Expect",
            f"Finding Good {st} Contractors Near You",
        ]
        return templates[h % len(templates)]

    # Contractor queries
    if re.search(r'\bcontract', kw_lower):
        subject = re.sub(r'\bcontract\w*\b', '', kw_lower)
        subject = clean_subject(subject)
        st = titlecase(subject)
        return f"Hiring a {st} Contractor: Red Flags and Tips"

    # Generic fallback — 5 templates for variety
    t = titlecase(kw)
    templates = [
        f"{t}: What Homeowners Should Know",
        f"{t}: A Practical Guide",
        f"The Real Deal on {t}",
        f"{t}: Honest Advice for Your Home",
        f"{t}: A DIYer's Honest Take",
    ]
    title = templates[h % len(templates)]

    # Enforce max 65 chars
    if len(title) > 65:
        # Try shorter suffix
        short_templates = [
            f"{t}: What to Know",
            f"{t}: A Practical Guide",
            f"{t}: Honest Guide",
        ]
        title = short_templates[h % len(short_templates)]
    if len(title) > 65:
        title = t[:62] + "..."
    return title


def generate_description(title, keyword, category):
    """Generate a 140-160 char meta description with good variety."""
    import hashlib
    kw_lower = keyword.lower()
    h = int(hashlib.md5(keyword.encode()).hexdigest(), 16)

    # Category-specific templates
    cat_templates = {
        "Kitchen & Bath Remodeling": [
            f"Real costs, realistic timelines, and practical steps for {kw_lower}. Written by a homeowner who's been through it.",
            f"Considering {kw_lower}? Here are the actual numbers, common pitfalls, and what most guides leave out.",
            f"A no-fluff guide to {kw_lower} with real material costs, labor estimates, and the mistakes to skip.",
        ],
        "Budget & Planning": [
            f"Honest cost breakdown for {kw_lower}. Real numbers from actual projects — not contractor marketing fluff.",
            f"How much does {kw_lower} really cost? Line-by-line budget with labor, materials, and hidden expenses.",
            f"Budget smarter for {kw_lower}. Real prices, trade-offs between DIY and pro, and where to save without regret.",
        ],
        "Flooring & Tile": [
            f"From subfloor prep to final trim — a practical guide to {kw_lower} with real costs and pro tips.",
            f"Thinking about {kw_lower}? Here's what it costs, how long it takes, and whether you should DIY it.",
            f"Step-by-step guide to {kw_lower}: material options, installation tips, and honest cost expectations.",
        ],
        "Painting & Walls": [
            f"How to get pro-level results with {kw_lower}. Prep tips, product picks, and honest time estimates.",
            f"A practical guide to {kw_lower} — from surface prep to final coat. Real techniques that work.",
            f"Skip the rookie mistakes on {kw_lower}. Prep, products, and techniques from someone who's painted 30+ rooms.",
        ],
        "Outdoor & Landscaping": [
            f"Planning {kw_lower}? Real costs, material comparisons, and the steps most DIY guides skip.",
            f"A hands-on guide to {kw_lower} with actual project costs, timelines, and what to watch out for.",
            f"Everything you need for {kw_lower}: materials, costs, permits, and lessons from actual backyard projects.",
        ],
        "Plumbing & Electrical": [
            f"Should you DIY {kw_lower} or call a pro? Real costs, skill requirements, and safety considerations.",
            f"A straightforward guide to {kw_lower}: what you can handle yourself and when to pick up the phone.",
            f"Know what you're getting into with {kw_lower}. Costs, code requirements, and the honest DIY difficulty level.",
        ],
        "Basement & Attic": [
            f"Practical guide to {kw_lower}: real costs per square foot, timelines, and the gotchas nobody warns about.",
            f"Considering {kw_lower}? Here's what it actually takes — costs, permits, and the decisions that matter most.",
            f"Turn unused space into livable rooms. A real-world guide to {kw_lower} with honest costs and timelines.",
        ],
        "Tools & Materials": [
            f"Honest picks for {kw_lower} — what's worth the money and what's marketing hype. Tested in real projects.",
            f"A no-nonsense guide to {kw_lower}: what to buy, what to skip, and what actually matters for home projects.",
            f"Cut through the noise on {kw_lower}. Real reviews and recommendations from hundreds of hours of project work.",
        ],
    }

    templates = cat_templates.get(category, [
        f"A practical, no-fluff guide to {kw_lower} with real costs and honest advice for homeowners.",
        f"What you actually need to know about {kw_lower}: costs, timelines, and trade-offs explained clearly.",
        f"Real-world guide to {kw_lower}. Practical steps, honest costs, and lessons from actual home projects.",
    ])

    desc = templates[h % len(templates)]

    if len(desc) > 165:
        desc = desc[:162] + "..."
    if len(desc) < 120:
        desc += " Practical tips from real projects."

    return desc


def generate_tags(keyword, category, pillar):
    """Generate 3-6 relevant tags."""
    kw_lower = keyword.lower()
    tags = set()

    # Category-based tags
    cat_tags = {
        "Kitchen & Bath Remodeling": ["bathroom remodel", "kitchen remodel", "renovation"],
        "Budget & Planning": ["home improvement cost", "budget renovation", "project planning"],
        "Flooring & Tile": ["flooring", "tile installation", "floor repair"],
        "Painting & Walls": ["painting", "wall repair", "interior design"],
        "Outdoor & Landscaping": ["outdoor projects", "landscaping", "curb appeal"],
        "Plumbing & Electrical": ["plumbing", "electrical", "home repair"],
        "Basement & Attic": ["basement finishing", "attic renovation", "home improvement"],
        "Tools & Materials": ["tools", "building materials", "DIY equipment"],
    }
    for t in cat_tags.get(category, ["home improvement"])[:2]:
        tags.add(t)

    # Keyword-derived tags
    kw_words = set(kw_lower.split())
    tag_map = {
        'cost': 'cost guide', 'diy': 'DIY', 'install': 'installation',
        'repair': 'home repair', 'bathroom': 'bathroom', 'kitchen': 'kitchen',
        'floor': 'flooring', 'tile': 'tile', 'paint': 'painting',
        'deck': 'deck building', 'fence': 'fencing', 'plumb': 'plumbing',
        'electric': 'electrical', 'basement': 'basement', 'attic': 'attic',
        'water': 'water damage', 'roof': 'roofing', 'window': 'windows',
        'door': 'doors', 'cabinet': 'cabinets', 'countertop': 'countertops',
        'hardwood': 'hardwood floors', 'laminate': 'laminate flooring',
        'vinyl': 'vinyl flooring', 'drywall': 'drywall', 'insulation': 'insulation',
    }
    for w in kw_words:
        for key, tag in tag_map.items():
            if key in w:
                tags.add(tag)

    tags = list(tags)[:6]
    if len(tags) < 3:
        tags.extend(["home improvement", "DIY", "renovation guide"][:3 - len(tags)])

    return tags[:6]


def generate_faq(keyword, category):
    """Generate 2-3 FAQ question/answer pairs, specific to the keyword."""
    import hashlib
    kw_lower = keyword.lower()
    h = int(hashlib.md5(keyword.encode()).hexdigest(), 16)

    faqs = []

    # Question 1: Cost or primary concern — varies by category
    cost_qs = {
        "Kitchen & Bath Remodeling": [
            {"q": f"How much does {kw_lower} cost on average?",
             "a": f"A mid-range {kw_lower} project typically runs $5,000–$15,000 depending on materials and whether you hire a contractor. Get three local quotes for the best estimate."},
            {"q": f"Is {kw_lower} worth the investment?",
             "a": f"Most homeowners recoup 60–70% of {kw_lower} costs at resale, and the daily comfort improvement is significant. Focus on quality basics over luxury upgrades for the best return."},
        ],
        "Budget & Planning": [
            {"q": f"What's the biggest hidden cost in this project?",
             "a": "Permit fees, unexpected structural issues, and temporary living adjustments often surprise homeowners. Budget 10–20% above your estimate for contingencies."},
            {"q": f"How can I reduce costs without cutting corners?",
             "a": "Do your own demolition, source materials during sales, keep the existing layout to avoid plumbing/electrical moves, and save the pro budget for the work that matters most."},
        ],
        "Flooring & Tile": [
            {"q": f"What's the most durable option for {kw_lower}?",
             "a": "Porcelain tile and luxury vinyl plank top the durability charts for most rooms. The right choice depends on your room's moisture exposure, traffic level, and subfloor condition."},
            {"q": f"Can I install {kw_lower} over existing flooring?",
             "a": "Some flooring goes directly over existing surfaces (LVP, laminate), while others need bare subfloor (tile, hardwood). Check your specific product requirements and subfloor condition first."},
        ],
        "Painting & Walls": [
            {"q": f"Do I need to prime before painting?",
             "a": "Yes, if you're covering dark colors, stains, or new drywall. For repaints in similar colors on clean, intact surfaces, a quality paint-and-primer combo usually works fine."},
            {"q": f"How many coats of paint do I actually need?",
             "a": "Two coats is the standard for good coverage and durability. One coat rarely looks right, and three is only needed over dark colors or with very light-colored paint."},
        ],
        "Outdoor & Landscaping": [
            {"q": f"Do I need a permit for this project?",
             "a": "Permit requirements vary by municipality. Generally, structures over a certain height or size, anything near property lines, and electrical/plumbing work require permits. Call your local building department to check."},
            {"q": f"What's the best time of year for this project?",
             "a": "Spring and fall offer the best weather for most outdoor projects. Avoid extreme heat, freezing temperatures, and the rainy season in your area. Many contractors offer off-season discounts."},
        ],
        "Plumbing & Electrical": [
            {"q": f"Should I DIY this or hire a licensed professional?",
             "a": "Basic tasks like replacing a faucet or outlet cover are DIY-friendly. Anything involving main lines, gas, load-bearing walls, or your electrical panel should go to a licensed pro — it's a safety and code issue."},
            {"q": f"How do I find a reliable plumber or electrician?",
             "a": "Ask neighbors for referrals, check reviews on multiple platforms, verify their license and insurance, and always get at least three written quotes before deciding."},
        ],
        "Basement & Attic": [
            {"q": f"Do I need a permit to finish this space?",
             "a": "Almost certainly yes. Finishing a basement or attic into livable space requires permits for framing, electrical, plumbing, and egress. Skipping permits creates problems at resale."},
            {"q": f"What about moisture problems?",
             "a": "Address any moisture issues before finishing. This means proper exterior grading, waterproofing, a sump pump if needed, and a good dehumidifier. Finishing over a wet problem guarantees mold."},
        ],
        "Tools & Materials": [
            {"q": f"What should I buy first on a limited budget?",
             "a": "Start with a quality cordless drill/driver, a good tape measure, a level, safety glasses, and a utility knife. These five tools cover 80% of basic home projects."},
            {"q": f"Is it worth buying premium tools?",
             "a": "For tools you'll use often (drill, circular saw), buy mid-range or better. For specialty tools you'll use once or twice, rent or buy budget versions."},
        ],
    }

    cat_options = cost_qs.get(category, cost_qs["Budget & Planning"])
    faqs.append(cat_options[h % len(cat_options)])

    # Question 2: DIY feasibility — specific to keyword
    if any(w in kw_lower for w in ['install', 'repair', 'replace', 'build', 'remodel']):
        faqs.append({
            "q": f"What tools do I need for this project?",
            "a": f"The exact tools depend on your approach, but most {kw_lower} projects need basic measuring and marking tools, safety gear, and the category-specific tools covered in the article above."
        })
    else:
        faqs.append({
            "q": "Can a beginner handle this project?",
            "a": "With proper research, the right tools, and realistic expectations about timeline, many first-timers succeed. Start with a small area to build confidence before tackling the main project."
        })

    # Question 3: Timeline or common mistake
    if h % 2 == 0:
        faqs.append({
            "q": "What's the most common mistake to avoid?",
            "a": "Skipping proper preparation is the number-one mistake. Whether it's surface prep, measuring twice, or reading the full instructions first — rushing the setup phase causes most DIY failures."
        })
    else:
        faqs.append({
            "q": "How long should I expect this project to take?",
            "a": "A focused DIYer working weekends should budget 2–3x the time a pro would take. Factor in supply runs, learning curves, and the inevitable re-dos. Better to plan generously than rush."
        })

    return faqs


def generate_image_prompt(title, keyword, category):
    """Generate a photorealistic image prompt — no AI artifacts, ICP-aware."""
    kw_lower = keyword.lower()

    # Build scene elements based on keyword/category
    setting = "a well-lit suburban home"
    subject = ""
    details = ""
    style = "natural lighting, shot on a Canon EOS R5 with a 35mm lens, shallow depth of field, editorial photography style"

    if 'bathroom' in kw_lower:
        if 'remodel' in kw_lower or 'renovation' in kw_lower:
            subject = "a bathroom mid-renovation"
            details = "with partially installed white subway tile, new fixtures still in packaging nearby, blue painter's tape on the edges, and a level tool resting on the vanity"
        elif 'tile' in kw_lower:
            subject = "a professional tile installer"
            details = "kneeling on a bathroom floor laying large-format porcelain tiles, with a wet saw visible in the background, spacers between tiles, and thinset mortar being applied"
        elif 'vanity' in kw_lower:
            subject = "a freshly installed floating bathroom vanity"
            details = "with a white quartz countertop, undermount sink, polished chrome faucet, and the tools used for installation still visible on the floor nearby"
        elif 'shower' in kw_lower:
            subject = "a modern walk-in shower under construction"
            details = "with waterproof membrane visible on one wall, large format tiles being set on another, a linear drain installed in the floor, and professional tools nearby"
        else:
            subject = "a clean, updated bathroom"
            details = "with white subway tile, a floating vanity with a vessel sink, brushed nickel fixtures, and natural light streaming through a frosted window"

    elif 'kitchen' in kw_lower:
        if 'cabinet' in kw_lower:
            subject = "kitchen cabinets being installed"
            details = "with a carpenter using a level to align white shaker-style upper cabinets, clamps holding them in place, and a drill on the countertop"
        elif 'countertop' in kw_lower or 'granite' in kw_lower or 'quartz' in kw_lower:
            subject = "a stone countertop being templated"
            details = "in a mid-renovation kitchen with a fabricator measuring a granite slab against new white cabinets, blue tape marking the cut lines"
        else:
            subject = "a kitchen mid-renovation"
            details = "with new cabinets partially installed, exposed plumbing visible, a miter saw on the floor, and natural light from a window over the sink area"

    elif 'floor' in kw_lower or 'tile' in kw_lower or 'hardwood' in kw_lower or 'laminate' in kw_lower or 'vinyl' in kw_lower or 'carpet' in kw_lower:
        if 'hardwood' in kw_lower:
            subject = "a homeowner installing hardwood flooring"
            details = "kneeling on a subfloor, fitting tongue-and-groove oak planks with a rubber mallet, with boxes of uninstalled planks stacked nearby and a tape measure on the floor"
        elif 'laminate' in kw_lower or 'vinyl' in kw_lower or 'lvp' in kw_lower:
            subject = "luxury vinyl plank flooring being installed"
            details = "in a bright living room, with click-lock planks being joined together, a utility knife and straightedge nearby, and the transition between old and new flooring visible"
        elif 'carpet' in kw_lower:
            subject = "a room with new carpet being stretched"
            details = "using a carpet stretcher and knee kicker, with the carpet padding visible at the edges and tack strips along the wall"
        elif 'grout' in kw_lower:
            subject = "a close-up of grout being applied between floor tiles"
            details = "with a rubber float spreading epoxy grout at a 45-degree angle, clean tile edges visible, and a bucket of grout and sponge nearby"
        else:
            subject = "a professional installing floor tiles"
            details = "in a spacious room with natural light, using a notched trowel to spread thinset, with tile spacers and a level tool visible"

    elif 'paint' in kw_lower or 'stain' in kw_lower:
        if 'exterior' in kw_lower or 'house' in kw_lower:
            subject = "the exterior of a two-story suburban home being painted"
            details = "with a painter on a ladder applying fresh white paint to wood siding, drop cloths protecting the foundation plantings, and a paint sprayer on the ground"
        elif 'cabinet' in kw_lower:
            subject = "kitchen cabinet doors being painted"
            details = "laid flat on sawhorses in a garage, with a HVLP sprayer applying smooth white paint, some doors drying on a rack in the background"
        else:
            subject = "a bright bedroom being freshly painted"
            details = "with a roller applying warm gray paint to one wall, crisp blue painter's tape along the trim, a drop cloth on the hardwood floor, and a paint tray nearby"

    elif 'drywall' in kw_lower or 'plaster' in kw_lower:
        subject = "a homeowner mudding drywall seams"
        details = "using a wide taping knife to smooth joint compound over paper tape, with a hawk in the other hand, bare drywall sheets visible, and sanding dust in the air"

    elif 'deck' in kw_lower:
        if 'build' in kw_lower or 'diy' in kw_lower:
            subject = "a homeowner building a pressure-treated wood deck"
            details = "in a suburban backyard, attaching deck boards with a cordless drill, with a framing square, level, and stacks of lumber visible nearby"
        else:
            subject = "a freshly completed backyard deck"
            details = "with composite decking in a warm brown tone, aluminum balusters, built-in bench seating, attached to a craftsman-style home with a green lawn"

    elif 'fence' in kw_lower:
        subject = "a cedar privacy fence being built"
        details = "in a suburban backyard, with a post hole digger next to a freshly set post, horizontal rails being nailed, and stacks of pickets leaning against the partially completed fence"

    elif 'patio' in kw_lower or 'paver' in kw_lower:
        subject = "a patio being laid with concrete pavers"
        details = "in a suburban backyard, with a herringbone pattern taking shape on a compacted gravel base, a plate compactor nearby, and polymeric sand being swept into joints"

    elif 'plumb' in kw_lower or 'pipe' in kw_lower or 'drain' in kw_lower or 'leak' in kw_lower:
        subject = "a homeowner working under a kitchen sink"
        details = "with a wrench adjusting PVC drain fittings, a flashlight illuminating the work area, plumber's tape and pipe fittings spread on the cabinet floor"

    elif 'water heater' in kw_lower or 'water heat' in kw_lower:
        subject = "a new tank water heater being installed"
        details = "in a utility closet, with copper supply lines being connected, a pipe wrench in use, and the old unit visible nearby waiting for removal"

    elif 'electric' in kw_lower or 'wiring' in kw_lower or 'circuit' in kw_lower or 'outlet' in kw_lower or 'cable' in kw_lower:
        subject = "an electrician installing a new outlet"
        details = "in a residential wall with exposed wiring visible in the open junction box, wire strippers and a voltage tester on a nearby step ladder"

    elif 'basement' in kw_lower:
        if 'finish' in kw_lower:
            subject = "a basement being finished"
            details = "with metal stud framing going up, fiberglass insulation batts between some studs, recessed lighting cans visible in the ceiling joists above, and a level leaning against the wall"
        elif 'waterproof' in kw_lower:
            subject = "a basement wall being waterproofed"
            details = "with a sump pump pit visible, drainage matting being applied to the concrete wall, and a dehumidifier running in the corner"
        else:
            subject = "a bright, freshly finished basement living space"
            details = "with luxury vinyl plank flooring, recessed lighting, light gray walls, and a mini kitchenette in the background"

    elif 'attic' in kw_lower or 'insulat' in kw_lower:
        subject = "an attic being insulated"
        details = "with blown-in cellulose insulation being applied between ceiling joists using a hose, the worker wearing a respirator and safety goggles, with kraft-faced batts visible on the walls"

    elif 'roof' in kw_lower:
        subject = "a suburban home getting a new roof"
        details = "with a roofing crew stripping old shingles, new underlayment partially rolled out, bundles of architectural shingles staged on the roof, and a dumpster below"

    elif 'window' in kw_lower:
        subject = "a replacement window being installed"
        details = "in a residential home, with the old window removed showing the rough opening, foam insulation being sprayed around the frame, and the new vinyl double-hung window ready to be set"

    elif 'door' in kw_lower:
        subject = "a new entry door being hung"
        details = "in the front of a craftsman-style home, with shims visible in the frame, a level being checked against the jamb, and the homeowner measuring the threshold"

    elif 'siding' in kw_lower:
        subject = "vinyl siding being installed on a home exterior"
        details = "with a worker snapping panels into the starter strip, a utility knife and tin snips on a scaffold platform, and house wrap visible where siding hasn't been applied yet"

    elif 'gutter' in kw_lower:
        subject = "seamless gutters being installed"
        details = "on the fascia of a suburban home, with a gutter machine visible on the ground below, the installer on a ladder securing hangers, and downspout components ready to be attached"

    elif 'tool' in kw_lower:
        subject = "a well-organized workshop pegboard wall"
        details = "with hand tools, power tools, a cordless drill, circular saw, levels, and clamps neatly arranged, a sturdy workbench below with a project in progress"

    elif 'water damage' in kw_lower or 'flood' in kw_lower or 'moisture' in kw_lower:
        subject = "a homeowner assessing water damage"
        details = "in a basement with a moisture meter pressed against a damp wall, dehumidifier running, and water stains visible on the lower portion of the drywall"

    elif 'mold' in kw_lower:
        subject = "mold being treated in a home"
        details = "with a section of drywall removed revealing mold on the studs, a HEPA air scrubber running, and the worker wearing protective equipment including an N95 respirator"

    elif 'crawl space' in kw_lower:
        subject = "a crawl space being encapsulated"
        details = "with thick white vapor barrier being installed over the dirt floor and up the foundation walls, a dehumidifier in place, and sealed vent covers visible"

    elif 'driveway' in kw_lower:
        subject = "a concrete driveway being poured"
        details = "in front of a suburban home, with workers smoothing wet concrete with a bull float, forms along the edges, and a concrete truck parked in the street"

    elif 'porch' in kw_lower:
        subject = "a front porch being rebuilt"
        details = "with new pressure-treated framing visible, composite decking boards being laid, and the craftsman-style home facade in the background"

    elif 'pergola' in kw_lower or 'gazebo' in kw_lower:
        subject = "a cedar pergola being assembled"
        details = "in a suburban backyard over a patio area, with the post-and-beam structure going up, a drill in use, and the homeowner consulting plans on their phone"

    elif 'landscap' in kw_lower or 'garden' in kw_lower or 'lawn' in kw_lower or 'yard' in kw_lower:
        subject = "a homeowner working on landscaping"
        details = "in a front yard, planting shrubs in a mulched bed along the foundation, with a wheelbarrow of compost, garden gloves, and a hand trowel visible"

    elif 'hvac' in kw_lower or 'heat pump' in kw_lower or 'furnace' in kw_lower or 'boiler' in kw_lower:
        subject = "an HVAC technician servicing a home system"
        details = "with the furnace panel open, a multimeter checking connections, refrigerant gauges visible, and the homeowner watching from the doorway"

    elif 'thermostat' in kw_lower:
        subject = "a smart thermostat being installed"
        details = "on a living room wall, with wires visible in the opened wall plate, wire labels attached, and the new thermostat unit ready to be mounted"

    elif 'retaining wall' in kw_lower:
        subject = "a retaining wall being built"
        details = "with interlocking concrete blocks being stacked in courses, gravel backfill being added behind the wall, a level on top, and a sloped yard visible"

    elif 'sprinkler' in kw_lower or 'irrigat' in kw_lower:
        subject = "a lawn irrigation system being installed"
        details = "with trenches dug in a front yard, PVC pipe and sprinkler heads being connected, a pipe cutter and glue nearby, and green grass on either side of the trench"

    elif 'pool' in kw_lower:
        subject = "a residential pool area under construction"
        details = "with gunite being applied to the pool shell, rebar visible on one end, plumbing lines coming in from the equipment pad, and a suburban home in the background"

    elif 'stucco' in kw_lower:
        subject = "stucco being applied to a home exterior"
        details = "with a mason using a hawk and trowel to apply the finish coat over wire mesh, scaffolding along the wall, and a mixer on the ground"

    elif 'wallpaper' in kw_lower:
        subject = "wallpaper being hung in a dining room"
        details = "with a pattern-matched seam being smoothed with a wallpaper brush, a plumb line on the next section of wall, and the paste tray on a folding table"

    elif 'epoxy' in kw_lower:
        subject = "an epoxy floor coating being applied"
        details = "in a residential garage with a roller spreading metallic gray epoxy, the floor partially coated showing the before and after, and a mixing bucket nearby"

    elif 'concrete' in kw_lower:
        subject = "a concrete surface being refinished"
        details = "with a worker using a concrete grinder on a patio slab, dust collection hose attached, and freshly ground smooth sections contrasting with the rough original"

    else:
        # Category-specific fallback scenes instead of one generic scene
        import hashlib
        h_img = int(hashlib.md5(keyword.encode()).hexdigest(), 16)
        cat_scenes = {
            "Kitchen & Bath Remodeling": [
                ("a homeowner measuring cabinet dimensions in a kitchen", "with a tape measure and notepad, new cabinet samples on the counter, morning light through a window above the sink"),
                ("a bright kitchen mid-renovation showing progress", "with new shaker cabinets on one wall and bare studs on the other, a level and drill on the counter, blue painter's tape along trim"),
                ("bathroom fixtures laid out on a clean countertop", "including a brushed nickel faucet, handles, a towel bar, and mounting hardware, with installation instructions visible"),
            ],
            "Budget & Planning": [
                ("a homeowner sitting at a kitchen table reviewing renovation plans", "with blueprints spread out, a laptop showing a spreadsheet, paint swatches, and a calculator, natural afternoon light"),
                ("a clipboard with a renovation cost estimate", "on a workbench next to a tape measure, pencil, and material samples, with a partially renovated room visible behind"),
                ("color-coded material samples arranged on a table", "including tile samples, paint swatches, flooring pieces, and hardware options, with price tags visible on each"),
            ],
            "Flooring & Tile": [
                ("a room showing the transition between old and new flooring", "with half the space covered in fresh flooring and the other half showing the subfloor, installation tools between them"),
                ("flooring material samples arranged in a fan pattern", "on a clean subfloor, showing different options side by side — hardwood, LVP, tile, and laminate — with a homeowner's hand reaching to compare"),
                ("a close-up of flooring being installed at a doorway transition", "showing the precision of the cut where two different floor materials meet, with a multi-tool and transition strip nearby"),
            ],
            "Painting & Walls": [
                ("a freshly painted room with one accent wall in progress", "showing the contrast between the old color and the new, a paint roller in a tray, crisp tape lines, and a drop cloth protecting the floor"),
                ("a homeowner comparing paint colors on a wall", "with multiple test patches painted in rectangles, paint cans below, a color fan deck in hand, in natural daylight"),
                ("painting supplies organized on a drop cloth", "including rollers, brushes of various sizes, painter's tape, a paint tray, and an open gallon of premium interior paint"),
            ],
            "Outdoor & Landscaping": [
                ("a suburban backyard project in progress", "with materials staged on the lawn, a homeowner consulting plans on a clipboard, tools organized on a portable workbench, green grass and mature trees"),
                ("a before-and-after view of a home's curb appeal improvement", "showing the front yard with fresh mulch beds, trimmed hedges, a power-washed walkway, and a newly painted front door"),
                ("a homeowner measuring outdoor space with a long tape measure", "in a sunny backyard, marking stakes in the ground, with lumber and hardware store bags nearby"),
            ],
            "Plumbing & Electrical": [
                ("a well-organized collection of plumbing and electrical parts", "laid out on a clean workbench — pipe fittings, wire nuts, outlets, a multimeter, and pipe wrenches — ready for a project"),
                ("a homeowner reading a how-to guide on a tablet", "in a utility room with exposed pipes and an electrical panel visible, a flashlight and basic tools nearby"),
                ("a close-up of hands connecting copper pipe fittings", "with a propane torch nearby, flux paste on the joint, and a fire-resistant cloth protecting the wall behind"),
            ],
            "Basement & Attic": [
                ("an unfinished basement with renovation planning marks on the walls", "chalk lines showing where framing will go, a laser level projecting a line, moisture meter readings noted on blue tape"),
                ("a partially finished basement showing different construction stages", "with framing complete on one wall, insulation installed on another, and bare concrete on the third, recessed light cans in the ceiling"),
                ("an attic space being evaluated for conversion", "with a tape measure extended floor to ridge, insulation visible between rafters, and a notepad listing renovation steps"),
            ],
            "Tools & Materials": [
                ("a well-organized garage workshop", "with a pegboard full of labeled tools, a clean workbench with a vise, overhead LED lighting, and material storage shelves"),
                ("a collection of essential home improvement tools", "arranged neatly on a workshop table — cordless drill, circular saw, level, speed square, utility knife, and safety glasses"),
                ("a homeowner's tool belt and safety gear", "laid out on a workbench including safety glasses, ear protection, work gloves, a dust mask, and a loaded tool belt"),
            ],
        }
        scenes = cat_scenes.get(category, cat_scenes["Budget & Planning"])
        subject, details = scenes[h_img % len(scenes)]

    prompt = (
        f"A photorealistic photograph of {subject} {details}. "
        f"The scene is set in {setting}. {style}. "
        f"No text overlays, no watermarks, no logos, no artificial lighting artifacts. "
        f"The image looks like it was taken by a professional home renovation photographer for an editorial magazine feature."
    )

    return prompt


def generate_external_links(keyword, category):
    """Return 2-3 authoritative, non-competing external link URLs per post."""
    kw_lower = keyword.lower()
    import hashlib
    h = int(hashlib.md5(keyword.encode()).hexdigest(), 16)

    # Authoritative sources by category
    cat_links = {
        "Kitchen & Bath Remodeling": [
            "https://www.tcnatile.com/",
            "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/irc/",
            "https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70",
            "https://www.epa.gov/lead",
            "https://www.epa.gov/watersense",
            "https://www.remodeling.hw.net/cost-vs-value/2025/",
            "https://www.ada.gov/law-and-regs/design-standards/",
        ],
        "Budget & Planning": [
            "https://www.consumerfinance.gov/",
            "https://www.remodeling.hw.net/cost-vs-value/2025/",
            "https://www.consumer.ftc.gov/articles/hiring-contractor",
            "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/irc/",
            "https://www.bls.gov/",
            "https://www.epa.gov/lead",
        ],
        "Flooring & Tile": [
            "https://www.tcnatile.com/",
            "https://www.epa.gov/lead",
            "https://www.epa.gov/asbestos",
            "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/irc/",
            "https://www.nwfa.org/",
            "https://www.ada.gov/law-and-regs/design-standards/",
        ],
        "Painting & Walls": [
            "https://www.epa.gov/lead",
            "https://www.epa.gov/indoor-air-quality-iaq/volatile-organic-compounds-impact-indoor-air-quality",
            "https://www.osha.gov/",
            "https://www.epa.gov/lead/renovation-repair-and-painting-program",
            "https://www.cpsc.gov/",
        ],
        "Outdoor & Landscaping": [
            "https://www.awc.org/",
            "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/irc/",
            "https://www.strongtie.com/",
            "https://www.epa.gov/watersense",
            "https://www.aarp.org/livable-communities/housing/",
            "https://www.usda.gov/",
        ],
        "Plumbing & Electrical": [
            "https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70",
            "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/irc/",
            "https://www.epa.gov/watersense",
            "https://www.osha.gov/",
            "https://www.ul.com/",
            "https://www.iapmo.org/",
        ],
        "Basement & Attic": [
            "https://www.epa.gov/radon",
            "https://www.epa.gov/mold",
            "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/irc/",
            "https://www.energy.gov/energysaver/insulation",
            "https://www.fema.gov/",
            "https://www.epa.gov/asbestos",
        ],
        "Tools & Materials": [
            "https://www.osha.gov/",
            "https://www.cpsc.gov/",
            "https://www.ul.com/",
            "https://www.ansi.org/",
            "https://www.epa.gov/lead",
        ],
    }

    # Keyword-specific overrides for common topics
    keyword_links = {}
    if 'water heater' in kw_lower or 'water heat' in kw_lower:
        keyword_links = {
            "https://www.energy.gov/energysaver/water-heating": True,
            "https://www.epa.gov/watersense": True,
        }
    elif 'mold' in kw_lower:
        keyword_links = {
            "https://www.epa.gov/mold": True,
            "https://www.cdc.gov/mold/": True,
        }
    elif 'radon' in kw_lower:
        keyword_links = {
            "https://www.epa.gov/radon": True,
            "https://www.who.int/news-room/fact-sheets/detail/radon-and-health": True,
        }
    elif 'lead' in kw_lower or 'paint removal' in kw_lower:
        keyword_links = {
            "https://www.epa.gov/lead": True,
            "https://www.epa.gov/lead/renovation-repair-and-painting-program": True,
        }
    elif 'asbestos' in kw_lower:
        keyword_links = {
            "https://www.epa.gov/asbestos": True,
            "https://www.osha.gov/asbestos": True,
        }
    elif 'permit' in kw_lower:
        keyword_links = {
            "https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/irc/": True,
        }
    elif 'insulation' in kw_lower or 'energy' in kw_lower:
        keyword_links = {
            "https://www.energy.gov/energysaver/insulation": True,
            "https://www.energystar.gov/": True,
        }
    elif 'mobile home' in kw_lower or 'manufactured home' in kw_lower:
        keyword_links = {
            "https://www.hud.gov/program_offices/housing/rmra/mhs/mhshome": True,
            "https://www.iapmo.org/": True,
        }
    elif 'accessib' in kw_lower or 'aging' in kw_lower or 'ada' in kw_lower:
        keyword_links = {
            "https://www.ada.gov/law-and-regs/design-standards/": True,
            "https://www.aarp.org/livable-communities/housing/": True,
        }
    elif 'roi' in kw_lower or 'value' in kw_lower or 'return' in kw_lower:
        keyword_links = {
            "https://www.remodeling.hw.net/cost-vs-value/2025/": True,
            "https://www.nar.realtor/": True,
        }

    # Build the final list: keyword-specific first, then fill from category pool
    selected = list(keyword_links.keys())
    pool = cat_links.get(category, cat_links["Budget & Planning"])
    for url in pool:
        if url not in selected:
            selected.append(url)
        if len(selected) >= 5:
            break

    # Pick 2-3 based on hash for deterministic variety
    count = 2 + (h % 2)  # 2 or 3
    if len(selected) > count:
        start = h % len(selected)
        picked = []
        for i in range(count):
            picked.append(selected[(start + i) % len(selected)])
        return picked
    return selected[:count]


def is_off_niche(kw_lower):
    """Return True if keyword is not genuinely about home improvement."""
    # Pharmaceutical/medical
    if re.search(r'\btolvaptan\b|\bsurgery\b|\bmedic\b|\bknee\b.*\breplacement\b|\bhip\b.*\breplacement\b', kw_lower):
        return True
    # City-specific (non-US-generic)
    if re.search(r'\bbrisbane\b|\bmelbourne\b|\bsydney\b|\blondon\b|\bmanchester\b|\btoronto\b|\bvancouver\b', kw_lower):
        return True
    # US city-specific (too narrow)
    if re.search(r'\bfort\s+collins\b|\bnew\s+jersey\b|\bchicago\b|\bhouston\b|\bphoenix\b|\bsan\s+diego\b|\batlanta\b|\bseattle\b|\bdenver\b|\bdallas\b|\baustin\b|\bportland\b', kw_lower):
        return True
    # Branded/commercial (specific company names)
    if re.search(r'\bcopeland\b|\brinnai\b|\brheem\b|\bao\s+smith\b|\blowes\b|\bhome\s+depot\b|\bmenards\b', kw_lower):
        return True
    # Insurance/finance unrelated
    if re.search(r'\binsurance\b|\bloan\b|\bpersonal\s+loan\b|\bmortgage\b|\bcredit\s+card\b', kw_lower):
        return True
    # Too vague / non-actionable
    if re.search(r'^do\s+tabs\b|^tab\s+cost', kw_lower):
        return True
    # Coastal kitchens (lifestyle, not improvement)
    if re.search(r'\bcoastal\s+kitchens\b', kw_lower):
        return True
    # IT certifications / exams
    if re.search(r'\baz-\d+\b|\bexam\b|\bcertification\b|\bcisco\b|\bmicrosoft\b', kw_lower):
        return True
    # US city/state-specific (too narrow for national blog)
    if re.search(r'\btuscaloosa\b|\bbirmingham\b|\bnashville\b|\bcharlotte\b|\braleigh\b|\bjacksonville\b|\btampa\b|\borlando\b|\bmiami\b|\bsan\s+antonio\b|\blas\s+vegas\b|\bsacramento\b|\bminneapolis\b|\bcleveland\b|\bcolumbus\b|\bindianapolis\b|\bmilwaukee\b|\bmemphis\b|\brichmond\b', kw_lower):
        return True
    # State abbreviations at end (e.g., "window tuscaloosa al")
    if re.search(r'\b[a-z]+\s+(al|ak|az|ar|ca|co|ct|de|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|mn|ms|mo|mt|ne|nv|nh|nj|nm|ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|va|wa|wv|wi|wy)\b$', kw_lower):
        return True
    # Finance/loans
    if re.search(r'\bpersonal\s+loan\b|\bcredit\s+score\b|\bfinancing\s+option\b|\bloans?\s+for\b', kw_lower):
        return True
    # Specific brands that aren't relevant
    if re.search(r'\bdouble\s+glazed\b', kw_lower):
        return True  # UK-specific term
    # Pharma / medical products
    if re.search(r'\bepclusa\b|\bsoliris\b|\bstelara\b|\bvasectomy\b|\badenoid\b|\bkaiser\b|\btolvaptan\b', kw_lower):
        return True
    # Tech / cloud / AI products
    if re.search(r'\bvertex\s+ai\b|\belastic\s+load\b|\bgpt\b|\bapi\s+cost\b|\belb\s+cost\b|\bpenetration\s+testing\b', kw_lower):
        return True
    # Advertising / commercial not home-related
    if re.search(r'\badvertis\b|\bcommercial\b(?!.*\bflooring\b|\b.*\bkitchen\b)|\btv\s+cost\b', kw_lower):
        return True
    # Automotive
    if re.search(r'\bspark\s+plug\b|\btransmission\b(?!.*\bline\b)|\bbrake\s+pad\b', kw_lower):
        return True
    # Tabs (browser / drug tabs)
    if re.search(r'\btabs?\s+cost\b', kw_lower):
        return True
    # Smart home might be relevant, but "smart home solar" and "security solutions" are too vague
    # Keep "smart home" only if paired with install/cost/diy
    if re.search(r'\bsmart\s+home\b', kw_lower) and not re.search(r'\binstall|\bcost|\bdiy|\bwiring|\bswitch|\bthermostat', kw_lower):
        return True

    # POSITIVE CHECK: if keyword doesn't contain ANY home improvement term, reject it
    home_terms = [
        'bathroom', 'kitchen', 'floor', 'tile', 'paint', 'wall', 'drywall',
        'deck', 'fence', 'patio', 'paver', 'landscap', 'garden', 'lawn',
        'roof', 'siding', 'gutter', 'window', 'door', 'porch', 'driveway',
        'plumb', 'pipe', 'drain', 'water heater', 'electric', 'wiring',
        'outlet', 'hvac', 'heat pump', 'furnace', 'boiler', 'thermostat',
        'basement', 'attic', 'crawl space', 'insulation', 'waterproof', 'mold',
        'foundation', 'sump', 'radon', 'tool', 'drill', 'saw', 'hammer',
        'remodel', 'renovati', 'home improvement', 'diy', 'repair', 'install',
        'replace', 'cabinet', 'countertop', 'granite', 'quartz', 'marble',
        'backsplash', 'sink', 'faucet', 'toilet', 'shower', 'tub', 'vanity',
        'stain', 'varnish', 'primer', 'caulk', 'sealant', 'grout',
        'carpet', 'hardwood', 'laminate', 'vinyl', 'lvp', 'subfloor', 'epoxy',
        'contractor', 'permit', 'budget', 'shed', 'garage', 'stucco', 'wallpaper',
        'leak', 'water damage', 'flood', 'moisture', 'retaining wall', 'concrete',
        'sprinkler', 'pool', 'composite', 'lumber', 'framing',
        'home value', 'curb appeal', 'exterior', 'interior',
        'closet', 'pantry', 'laundry', 'fireplace', 'chimney', 'handrail',
        'stair', 'railing', 'molding', 'trim', 'baseboard', 'shingle',
        'soffit', 'fascia', 'flashing', 'underlayment', 'vapor barrier',
        'dehumidifier', 'ventilat', 'duct', 'vent', 'appliance', 'dishwasher',
        'garbage disposal', 'range hood', 'water softener', 'septic',
        'house', 'home', 'room', 'ceiling', 'light', 'switch', 'panel',
        'breaker', 'build', 'pergola', 'gazebo',
    ]
    if not any(t in kw_lower for t in home_terms):
        return True
    # Beauty/personal care
    if re.search(r'\bbrazilian\s+wax|\bwax\w*\s+cost\b|\bmassage\b|\btattoo\b|\bbotox\b|\bhair\s+cost\b|\bnails?\s+cost\b', kw_lower):
        return True
    # Brand names that aren't home improvement terms
    if re.search(r'\btarr.?s\b|\bmenards\b', kw_lower):
        return True
    # US state names (too location-specific for national blog)
    if re.search(r'\bcolorado\b|\bcalifornia\b|\bflorida\b|\btexas\b|\bmichigan\b|\bohio\b|\bpennsylvania\b|\bgeorgia\b|\bvirginia\b|\bmaryland\b|\bmassachusetts\b|\bwisconsin\b|\bminnesota\b|\btennessee\b|\billinois\b|\bindiana\b', kw_lower):
        return True
    return False


def dedupe_further(keywords):
    """Additional deduplication + off-niche filtering."""
    # First, filter off-niche
    keywords = [kw for kw in keywords if not is_off_niche(kw['keyword'].lower())]

    seen_cores = {}
    result = []

    for kw in keywords:
        words = kw['keyword'].lower().split()
        # Remove common filler words for comparison
        core_words = sorted([w for w in words if w not in ('a', 'an', 'the', 'of', 'to', 'for', 'in', 'on', 'my', 'your', 'is', 'and', 'or', 'with', 'it', 'do', 'does', 'should', 'i', 'can')])
        core = ' '.join(core_words[:5])

        if core in seen_cores:
            existing = seen_cores[core]
            existing_cpc = float(existing['cpc']) if existing['cpc'] else 0
            new_cpc = float(kw['cpc']) if kw['cpc'] else 0
            if new_cpc > existing_cpc:
                idx = result.index(existing)
                result[idx] = kw
                seen_cores[core] = kw
        else:
            seen_cores[core] = kw
            result.append(kw)

    return result


def main():
    # ── 1. Load keywords ────────────────────────────────────────────
    kw_file = os.path.join(PROJECT_DIR, "hi-keywords.csv")
    with open(kw_file) as f:
        reader = csv.DictReader(f)
        keywords = list(reader)

    print(f"Loaded {len(keywords)} keywords")

    # ── 2. Further deduplicate ──────────────────────────────────────
    keywords = dedupe_further(keywords)
    print(f"After additional dedup: {len(keywords)} keywords")

    # ── 3. Load existing posts ──────────────────────────────────────
    blog_dir = os.path.join(PROJECT_DIR, "src", "content", "blog")
    existing_posts = []
    for fname in sorted(os.listdir(blog_dir)):
        if not fname.endswith('.md'):
            continue
        filepath = os.path.join(blog_dir, fname)
        with open(filepath) as f:
            content = f.read()

        # Parse frontmatter
        parts = content.split('---')
        if len(parts) < 3:
            continue
        fm = parts[1]

        post = {'slug': fname.replace('.md', ''), 'existing': True}
        for line in fm.split('\n'):
            line = line.strip()
            if line.startswith('title:'):
                post['title'] = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('description:'):
                post['description'] = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('category:'):
                post['category'] = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('date:'):
                date_str = line.split(':', 1)[1].strip().strip('"').strip("'")
                try:
                    post['date'] = datetime.strptime(date_str[:10], '%Y-%m-%d')
                except:
                    post['date'] = datetime(2026, 5, 10)
            elif line.startswith('hero_image_prompt:'):
                post['hero_image_prompt'] = line.split(':', 1)[1].strip().strip('"').strip("'")

        # Parse tags (multi-line YAML array)
        import yaml
        try:
            fm_data = yaml.safe_load(fm)
            post['tags'] = fm_data.get('tags', [])
            post['faq'] = fm_data.get('faq', [])
        except:
            post['tags'] = []
            post['faq'] = []

        existing_posts.append(post)

    existing_posts.sort(key=lambda p: p.get('date', datetime(2026, 5, 10)))
    print(f"Loaded {len(existing_posts)} existing posts")

    # ── 4. Categorize & assign pillars ──────────────────────────────
    for kw in keywords:
        kw['category'] = categorize_keyword(kw['keyword'])
        kw['pillar'] = assign_pillar(kw['keyword'], kw['category'])

    # Count per category
    cat_counts = defaultdict(int)
    for kw in keywords:
        cat_counts[kw['category']] += 1
    print("\nCategory distribution:")
    for cat in CATEGORIES:
        print(f"  {cat}: {cat_counts.get(cat, 0)}")

    # Count per pillar
    pillar_counts = defaultdict(int)
    for kw in keywords:
        pillar_counts[kw['pillar']] += 1
    print(f"\nPillar clusters: {len(pillar_counts)}")
    for p, c in sorted(pillar_counts.items(), key=lambda x: -x[1]):
        print(f"  {p}: {c}")

    # ── 5. Remove keywords already covered by existing posts ────────
    existing_slugs = {p['slug'] for p in existing_posts}
    existing_titles_lower = {p.get('title', '').lower() for p in existing_posts}
    existing_kw_stems = set()
    for p in existing_posts:
        # Extract core topic from slug
        slug_words = set(p['slug'].split('-'))
        existing_kw_stems.add(frozenset(slug_words))

    filtered_kws = []
    for kw in keywords:
        kw_words = set(kw['keyword'].lower().split())
        # Skip if keyword is very close to an existing post's slug words
        overlap = False
        for stem in existing_kw_stems:
            common = kw_words & stem
            if len(common) >= min(3, len(kw_words)):
                overlap = True
                break
        if not overlap:
            filtered_kws.append(kw)

    print(f"\nAfter removing existing coverage: {len(filtered_kws)} keywords")

    # ── 6. Select best 345 new keywords ─────────────────────────────
    # Score: CPC × volume / (difficulty + 1), prefer diversity across categories
    for kw in filtered_kws:
        cpc = float(kw['cpc']) if kw['cpc'] else 0
        vol = int(kw['search_volume']) if kw['search_volume'] else 0
        kd = int(kw['keyword_difficulty']) if kw['keyword_difficulty'] else 20
        kw['score'] = cpc * max(vol, 10) / (kd + 1)

    # Sort by score descending
    filtered_kws.sort(key=lambda x: x['score'], reverse=True)

    # Select with category balance — aim for proportional distribution
    # but ensure every category has at least 20 posts
    needed = TOTAL_POSTS - len(existing_posts)
    target_per_cat = defaultdict(int)

    # Count existing per category
    existing_cat_counts = defaultdict(int)
    for p in existing_posts:
        existing_cat_counts[p.get('category', 'Budget & Planning')] += 1

    # Target proportions (roughly)
    cat_weights = {
        "Kitchen & Bath Remodeling": 0.18,
        "Budget & Planning": 0.15,
        "Flooring & Tile": 0.13,
        "Painting & Walls": 0.10,
        "Outdoor & Landscaping": 0.15,
        "Plumbing & Electrical": 0.12,
        "Basement & Attic": 0.09,
        "Tools & Materials": 0.08,
    }

    for cat in CATEGORIES:
        total_target = int(TOTAL_POSTS * cat_weights.get(cat, 0.1))
        already = existing_cat_counts.get(cat, 0)
        target_per_cat[cat] = max(total_target - already, 15)

    # Adjust to fill exactly needed slots
    total_target = sum(target_per_cat.values())
    if total_target != needed:
        diff = needed - total_target
        # Distribute evenly among largest categories
        sorted_cats = sorted(target_per_cat.keys(), key=lambda c: target_per_cat[c], reverse=True)
        for i in range(abs(diff)):
            cat = sorted_cats[i % len(sorted_cats)]
            target_per_cat[cat] += 1 if diff > 0 else -1

    selected = []
    selected_per_cat = defaultdict(int)

    # First pass — fill each category up to its target
    for kw in filtered_kws:
        cat = kw['category']
        if selected_per_cat[cat] < target_per_cat[cat]:
            selected.append(kw)
            selected_per_cat[cat] += 1

    # Second pass — fill remaining from best scoring regardless of category
    remaining = needed - len(selected)
    if remaining > 0:
        used_keywords = {kw['keyword'] for kw in selected}
        for kw in filtered_kws:
            if kw['keyword'] not in used_keywords:
                selected.append(kw)
                selected_per_cat[kw['category']] += 1
                remaining -= 1
                if remaining <= 0:
                    break

    # If still short, pad with lower-scoring keywords
    if len(selected) < needed:
        used_keywords = {kw['keyword'] for kw in selected}
        for kw in filtered_kws:
            if kw['keyword'] not in used_keywords:
                selected.append(kw)
                if len(selected) >= needed:
                    break

    print(f"\nSelected {len(selected)} new keywords")
    print("New posts per category:")
    for cat in CATEGORIES:
        print(f"  {cat}: {selected_per_cat.get(cat, 0)} new + {existing_cat_counts.get(cat, 0)} existing = {selected_per_cat.get(cat, 0) + existing_cat_counts.get(cat, 0)}")

    # ── 7. Build post objects for new keywords ──────────────────────
    new_posts = []
    for kw in selected:
        title = generate_title(kw['keyword'])
        slug = generate_slug(title)
        desc = generate_description(title, kw['keyword'], kw['category'])
        tags = generate_tags(kw['keyword'], kw['category'], kw['pillar'])
        faq = generate_faq(kw['keyword'], kw['category'])
        image_prompt = generate_image_prompt(title, kw['keyword'], kw['category'])

        new_posts.append({
            'slug': slug,
            'title': title,
            'description': desc,
            'category': kw['category'],
            'pillar': kw['pillar'],
            'tags': tags,
            'faq': faq,
            'hero_image_prompt': image_prompt,
            'keyword': kw['keyword'],
            'search_volume': kw['search_volume'],
            'cpc': kw['cpc'],
            'keyword_difficulty': kw['keyword_difficulty'],
            'intent': kw.get('intent', 'informational'),
            'score': kw['score'],
            'existing': False,
        })

    # ── 8. Sequence: depth-first by pillar cluster ──────────────────
    # Group new posts by pillar
    pillar_groups = defaultdict(list)
    for post in new_posts:
        pillar_groups[post['pillar']].append(post)

    # Sort within each pillar by score (best first = pillar post, then supporting)
    for pillar in pillar_groups:
        pillar_groups[pillar].sort(key=lambda p: p['score'], reverse=True)

    # Order pillars by total value (sum of scores)
    pillar_order = sorted(pillar_groups.keys(),
                          key=lambda p: sum(post['score'] for post in pillar_groups[p]),
                          reverse=True)

    # Interleave: complete one pillar cluster, then the next
    # But mix in variety — after every 8-12 posts from one pillar, switch
    sequenced_new = []
    pillar_idx = {p: 0 for p in pillar_order}
    max_consecutive = 10

    while len(sequenced_new) < len(new_posts):
        made_progress = False
        for pillar in pillar_order:
            posts_in_pillar = pillar_groups[pillar]
            start = pillar_idx[pillar]
            if start >= len(posts_in_pillar):
                continue
            end = min(start + max_consecutive, len(posts_in_pillar))
            for i in range(start, end):
                sequenced_new.append(posts_in_pillar[i])
            pillar_idx[pillar] = end
            made_progress = True

        if not made_progress:
            break

    # ── 9. Merge existing + new, assign dates ───────────────────────
    # Existing posts keep their dates
    # New posts get dates starting from day after last existing post
    last_existing_date = max(p['date'] for p in existing_posts)
    next_date = last_existing_date + timedelta(days=1)
    posts_today = 0

    all_posts = []

    # Add existing posts first (already have dates)
    for i, post in enumerate(existing_posts):
        post['post_number'] = i + 1
        post['status'] = 'published'
        post['author'] = AUTHOR
        if 'pillar' not in post:
            post['pillar'] = assign_pillar(post.get('title', ''), post.get('category', ''))
        if 'keyword' not in post:
            post['keyword'] = post.get('slug', '').replace('-', ' ')
        if 'search_volume' not in post:
            post['search_volume'] = ''
        if 'cpc' not in post:
            post['cpc'] = ''
        if 'keyword_difficulty' not in post:
            post['keyword_difficulty'] = ''
        if 'intent' not in post:
            post['intent'] = 'informational'
        if 'hero_image_prompt' not in post or not post['hero_image_prompt']:
            post['hero_image_prompt'] = generate_image_prompt(
                post.get('title', ''), post.get('keyword', ''), post.get('category', ''))
        all_posts.append(post)

    # Add new posts with date assignment
    posts_today_count = 0
    for post in sequenced_new:
        if posts_today_count >= POSTS_PER_DAY:
            next_date += timedelta(days=1)
            posts_today_count = 0

        # Skip weekends (optional — remove if publishing 7 days/week)
        # while next_date.weekday() >= 5:  # Saturday=5, Sunday=6
        #     next_date += timedelta(days=1)

        post['date'] = next_date
        post['post_number'] = len(all_posts) + 1
        post['status'] = 'idea'
        post['author'] = AUTHOR
        all_posts.append(post)
        posts_today_count += 1

    print(f"\nTotal posts: {len(all_posts)}")
    print(f"Date range: {all_posts[0]['date'].strftime('%Y-%m-%d')} to {all_posts[-1]['date'].strftime('%Y-%m-%d')}")

    # ── 10. Build internal link candidates (chronological) ──────────
    slug_to_idx = {post['slug']: i for i, post in enumerate(all_posts)}
    for i, post in enumerate(all_posts):
        # STRICT: only link to posts with index < i (published before)
        candidates = []
        # First: same pillar posts (highest relevance)
        for j in range(i):
            prev = all_posts[j]
            if prev.get('pillar') == post.get('pillar') and prev['slug'] != post['slug']:
                candidates.append(prev['slug'])
        # Then: same category posts
        if len(candidates) < 8:
            for j in range(i):
                prev = all_posts[j]
                if prev.get('category') == post.get('category') and prev['slug'] not in candidates:
                    candidates.append(prev['slug'])
        # Then: recent cross-category posts
        if len(candidates) < 5:
            for j in range(max(0, i - 10), i):
                prev = all_posts[j]
                if prev['slug'] not in candidates:
                    candidates.append(prev['slug'])

        # Limit to 5, prefer most recent
        candidates = candidates[-5:] if len(candidates) > 5 else candidates
        # Final safety check: verify every candidate has index < i
        candidates = [c for c in candidates if slug_to_idx.get(c, i+1) < i]
        post['internal_link_candidates'] = candidates

    # ── 11. Generate image prompts for existing posts that need them ─
    for post in all_posts:
        if post.get('existing') and (not post.get('hero_image_prompt') or len(post.get('hero_image_prompt', '')) < 20):
            post['hero_image_prompt'] = generate_image_prompt(
                post.get('title', ''), post.get('keyword', ''), post.get('category', ''))

    # ── 12. Output CSV ──────────────────────────────────────────────
    output_file = os.path.join(PROJECT_DIR, "content-calendar-365.csv")
    fieldnames = [
        'post_number', 'publish_date', 'pillar', 'primary_keyword',
        'search_volume', 'cpc', 'keyword_difficulty', 'intent',
        'suggested_title', 'slug', 'description', 'category', 'tags',
        'internal_link_candidates', 'external_link_candidates',
        'hero_image_prompt', 'faq_seeds',
        'status', 'author',
    ]

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for post in all_posts:
            tags = post.get('tags', [])
            if isinstance(tags, list):
                tags_str = '; '.join(tags)
            else:
                tags_str = str(tags)

            links = post.get('internal_link_candidates', [])
            links_str = '; '.join(links)

            ext_links = generate_external_links(
                post.get('keyword', post.get('title', '')),
                post.get('category', ''))
            ext_links_str = '; '.join(ext_links)

            faq = post.get('faq', [])
            if isinstance(faq, list) and faq:
                faq_parts = []
                for item in faq:
                    if isinstance(item, dict):
                        faq_parts.append(f"Q: {item.get('q', '')} A: {item.get('a', '')}")
                faq_str = ' | '.join(faq_parts)
            else:
                faq_str = ''

            writer.writerow({
                'post_number': post.get('post_number', ''),
                'publish_date': post['date'].strftime('%Y-%m-%d'),
                'pillar': post.get('pillar', ''),
                'primary_keyword': post.get('keyword', ''),
                'search_volume': post.get('search_volume', ''),
                'cpc': post.get('cpc', ''),
                'keyword_difficulty': post.get('keyword_difficulty', ''),
                'intent': post.get('intent', ''),
                'suggested_title': post.get('title', ''),
                'slug': post.get('slug', ''),
                'description': post.get('description', ''),
                'category': post.get('category', ''),
                'tags': tags_str,
                'internal_link_candidates': links_str,
                'external_link_candidates': ext_links_str,
                'hero_image_prompt': post.get('hero_image_prompt', ''),
                'faq_seeds': faq_str,
                'status': post.get('status', 'idea'),
                'author': post.get('author', AUTHOR),
            })

    print(f"\nCalendar written to: {output_file}")

    # ── 13. Summary stats ───────────────────────────────────────────
    final_cat_counts = defaultdict(int)
    for post in all_posts:
        final_cat_counts[post.get('category', 'Unknown')] += 1

    print("\nFinal category distribution:")
    for cat in CATEGORIES:
        print(f"  {cat}: {final_cat_counts.get(cat, 0)}")

    final_pillar_counts = defaultdict(int)
    for post in all_posts:
        final_pillar_counts[post.get('pillar', 'unknown')] += 1

    print(f"\nPillar clusters used: {len(final_pillar_counts)}")
    for p, c in sorted(final_pillar_counts.items(), key=lambda x: -x[1]):
        print(f"  {p}: {c} posts")


if __name__ == '__main__':
    main()
