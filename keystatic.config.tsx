import { config, fields, collection } from "@keystatic/core";

const categories = [
  "Kitchen & Bath Remodeling",
  "Budget & Planning",
  "Flooring & Tile",
  "Painting & Walls",
  "Outdoor & Landscaping",
  "Plumbing & Electrical",
  "Basement & Attic",
  "Tools & Materials",
] as const;

export default config({
  storage: { kind: "local" },
  ui: {
    brand: { name: "Miter House" },
  },
  collections: {
    blog: collection({
      label: "Blog Posts",
      slugField: "title",
      path: "src/content/blog/*",
      format: { contentField: "content" },
      schema: {
        title: fields.slug({
          name: { label: "Title", validation: { length: { max: 70 } } },
        }),
        description: fields.text({
          label: "Meta Description",
          validation: { isRequired: true, length: { min: 120, max: 165 } },
        }),
        author: fields.text({
          label: "Author",
          defaultValue: "Daniel Ware",
          validation: { isRequired: true },
        }),
        category: fields.select({
          label: "Category",
          options: categories.map((c) => ({ label: c, value: c })),
          defaultValue: "Kitchen & Bath Remodeling",
        }),
        tags: fields.array(fields.text({ label: "Tag" }), {
          label: "Tags",
          itemLabel: (props) => props.value,
        }),
        date: fields.date({
          label: "Publish Date",
          validation: { isRequired: true },
        }),
        updated: fields.date({ label: "Last Updated" }),
        hero_image: fields.image({
          label: "Hero Image",
          directory: "public/images/posts",
          publicPath: "/images/posts/",
        }),
        hero_image_prompt: fields.text({
          label: "Hero Image Prompt",
          description: "AI prompt for generating the hero image",
        }),
        faq: fields.array(
          fields.object({
            q: fields.text({ label: "Question", validation: { isRequired: true } }),
            a: fields.text({ label: "Answer", multiline: true, validation: { isRequired: true } }),
          }),
          {
            label: "FAQ",
            itemLabel: (props) => props.fields.q.value,
          }
        ),
        draft: fields.checkbox({ label: "Draft", defaultValue: false }),
        content: fields.markdoc({
          label: "Content",
          extension: "md",
        }),
      },
    }),
    authors: collection({
      label: "Authors",
      slugField: "name",
      path: "src/content/authors/*",
      format: { contentField: "content" },
      schema: {
        name: fields.slug({
          name: { label: "Name" },
        }),
        bio: fields.text({
          label: "Bio",
          multiline: true,
          validation: { isRequired: true },
        }),
        avatar: fields.image({
          label: "Avatar",
          directory: "public/images/authors",
          publicPath: "/images/authors/",
        }),
        externalUrl: fields.text({ label: "External URL" }),
        content: fields.markdoc({
          label: "Content",
          extension: "md",
        }),
      },
    }),
  },
});
