import { Suspense } from "react";
import { redirect } from "next/navigation";
import { auth } from "@/auth";
import { SignOutButton } from "@/components/auth-buttons";
import { Chip } from "@/components/ui/chip";
import { FilterItem } from "@/components/ui/filter-item";
import { SectionHeading } from "@/components/ui/section-heading";
import { PostListClient } from "@/components/reader/post-list-client";
import { SidebarReaderFilters } from "@/components/reader/sidebar-reader-filters";
import { getAllPostMetas, getUsers } from "@/lib/posts";
import { CATEGORIES, CATEGORY_LABELS } from "@/types/post";
import type { CategorySlug } from "@/types/post";

function buildHref(params: { user?: string; category?: string }) {
  const q = new URLSearchParams();
  if (params.user) q.set("user", params.user);
  if (params.category) q.set("category", params.category);
  const s = q.toString();
  return s ? `/?${s}` : "/";
}

type PageProps = {
  searchParams?: { user?: string; category?: string };
};

export default async function HomePage({ searchParams }: PageProps) {
  const session = await auth();
  if (!session) redirect("/login");

  const allPosts = getAllPostMetas();
  const users = getUsers();

  const userFilter = searchParams?.user;
  const categoryFilter = searchParams?.category as CategorySlug | undefined;

  const filtered = allPosts.filter((p) => {
    if (userFilter && p.usernameSlug !== userFilter) return false;
    if (categoryFilter && p.categorySlug !== categoryFilter) return false;
    return true;
  });

  // Compute AI label counts for the filtered set (descending order, min count 1)
  const labelCountMap = new Map<string, number>();
  for (const p of filtered) {
    for (const lbl of p.labels ?? []) {
      labelCountMap.set(lbl, (labelCountMap.get(lbl) ?? 0) + 1);
    }
  }
  const autoLabelCounts = Array.from(labelCountMap.entries())
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count);

  return (
    <>
      <header className="app-header">
        <div className="app-header-brand">
          <span className="app-header-wordmark">Thread Collector</span>
          <span className="app-header-sub">Private Reader</span>
        </div>
        <div className="app-header-actions">
          <div className="chip-row">
            <Chip>{allPosts.length} posts</Chip>
            <Chip>{users.length} users</Chip>
          </div>
          <SignOutButton />
        </div>
      </header>

      <main className="page-shell">
        <div className="layout">
          {/* Sidebar */}
          <aside className="sidebar">
            <section className="surface sidebar">
              <div className="sidebar-group">
                <SectionHeading kind="sidebar">Users</SectionHeading>
                <div className="filter-list">
                  <FilterItem
                    href={buildHref({ category: categoryFilter })}
                    active={!userFilter}
                    label="전체 유저"
                    count={allPosts.length}
                  />
                  {users.map((u) => (
                    <FilterItem
                      key={u}
                      href={buildHref({ user: u, category: categoryFilter })}
                      active={userFilter === u}
                      label={`@${u}`}
                      count={allPosts.filter((p) => p.usernameSlug === u).length}
                    />
                  ))}
                </div>
              </div>

              <div className="sidebar-group">
                <SectionHeading kind="sidebar">Category</SectionHeading>
                <div className="filter-list">
                  <FilterItem
                    href={buildHref({ user: userFilter })}
                    active={!categoryFilter}
                    label="전체 카테고리"
                    count={allPosts.filter((p) => !userFilter || p.usernameSlug === userFilter).length}
                  />
                  {CATEGORIES.map((cat) => (
                    <FilterItem
                      key={cat}
                      href={buildHref({ user: userFilter, category: cat })}
                      active={categoryFilter === cat}
                      label={CATEGORY_LABELS[cat]}
                      count={allPosts.filter(
                        (p) =>
                          p.categorySlug === cat &&
                          (!userFilter || p.usernameSlug === userFilter)
                      ).length}
                    />
                  ))}
                </div>
              </div>

              <Suspense fallback={null}>
                <SidebarReaderFilters
                  posts={filtered}
                  userFilter={userFilter}
                  categoryFilter={categoryFilter}
                  autoLabelCounts={autoLabelCounts}
                />
              </Suspense>
            </section>
          </aside>

          {/* Post List */}
          <Suspense fallback={null}>
            <PostListClient
              posts={filtered}
              userFilter={userFilter}
              categoryFilter={categoryFilter}
            />
          </Suspense>
        </div>
      </main>
    </>
  );
}
