"use client";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import type { NaverPostMeta } from "@/types/naver-post";
import { NaverCatBadge } from "@/components/naver/naver-cat-badge";
import { useNaverReader } from "@/components/naver/naver-reader-context";

type Props = {
  posts: NaverPostMeta[];
  cafe: string;
  segmentFilter?: string;
  categoryFilter?: string;
};

function buildHref(cafe: string, params: Record<string, string | undefined>) {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v) q.set(k, v);
  }
  const s = q.toString();
  return s ? `/naver/${cafe}?${s}` : `/naver/${cafe}`;
}

export function NaverPostListClient({ posts, cafe, segmentFilter, categoryFilter }: Props) {
  const { hydrated, getStatus, toggleStar, toggleHide } = useNaverReader();
  const searchParams = useSearchParams();
  const statusFilter = searchParams.get("status") ?? "";

  const filtered = posts.filter((p) => {
    if (!hydrated) return true;
    const s = getStatus(p.id);
    if (statusFilter === "hidden") return !!s.hidden;
    if (s.hidden) return false;
    if (statusFilter === "starred") return !!s.starred;
    return true;
  });

  const isFiltered = !!(segmentFilter || categoryFilter || statusFilter);

  return (
    <div style={!hydrated ? { visibility: "hidden" } : undefined}>
      <div className="toolbar">
        <span className="muted" style={{ fontSize: "var(--text-sm)" }}>
          {filtered.length}개 글
        </span>
        {isFiltered && (
          <Link href={`/naver/${cafe}`} className="reset-link">
            필터 초기화
          </Link>
        )}
      </div>

      {filtered.length === 0 ? (
        <p className="muted" style={{ fontSize: "var(--text-sm)", padding: "var(--space-4) 0" }}>
          조건에 맞는 글이 없습니다.
        </p>
      ) : (
        <div className="card-list">
          {filtered.map((post) => {
            const s = hydrated ? getStatus(post.id) : {};
            return (
              <Link
                key={post.id}
                href={`/naver/${cafe}/posts/${post.id}`}
                className={`post-card${s.starred ? " is-starred" : ""}`}
              >
                <div className="post-card-meta">
                  <NaverCatBadge categorySlug={post.categorySlug} label={post.category} />
                  <span className="post-card-author">{post.writer}</span>
                  <span className="post-card-date">{post.date}</span>
                  <span className="post-auto-label-chip" style={{ fontSize: "10px" }}>
                    {post.menu}
                  </span>
                </div>
                <h3 className="post-card-title">{post.title}</h3>
                <p className="post-card-excerpt">{post.excerpt}</p>

                {hydrated && (
                  <div className="post-card-quick-actions">
                    <button
                      className={`post-card-quick-btn${s.starred ? " is-starred" : ""}`}
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        toggleStar(post.id);
                      }}
                      title={s.starred ? "중요 해제" : "중요 표시"}
                    >
                      {s.starred ? "⭐" : "☆"} 중요
                    </button>
                    <button
                      className="post-card-quick-btn"
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        toggleHide(post.id);
                      }}
                      title="목록에서 숨기기"
                    >
                      숨기기
                    </button>
                  </div>
                )}
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
