export type CategorySlug = "tech-dev" | "product-business" | "career-philosophy";

export const CATEGORY_LABELS: Record<CategorySlug, string> = {
  "tech-dev": "기술/개발",
  "product-business": "프로덕트/비즈니스",
  "career-philosophy": "커리어/철학",
};

export const CATEGORIES: CategorySlug[] = ["tech-dev", "product-business", "career-philosophy"];

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
