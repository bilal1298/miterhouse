import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

const isDev = process.argv.includes("dev");

const integrations = [sitemap()];
let adapter;

if (isDev) {
  const { default: react } = await import("@astrojs/react");
  const { default: keystatic } = await import("@keystatic/astro");
  const { default: node } = await import("@astrojs/node");
  integrations.push(react(), keystatic());
  adapter = node({ mode: "standalone" });
}

export default defineConfig({
  site: "https://miterhouse.com",
  adapter,
  integrations,
  markdown: {
    shikiConfig: { theme: "github-light" },
  },
});
