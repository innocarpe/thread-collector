import { Suspense } from "react";
import Link from "next/link";
import { redirect } from "next/navigation";
import { auth } from "@/auth";
import { FilterItem } from "@/components/ui/filter-item";
import { SectionHeading } from "@/components/ui/section-heading";
import { Chip } from "@/components/ui/chip";
import { NaverReaderProvider } from "@/components/naver/naver-reader-context";
import { NaverPostListClient } from "@/components/naver/naver-post-list-client";
import { NaverSidebarStatusFilters } from "@/components/naver/naver-sidebar-status-filters";
import {
  getNaverPostMetas,
  getNaverInsights,
  getNaverCafes,
} from "@/lib/naver-posts";
import {
  NAVER_CATEGORIES,
  NAVER_CATEGORY_LABELS,
  NAVER_SEGMENT_LABELS,
} from "@/types/naver-post";
import type { NaverCategorySlug, NaverSegment } from "@/types/naver-post";

type PageProps = {
  params: { cafe: string };
  searchParams?: { segment?: string; category?: string; status?: string };
};

function buildHref(
  cafe: string,
  params: { segment?: string; category?: string; status?: string }
) {
  const q = new URLSearchParams();
  if (params.segment) q.set("segment", params.segment);
  if (params.category) q.set("category", params.category);
  if (params.status) q.set("status", params.status);
  const s = q.toString();
  return s ? `/naver/${cafe}?${s}` : `/naver/${cafe}`;
}

export async function generateStaticParams() {
  return getNaverCafes().map((cafe) => ({ cafe }));
}

export async function generateMetadata({ params }: { params: { cafe: string } }) {
  return { title: `${params.cafe} — NaverCafe Reader` };
}

export default async function NaverCafePage({ params, searchParams }: PageProps) {
  const session = await auth();
  if (!session) redirect("/login");

  const { cafe } = params;
  const segmentFilter = searchParams?.segment as NaverSegment | undefined;
  const categoryFilter = searchParams?.category as NaverCategorySlug | undefined;

  const allPosts = getNaverPostMetas(cafe);
  const insights = getNaverInsights(cafe);
  const hasInsights = Boolean(insights && Object.values(insights).some(Boolean));

  // Pre-filter by segment/category (server-side); status filter is client-side
  const preFiltered = allPosts.filter((p) => {
    if (segmentFilter && p.segment !== segmentFilter) return false;
    if (categoryFilter && p.categorySlug !== categoryFilter) return false;
    return true;
  });

  return (
    <NaverReaderProvider>
      <header className="app-header">
        <div className="app-header-brand">
          <Link href="/" className="app-header-wordmark" style={{ cursor: "pointer" }}>
            Thread Collector
          </Link>
          <span className="app-header-sub">NaverCafe</span>
          <span
            className="app-header-wordmark"
            style={{ color: "var(--color-accent)", fontWeight: 700 }}
          >
            {cafe}
          </span>
        </div>
        <div className="app-header-actions">
          <div className="chip-row">
            <Chip>{allPosts.length} posts</Chip>
          </div>
          <Link href="/" className="button ghost" style={{ borderRadius: "var(--radius-sm)" }}>
            ← 홈으로
          </Link>
        </div>
      </header>

      <main className="page-shell">
        <div className="layout">
          {/* Sidebar */}
          <aside className="sidebar">
            <section className="surface sidebar">
              <div className="sidebar-group">
                <SectionHeading kind="sidebar">Segment</SectionHeading>
                <div className="filter-list">
                  <FilterItem
                    href={buildHref(cafe, { category: categoryFilter })}
                    active={!segmentFilter}
                    label="전체"
                    count={allPosts.filter((p) =>
                      !categoryFilter || p.categorySlug === categoryFilter
                    ).length}
                  />
                  {(["operator", "community"] as NaverSegment[]).map((seg) => (
                    <FilterItem
                      key={seg}
                      href={buildHref(cafe, { segment: seg, category: categoryFilter })}
                      active={segmentFilter === seg}
                      label={NAVER_SEGMENT_LABELS[seg]}
                      count={allPosts.filter(
                        (p) =>
                          p.segment === seg &&
                          (!categoryFilter || p.categorySlug === categoryFilter)
                      ).length}
                    />
                  ))}
                </div>
              </div>

              <div className="sidebar-group">
                <SectionHeading kind="sidebar">Category</SectionHeading>
                <div className="filter-list">
                  <FilterItem
                    href={buildHref(cafe, { segment: segmentFilter })}
                    active={!categoryFilter}
                    label="전체 카테고리"
                    count={allPosts.filter(
                      (p) => !segmentFilter || p.segment === segmentFilter
                    ).length}
                  />
                  {NAVER_CATEGORIES.filter((cat) =>
                    allPosts.some((p) => p.categorySlug === cat)
                  ).map((cat) => (
                    <FilterItem
                      key={cat}
                      href={buildHref(cafe, { segment: segmentFilter, category: cat })}
                      active={categoryFilter === cat}
                      label={NAVER_CATEGORY_LABELS[cat]}
                      count={allPosts.filter(
                        (p) =>
                          p.categorySlug === cat &&
                          (!segmentFilter || p.segment === segmentFilter)
                      ).length}
                    />
                  ))}
                </div>
              </div>

              <Suspense fallback={null}>
                <NaverSidebarStatusFilters
                  posts={preFiltered}
                  cafe={cafe}
                  segmentFilter={segmentFilter}
                  categoryFilter={categoryFilter}
                />
              </Suspense>

              {hasInsights && (
                <div className="sidebar-group">
                  <SectionHeading kind="sidebar">Insights</SectionHeading>
                  <div className="filter-list">
                    <Link
                      href={`/naver/${cafe}/insights`}
                      className="filter-item"
                    >
                      <span>✨ 인사이트 보기</span>
                    </Link>
                  </div>
                </div>
              )}
            </section>
          </aside>

          {/* Post List — client component for star/hide filtering */}
          <Suspense fallback={null}>
            <NaverPostListClient
              posts={preFiltered}
              cafe={cafe}
              segmentFilter={segmentFilter}
              categoryFilter={categoryFilter}
            />
          </Suspense>
        </div>
      </main>
    </NaverReaderProvider>
  );
}
