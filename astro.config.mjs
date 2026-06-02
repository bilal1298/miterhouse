import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://miterhouse.com",
  output: "static",
  integrations: [sitemap()],
  markdown: {
    shikiConfig: { theme: "github-light" },
  },
});
