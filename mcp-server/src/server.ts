import fs from "node:fs";
import path from "node:path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { DocEntry, NavItem, ApiEndpoint } from "./content/types.js";
import { DocsSearch } from "./content/search.js";
import { registerSearchDocs } from "./tools/search-docs.js";
import { registerGetPages } from "./tools/get-pages.js";
import { registerListSections } from "./tools/list-sections.js";
import { registerGetApiReference } from "./tools/get-api-reference.js";
import { formatNavTree } from "./tools/list-sections.js";

function loadJson<T>(filename: string): T {
  const dataDir = path.resolve(import.meta.dirname, "../data");
  const filePath = path.join(dataDir, filename);
  return JSON.parse(fs.readFileSync(filePath, "utf-8")) as T;
}

// Load content once at module init — shared across all sessions
const docs = loadJson<DocEntry[]>("docs-index.json");
const navTree = loadJson<NavItem[]>("nav-tree.json");
const apiEndpoints = loadJson<Record<string, ApiEndpoint[]>>("api-summary.json");
const search = new DocsSearch(docs);

console.error(`Loaded ${docs.length} docs, ${Object.keys(apiEndpoints).length} API specs`);

export function createMcpServer(): McpServer {
  const server = new McpServer({
    name: "assemblyai-docs",
    version: "1.0.0",
  });

  // --- Resources ---
  server.registerResource(
    "docs-overview",
    "assemblyai://docs/overview",
    {
      description:
        "Complete overview of AssemblyAI documentation including table of contents, page descriptions, and structure. Use this to understand what documentation is available.",
    },
    async () => ({
      contents: [
        {
          uri: "assemblyai://docs/overview",
          mimeType: "text/plain",
          text: formatNavTree(navTree, 0),
        },
      ],
    })
  );

  server.registerResource(
    "api-endpoints",
    "assemblyai://api/endpoints",
    {
      description:
        "Summary of all AssemblyAI API endpoints (REST, Streaming, LLM Gateway) including methods, paths, and descriptions.",
    },
    async () => {
      const lines: string[] = [];
      for (const [specName, endpoints] of Object.entries(apiEndpoints)) {
        lines.push(`# ${specName.toUpperCase()} API\n`);
        for (const ep of endpoints) {
          lines.push(`- **${ep.method} ${ep.path}**: ${ep.summary}`);
        }
        lines.push("");
      }
      return {
        contents: [
          {
            uri: "assemblyai://api/endpoints",
            mimeType: "text/plain",
            text: lines.join("\n"),
          },
        ],
      };
    }
  );

  // --- Tools ---
  registerSearchDocs(server, search);
  registerGetPages(server, search);
  registerListSections(server, navTree);
  registerGetApiReference(server, apiEndpoints);

  return server;
}
