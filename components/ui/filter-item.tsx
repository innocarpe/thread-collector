import Link from "next/link";

type FilterItemProps = {
  href: string;
  active?: boolean;
  label: string;
  count: number;
};

export function FilterItem({ href, active = false, label, count }: FilterItemProps) {
  return (
    <Link href={href} className={`filter-item ${active ? "active" : ""}`}>
      <span>{label}</span>
      <span className="count-pill">{count}</span>
    </Link>
  );
}
