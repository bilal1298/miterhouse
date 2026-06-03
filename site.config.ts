export const siteConfig = {
  // ── Core identity ──────────────────────────────────────────────
  name: "Miter House",
  tagline: "Practical home improvement guides from someone who's done it wrong first.",
  description:
    "Miter House publishes no-fluff home improvement guides — real costs, real steps, real trade-offs — written for DIYers and budget-conscious homeowners.",
  siteUrl: "https://miterhouse.com",
  language: "en",
  locale: "en_US",

  // ── Niche & audience ───────────────────────────────────────────
  niche: "home improvement",
  audience: "US homeowners — DIYers and budget-conscious renovators",
  brandVoice:
    "Straightforward, experienced, and practical. Like a neighbor who's done the project before — gives you the real steps, warns you about the gotchas, skips the filler.",

  // ── Categories ─────────────────────────────────────────────────
  categories: [
    "Kitchen & Bath Remodeling",
    "Budget & Planning",
    "Flooring & Tile",
    "Painting & Walls",
    "Outdoor & Landscaping",
    "Plumbing & Electrical",
    "Basement & Attic",
    "Tools & Materials",
  ] as const,

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

  // ── Author persona(s) ─────────────────────────────────────────
  authors: {
    "daniel-ware": {
      name: "Daniel Ware",
      slug: "daniel-ware",
      bio: "Daniel Ware has spent over a decade tackling home improvement projects — from gutting and refinishing basements to rebuilding decks and retiling bathrooms. He learned most of what he knows the hard way: by making mistakes on his own house before getting it right. At Miter House, he writes the kind of practical, no-fluff guides he wished he'd had when starting out.",
      avatar: "/images/authors/daniel-ware.jpg",
      // Guest-post dofollow link slot — populated when a placement is sold
      externalUrl: "",
    },
  },
  defaultAuthor: "daniel-ware",

  // ── Navigation ─────────────────────────────────────────────────
  nav: [
    { label: "Home", href: "/" },
    { label: "Blog", href: "/blog/" },
    { label: "About", href: "/about/" },
    { label: "Write for Us", href: "/write-for-us/" },
    { label: "Contact", href: "/contact/" },
  ],

  // ── Theme (GATHER editorial tokens — drives CSS variables) ────
  theme: {
    paper: "#F6F1E9",
    paper2: "#EFE8DC",
    paper3: "#E7DECF",
    ink: "#1B1916",
    inkSoft: "#4B463E",
    muted: "#908779",
    line: "#D8CFBF",
    accent: "#BB4626",
    accentDeep: "#8F3318",
    fontDisplay: '"Fraunces", Georgia, serif',
    fontRead: '"Newsreader", Georgia, serif',
    fontLabel: '"Hanken Grotesk", system-ui, sans-serif',
    maxWidth: "1240px",
    googleFontsHref:
      "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,400..900&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&family=Hanken+Grotesk:wght@400;500;600;700;800&display=swap",
  },

  // ── Monetization ───────────────────────────────────────────────
  adsense: {
    publisherId: "ca-pub-XXXXXXXXXXXXXXXX", // replace after approval
    slots: {
      inContent: "XXXXXXXXXX",
      sidebar: "XXXXXXXXXX",
      belowHeader: "XXXXXXXXXX",
    },
  },

  // ── Contact & social ───────────────────────────────────────────
  email: "hello@miterhouse.com",
  social: {
    twitter: "",
    facebook: "",
    pinterest: "",
  },

  // ── Publishing ─────────────────────────────────────────────────
  postsPerPage: 12,
  publishCadencePerDay: 2,
  wordRange: "1200-2200",
} as const;

export type Category = (typeof siteConfig.categories)[number];
