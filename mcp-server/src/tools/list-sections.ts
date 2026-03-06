import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { NavItem } from "../content/types.js";

export function registerListSections(server: McpServer, navTree: NavItem[]) {
  server.registerTool(
    "list_sections",
    {
      title: "List Documentation Sections",
      description:
        "List all available sections and pages in AssemblyAI documentation. Useful for understanding the documentation structure and finding the right topic.",
      inputSchema: {
        section: z
          .string()
          .optional()
          .describe(
            "Optional: a specific section to list contents of (e.g. 'Speech-to-text', 'Audio Intelligence'). Omit to see all top-level sections."
          ),
      },
    },
    async ({ section }) => {
      if (section) {
        const found = findSection(navTree, section);
        if (!found) {
          return {
            content: [
              {
                type: "text" as const,
                text: `Section "${section}" not found. Use list_sections without a section parameter to see all available sections.`,
              },
            ],
          };
        }
        return {
          content: [
            {
              type: "text" as const,
              text: formatNavTree([found], 0),
            },
          ],
        };
      }

      return {
        content: [
          {
            type: "text" as const,
            text: formatNavTree(navTree, 0),
          },
        ],
      };
    }
  );
}

function findSection(items: NavItem[], name: string): NavItem | null {
  const nameLower = name.toLowerCase();
  for (const item of items) {
    if (item.title.toLowerCase().includes(nameLower)) {
      return item;
    }
    if (item.children) {
      const found = findSection(item.children, name);
      if (found) return found;
    }
  }
  return null;
}

export function formatNavTree(items: NavItem[], depth: number): string {
  const indent = "  ".repeat(depth);
  const lines: string[] = [];

  for (const item of items) {
    if (item.hidden) continue;

    if (item.type === "link") {
      lines.push(`${indent}- [${item.title}](${item.href})`);
    } else if (item.type === "section") {
      lines.push(`${indent}## ${item.title}${item.slug ? ` (${item.slug})` : ""}`);
      if (item.children) {
        lines.push(formatNavTree(item.children, depth + 1));
      }
    } else {
      lines.push(`${indent}- ${item.title} → ${item.slug || ""}`);
    }
  }

  return lines.join("\n");
}
