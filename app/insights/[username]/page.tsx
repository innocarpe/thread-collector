import Link from "next/link";
import { redirect } from "next/navigation";
import { auth } from "@/auth";
import { getInsightsForUser } from "@/lib/posts";
import { SectionHeading } from "@/components/ui/section-heading";
import { MarkdownBody } from "@/components/ui/markdown-body";

type PageProps = {
  params: { username: string };
};

export default async function InsightsPage({ params }: PageProps) {
  const session = await auth();
  if (!session) redirect("/login");

  const usernameSlug = params.username;
  const insights = getInsightsForUser(usernameSlug);

  return (
    <main className="page-shell">
      <Link href="/" className="post-back">
        <span aria-hidden>←</span> 홈으로
      </Link>
      <section className="surface detail">
        <header className="insights-header">
          <p className="eyebrow">Insights</p>
          <h1 className="insights-title">@{usernameSlug}</h1>
          <p className="insights-subtitle">AI가 요약한 글쓴이의 관점과 패턴</p>
        </header>

        {!insights && (
          <p className="text-muted">
            아직 AI 인사이트가 생성되지 않았습니다. `/insights @{usernameSlug}`를 다시 실행해 주세요.
          </p>
        )}

        {insights?.overview && (
          <article className="insights-section">
            <SectionHeading kind="detail">Overview</SectionHeading>
            <MarkdownBody content={insights.overview} />
          </article>
        )}

        {insights?.patterns && (
          <article className="insights-section">
            <SectionHeading kind="detail">Patterns</SectionHeading>
            <MarkdownBody content={insights.patterns} />
          </article>
        )}

        {insights?.keyPosts && (
          <article className="insights-section">
            <SectionHeading kind="detail">Key Posts</SectionHeading>
            <MarkdownBody content={insights.keyPosts} />
          </article>
        )}
      </section>
    </main>
  );
}
