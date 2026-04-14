export type NaverSegment = "operator" | "community";
export type NaverCategorySlug =
  | "income-methods"
  | "tools-ai"
  | "case-studies"
  | "marketing"
  | "uncategorized";

export const NAVER_CATEGORY_LABELS: Record<NaverCategorySlug, string> = {
  "income-methods": "수익화 방법",
  "tools-ai": "도구/AI",
  "case-studies": "성공 사례",
  "marketing": "마케팅",
  "uncategorized": "미분류",
};

export const NAVER_CATEGORIES: NaverCategorySlug[] = [
  "income-methods",
  "tools-ai",
  "case-studies",
  "marketing",
  "uncategorized",
];

export const NAVER_SEGMENT_LABELS: Record<NaverSegment, string> = {
  operator: "★ 운영자",
  community: "일반 커뮤니티",
};

export type NaverPostMeta = {
  id: string;           // article_id as string
  cafe: string;
  segment: NaverSegment;
  category: string;     // 한글 display name
  categorySlug: NaverCategorySlug;
  menu: string;
  writer: string;
  date: string;
  writeDateMs: number;
  source: string;
  title: string;
  excerpt: string;
};

export type NaverPost = NaverPostMeta & {
  content: string;
};

export type NaverCafeInsights = {
  overview?: string;           // 00-overview.md
  operatorAnalysis?: string;   // operator/full-analysis.md
  operatorIncome?: string;     // operator/income-methods.md
  operatorTools?: string;      // operator/tools-stack.md
  operatorMarketing?: string;  // operator/marketing-tactics.md
  communityIncome?: string;    // community/income-methods.md
  communityTools?: string;     // community/tools-ai.md
  communityCases?: string;     // community/case-studies.md
  communityQa?: string;        // community/qa-pain-points.md
};
