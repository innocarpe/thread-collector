import Link from "next/link";
import type { PostMeta } from "@/types/post";
import type { PostStatus } from "@/lib/reader-store";
import { CatBadge } from "@/components/ui/cat-badge";

type PostCardProps = {
  post: PostMeta;
  showAuthor?: boolean;
  status?: PostStatus;
};

export function PostCard({ post, showAuthor = true, status = {} }: PostCardProps) {
  return (
    <Link href={`/posts/${post.pk}`} className={`post-card ${status.read ? "is-read" : ""}`}>
      <div className="post-card-meta">
        <CatBadge categorySlug={post.categorySlug} label={post.category} />
        {showAuthor && <span className="post-card-author">{post.username}</span>}
        <span className="post-card-date">{post.date}</span>
        {status.starred && <span className="post-card-star">⭐</span>}
        {status.labels?.map((lbl) => (
          <span key={lbl} className="post-label-chip">{lbl}</span>
        ))}
      </div>
      <h3 className="post-card-title">{post.title}</h3>
      <p className="post-card-excerpt">{post.excerpt}</p>
      <div className="post-card-footer">
        {status.read && <span className="post-card-read-mark">읽음</span>}
        <span>읽기 →</span>
      </div>
    </Link>
  );
}
