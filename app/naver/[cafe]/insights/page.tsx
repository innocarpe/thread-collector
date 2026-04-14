import Link from "next/link";
import { redirect } from "next/navigation";
import { auth } from "@/auth";
import { SectionHeading } from "@/components/ui/section-heading";
import { MarkdownBody } from "@/components/ui/markdown-body";
import { NaverInsightsTabs } from "@/components/naver/naver-insights-tabs";
import { getNaverInsights, getNaverCafes } from "@/lib/naver-posts";

type Props = {
  params: { cafe: string };
};

export async function generateStaticParams() {
  return getNaverCafes().map((cafe) => ({ cafe }));
}

export async function generateMetadata({ params }: Props) {
  return { title: `${params.cafe} 인사이트 — NaverCafe Reader` };
}

export default async function NaverInsightsPage({ params }: Props) {
  const session = await auth();
  if (!session) redirect("/login");

  const { cafe } = params;
  const insights = getNaverInsights(cafe);

  const operatorTabs = [
    { key: "full-analysis", label: "전체 분석", content: insights?.operatorAnalysis },
    { key: "income-methods", label: "수익화 방법", content: insights?.operatorIncome },
    { key: "tools-stack", label: "도구/스택", content: insights?.operatorTools },
    { key: "marketing-tactics", label: "마케팅 전략", content: insights?.operatorMarketing },
  ];

  const communityTabs = [
    { key: "income-methods", label: "수익화 방법", content: insights?.communityIncome },
    { key: "tools-ai", label: "도구/AI", content: insights?.communityTools },
    { key: "case-studies", label: "성공 사례", content: insights?.communityCases },
    { key: "qa-pain-points", label: "Q&A / 고민", content: insights?.communityQa },
  ];

  return (
    <main className="page-shell">
      <Link href={`/naver/${cafe}`} className="post-back">
        <span aria-hidden>←</span> {cafe} 목록으로
      </Link>

      <section className="surface detail">
        <header className="insights-header">
          <p className="eyebrow">NaverCafe Insights</p>
          <h1 className="insights-title">{cafe}</h1>
          <p className="insights-subtitle">AI가 분석한 카페 게시글 인사이트</p>
        </header>

        {!insights && (
          <p className="muted" style={{ fontSize: "var(--text-sm)" }}>
            아직 인사이트가 생성되지 않았습니다. `/insights {cafe}` 를 실행해 주세요.
          </p>
        )}

        {/* Overview */}
        {insights?.overview && (
          <article className="insights-section">
            <SectionHeading kind="detail">Overview</SectionHeading>
            <MarkdownBody content={insights.overview} />
          </article>
        )}

        {/* Operator Analysis */}
        <article className="insights-section">
          <SectionHeading kind="detail">★ 운영자 분석</SectionHeading>
          <NaverInsightsTabs tabs={operatorTabs} heading="운영자 분석" />
        </article>

        {/* Community Analysis */}
        <article className="insights-section">
          <SectionHeading kind="detail">커뮤니티 분석</SectionHeading>
          <NaverInsightsTabs tabs={communityTabs} heading="커뮤니티 분석" />
        </article>
      </section>
    </main>
  );
}
