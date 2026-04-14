"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import type { NaverPostMeta } from "@/types/naver-post";
import { useNaverReader } from "@/components/naver/naver-reader-context";
import { FilterItem } from "@/components/ui/filter-item";
import { SectionHeading } from "@/components/ui/section-heading";

type Props = {
  posts: NaverPostMeta[];
  cafe: string;
  segmentFilter?: string;
  categoryFilter?: string;
};

export function NaverSidebarStatusFilters({ posts, cafe, segmentFilter, categoryFilter }: Props) {
  const { getStatus } = useNaverReader();
  const searchParams = useSearchParams();
  const statusFilter = searchParams.get("status") ?? "";
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  function buildHref(extra: Record<string, string>) {
    const q = new URLSearchParams();
    if (segmentFilter) q.set("segment", segmentFilter);
    if (categoryFilter) q.set("category", categoryFilter);
    for (const [k, v] of Object.entries(extra)) {
      if (v) q.set(k, v);
    }
    const s = q.toString();
    return s ? `/naver/${cafe}?${s}` : `/naver/${cafe}`;
  }

  const visiblePosts = mounted ? posts.filter((p) => !getStatus(p.id).hidden) : posts;
  const starredCount = mounted ? visiblePosts.filter((p) => getStatus(p.id).starred).length : 0;
  const hiddenCount = mounted ? posts.filter((p) => getStatus(p.id).hidden).length : 0;

  return (
    <div className="sidebar-group">
      <SectionHeading kind="sidebar">Status</SectionHeading>
      <div className="filter-list">
        <FilterItem
          href={buildHref({})}
          active={!statusFilter}
          label="전체"
          count={visiblePosts.length}
        />
        <FilterItem
          href={buildHref({ status: "starred" })}
          active={statusFilter === "starred"}
          label="⭐ 중요"
          count={starredCount}
        />
        {hiddenCount > 0 && (
          <FilterItem
            href={buildHref({ status: "hidden" })}
            active={statusFilter === "hidden"}
            label="숨긴 글"
            count={hiddenCount}
          />
        )}
      </div>
    </div>
  );
}
