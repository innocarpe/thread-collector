"use client";
import { useRouter } from "next/navigation";
import { useNaverReader } from "@/components/naver/naver-reader-context";

type Props = { id: string; cafe: string };

export function NaverPostActions({ id, cafe }: Props) {
  const router = useRouter();
  const { hydrated, getStatus, toggleStar, toggleHide } = useNaverReader();

  if (!hydrated) return null;

  const status = getStatus(id);

  return (
    <div className="post-actions">
      <button
        className={`post-action-btn ${status.starred ? "active-star" : ""}`}
        onClick={() => toggleStar(id)}
        title={status.starred ? "중요 해제" : "중요 표시"}
      >
        {status.starred ? "⭐ 중요" : "☆ 중요 표시"}
      </button>

      <button
        className={`post-action-btn ${status.hidden ? "active-hide" : ""}`}
        onClick={() => {
          toggleHide(id);
          if (!status.hidden) router.push(`/naver/${cafe}`);
        }}
        title={status.hidden ? "숨기기 취소" : "목록에서 숨기기"}
      >
        {status.hidden ? "숨김 해제" : "숨기기"}
      </button>
    </div>
  );
}
