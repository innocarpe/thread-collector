"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import type { PostMeta } from "@/types/post";
import { useReader } from "./reader-context";
import { FilterItem } from "@/components/ui/filter-item";
import { SectionHeading } from "@/components/ui/section-heading";

type AutoLabelCount = { label: string; count: number };

type Props = {
  posts: PostMeta[];
  userFilter?: string;
  categoryFilter?: string;
  autoLabelCounts?: AutoLabelCount[];
  section?: "status" | "topics";
};

export function SidebarReaderFilters({
  posts,
  userFilter,
  categoryFilter,
  autoLabelCounts,
  section,
}: Props) {
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

  const showStatus = !section || section === "status";
  const showTopics = !section || section === "topics";

  return (
    <>
      {showStatus && (
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
      )}

      {showTopics && (autoLabelCounts?.length ?? 0) > 0 && (
        <div className="sidebar-group">
          <SectionHeading kind="sidebar">토픽</SectionHeading>
          <div className="filter-list">
            {autoLabelCounts!.map(({ label, count }) => (
              <FilterItem
                key={label}
                href={buildHref({ label })}
                active={labelFilter === label}
                label={label}
                count={count}
              />
            ))}
          </div>
        </div>
      )}

      {showTopics && allLabels.length > 0 && (
        <div className="sidebar-group">
          <SectionHeading kind="sidebar">내 태그</SectionHeading>
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
