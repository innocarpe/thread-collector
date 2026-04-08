import type { CategorySlug } from "@/types/post";

type CatBadgeProps = {
  categorySlug: CategorySlug;
  label: string;
};

export function CatBadge({ categorySlug, label }: CatBadgeProps) {
  return <span className={`cat-badge ${categorySlug}`}>{label}</span>;
}
