import { getCollection, type CollectionEntry } from "astro:content";

export type Post = CollectionEntry<"blog">;
export type Author = CollectionEntry<"authors">;
export type Category = CollectionEntry<"categories">;
export type Tag = CollectionEntry<"tags">;

export async function getSortedPosts(): Promise<Post[]> {
  const posts = await getCollection("blog");
  return posts.sort(
    (a, b) => b.data.date.getTime() - a.data.date.getTime()
  );
}

export async function getAuthorById(id: string): Promise<Author | undefined> {
  const authors = await getCollection("authors");
  return authors.find((a) => a.id === id);
}

export async function getAllAuthors(): Promise<Author[]> {
  return getCollection("authors");
}

export async function getCategoryById(id: string): Promise<Category | undefined> {
  const categories = await getCollection("categories");
  return categories.find((c) => c.id === id);
}

export async function getAllCategories(): Promise<Category[]> {
  return getCollection("categories");
}

export async function getTagById(id: string): Promise<Tag | undefined> {
  const tags = await getCollection("tags");
  return tags.find((t) => t.id === id);
}

export async function getAllTags(): Promise<Tag[]> {
  return getCollection("tags");
}

export async function getCategoryName(slug: string): Promise<string> {
  const cat = await getCategoryById(slug);
  return cat?.data.name || slug;
}

export async function getTagName(slug: string): Promise<string> {
  const tag = await getTagById(slug);
  return tag?.data.name || slug;
}

export async function buildCategoryMap(): Promise<Map<string, Category>> {
  const categories = await getAllCategories();
  return new Map(categories.map((c) => [c.id, c]));
}

export async function buildTagMap(): Promise<Map<string, Tag>> {
  const tags = await getAllTags();
  return new Map(tags.map((t) => [t.id, t]));
}

export const slugify = (s: string) =>
  s
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

export function categoryPath(slug: string) {
  return `/category/${slug}/`;
}
export function tagPath(slug: string) {
  return `/tag/${slug}/`;
}
export function authorPath(a: string) {
  return `/author/${slugify(a)}/`;
}
export function postPath(p: Post) {
  return `/blog/${p.id}/`;
}

export function uniqueCategories(posts: Post[]) {
  return [...new Set(posts.map((p) => p.data.category))].sort();
}
export function uniqueTags(posts: Post[]) {
  return [...new Set(posts.flatMap((p) => p.data.tags))].sort();
}

export function readingTime(body: string | undefined) {
  const words = (body || "").trim().split(/\s+/).length;
  return Math.max(1, Math.round(words / 200));
}

export function relatedPosts(current: Post, all: Post[], n: number) {
  const scored = all
    .filter((p) => p.id !== current.id)
    .map((p) => {
      let score = p.data.category === current.data.category ? 2 : 0;
      score += p.data.tags.filter((t) =>
        current.data.tags.includes(t)
      ).length;
      return { p, score };
    })
    .sort(
      (a, b) =>
        b.score - a.score ||
        b.p.data.date.getTime() - a.p.data.date.getTime()
    );
  return scored.slice(0, n).map((s) => s.p);
}

export function formatDate(d: Date, locale = "en-US") {
  return d.toLocaleDateString(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}
