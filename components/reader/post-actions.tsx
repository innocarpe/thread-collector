"use client";
import { useEffect, useRef, useState } from "react";
import { useReader } from "./reader-context";

type Props = { pk: string };

export function PostActions({ pk }: Props) {
  const { getStatus, markRead, toggleRead, toggleStar, toggleHide, toggleLabel, createLabel, allLabels } = useReader();
  const [mounted, setMounted] = useState(false);
  const [showLabelMenu, setShowLabelMenu] = useState(false);
  const [newLabel, setNewLabel] = useState("");
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
    // Auto-mark as read
    markRead(pk);
  }, [pk, markRead]);

  useEffect(() => {
    function handle(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setShowLabelMenu(false);
      }
    }
    document.addEventListener("mousedown", handle);
    return () => document.removeEventListener("mousedown", handle);
  }, []);

  if (!mounted) return null;

  const status = getStatus(pk);

  function handleAddLabel(e: React.FormEvent) {
    e.preventDefault();
    const label = newLabel.trim();
    if (!label) return;
    createLabel(label);
    toggleLabel(pk, label);
    setNewLabel("");
  }

  return (
    <div className="post-actions">
      {/* Read toggle */}
      <button
        className={`post-action-btn ${status.read ? "active-read" : ""}`}
        onClick={() => toggleRead(pk)}
        title={status.read ? "읽음 취소" : "읽음 표시"}
      >
        {status.read ? "✓ 읽음" : "읽음 표시"}
      </button>

      {/* Star toggle */}
      <button
        className={`post-action-btn ${status.starred ? "active-star" : ""}`}
        onClick={() => toggleStar(pk)}
        title={status.starred ? "중요 해제" : "중요 표시"}
      >
        {status.starred ? "⭐ 중요" : "☆ 중요 표시"}
      </button>

      {/* Hide toggle */}
      <button
        className={`post-action-btn ${status.hidden ? "active-hide" : ""}`}
        onClick={() => toggleHide(pk)}
        title={status.hidden ? "숨기기 취소" : "목록에서 숨기기"}
      >
        {status.hidden ? "숨김 해제" : "숨기기"}
      </button>

      {/* Label menu */}
      <div ref={menuRef} style={{ position: "relative" }}>
        <button
          className={`post-action-btn ${(status.labels?.length ?? 0) > 0 ? "active-label" : ""}`}
          onClick={() => setShowLabelMenu((v) => !v)}
        >
          🏷 레이블{status.labels?.length ? ` (${status.labels.length})` : ""}
        </button>

        {showLabelMenu && (
          <div className="label-menu">
            {allLabels.length > 0 && (
              <div className="label-menu-list">
                {allLabels.map((lbl) => (
                  <label key={lbl} className="label-menu-item">
                    <input
                      type="checkbox"
                      checked={status.labels?.includes(lbl) ?? false}
                      onChange={() => toggleLabel(pk, lbl)}
                    />
                    <span>{lbl}</span>
                  </label>
                ))}
              </div>
            )}
            <form onSubmit={handleAddLabel} className="label-menu-add">
              <input
                placeholder="새 레이블 추가"
                value={newLabel}
                onChange={(e) => setNewLabel(e.target.value)}
                className="label-input"
                autoFocus
              />
              <button type="submit" className="label-add-btn">추가</button>
            </form>
          </div>
        )}
      </div>

      {/* Applied labels */}
      {(status.labels?.length ?? 0) > 0 && (
        <div className="post-action-labels">
          {status.labels!.map((lbl) => (
            <span key={lbl} className="post-label-chip" onClick={() => toggleLabel(pk, lbl)}>
              {lbl} ×
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
