import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { auth } from "@/auth";
import { MarkdownBody } from "@/components/ui/markdown-body";
import { CatBadge } from "@/components/ui/cat-badge";
import { PostActions } from "@/components/reader/post-actions";
import { getAllPks, getPostByPk } from "@/lib/posts";

type Props = { params: { slug: string } };

// Pre-render all post pages at build time
export async function generateStaticParams() {
  return getAllPks().map((pk) => ({ slug: pk }));
}

export async function generateMetadata({ params }: Props) {
  const post = getPostByPk(params.slug);
  return { title: post ? `${post.title} — Thread Collector` : "Not Found" };
}

export default async function PostPage({ params }: Props) {
  const session = await auth();
  if (!session) redirect("/login");

  const post = getPostByPk(params.slug);
  if (!post) notFound();

  return (
    <>
      {/* App Header */}
      <header className="app-header">
        <div className="app-header-brand">
          <span className="app-header-wordmark">Thread Collector</span>
        </div>
        <nav style={{ display: "flex", gap: "var(--space-3)" }}>
          <Link href="/" className="button ghost" style={{ borderRadius: "var(--radius-sm)" }}>
            ← 목록으로
          </Link>
        </nav>
      </header>

      <main className="post-page">
        <div className="post-layout">
          {/* Rail (metadata) */}
          <aside className="post-rail">
            <div className="post-rail-block">
              <div className="post-rail-label">Category</div>
              <CatBadge categorySlug={post.categorySlug} label={post.category} />
            </div>

            <div className="post-rail-block">
              <div className="post-rail-label">Author</div>
              <span className="post-rail-value">{post.username}</span>
            </div>

            <div className="post-rail-block">
              <div className="post-rail-label">Date</div>
              <span className="post-rail-value">{post.date}</span>
              {post.takenAt > 0 && (
                <span className="post-rail-timestamp" title={new Date(post.takenAt * 1000).toISOString()}>
                  {new Date(post.takenAt * 1000).toLocaleString("ko-KR", {
                    timeZone: "Asia/Seoul",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
              )}
            </div>

            {post.chainPks && post.chainPks.length > 0 && (
              <div className="post-rail-block">
                <div className="post-rail-label">Chain</div>
                <div className="post-rail-chain">
                  <span className="post-rail-value" style={{ fontSize: "11px" }}>
                    {post.chainPks.length + 1}개 파트 병합
                  </span>
                  <details style={{ marginTop: "4px" }}>
                    <summary style={{ fontSize: "11px", cursor: "pointer", color: "var(--color-text-soft)" }}>
                      PKs 보기
                    </summary>
                    <div style={{ marginTop: "4px", display: "grid", gap: "2px" }}>
                      <code style={{ fontSize: "10px", color: "var(--color-text-soft)" }}>{post.pk} (main)</code>
                      {post.chainPks.map((cpk) => (
                        <code key={cpk} style={{ fontSize: "10px", color: "var(--color-text-soft)" }}>{cpk}</code>
                      ))}
                    </div>
                  </details>
                </div>
              </div>
            )}

            <div className="post-rail-block">
              <div className="post-rail-label">Source</div>
              <a
                href={post.source}
                target="_blank"
                rel="noreferrer"
                className="post-rail-link"
              >
                Threads에서 보기 ↗
              </a>
            </div>

            <div style={{ marginTop: "var(--space-3)" }}>
              <Link
                href={`/?user=${post.usernameSlug}&category=${post.categorySlug}`}
                className="button secondary"
                style={{ fontSize: "var(--text-xs)", padding: "6px var(--space-3)" }}
              >
                같은 카테고리 보기
              </Link>
            </div>
          </aside>

          {/* Article */}
          <article className="post-article">
            <header className="post-header">
              <div className="post-header-meta">
                <CatBadge categorySlug={post.categorySlug} label={post.category} />
                <span className="soft" style={{ fontSize: "var(--text-sm)" }}>
                  {post.username}
                </span>
                <span className="soft" style={{ fontSize: "var(--text-sm)" }}>
                  {post.date}
                </span>
              </div>
              <h1 className="post-title">{post.title}</h1>
            </header>

            <MarkdownBody content={post.content} />
            <PostActions pk={post.pk} />
          </article>
        </div>
      </main>
    </>
  );
}
