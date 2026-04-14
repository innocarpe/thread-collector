import Link from "next/link";
import type { NaverPostMeta } from "@/types/naver-post";
import { NaverCatBadge } from "@/components/naver/naver-cat-badge";

type NaverPostCardProps = {
  post: NaverPostMeta;
  cafe: string;
};

export function NaverPostCard({ post, cafe }: NaverPostCardProps) {
  return (
    <Link href={`/naver/${cafe}/posts/${post.id}`} className="post-card">
      <div className="post-card-meta">
        <NaverCatBadge categorySlug={post.categorySlug} label={post.category} />
        <span className="post-card-author">{post.writer}</span>
        <span className="post-card-date">{post.date}</span>
        <span
          className="post-auto-label-chip"
          style={{ fontSize: "10px" }}
        >
          {post.menu}
        </span>
      </div>
      <h3 className="post-card-title">{post.title}</h3>
      <p className="post-card-excerpt">{post.excerpt}</p>
    </Link>
  );
}
