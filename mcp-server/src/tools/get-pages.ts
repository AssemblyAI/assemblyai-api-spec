import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { DocsSearch } from "../content/search.js";

export function registerGetPages(server: McpServer, search: DocsSearch) {
  server.registerTool(
    "get_pages",
    {
      title: "Get Documentation Pages",
      description:
        "Retrieve the full content of one or more AssemblyAI documentation pages by path. " +
        "Use search_docs first to find the right page paths, or list_sections to browse the structure. " +
        "Supports fetching multiple pages in a single call to reduce round-trips.",
      inputSchema: {
        paths: z
          .array(z.string())
          .describe(
            "One or more page paths (e.g. ['/getting-started/transcribe-an-audio-file', '/pre-recorded-audio/speaker-diarization'])"
          ),
      },
    },
    async ({ paths }) => {
      const results: string[] = [];

      for (const pagePath of paths) {
        const doc = search.getDoc(pagePath);

        if (!doc) {
          results.push(
            `## Page not found: "${pagePath}"\n\nUse search_docs to find the correct page path, or list_sections to browse available pages.\n`
          );
          continue;
        }

        const header =
          `# ${doc.title}\n\n` +
          (doc.description ? `> ${doc.description}\n\n` : "") +
          `**Section**: ${doc.section}\n**Path**: ${doc.slug}\n\n---\n\n`;

        results.push(header + doc.content);
      }

      return {
        content: [
          {
            type: "text" as const,
            text: results.join("\n\n---\n\n"),
          },
        ],
      };
    }
  );
}
