import { getCollection, type CollectionEntry } from "astro:content";

export type Post = CollectionEntry<"blog">;
export type Author = CollectionEntry<"authors">;

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

export const slugify = (s: string) =>
  s
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

export function categoryPath(c: string) {
  return `/category/${slugify(c)}/`;
}
export function tagPath(t: string) {
  return `/tag/${slugify(t)}/`;
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
