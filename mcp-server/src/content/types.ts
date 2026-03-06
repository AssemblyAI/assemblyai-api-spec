export interface DocEntry {
  id: string;
  title: string;
  slug: string;
  section: string;
  description: string;
  content: string;
  filePath: string;
}

export interface NavItem {
  type: "page" | "section" | "link";
  title: string;
  slug?: string;
  path?: string;
  href?: string;
  hidden?: boolean;
  children?: NavItem[];
}

export interface ApiEndpoint {
  method: string;
  path: string;
  summary: string;
  description: string;
  parameters: ApiParameter[];
  requestBody?: string;
  responses: Record<string, string>;
  tags: string[];
}

export interface ApiParameter {
  name: string;
  in: string;
  required: boolean;
  description: string;
  type: string;
}

export interface ContentIndex {
  docs: DocEntry[];
  navTree: NavItem[];
  apiEndpoints: Record<string, ApiEndpoint[]>;
}
