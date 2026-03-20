# AssemblyAI Docs MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) server that gives AI coding assistants access to AssemblyAI's documentation and API reference.

## How It Works

The server pre-processes AssemblyAI's docs (MDX files + OpenAPI specs) into a searchable in-memory index at build time. At runtime, it exposes this data over MCP's Streamable HTTP transport so tools like Claude Code can search docs, retrieve pages, browse the doc structure, and look up API endpoints — all without hitting external APIs.

## Project Structure

```
mcp-server/
├── src/
│   ├── index.ts                  # Express HTTP server, session management, rate limiting
│   ├── server.ts                 # MCP server factory, registers tools + resources
│   ├── content/
│   │   ├── types.ts              # TypeScript interfaces (DocEntry, NavItem, ApiEndpoint)
│   │   ├── ingest.ts             # Content pipeline: docs.yml → MDX → JSON index
│   │   └── search.ts             # Full-text search engine (MiniSearch)
│   └── tools/
│       ├── search-docs.ts        # search_docs — full-text search with fuzzy matching
│       ├── get-pages.ts          # get_pages — retrieve full page content by slug
│       ├── list-sections.ts      # list_sections — browse documentation hierarchy
│       └── get-api-reference.ts  # get_api_reference — API endpoint details
├── data/                         # Generated JSON indices (git-ignored)
│   ├── docs-index.json           # 305 doc entries with full markdown content
│   ├── nav-tree.json             # Navigation hierarchy from docs.yml
│   └── api-summary.json          # API endpoints from OpenAPI specs
├── build/                        # Compiled JS output (git-ignored)
├── Dockerfile                    # Multi-stage production build
├── deploy-mcp.yml                # GitHub Actions Cloud Run deployment template
├── package.json
└── tsconfig.json
```

## Running Locally

```bash
cd mcp-server
npm install
npm run build
npx tsx src/content/ingest.ts   # generate data/ from docs
npm start                       # starts on http://localhost:3000
```

The ingest step reads from the parent repo (`fern/docs.yml`, `fern/pages/`, and OpenAPI specs at the repo root) and writes JSON files to `data/`.

### Dev mode (auto-reload)

```bash
npm run dev
```

## Connecting to Claude Code

```bash
claude mcp add assemblyai-docs --transport http http://localhost:3000/mcp
```

Verify with:

```bash
claude mcp list
```

## Tools

| Tool | Description |
|------|-------------|
| `search_docs` | Full-text search across all docs. Supports fuzzy matching, section filtering, and pagination. |
| `get_pages` | Retrieve full markdown content for one or more pages by slug path. |
| `list_sections` | Browse the documentation hierarchy. Optionally drill into a specific section. |
| `get_api_reference` | Look up API endpoint details (params, request body, responses). Supports REST, Streaming, and LLM Gateway specs. |

## Resources

| Resource | URI | Description |
|----------|-----|-------------|
| `docs-overview` | `assemblyai://docs/overview` | Full documentation navigation tree |
| `api-endpoints` | `assemblyai://api/endpoints` | Summary of all API endpoints |

## Content Pipeline

The ingest script (`src/content/ingest.ts`) runs at build time:

1. **Parse `fern/docs.yml`** — builds the navigation tree from docs/faq/cookbooks tabs
2. **Read MDX files** — extracts frontmatter, strips JSX/React components to clean markdown
3. **Parse OpenAPI specs** — extracts endpoints from `openapi.yml`, `usm-streaming.yml`, `llm-gateway.yml`
4. **Write JSON** — outputs `docs-index.json`, `nav-tree.json`, `api-summary.json` to `data/`

Hidden pages (`hidden: true` in docs.yml) are filtered from all outputs.

## Server Details

- **Transport:** Streamable HTTP (JSON-RPC 2.0 over HTTP + SSE)
- **Port:** 3000
- **Rate limiting:** 60 requests/IP/minute
- **Sessions:** Max 1000 concurrent, 30-minute idle timeout
- **Endpoints:**
  - `POST /mcp` — client requests
  - `GET /mcp` — SSE stream
  - `DELETE /mcp` — end session
  - `GET /health` — health check

## Docker

```bash
# Build from repo root (needs access to fern/ and OpenAPI specs)
docker build -f mcp-server/Dockerfile -t assemblyai-docs-mcp .
docker run -p 3000:3000 assemblyai-docs-mcp
```

## Scripts

| Script | Command | Description |
|--------|---------|-------------|
| `build` | `tsc` | Compile TypeScript to `build/` |
| `build:content` | `tsx src/content/ingest.ts` | Run content ingestion pipeline |
| `start` | `node build/index.js` | Start production server |
| `dev` | `tsx --watch src/index.ts` | Start dev server with auto-reload |
