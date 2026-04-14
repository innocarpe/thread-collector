"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

type Ctx = {
  openId: string | null;
  setOpenId: (id: string | null) => void;
};

const FilterSheetCtx = createContext<Ctx>({
  openId: null,
  setOpenId: () => {},
});

export function FilterSheetProvider({ children }: { children: React.ReactNode }) {
  const [openId, setOpenId] = useState<string | null>(null);
  const searchParams = useSearchParams();
  const key = searchParams.toString();

  useEffect(() => {
    setOpenId(null);
  }, [key]);

  useEffect(() => {
    if (!openId) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpenId(null);
    };
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener("keydown", onKey);
    };
  }, [openId]);

  return (
    <FilterSheetCtx.Provider value={{ openId, setOpenId }}>
      {children}
    </FilterSheetCtx.Provider>
  );
}

export function FilterSheetTrigger({
  id,
  label,
  summary,
}: {
  id: string;
  label: string;
  summary?: string;
}) {
  const { setOpenId } = useContext(FilterSheetCtx);
  return (
    <button
      type="button"
      className="filter-sheet-trigger"
      onClick={() => setOpenId(id)}
      aria-label={`${label} 필터 열기`}
    >
      <span className="filter-sheet-trigger-label">{label}</span>
      {summary && <span className="filter-sheet-trigger-summary">{summary}</span>}
      <span className="filter-sheet-trigger-caret" aria-hidden>
        ▾
      </span>
    </button>
  );
}

export function FilterSheetPanel({
  id,
  label,
  children,
}: {
  id: string;
  label: string;
  children: React.ReactNode;
}) {
  const { openId, setOpenId } = useContext(FilterSheetCtx);
  const open = openId === id;
  return (
    <div className={`filter-sheet ${open ? "open" : ""}`} data-sheet-id={id}>
      <div
        className="filter-sheet-overlay"
        onClick={() => setOpenId(null)}
        aria-hidden
      />
      <div className="filter-sheet-panel" role="dialog" aria-modal="true" aria-label={label}>
        <div className="filter-sheet-header">
          <span className="filter-sheet-handle" aria-hidden />
          <span className="filter-sheet-title">{label}</span>
          <button
            type="button"
            className="filter-sheet-close"
            onClick={() => setOpenId(null)}
            aria-label="닫기"
          >
            ✕
          </button>
        </div>
        <div className="filter-sheet-body">{children}</div>
      </div>
    </div>
  );
}
