import MiniSearch from "minisearch";
import type { DocEntry } from "./types.js";

export interface SearchResult {
  id: string;
  title: string;
  slug: string;
  section: string;
  description: string;
  excerpt: string;
  score: number;
}

export class DocsSearch {
  private index: MiniSearch<DocEntry>;
  private docs: Map<string, DocEntry>;

  constructor(docs: DocEntry[]) {
    this.docs = new Map(docs.map((d) => [d.id, d]));

    this.index = new MiniSearch<DocEntry>({
      fields: ["title", "description", "content", "section"],
      storeFields: ["title", "slug", "section", "description"],
      searchOptions: {
        boost: { title: 3, description: 2, section: 1 },
        fuzzy: 0.2,
        prefix: true,
      },
    });

    this.index.addAll(docs);
  }

  search(
    query: string,
    options?: { section?: string; page?: number; hitsPerPage?: number }
  ): { results: SearchResult[]; totalHits: number; page: number; totalPages: number } {
    const hitsPerPage = options?.hitsPerPage || 10;
    const page = options?.page || 0;

    let filter: ((result: { id: string }) => boolean) | undefined;
    if (options?.section) {
      const sectionLower = options.section.toLowerCase();
      filter = (result) => {
        const doc = this.docs.get(result.id as string);
        return doc?.section.toLowerCase().includes(sectionLower) ?? false;
      };
    }

    const allResults = this.index.search(query, { filter });
    const totalHits = allResults.length;
    const totalPages = Math.ceil(totalHits / hitsPerPage);
    const offset = page * hitsPerPage;
    const paged = allResults.slice(offset, offset + hitsPerPage);

    const results = paged.map((result) => {
      const doc = this.docs.get(result.id as string)!;
      return {
        id: doc.id,
        title: doc.title,
        slug: doc.slug,
        section: doc.section,
        description: doc.description,
        excerpt: extractExcerpt(doc.content, query),
        score: result.score,
      };
    });

    return { results, totalHits, page, totalPages };
  }

  getDoc(slug: string): DocEntry | undefined {
    // Try exact match first
    const direct = this.docs.get(slug);
    if (direct) return direct;

    // Try with leading slash
    const withSlash = this.docs.get(`/${slug}`);
    if (withSlash) return withSlash;

    // Try without leading slash
    const withoutSlash = this.docs.get(slug.replace(/^\//, ""));
    if (withoutSlash) return withoutSlash;

    // Fuzzy path match
    for (const doc of this.docs.values()) {
      if (doc.slug.endsWith(slug) || slug.endsWith(doc.slug)) {
        return doc;
      }
    }

    return undefined;
  }
}

function extractExcerpt(content: string, query: string, maxLength = 300): string {
  const queryTerms = query.toLowerCase().split(/\s+/);
  const lines = content.split("\n");

  // Find the first line containing a query term
  for (const line of lines) {
    const lineLower = line.toLowerCase();
    if (queryTerms.some((term) => lineLower.includes(term))) {
      const trimmed = line.trim();
      if (trimmed.length > maxLength) {
        return trimmed.slice(0, maxLength) + "...";
      }
      return trimmed;
    }
  }

  // Fallback: first non-empty, non-heading line
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith("#") && trimmed.length > 20) {
      return trimmed.slice(0, maxLength) + (trimmed.length > maxLength ? "..." : "");
    }
  }

  return content.slice(0, maxLength) + "...";
}
