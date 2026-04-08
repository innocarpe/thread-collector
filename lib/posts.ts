import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type { Post, PostMeta, CategorySlug } from "@/types/post";
import { CATEGORIES } from "@/types/post";

const THREADS_DIR = path.join(process.cwd(), "Threads");

// Module-level cache — built once per process (build time or serverless cold start)
let _cache: Map<string, Post> | null = null;

function buildCache(): Map<string, Post> {
  if (_cache) return _cache;
  _cache = new Map();

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
        const excerpt = bodyText.slice(0, 150) + (bodyText.length > 150 ? "…" : "");

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
