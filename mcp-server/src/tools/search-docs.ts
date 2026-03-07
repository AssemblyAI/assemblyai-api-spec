import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { DocsSearch } from "../content/search.js";

export function registerSearchDocs(server: McpServer, search: DocsSearch) {
  server.registerTool(
    "search_docs",
    {
      title: "Search AssemblyAI Documentation",
      description:
        "Search across all AssemblyAI documentation including guides, API reference, tutorials, FAQ, and cookbooks. " +
        "Returns matching pages with relevant excerpts. " +
        "Search should be used as a complement to browsing the docs (list_sections), not as a replacement. " +
        "Use get_pages to read the full content of any result.",
      inputSchema: {
        query: z
          .string()
          .describe(
            "Search query (e.g. 'speaker diarization', 'streaming websocket', 'PII redaction')"
          ),
        section: z
          .string()
          .optional()
          .describe(
            "Optional: filter to a section (e.g. 'speech-to-text', 'audio-intelligence', 'lemur', 'getting-started', 'faq', 'guides')"
          ),
        page: z
          .number()
          .optional()
          .default(0)
          .describe("Page number, starts at 0"),
        hitsPerPage: z
          .number()
          .optional()
          .default(10)
          .describe("Results per page (default 10, max 50)"),
      },
    },
    async ({ query, section, page, hitsPerPage }) => {
      const clampedHitsPerPage = Math.min(hitsPerPage ?? 10, 50);
      const { results, totalHits, page: currentPage, totalPages } = search.search(query, {
        section,
        page: page ?? 0,
        hitsPerPage: clampedHitsPerPage,
      });

      if (results.length === 0) {
        return {
          content: [
            {
              type: "text" as const,
              text: `No results found for "${query}"${section ? ` in section "${section}"` : ""}. Try a different search query or remove the section filter.`,
            },
          ],
        };
      }

      const formatted = results
        .map(
          (r, i) =>
            `${currentPage * clampedHitsPerPage + i + 1}. **${r.title}**\n   Path: ${r.slug}\n   Section: ${r.section}\n   ${r.description ? `Description: ${r.description}\n   ` : ""}Excerpt: ${r.excerpt}`
        )
        .join("\n\n");

      const pagination =
        totalPages > 1
          ? `\n\nShowing page ${currentPage + 1} of ${totalPages} (${totalHits} total results). Use page parameter to see more.`
          : "";

      return {
        content: [
          {
            type: "text" as const,
            text: `Found ${totalHits} results for "${query}":\n\n${formatted}${pagination}\n\nUse the get_pages tool with page paths to read the full content.`,
          },
        ],
      };
    }
  );
}
