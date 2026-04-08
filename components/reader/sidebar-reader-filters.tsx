"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import type { PostMeta } from "@/types/post";
import { useReader } from "./reader-context";
import { FilterItem } from "@/components/ui/filter-item";
import { SectionHeading } from "@/components/ui/section-heading";

type Props = {
  posts: PostMeta[];
  userFilter?: string;
  categoryFilter?: string;
};

export function SidebarReaderFilters({ posts, userFilter, categoryFilter }: Props) {
  const { getStatus, allLabels } = useReader();
  const searchParams = useSearchParams();
  const statusFilter = searchParams.get("status") ?? "";
  const labelFilter = searchParams.get("label") ?? "";
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  function buildHref(extra: Record<string, string>) {
    const q = new URLSearchParams();
    if (userFilter) q.set("user", userFilter);
    if (categoryFilter) q.set("category", categoryFilter);
    for (const [k, v] of Object.entries(extra)) {
      if (v) q.set(k, v);
    }
    const s = q.toString();
    return s ? `/?${s}` : "/";
  }

  const visiblePosts = mounted ? posts.filter((p) => !getStatus(p.pk).hidden) : posts;
  const unreadCount = mounted ? visiblePosts.filter((p) => !getStatus(p.pk).read).length : 0;
  const starredCount = mounted ? visiblePosts.filter((p) => getStatus(p.pk).starred).length : 0;
  const hiddenCount = mounted ? posts.filter((p) => getStatus(p.pk).hidden).length : 0;

  return (
    <>
      <div className="sidebar-group">
        <SectionHeading kind="sidebar">Status</SectionHeading>
        <div className="filter-list">
          <FilterItem
            href={buildHref({})}
            active={!statusFilter && !labelFilter}
            label="전체"
            count={visiblePosts.length}
          />
          <FilterItem
            href={buildHref({ status: "unread" })}
            active={statusFilter === "unread"}
            label="안읽음"
            count={unreadCount}
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

      {allLabels.length > 0 && (
        <div className="sidebar-group">
          <SectionHeading kind="sidebar">Labels</SectionHeading>
          <div className="filter-list">
            {allLabels.map((lbl) => {
              const cnt = mounted
                ? posts.filter((p) => getStatus(p.pk).labels?.includes(lbl)).length
                : 0;
              return (
                <FilterItem
                  key={lbl}
                  href={buildHref({ label: lbl })}
                  active={labelFilter === lbl}
                  label={lbl}
                  count={cnt}
                />
              );
            })}
          </div>
        </div>
      )}
    </>
  );
}
