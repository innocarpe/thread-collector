import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { auth } from "@/auth";
import { MarkdownBody } from "@/components/ui/markdown-body";
import { NaverCatBadge } from "@/components/naver/naver-cat-badge";
import { getNaverPost, getAllNaverPostIds, getNaverCafes } from "@/lib/naver-posts";
import { NAVER_SEGMENT_LABELS } from "@/types/naver-post";

type Props = {
  params: { cafe: string; id: string };
};

export async function generateStaticParams() {
  const cafes = getNaverCafes();
  const result: { cafe: string; id: string }[] = [];
  for (const cafe of cafes) {
    const ids = getAllNaverPostIds(cafe);
    for (const id of ids) {
      result.push({ cafe, id });
    }
  }
  return result;
}

export async function generateMetadata({ params }: Props) {
  const post = getNaverPost(params.cafe, params.id);
  return {
    title: post ? `${post.title} — NaverCafe Reader` : "Not Found",
  };
}

export default async function NaverPostPage({ params }: Props) {
  const session = await auth();
  if (!session) redirect("/login");

  const { cafe, id } = params;
  const post = getNaverPost(cafe, id);
  if (!post) notFound();

  return (
    <>
      <header className="app-header">
        <div className="app-header-brand">
          <Link href="/" className="app-header-wordmark">
            Thread Collector
          </Link>
          <span className="app-header-sub">NaverCafe</span>
        </div>
        <nav style={{ display: "flex", gap: "var(--space-3)" }}>
          <Link
            href={`/naver/${cafe}`}
            className="button ghost"
            style={{ borderRadius: "var(--radius-sm)" }}
          >
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
              <NaverCatBadge categorySlug={post.categorySlug} label={post.category} />
            </div>

            <div className="post-rail-block">
              <div className="post-rail-label">Segment</div>
              <span className="post-rail-value">
                {NAVER_SEGMENT_LABELS[post.segment]}
              </span>
            </div>

            <div className="post-rail-block">
              <div className="post-rail-label">게시판</div>
              <span className="post-rail-value">{post.menu}</span>
            </div>

            <div className="post-rail-block">
              <div className="post-rail-label">작성자</div>
              <span className="post-rail-value">{post.writer}</span>
            </div>

            <div className="post-rail-block">
              <div className="post-rail-label">Date</div>
              <span className="post-rail-value">{post.date}</span>
              {post.writeDateMs > 0 && (
                <span
                  className="post-rail-timestamp"
                  title={new Date(post.writeDateMs).toISOString()}
                >
                  {new Date(post.writeDateMs).toLocaleString("ko-KR", {
                    timeZone: "Asia/Seoul",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
              )}
            </div>

            <div className="post-rail-block">
              <div className="post-rail-label">Source</div>
              <a
                href={post.source}
                target="_blank"
                rel="noreferrer"
                className="post-rail-link"
              >
                카페에서 보기 ↗
              </a>
            </div>

            <div className="post-rail-cat-link">
              <Link
                href={`/naver/${cafe}?segment=${post.segment}&category=${post.categorySlug}`}
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
                <NaverCatBadge categorySlug={post.categorySlug} label={post.category} />
                <span className="soft" style={{ fontSize: "var(--text-sm)" }}>
                  {post.writer}
                </span>
                <span className="soft" style={{ fontSize: "var(--text-sm)" }}>
                  {post.date}
                </span>
              </div>
              <h1 className="post-title">{post.title}</h1>
            </header>

            <MarkdownBody content={post.content} />
          </article>
        </div>
      </main>
    </>
  );
}
