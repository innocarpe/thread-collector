import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type { InsightsContent, Post, PostMeta, CategorySlug } from "@/types/post";
import { CATEGORIES } from "@/types/post";

const THREADS_DIR = path.join(process.cwd(), "Threads");

// Module-level cache — built once per process (build time or serverless cold start)
let _cache: Map<string, Post> | null = null;
let _insights: Map<string, InsightsContent> | null = null;

function buildCache(): Map<string, Post> {
  if (_cache) return _cache;
  _cache = new Map();
  _insights = new Map();

  if (!fs.existsSync(THREADS_DIR)) return _cache;

  const userDirs = fs
    .readdirSync(THREADS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  for (const usernameSlug of userDirs) {
    for (const categorySlug of CATEGORIES) {
      const dir = path.join(THREADS_DIR, usernameSlug, categorySlug);
      if (!fs.existsSync(dir)) continue;

      const files = fs.readdirSync(dir).filter((f) => f.endsWith(".md"));

      for (const filename of files) {
        const filePath = `Threads/${usernameSlug}/${categorySlug}/${filename}`;
        const raw = fs.readFileSync(path.join(dir, filename), "utf-8");
        const { data, content } = matter(raw);

        const pk = String(data.pk);
        if (!pk || pk === "undefined") continue;

        // Extract title from first # heading or first non-empty line
        const lines = content.trim().split("\n");
        const headingLine = lines.find((l) => l.startsWith("# "));
        const title = headingLine
          ? headingLine.replace(/^#\s*/, "").trim()
          : lines[0]?.trim() || "(제목 없음)";

        // Excerpt: body without the heading, first 150 chars
        const bodyText = lines
          .filter((l) => !l.startsWith("# "))
          .join(" ")
          .replace(/\s+/g, " ")
          .trim();
        // Slice by code points (not UTF-16 code units) so we never split
        // a surrogate pair / ZWJ emoji sequence mid-character, which would
        // otherwise cause a React hydration mismatch.
        const codePoints = Array.from(bodyText);
        const excerpt =
          codePoints.length > 150
            ? codePoints.slice(0, 150).join("") + "…"
            : bodyText;

        // Preserve raw frontmatter for GitHub API updates
        const rawFrontmatter = raw.startsWith("---")
          ? raw.slice(0, raw.indexOf("---", 3) + 3)
          : "";

        const chainPksRaw = data.chain_pks;
        const chainPks: string[] | undefined = chainPksRaw
          ? String(chainPksRaw).replace(/[\[\]]/g, "").split(",").map((s: string) => s.trim()).filter(Boolean)
          : undefined;

        // Parse AI-assigned labels from frontmatter (array or inline [a, b] string)
        let labels: string[] | undefined;
        if (data.labels) {
          if (Array.isArray(data.labels)) {
            labels = data.labels.map(String).filter(Boolean);
          } else {
            const raw = String(data.labels).replace(/[\[\]]/g, "");
            labels = raw.split(",").map((s) => s.trim().replace(/^"|"$/g, "")).filter(Boolean);
          }
          if (labels.length === 0) labels = undefined;
        }

        _cache.set(pk, {
          pk,
          filePath,
          username: `@${String(data.username || usernameSlug).replace(/^@/, "")}`,
          usernameSlug,
          category: String(data.category || categorySlug),
          categorySlug: categorySlug as CategorySlug,
          date: data.date instanceof Date
            ? data.date.toISOString().slice(0, 10)
            : String(data.date || ""),
          takenAt: Number(data.taken_at || 0),
          source: String(data.source || ""),
          title,
          excerpt,
          chainPks,
          labels,
          content,
          rawFrontmatter,
        });
      }
    }

    const insightsDir = path.join(THREADS_DIR, usernameSlug, "insights");
    if (fs.existsSync(insightsDir)) {
      const insightFiles = ["overview.md", "patterns.md", "key-posts.md"];
      const insights: InsightsContent = {};
      for (const fileName of insightFiles) {
        const key = fileName === "key-posts.md" ? "keyPosts" : fileName.replace(/\.md$/, "");
        const filePath = path.join(insightsDir, fileName);
        if (fs.existsSync(filePath)) {
          insights[key as keyof InsightsContent] = fs.readFileSync(filePath, "utf-8");
        }
      }
      if (Object.keys(insights).length) {
        _insights?.set(usernameSlug, insights);
      }
    }
  }

  return _cache;
}

export function getAllPostMetas(): PostMeta[] {
  const posts = Array.from(buildCache().values()).map(
    ({ content: _content, rawFrontmatter: _raw, ...meta }) => meta
  );
  return posts.sort((a, b) => b.date.localeCompare(a.date));
}

export function getPostByPk(pk: string): Post | undefined {
  return buildCache().get(pk);
}

export function getAllPks(): string[] {
  return Array.from(buildCache().keys());
}

export function getUsers(): string[] {
  return [...new Set(getAllPostMetas().map((p) => p.usernameSlug))].sort();
}

export function getInsightsForUser(usernameSlug: string): InsightsContent | undefined {
  buildCache();
  return _insights?.get(usernameSlug);
}
