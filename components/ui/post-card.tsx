import Link from "next/link";
import type { PostMeta } from "@/types/post";
import type { PostStatus } from "@/lib/reader-store";
import { CatBadge } from "@/components/ui/cat-badge";
import type { ReactNode } from "react";

type PostCardProps = {
  post: PostMeta;
  showAuthor?: boolean;
  status?: PostStatus;
  actions?: ReactNode;
};

export function PostCard({ post, showAuthor = true, status = {}, actions }: PostCardProps) {
  return (
    <Link href={`/posts/${post.pk}`} className={`post-card ${status.read ? "is-read" : ""}`}>
      <div className="post-card-meta">
        <CatBadge categorySlug={post.categorySlug} label={post.category} />
        {showAuthor && <span className="post-card-author">{post.username}</span>}
        <span className="post-card-date">{post.date}</span>
        {status.labels?.map((lbl) => (
          <span key={lbl} className="post-label-chip">{lbl}</span>
        ))}
      </div>
      <h3 className="post-card-title">{post.title}</h3>
      <p className="post-card-excerpt">{post.excerpt}</p>
      {actions && <div className="post-card-footer">{actions}</div>}
    </Link>
  );
}
