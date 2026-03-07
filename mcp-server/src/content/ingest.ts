import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";
import matter from "gray-matter";
import type {
  DocEntry,
  NavItem,
  ApiEndpoint,
  ApiParameter,
} from "./types.js";

const REPO_ROOT = path.resolve(import.meta.dirname, "../../../");
const DATA_DIR = path.resolve(import.meta.dirname, "../../data");

// --- MDX Stripping ---

function stripMdxToMarkdown(content: string): string {
  let text = content;

  // Remove import statements
  text = text.replace(/^import\s+.*$/gm, "");

  // Convert <Tab> with title to labeled section
  text = text.replace(
    /<Tab[^>]*title="([^"]*)"[^>]*>/g,
    "\n**[$1]**\n"
  );
  text = text.replace(/<\/Tab>/g, "");

  // Remove <Tabs> wrappers
  text = text.replace(/<\/?Tabs[^>]*>/g, "");

  // Convert <Note>, <Warning>, <Info>, <Tip> to markdown callouts
  text = text.replace(
    /<(Note|Warning|Info|Tip)[^>]*>/gi,
    (_, tag) => `\n> **${tag}**: `
  );
  text = text.replace(/<\/(Note|Warning|Info|Tip)>/gi, "\n");

  // Remove <Frame> tags (image wrappers)
  text = text.replace(/<\/?Frame[^>]*>/g, "");

  // Remove <Accordion> / <AccordionGroup> but keep content (handles multi-line)
  text = text.replace(/<Accordion[\s\S]*?>/g, "");
  text = text.replace(/<\/Accordion>/g, "");
  text = text.replace(/<\/?AccordionGroup[^>]*>/g, "");

  // Remove <CardGroup> / <Card> but keep content (handles multi-line JSX tags with nested braces)
  text = text.replace(/<\/?CardGroup[^>]*>/gs, "");
  text = text.replace(/<Card(?:\s+(?:[^>{}]|\{[\s\S]*?\})*)?>/gs, "");
  text = text.replace(/<\/Card>/g, "");

  // Remove <CodeGroup> wrappers
  text = text.replace(/<\/?CodeGroup[^>]*>/g, "");

  // Remove <Tooltip> wrappers but keep inner text
  text = text.replace(/<Tooltip[^>]*>/g, "");
  text = text.replace(/<\/Tooltip>/g, "");

  // Remove HTML elements with JSX-style attributes (style objects, event handlers)
  // These are layout/interactive elements with no semantic value
  text = text.replace(/<[a-z][a-zA-Z]*\s[^>]*(?:style=\{\{|on[A-Z])[^>]*>[\s\S]*?<\/[a-z][a-zA-Z]*>/g, "");

  // --- Convert semantic HTML to markdown equivalents ---

  // <h1>-<h6> → # headings (preserve hierarchy)
  text = text.replace(/<h([1-6])[^>]*>([\s\S]*?)<\/h[1-6]>/gi, (_, level, inner) => {
    return "\n" + "#".repeat(Number(level)) + " " + inner.trim() + "\n";
  });

  // <a href="...">text</a> → [text](href)
  text = text.replace(/<a\s+href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, (_, href, inner) => {
    return `[${inner.trim()}](${href})`;
  });

  // <strong>/<b> → **bold**
  text = text.replace(/<\/?(?:strong|b)>/gi, "**");

  // <em>/<i> → *italic*
  text = text.replace(/<\/?(?:em|i)>/gi, "*");

  // <code> (inline) → `code`
  text = text.replace(/<\/?code>/gi, "`");

  // <br> → newline
  text = text.replace(/<br\s*\/?>/gi, "\n");

  // <hr> → ---
  text = text.replace(/<hr\s*\/?>/gi, "\n---\n");

  // --- Strip purely presentational HTML (keep text between tags) ---
  text = text.replace(/<\/?(?:div|span|video|source|img|p|ul|ol|li|table|thead|tbody|tr|td|th|button|label|input|form|section|header|footer|nav|main|aside|figure|figcaption|details|summary)[^>]*>/gi, "");

  // Remove remaining self-closing JSX tags
  text = text.replace(/<[A-Z][a-zA-Z]*\s[^>]*\/>/g, "");

  // Remove remaining opening/closing JSX tags (but preserve content between them)
  text = text.replace(/<\/?[A-Z][a-zA-Z]*[^>]*>/g, "");

  // Clean up excessive blank lines
  text = text.replace(/\n{4,}/g, "\n\n\n");

  return text.trim();
}

// --- Navigation Tree Parsing ---

interface DocsYmlEntry {
  page?: string;
  section?: string;
  link?: string;
  path?: string;
  slug?: string;
  href?: string;
  hidden?: boolean;
  contents?: DocsYmlEntry[];
  layout?: DocsYmlEntry[];
  "skip-slug"?: boolean;
}

function parseNavEntry(entry: DocsYmlEntry, parentSlug: string): NavItem | null {
  if (entry.link && entry.href) {
    return { type: "link", title: entry.link, href: entry.href };
  }

  if (entry.page) {
    const slug = entry.slug
      ? (entry.slug.startsWith("/") ? entry.slug : `${parentSlug}/${entry.slug}`)
      : `${parentSlug}/${slugify(entry.page)}`;
    return {
      type: "page",
      title: entry.page,
      slug: normSlug(slug),
      path: entry.path,
      hidden: entry.hidden,
    };
  }

  if (entry.section) {
    const sectionSlug = entry["skip-slug"]
      ? parentSlug
      : entry.slug
        ? (entry.slug.startsWith("/") ? entry.slug : `${parentSlug}/${entry.slug}`)
        : `${parentSlug}/${slugify(entry.section)}`;
    const children = (entry.contents || [])
      .map((child) => parseNavEntry(child, normSlug(sectionSlug)))
      .filter((c): c is NavItem => c !== null);
    return {
      type: "section",
      title: entry.section,
      slug: normSlug(sectionSlug),
      path: entry.path,
      hidden: entry.hidden,
      children,
    };
  }

  return null;
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function normSlug(slug: string): string {
  return slug.replace(/\/+/g, "/").replace(/\/$/, "") || "/";
}

function parseDocsYml(): NavItem[] {
  const docsYmlPath = path.join(REPO_ROOT, "fern", "docs.yml");
  const raw = fs.readFileSync(docsYmlPath, "utf-8");
  const config = yaml.load(raw) as {
    navigation: Array<{ tab: string; layout: DocsYmlEntry[] }>;
  };

  const navTree: NavItem[] = [];
  for (const tab of config.navigation) {
    if (tab.tab === "docs" || tab.tab === "faq" || tab.tab === "cookbooks") {
      const items = (tab.layout || [])
        .map((entry) => parseNavEntry(entry, ""))
        .filter((item): item is NavItem => item !== null);
      navTree.push({
        type: "section",
        title: tab.tab === "docs" ? "Documentation" : tab.tab === "faq" ? "FAQ" : "Cookbooks",
        slug: tab.tab === "docs" ? "/" : `/${tab.tab}`,
        children: items,
      });
    }
  }
  return navTree;
}

// --- Doc Entry Extraction ---

function collectPages(items: NavItem[], section: string): Array<{ title: string; slug: string; path: string; section: string }> {
  const pages: Array<{ title: string; slug: string; path: string; section: string }> = [];
  for (const item of items) {
    if (item.hidden) continue;

    if (item.type === "page" && item.path && item.slug) {
      pages.push({ title: item.title, slug: item.slug, path: item.path, section });
    }
    if (item.type === "section") {
      const sectionName = item.title;
      if (item.path && item.slug) {
        pages.push({ title: item.title, slug: item.slug, path: item.path, section: sectionName });
      }
      if (item.children) {
        pages.push(...collectPages(item.children, sectionName));
      }
    }
  }
  return pages;
}

function buildDocEntries(navTree: NavItem[]): DocEntry[] {
  const allPages = collectPages(navTree, "");
  const entries: DocEntry[] = [];
  const seenIds = new Set<string>();

  for (const page of allPages) {
    const filePath = path.join(REPO_ROOT, "fern", page.path);
    if (!fs.existsSync(filePath)) {
      console.warn(`File not found: ${filePath}`);
      continue;
    }

    // Deduplicate by slug — keep the first occurrence
    let id = page.slug;
    if (seenIds.has(id)) {
      // Append section to make unique
      id = `${page.slug}--${slugify(page.section)}`;
      if (seenIds.has(id)) continue;
    }
    seenIds.add(id);

    const raw = fs.readFileSync(filePath, "utf-8");
    const { data: frontmatter, content: mdxContent } = matter(raw);
    const cleanContent = stripMdxToMarkdown(mdxContent);
    const description = (frontmatter.description as string) || (frontmatter.subtitle as string) || "";

    entries.push({
      id,
      title: (frontmatter.title as string) || page.title,
      slug: page.slug,
      section: page.section,
      description,
      content: cleanContent,
      filePath: page.path,
    });
  }

  return entries;
}

// --- OpenAPI Parsing ---

function parseOpenApiSpec(specPath: string, apiName: string): ApiEndpoint[] {
  if (!fs.existsSync(specPath)) {
    console.warn(`API spec not found: ${specPath}`);
    return [];
  }

  const raw = fs.readFileSync(specPath, "utf-8");
  const spec = yaml.load(raw) as {
    paths?: Record<string, Record<string, {
      summary?: string;
      description?: string;
      parameters?: Array<{
        name: string;
        in: string;
        required?: boolean;
        description?: string;
        schema?: { type?: string };
      }>;
      requestBody?: { content?: Record<string, { schema?: unknown }> };
      responses?: Record<string, { description?: string }>;
      tags?: string[];
    }>>;
  };

  const endpoints: ApiEndpoint[] = [];

  if (!spec.paths) return endpoints;

  for (const [pathStr, methods] of Object.entries(spec.paths)) {
    for (const [method, details] of Object.entries(methods)) {
      if (["get", "post", "put", "patch", "delete"].includes(method)) {
        const params: ApiParameter[] = (details.parameters || []).map((p) => ({
          name: p.name,
          in: p.in,
          required: p.required || false,
          description: p.description || "",
          type: p.schema?.type || "string",
        }));

        let requestBody = "";
        if (details.requestBody?.content) {
          const contentTypes = Object.keys(details.requestBody.content);
          requestBody = `Content types: ${contentTypes.join(", ")}`;
          const jsonSchema = details.requestBody.content["application/json"]?.schema;
          if (jsonSchema) {
            requestBody += `\nSchema: ${JSON.stringify(jsonSchema, null, 2).slice(0, 2000)}`;
          }
        }

        const responses: Record<string, string> = {};
        if (details.responses) {
          for (const [code, resp] of Object.entries(details.responses)) {
            responses[code] = resp.description || "";
          }
        }

        endpoints.push({
          method: method.toUpperCase(),
          path: pathStr,
          summary: details.summary || "",
          description: details.description || "",
          parameters: params,
          requestBody: requestBody || undefined,
          responses,
          tags: details.tags || [],
        });
      }
    }
  }

  return endpoints;
}

// --- Main ---

function main() {
  console.log("Starting content ingestion...");

  // Parse navigation tree
  console.log("Parsing docs.yml navigation...");
  const navTree = parseDocsYml();

  // Build doc entries
  console.log("Processing MDX files...");
  const docs = buildDocEntries(navTree);
  console.log(`Processed ${docs.length} documentation pages`);

  // Parse API specs
  console.log("Parsing API specs...");
  const apiEndpoints: Record<string, ApiEndpoint[]> = {
    rest: parseOpenApiSpec(path.join(REPO_ROOT, "openapi.yml"), "rest"),
    streaming: parseOpenApiSpec(path.join(REPO_ROOT, "usm-streaming.yml"), "streaming"),
    "llm-gateway": parseOpenApiSpec(path.join(REPO_ROOT, "llm-gateway.yml"), "llm-gateway"),
  };
  for (const [name, endpoints] of Object.entries(apiEndpoints)) {
    console.log(`  ${name}: ${endpoints.length} endpoints`);
  }

  // Write output files
  fs.mkdirSync(DATA_DIR, { recursive: true });

  fs.writeFileSync(
    path.join(DATA_DIR, "docs-index.json"),
    JSON.stringify(docs, null, 2)
  );
  fs.writeFileSync(
    path.join(DATA_DIR, "nav-tree.json"),
    JSON.stringify(navTree, null, 2)
  );
  fs.writeFileSync(
    path.join(DATA_DIR, "api-summary.json"),
    JSON.stringify(apiEndpoints, null, 2)
  );

  console.log(`\nContent ingestion complete. Output written to ${DATA_DIR}`);
}

main();
