import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ApiEndpoint } from "../content/types.js";

export function registerGetApiReference(
  server: McpServer,
  apiEndpoints: Record<string, ApiEndpoint[]>
) {
  server.registerTool(
    "get_api_reference",
    {
      title: "Get API Reference",
      description:
        "Get details about AssemblyAI API endpoints including request/response schemas, parameters, and descriptions. Covers REST API, Streaming WebSocket API, and LLM Gateway API.",
      inputSchema: {
        endpoint: z
          .string()
          .optional()
          .describe(
            "API endpoint path (e.g. '/v2/transcript', '/v2/upload'). Omit to list all available endpoints."
          ),
        api: z
          .enum(["rest", "streaming", "llm-gateway"])
          .optional()
          .default("rest")
          .describe("Which API spec: 'rest' (default), 'streaming', 'llm-gateway'"),
      },
    },
    async ({ endpoint, api }) => {
      const specName = api || "rest";
      const endpoints = apiEndpoints[specName];

      if (!endpoints || endpoints.length === 0) {
        return {
          content: [
            {
              type: "text" as const,
              text: `No API spec found for "${specName}". Available APIs: ${Object.keys(apiEndpoints).join(", ")}`,
            },
          ],
        };
      }

      if (!endpoint) {
        // List all endpoints
        const grouped = new Map<string, ApiEndpoint[]>();
        for (const ep of endpoints) {
          const tag = ep.tags[0] || "Other";
          const group = grouped.get(tag) || [];
          group.push(ep);
          grouped.set(tag, group);
        }

        const lines: string[] = [`# ${specName.toUpperCase()} API Endpoints\n`];
        for (const [tag, eps] of grouped) {
          lines.push(`## ${tag}`);
          for (const ep of eps) {
            lines.push(`- **${ep.method} ${ep.path}**: ${ep.summary}`);
          }
          lines.push("");
        }

        return {
          content: [
            {
              type: "text" as const,
              text: lines.join("\n") +
                "\n\nUse get_api_reference with an endpoint path to get full details.",
            },
          ],
        };
      }

      // Find matching endpoint(s)
      const matches = endpoints.filter(
        (ep) =>
          ep.path === endpoint ||
          ep.path.includes(endpoint) ||
          endpoint.includes(ep.path)
      );

      if (matches.length === 0) {
        return {
          content: [
            {
              type: "text" as const,
              text: `No endpoint matching "${endpoint}" found in the ${specName} API. Use get_api_reference without an endpoint to list all available endpoints.`,
            },
          ],
        };
      }

      const formatted = matches
        .map((ep) => {
          const parts = [`## ${ep.method} ${ep.path}\n`];
          if (ep.summary) parts.push(`**Summary**: ${ep.summary}`);
          if (ep.description) parts.push(`\n${ep.description}`);

          if (ep.parameters.length > 0) {
            parts.push("\n### Parameters");
            for (const p of ep.parameters) {
              parts.push(
                `- **${p.name}** (${p.in}, ${p.required ? "required" : "optional"}, ${p.type}): ${p.description}`
              );
            }
          }

          if (ep.requestBody) {
            parts.push(`\n### Request Body\n${ep.requestBody}`);
          }

          if (Object.keys(ep.responses).length > 0) {
            parts.push("\n### Responses");
            for (const [code, desc] of Object.entries(ep.responses)) {
              parts.push(`- **${code}**: ${desc}`);
            }
          }

          return parts.join("\n");
        })
        .join("\n\n---\n\n");

      return {
        content: [
          {
            type: "text" as const,
            text: formatted,
          },
        ],
      };
    }
  );
}
