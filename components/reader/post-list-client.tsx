"use client";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import type { PostMeta } from "@/types/post";
import { useReader } from "./reader-context";
import { PostCard } from "@/components/ui/post-card";
import { SectionHeading } from "@/components/ui/section-heading";

type Props = {
  posts: PostMeta[];
  userFilter?: string;
  categoryFilter?: string;
};

export function PostListClient({ posts, userFilter, categoryFilter }: Props) {
  const { hydrated, getStatus, toggleHide, toggleStar } = useReader();
  const searchParams = useSearchParams();
  const statusFilter = searchParams.get("status") ?? "";
  const labelFilter = searchParams.get("label") ?? "";

  const filtered = posts.filter((p) => {
    if (!hydrated) return true; // localStorage 로드 전: 전부 표시 (visibility:hidden으로 가림)
    const s = getStatus(p.pk);
    if (statusFilter === "hidden") return !!s.hidden;
    if (s.hidden) return false;
    if (statusFilter === "unread") return !s.read;
    if (statusFilter === "starred") return !!s.starred;
    if (labelFilter) {
      // AI labels (from frontmatter) OR user-assigned labels (from localStorage)
      return (p.labels?.includes(labelFilter) ?? false) || (s.labels?.includes(labelFilter) ?? false);
    }
    return true;
  });

  const isFiltered = !!(userFilter || categoryFilter || statusFilter || labelFilter);

  return (
    <div style={!hydrated ? { visibility: "hidden" } : undefined}>
      <section className="surface section">
        <div className="toolbar">
          <SectionHeading>Posts</SectionHeading>
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
            <span className="muted" style={{ fontSize: "var(--text-sm)" }}>
              {filtered.length}개
            </span>
            {isFiltered && (
              <Link href="/" className="reset-link">
                필터 초기화
              </Link>
            )}
          </div>
        </div>

        <div className="card-list">
          {filtered.length > 0 ? (
            filtered.map((post) => {
              const s = hydrated ? getStatus(post.pk) : {};
              return (
                <PostCard
                  key={post.pk}
                  post={post}
                  showAuthor={!userFilter}
                  status={s}
                  actions={hydrated ? (
                    <div className="post-card-quick-actions">
                      <button
                        className={`post-card-quick-btn${s.starred ? " is-starred" : ""}`}
                        onClick={(e) => { e.preventDefault(); e.stopPropagation(); toggleStar(post.pk); }}
                        title={s.starred ? "중요 해제" : "중요 표시"}
                      >
                        {s.starred ? "⭐" : "☆"} 중요
                      </button>
                      <button
                        className="post-card-quick-btn"
                        onClick={(e) => { e.preventDefault(); e.stopPropagation(); toggleHide(post.pk); }}
                        title="목록에서 숨기기"
                      >
                        숨기기
                      </button>
                    </div>
                  ) : null}
                />
              );
            })
          ) : (
            <p className="muted" style={{ fontSize: "var(--text-sm)", padding: "var(--space-4) 0" }}>
              조건에 맞는 포스트가 없습니다.
            </p>
          )}
        </div>
      </section>
    </div>
  );
}
