import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type {
  NaverPost,
  NaverPostMeta,
  NaverCafeInsights,
  NaverCategorySlug,
  NaverSegment,
} from "@/types/naver-post";
import { NAVER_CATEGORIES } from "@/types/naver-post";

const NAVER_DIR = path.join(process.cwd(), "NaverCafe");

/** Decode HTML numeric entities (e.g. &#128172; → 💬) stored in frontmatter */
function decodeHtmlEntities(str: string): string {
  return str.replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)));
}

const SEGMENTS: NaverSegment[] = ["operator", "community"];

// Module-level cache — built once per process (build time or serverless cold start)
let _cache: Map<string, NaverPost> | null = null;
let _insightsCache: Map<string, NaverCafeInsights> | null = null;

function buildCache(): Map<string, NaverPost> {
  if (_cache) return _cache;
  _cache = new Map();
  _insightsCache = new Map();

  if (!fs.existsSync(NAVER_DIR)) return _cache;

  const cafeDirs = fs
    .readdirSync(NAVER_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  for (const cafe of cafeDirs) {
    for (const segment of SEGMENTS) {
      for (const categorySlug of NAVER_CATEGORIES) {
        const dir = path.join(NAVER_DIR, cafe, segment, categorySlug);
        if (!fs.existsSync(dir)) continue;

        const files = fs.readdirSync(dir).filter((f) => f.endsWith(".md"));

        for (const filename of files) {
          const raw = fs.readFileSync(path.join(dir, filename), "utf-8");
          const { data, content } = matter(raw);

          const articleId = String(data.article_id ?? "");
          if (!articleId || articleId === "undefined") continue;

          // Use composite key: cafe/id to avoid collisions across cafes
          const cacheKey = `${cafe}/${articleId}`;

          // Extract title from first # heading
          const lines = content.trim().split("\n");
          const headingLine = lines.find((l) => l.startsWith("# "));
          const title = headingLine
            ? headingLine.replace(/^#\s*/, "").trim()
            : lines[0]?.trim() || "(제목 없음)";

          // Excerpt: body without the heading, first 150 code points
          const bodyText = lines
            .filter((l) => !l.startsWith("# "))
            .join(" ")
            .replace(/\s+/g, " ")
            .trim();
          const codePoints = Array.from(bodyText);
          const excerpt =
            codePoints.length > 150
              ? codePoints.slice(0, 150).join("") + "…"
              : bodyText;

          _cache.set(cacheKey, {
            id: articleId,
            cafe: String(data.cafe || cafe),
            segment: (data.segment as NaverSegment) || segment,
            category: String(data.category || categorySlug),
            categorySlug: categorySlug as NaverCategorySlug,
            menu: decodeHtmlEntities(String(data.menu || "")),
            writer: String(data.writer || ""),
            date: data.date instanceof Date
              ? data.date.toISOString().slice(0, 10)
              : String(data.date || ""),
            writeDateMs: Number(data.write_date_ms || 0),
            source: String(data.source || ""),
            title,
            excerpt,
            content,
          });
        }
      }
    }

    // Load insights for this cafe
    const insightsDir = path.join(NAVER_DIR, cafe, "insights");
    if (fs.existsSync(insightsDir)) {
      const insights: NaverCafeInsights = {};

      const tryRead = (filePath: string): string | undefined => {
        const full = path.join(insightsDir, filePath);
        return fs.existsSync(full) ? fs.readFileSync(full, "utf-8") : undefined;
      };

      insights.overview = tryRead("00-overview.md");
      insights.operatorAnalysis = tryRead("operator/full-analysis.md");
      insights.operatorIncome = tryRead("operator/income-methods.md");
      insights.operatorTools = tryRead("operator/tools-stack.md");
      insights.operatorMarketing = tryRead("operator/marketing-tactics.md");
      insights.communityIncome = tryRead("community/income-methods.md");
      insights.communityTools = tryRead("community/tools-ai.md");
      insights.communityCases = tryRead("community/case-studies.md");
      insights.communityQa = tryRead("community/qa-pain-points.md");

      if (Object.values(insights).some(Boolean)) {
        _insightsCache?.set(cafe, insights);
      }
    }
  }

  return _cache;
}

export function getNaverCafes(): string[] {
  if (!fs.existsSync(NAVER_DIR)) return [];
  return fs
    .readdirSync(NAVER_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();
}

export function getNaverPostMetas(cafe: string): NaverPostMeta[] {
  const cache = buildCache();
  const posts: NaverPostMeta[] = [];

  for (const [key, post] of cache.entries()) {
    if (key.startsWith(`${cafe}/`)) {
      const { content: _content, ...meta } = post;
      posts.push(meta);
    }
  }

  return posts.sort((a, b) => b.date.localeCompare(a.date));
}

export function getNaverPost(cafe: string, id: string): NaverPost | undefined {
  return buildCache().get(`${cafe}/${id}`);
}

export function getAllNaverPostIds(cafe: string): string[] {
  const cache = buildCache();
  const ids: string[] = [];
  for (const key of cache.keys()) {
    if (key.startsWith(`${cafe}/`)) {
      ids.push(key.split("/")[1]);
    }
  }
  return ids;
}

export function getNaverInsights(cafe: string): NaverCafeInsights | undefined {
  buildCache();
  return _insightsCache?.get(cafe);
}
