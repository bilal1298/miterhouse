import { z, defineCollection } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string().max(70),
    description: z.string().min(120).max(165),
    author: z.string(),
    category: z.string(),
    tags: z.array(z.string()).min(2).max(6),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    hero_image: z.string().optional(),
    hero_image_prompt: z.string().optional(),
    faq: z
      .array(z.object({ q: z.string(), a: z.string() }))
      .optional(),
    draft: z.boolean().default(false),
  }),
});

const authors = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/authors" }),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
    avatar: z.string().optional(),
    externalUrl: z.string().optional(),
  }),
});

const categories = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/categories" }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
  }),
});

const tags = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/tags" }),
  schema: z.object({
    name: z.string(),
    description: z.string().optional(),
  }),
});

export const collections = { blog, authors, categories, tags };
