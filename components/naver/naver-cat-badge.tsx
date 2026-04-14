import type { NaverCategorySlug } from "@/types/naver-post";

type NaverCatBadgeProps = {
  categorySlug: NaverCategorySlug;
  label: string;
};

export function NaverCatBadge({ categorySlug, label }: NaverCatBadgeProps) {
  return (
    <span className={`cat-badge naver-cat-${categorySlug}`}>{label}</span>
  );
}
