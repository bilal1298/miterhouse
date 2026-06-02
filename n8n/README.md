# n8n Workflows — Miter House

Two workflows to import into your self-hosted n8n instance.

## 1. Content Planner (`planner-workflow.json`)

**Trigger:** Manual
**Purpose:** Generate new post ideas for a pillar cluster using DataForSEO + AI
**Output:** Appends rows to the Google Sheet with `status: idea`

### Setup
1. Import the JSON in n8n (Settings > Import from file)
2. Configure credentials:
   - **DataForSEO** — HTTP Basic Auth (login + password from your DataForSEO account)
   - **Google Sheets** — OAuth2 (needs access to the Content Queue sheet)
   - **Anthropic** — API key for Claude
3. Edit the "Set Pillar Config" node to set the pillar topic and number of ideas
4. Run manually whenever you want to seed a new cluster

## 2. Content Publisher (`publisher-workflow.json`)

**Trigger:** Schedule (every 12 hours = max 2 posts/day)
**Purpose:** Pick up `ready` rows, generate full posts, commit to GitHub
**Output:** Publishes `.md` files to the repo; updates Sheet status

### Setup
1. Import the JSON in n8n
2. Configure credentials:
   - **Google Sheets** — OAuth2 (same as Planner)
   - **Anthropic** — API key for Claude
   - **GitHub** — HTTP Header Auth with `Authorization: Bearer <your-token>`
3. In the "Commit to GitHub" node, replace `OWNER/REPO` with your actual GitHub path
4. Activate the workflow

### Human Review Gate

The review gate is built into the Sheet workflow, not n8n itself:

1. **Planner** outputs rows with `status: idea`
2. A human reviews ideas and flips promising ones to `status: ready`
3. **Publisher** only picks up `ready` rows
4. After publishing, status becomes `published` with the live URL

This ensures no content goes live without human approval.

### Error Handling

If the Publisher encounters an error (bad AI output, GitHub API failure, etc.):
- The row's status is set to `error`
- The error message is written to the `notes` column
- The workflow continues on the next scheduled run with the next `ready` row

## Sheet Structure

| Column | Purpose |
|--------|---------|
| status | `idea` → `ready` → `published` (or `error`) |
| pillar | Topical cluster name |
| primary_keyword | The target query |
| search_volume | Monthly searches |
| cpc | Cost per click ($) |
| difficulty | Keyword difficulty (0-100) |
| intent | informational / commercial / how-to |
| suggested_title | Working title |
| category | Site category |
| slug | URL slug |
| live_url | Populated after publishing |
| notes | Error messages, dates, etc. |
