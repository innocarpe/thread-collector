type SectionHeadingProps = {
  children: React.ReactNode;
  kind?: "section" | "sidebar" | "detail";
};

export function SectionHeading({ children, kind = "section" }: SectionHeadingProps) {
  const cls =
    kind === "sidebar" ? "sidebar-title" :
    kind === "detail"  ? "detail-section-title" :
    "section-title";
  return <h2 className={cls}>{children}</h2>;
}
