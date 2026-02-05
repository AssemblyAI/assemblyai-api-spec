# Migration Plan: Fern to Astro + Scalar

## Executive Summary

Migrate the AssemblyAI documentation site from Fern to a self-hosted Astro site on Vercel, using Starlight (Astro's official docs theme) for content pages and Scalar for the interactive API reference. Fern is removed entirely — the Fern SDKs are deprecated, so there are no dependencies to maintain.

---

## Current State

| Concern | Current Tool |
|---------|-------------|
| Documentation site | Fern Docs (`fern docs dev`, `fern generate --docs`) |
| API reference | Fern (auto-generated from OpenAPI specs) |
| SDK generation (Ruby, C#, Java) | Fern generators — **deprecated** |
| Content format | 402 MDX pages in `fern/pages/` |
| Custom components | React TSX (AudioPlayer, LanguageTable, PromptGenerator, PromptLibrary) |
| Styling | Custom CSS + custom fonts (ABCMonumentGrotesk, JetBrainsMono) |
| JS integrations | RudderStack analytics, Kapa AI search, Pylon chat, voice agent |
| Navigation | `docs.yml` (tabs: Documentation, API Reference, Cookbooks, FAQ) |
| Hosting | Fern-managed (`assemblyai.docs.buildwithfern.com` → `www.assemblyai.com/docs`) |

## Target State

| Concern | New Tool |
|---------|----------|
| Documentation site | **Astro + Starlight** |
| API reference | **Scalar** (embedded in Astro) |
| SDK generation | N/A — Fern SDKs deprecated |
| Content format | Same MDX pages (with minor adaptations) |
| Custom components | Astro components (port from React TSX) |
| JS integrations | **RudderStack + Pylon only** (Kapa and voice agent dropped) |
| Hosting | **Vercel** |

---

## Phase 0: Preparation & Proof of Concept

### 0.1 — Set up Astro + Starlight project

- Initialize an Astro project in a new `docs/` directory at the repo root
- Install Starlight: `npx astro add starlight`
- Configure `astro.config.mjs` with:
  - `base: '/docs'` (to match current URL structure under `/docs/`)
  - Site URL pointing to `www.assemblyai.com`
- Verify `pnpm dev` runs and serves a blank Starlight site

### 0.2 — Install and configure Scalar

- Install `@scalar/api-reference` package
- Create an Astro page at `src/pages/api-reference/index.astro` that renders the Scalar API reference UI
- Point Scalar at the existing OpenAPI specs:
  - `openapi.yml` (main API)
  - `usm-streaming.yml` (Universal Streaming)
  - `streaming-token.yml` (token endpoint)
  - `llm-gateway.yml` (LLM Gateway)
- Merge or federate specs if Scalar supports multi-spec, or create a combined spec
- Configure Scalar theming to match AssemblyAI brand colors (`#2545D3` light accent, `#df9844` dark accent, `#09060F` dark bg)

### 0.3 — Validate API reference parity

- Compare Fern's rendered API reference against Scalar's output
- Verify all endpoints are documented: files, transcripts (submit, get, getSentences, getParagraphs, getSubtitles, getRedactedAudio, wordSearch, list, delete), LLM Gateway (createChatCompletion, createSpeechUnderstanding), Streaming API
- Verify request/response examples render correctly
- Verify WebSocket/AsyncAPI streaming docs render (Scalar may need the OpenAPI representation rather than AsyncAPI directly)

---

## Phase 1: Content Migration

### 1.1 — Migrate MDX pages

The 402 MDX files in `fern/pages/` need to be moved to `docs/src/content/docs/`. Starlight uses file-based routing with frontmatter for metadata.

**Frontmatter transformation:**
```yaml
# Fern format (in docs.yml):
#   - page: Transcribe a pre-recorded audio file
#     path: pages/01-getting-started/transcribe-an-audio-file2.mdx
#     slug: /getting-started/transcribe-an-audio-file

# Starlight format (in the MDX file itself):
---
title: Transcribe a pre-recorded audio file
description: "..."  # from existing description frontmatter
sidebar:
  order: 1
---
```

**Migration steps:**
1. Write a migration script (`scripts/migrate-content.ts`) that:
   - Parses `fern/docs.yml` to extract the page → slug → title mapping
   - Copies each MDX file to the correct location in `docs/src/content/docs/` based on its slug
   - Adds/updates frontmatter with `title`, `description`, and `sidebar.order`
   - Preserves the `hidden: true` property as `sidebar.hidden: true` (or uses `draft: true`)
2. Run the script and verify all pages are accessible

**Key directory mapping:**
```
fern/pages/home.mdx                          → docs/src/content/docs/index.mdx
fern/pages/01-getting-started/...            → docs/src/content/docs/getting-started/...
fern/pages/02-speech-to-text/pre-recorded-audio/... → docs/src/content/docs/pre-recorded-audio/...
fern/pages/02-speech-to-text/universal-streaming/...→ docs/src/content/docs/universal-streaming/...
fern/pages/03-audio-intelligence/...         → docs/src/content/docs/speech-understanding/...
fern/pages/04-lemur/...                      → docs/src/content/docs/llm-gateway/...
fern/pages/05-guides/...                     → docs/src/content/docs/guides/...
fern/pages/06-integrations/...               → docs/src/content/docs/integrations/...
fern/pages/07-llm-gateway/...                → docs/src/content/docs/llm-gateway/...
fern/pages/07-use-cases/...                  → docs/src/content/docs/use-cases/...
fern/pages/08-concepts/...                   → docs/src/content/docs/concepts/...
fern/pages/08-speech-understanding/...       → docs/src/content/docs/speech-understanding/...
fern/pages/faq/...                           → docs/src/content/docs/faq/...
```

### 1.2 — Adapt MDX component syntax

Fern uses specific MDX components that need Starlight equivalents:

| Fern Component | Starlight Equivalent |
|---------------|---------------------|
| `<Info>` | `<Aside type="note">` (Starlight built-in) |
| `<Note>` | `<Aside type="note">` |
| `<Warning>` | `<Aside type="caution">` |
| `<Tip>` | `<Aside type="tip">` |
| `<Tab>` / `<Tabs>` | `<Tabs>` / `<TabItem>` (Starlight built-in) |
| `<CodeBlock>` / `<CodeBlocks>` | Starlight's built-in code fences with `title` attribute |
| `<Accordion>` / `<AccordionGroup>` | `<Details>` or custom Astro component |
| `<Card>` / `<CardGroup>` | Starlight `<Card>` / `<CardGrid>` |
| `<Frame>` | Standard `<img>` or custom wrapper |

**Migration approach:**
1. Write a codemod script (`scripts/transform-mdx.ts`) that does find-and-replace across all MDX files
2. Handle edge cases manually where the transformation isn't 1:1
3. Import Starlight components at the top of each MDX file that uses them

### 1.3 — Port custom React components to Astro

Four custom React components need to be ported:

1. **AudioPlayer** (`fern/assets/components/AudioPlayer.tsx`)
   - Simple HTML5 `<audio>` component — straightforward port to an Astro component
   - Place at `docs/src/components/AudioPlayer.astro`

2. **LanguageTable** (`fern/assets/components/LanguageTable.tsx`)
   - Grid display of supported languages — straightforward Astro component
   - Place at `docs/src/components/LanguageTable.astro`

3. **PromptGenerator** (`fern/assets/components/PromptGenerator.tsx`)
   - Interactive client-side component calling an external API
   - Keep as a React component with `client:load` directive in Astro (React integration)
   - Install `@astrojs/react`
   - Place at `docs/src/components/PromptGenerator.tsx`

4. **PromptLibrary** (`fern/assets/components/PromptLibrary.tsx`)
   - Complex interactive component with Supabase backend
   - Keep as a React component with `client:load` directive
   - Place at `docs/src/components/PromptLibrary.tsx`

### 1.4 — Configure navigation / sidebar

Starlight supports sidebar configuration in `astro.config.mjs`. Translate the `docs.yml` navigation structure:

```js
// astro.config.mjs
starlight({
  sidebar: [
    {
      label: 'Getting started',
      items: [
        { label: 'Overview', slug: '' },
        { label: 'Transcribe a pre-recorded audio file', slug: 'getting-started/transcribe-an-audio-file' },
        // ...
      ],
    },
    // ... mirror the full docs.yml structure
  ],
})
```

**Tabs implementation:**
Fern uses top-level tabs (Documentation, API Reference, Cookbooks, FAQ). In Astro/Starlight:
- Use Starlight's built-in tabbed navigation or a custom header component
- "API Reference" tab links to the Scalar-powered page
- "Playground", "Changelog", "Roadmap" remain external links
- Cookbooks and FAQ become sidebar sections or separate Starlight instances

---

## Phase 2: Styling & Branding

### 2.1 — Typography

- Copy font files from `fern/assets/` to `docs/public/fonts/`
  - `ABCMonumentGrotesk-*.woff2` (heading + body)
  - `JetBrainsMono-*.woff2` (code)
- Register fonts via CSS `@font-face` in a global stylesheet
- Configure Starlight's CSS custom properties to use these fonts

### 2.2 — Colors and theme

Translate the Fern color config into Starlight CSS custom properties:

```css
/* docs/src/styles/custom.css */
:root {
  --sl-color-accent: #2545D3;
  --sl-color-bg: #FFFFFF;
  --sl-color-border: #E5E5E5;
}
[data-theme='dark'] {
  --sl-color-accent: #df9844;
  --sl-color-bg: #09060F;
  --sl-color-border: #2A2522;
}
```

### 2.3 — Migrate custom CSS

- Port `fern/assets/custom-styles.css` (446 lines) to Starlight-compatible CSS
- Adapt selectors — Fern uses its own DOM structure; Starlight uses different class names
- Key styles to port:
  - Sidebar blur/transparency effects
  - Home page animations (`bigPulse`, `oppositePulse`)
  - Gradient card styling
  - Announcement banner
  - Header height (56px) and sidebar width (316px)

### 2.4 — Logo and favicon

- Copy `logo-light.svg`, `AssemblyAI_White.svg`, `favicon.png` to `docs/src/assets/` and `docs/public/`
- Configure in `astro.config.mjs`:
  ```js
  starlight({
    logo: {
      light: './src/assets/logo-light.svg',
      dark: './src/assets/AssemblyAI_White.svg',
      replacesTitle: true,
    },
    favicon: '/favicon.png',
  })
  ```

---

## Phase 3: JavaScript Integrations

Only RudderStack analytics and Pylon chat widget are carried forward. Kapa AI search and the voice agent widget are dropped.

### 3.1 — RudderStack analytics

- Inject via a custom Starlight `Head` component override:
  ```js
  starlight({
    components: {
      Head: './src/components/Head.astro',
    },
  })
  ```
- The custom `Head.astro` extends Starlight's default Head and appends the RudderStack inline script

### 3.2 — Pylon chat widget

- Also injected via the custom `Head.astro` component
- Loads the Pylon widget script asynchronously on page load
- Personalizes chat with user credentials from the dashboard API

### 3.3 — Redirect scripts

- `pre-recorded-audio-redirect.js` and `universal-3-pro-redirect.js` — convert to Vercel redirect rules in `vercel.json`

### 3.4 — Dropped integrations

The following are **not migrated**:
- `kapa.js` — Kapa AI search widget (Starlight has built-in Pagefind search)
- `voice-agent.js` — Voice agent button
- `scroll-highlighted-lines.js` — Starlight has built-in code highlighting
- `inject-legal-footer.js` — Port to an Astro layout component if still needed

---

## Phase 4: Redirects

### 4.1 — Migrate 100+ redirects to Vercel

Convert all redirects from the Fern `docs.yml` `redirects:` section into `vercel.json`:

```json
{
  "redirects": [
    {
      "source": "/docs/lemur/:path*",
      "destination": "/docs/llm-gateway/:path*",
      "permanent": true
    }
  ]
}
```

Vercel handles redirects at the edge, so they're fast and don't require the Astro runtime.

### 4.2 — Parameterized redirects

Vercel supports wildcard redirects via `:path*` syntax. Convert Fern's `:slug` patterns:
- `/docs/lemur/:slug` → `/docs/llm-gateway/:slug` becomes `/docs/lemur/:path*` → `/docs/llm-gateway/:path*`
- `/docs/audio-intelligence/:slug` → `/docs/:slug` becomes `/docs/audio-intelligence/:path*` → `/docs/speech-understanding/:path*`

---

## Phase 5: API Reference with Scalar

### 5.1 — Scalar integration approach

Create a dedicated Astro page at `src/pages/api-reference/index.astro` that renders the Scalar API reference:

```astro
<div id="api-reference"></div>
<script
  id="api-reference-script"
  type="application/json"
  data-url="/docs/openapi.yml"
  data-configuration={JSON.stringify({ spec: { url: '/docs/openapi.yml' } })}
></script>
<script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
```

This page has its own navigation bar matching the docs site header, linking back to the Starlight docs.

### 5.2 — Multi-spec handling

The current API reference covers multiple specs:
1. **Main API** (`openapi.yml`) — transcripts, files, LLM Gateway
2. **Streaming API** (`usm-streaming.yml`) — WebSocket streaming
3. **Streaming Token** (`streaming-token.yml`) — token generation
4. **LLM Gateway** (`llm-gateway.yml`) — chat completions

**Options:**
- **Merge specs** into a single OpenAPI file for a unified reference (recommended for UX consistency)
- **Separate pages** — one Scalar instance per spec, linked via tabs
- **Scalar sidebar grouping** — if Scalar supports multi-spec federation

### 5.3 — Spec overrides

The Fern-specific overrides (`openapi-overrides.yml`, `usm-streaming-overrides.yml`) are no longer needed. Instead:
- Use OpenAPI `tags` and `x-tagGroups` directly in the spec for endpoint organization
- Move relevant examples directly into the OpenAPI spec
- SDK-specific overrides are no longer relevant (Fern SDKs deprecated)

### 5.4 — API reference overview page

The current API reference includes a custom overview page (`pages/overview.mdx`). In Scalar:
- Use Scalar's description/introduction section (from the OpenAPI `info.description`)
- Or place the overview as a regular Astro page above the Scalar widget

### 5.5 — Scalar theming

Configure Scalar to match AssemblyAI branding:
```js
{
  theme: 'none',
  customCss: `
    :root {
      --scalar-color-1: #2545d3;
      --scalar-color-accent: #2545d3;
      --scalar-font: "MonumentGrotesk", sans-serif;
    }
    .dark-mode {
      --scalar-color-1: #df9844;
      --scalar-color-accent: #df9844;
      --scalar-background-1: #09060f;
    }
  `,
}
```

---

## Phase 6: CI/CD & Deployment on Vercel

### 6.1 — Update build scripts

Update `package.json`:
```json
{
  "scripts": {
    "dev": "astro dev --root docs",
    "build": "astro build --root docs",
    "preview": "astro preview --root docs",
    "lint": "spectral lint {openapi,asyncapi}.yml --ruleset .spectral.yml",
    "format": "prettier . --write --no-error-on-unmatched-pattern",
    "to-json": "pnpm js-yaml openapi.yml > openapi.json && pnpm js-yaml asyncapi.yml > asyncapi.json",
    "precommit": "pnpm lint && pnpm to-json && pnpm format"
  }
}
```

### 6.2 — Vercel project setup

1. Connect the GitHub repo to Vercel
2. Set root directory to `docs/`
3. Framework preset: Astro
4. Build command: `pnpm build`
5. Output directory: `dist`
6. Configure `vercel.json` with redirects and cache headers

### 6.3 — Update GitHub workflows

**Replace `publish-docs.yml`:**
- Vercel auto-deploys on push to `main` — no custom workflow needed
- Alternatively, use `vercel --prod` in a workflow if more control is needed

**Replace `preview-docs.yml`:**
- Vercel automatically creates preview deployments for every PR
- PR preview URLs are posted as comments by the Vercel GitHub integration

**Update `ci.yml`:**
- Remove `fern check` from the lint step (Fern is gone)
- Keep Spectral linting for OpenAPI specs
- Add `pnpm build` step to verify the Astro site builds cleanly

**Remove SDK workflows:**
- Delete `ruby-sdk.yml`, `csharp-sdk.yml`, `java-sdk.yml`, `postman.yml` (Fern SDKs deprecated)

### 6.4 — Remove Fern entirely

After migration is verified and live:
1. Delete the entire `fern/` directory:
   - `fern/fern.config.json`
   - `fern/generators.yml`
   - `fern/.definition/`
   - `fern/docs.yml`
   - `fern/pages/`
   - `fern/assets/`
   - `fern/*.js` (all integration scripts)
   - `fern/*-overrides.yml`
2. Remove `fern-api` from `package.json` devDependencies
3. Remove `fern check` from CI workflow
4. Remove `generate:fern-definition` script
5. Clean up `.spectral.yml` if any Fern-specific rules exist

### 6.5 — Custom domain

- Point `www.assemblyai.com/docs` to Vercel instead of Fern
- Add the domain in Vercel project settings
- Vercel handles SSL automatically
- Verify DNS propagation and test all redirects

---

## Phase 7: Testing & QA

### 7.1 — Content parity check

- Crawl both old and new sites to verify all pages exist
- Compare page titles, descriptions, and content
- Verify all internal links resolve correctly
- Check all images and assets load

### 7.2 — SEO validation

- Verify canonical URLs are set correctly (`assemblyai.com`)
- Check meta tags (title, description, og:image)
- Verify sitemap generation (`sitemap-index.xml` is auto-generated by Astro)
- Test redirect chains — no 404s for old URLs

### 7.3 — API reference validation

- Verify all endpoints are documented in Scalar
- Test "Try it" functionality if enabled
- Verify request/response examples match Fern's output
- Check code snippet generation (curl, Python, JavaScript, etc.)

### 7.4 — Cross-browser and mobile testing

- Test on Chrome, Firefox, Safari, Edge
- Verify responsive design on mobile/tablet
- Check dark mode toggle works correctly

### 7.5 — Performance

- Run Lighthouse on key pages
- Compare load times with Fern-hosted version
- Verify assets are properly cached and compressed
- Verify Vercel edge caching is working (font files should be immutable-cached)

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| SEO ranking drop from URL changes | High | Comprehensive redirects in `vercel.json`, preserve all URLs where possible |
| Broken internal links | Medium | Automated link checking in CI, crawl comparison |
| Missing content during migration | Medium | Migration script + diff comparison against `docs.yml` |
| Scalar doesn't support AsyncAPI/WebSocket docs | Medium | Use OpenAPI representation of streaming endpoints, or add custom docs page |
| Custom component breakage | Medium | Test PromptGenerator and PromptLibrary thoroughly — they have external dependencies (Supabase, Claude API) |
| Dropping Kapa search degrades search UX | Low | Starlight's built-in Pagefind provides full-text search; evaluate and add Algolia/Kapa later if needed |
| Custom font licensing | Low | Fonts are already self-hosted; just move files |

---

## Migration Order (Recommended)

1. **Phase 0** — Set up Astro + Scalar proof of concept, validate API reference (**done** — see `docs/` directory)
2. **Phase 2** — Get styling/branding right early for visual feedback
3. **Phase 1** — Migrate content (largest effort — 402 pages)
4. **Phase 3** — Port RudderStack + Pylon integrations
5. **Phase 4** — Configure redirects in `vercel.json`
6. **Phase 5** — Finalize Scalar API reference
7. **Phase 6** — Connect to Vercel, update CI/CD, remove Fern
8. **Phase 7** — Testing and QA
9. **Go-live** — DNS cutover from Fern to Vercel

---

## Estimated Scope

| Phase | Effort |
|-------|--------|
| Phase 0: Setup & PoC | Small — **done** |
| Phase 1: Content migration (402 pages + components) | Large |
| Phase 2: Styling & branding | Medium |
| Phase 3: JS integrations (RudderStack + Pylon only) | Small |
| Phase 4: Redirects (100+ rules in vercel.json) | Small |
| Phase 5: Scalar API reference | Medium |
| Phase 6: CI/CD + Fern removal | Small |
| Phase 7: Testing & QA | Medium |
