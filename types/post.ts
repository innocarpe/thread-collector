export type CategorySlug =
  | "ai-llm"
  | "viral-sns"
  | "monetization"
  | "dev-tools"
  | "product-strategy"
  | "startup-philosophy"
  | "career-growth"
  | "learning-retro"
  | "productivity"
  | "web-app"
  | "portfolio-ops"
  | "aso"
  | "case-study";

export const CATEGORY_LABELS: Record<CategorySlug, string> = {
  "ai-llm": "AI/LLM",
  "viral-sns": "바이럴/SNS/마케팅",
  "monetization": "수익화/부수입",
  "dev-tools": "개발도구/스택",
  "product-strategy": "제품전략/PMF",
  "startup-philosophy": "창업철학/인디해킹",
  "career-growth": "커리어/성장",
  "learning-retro": "학습/회고",
  "productivity": "생산성/워크플로우",
  "web-app": "웹/앱 개발",
  "portfolio-ops": "포트폴리오 운영",
  "aso": "ASO/출시전략",
  "case-study": "사례연구",
};

export const CATEGORIES: CategorySlug[] = [
  "ai-llm",
  "viral-sns",
  "monetization",
  "dev-tools",
  "product-strategy",
  "startup-philosophy",
  "career-growth",
  "learning-retro",
  "productivity",
  "web-app",
  "portfolio-ops",
  "aso",
  "case-study",
];

export type InsightsContent = {
  overview?: string;
  patterns?: string;
  keyPosts?: string;
};

export type PostMeta = {
  pk: string;           // Threads post ID — used as URL slug
  username: string;     // "@dalgom.bami"
  usernameSlug: string; // "dalgom.bami"
  category: string;     // display name e.g. "기술/개발"
  categorySlug: CategorySlug;
  date: string;         // "2025-02-04"
  takenAt: number;      // unix timestamp
  source: string;       // Threads URL
  title: string;        // first sentence of the post
  excerpt: string;      // first 150 chars of body
  chainPks?: string[];  // pks of continuation posts merged into this one
  labels?: string[];    // AI-assigned topic labels from frontmatter
};

export type PostMetaWithPath = PostMeta & {
  filePath: string;     // relative path e.g. "Threads/dalgom.bami/tech-dev/2025-02-04-foo.md"
};

export type Post = PostMetaWithPath & {
  content: string;      // full markdown body (frontmatter stripped)
  rawFrontmatter: string; // original frontmatter block (for GitHub API updates)
};
