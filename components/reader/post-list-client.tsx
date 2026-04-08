"use client";
import { useEffect, useState } from "react";
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
  const { getStatus } = useReader();
  const searchParams = useSearchParams();
  const statusFilter = searchParams.get("status") ?? "";
  const labelFilter = searchParams.get("label") ?? "";
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  const filtered = posts.filter((p) => {
    if (!mounted) return true; // SSR: show all (hidden via CSS until mounted)
    const s = getStatus(p.pk);
    if (statusFilter === "hidden") return !!s.hidden;
    if (s.hidden) return false;
    if (statusFilter === "unread") return !s.read;
    if (statusFilter === "starred") return !!s.starred;
    if (labelFilter) return s.labels?.includes(labelFilter) ?? false;
    return true;
  });

  const isFiltered = !!(userFilter || categoryFilter || statusFilter || labelFilter);

  return (
    <div style={!mounted ? { visibility: "hidden" } : undefined}>
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
            filtered.map((post) => (
              <PostCard
                key={post.pk}
                post={post}
                showAuthor={!userFilter}
                status={mounted ? getStatus(post.pk) : {}}
              />
            ))
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
