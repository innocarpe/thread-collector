"use client";
import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from "react";
import {
  getNaverStore,
  saveNaverStore,
  type NaverPostStatus,
} from "@/lib/naver-reader-store";

type NaverReaderCtx = {
  hydrated: boolean;
  getStatus: (id: string) => NaverPostStatus;
  toggleStar: (id: string) => void;
  toggleHide: (id: string) => void;
};

const Ctx = createContext<NaverReaderCtx | null>(null);

export function NaverReaderProvider({ children }: { children: ReactNode }) {
  const [store, setStore] = useState<Record<string, NaverPostStatus>>({});
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setStore(getNaverStore());
    setHydrated(true);
  }, []);

  const mutate = useCallback(
    (id: string, fn: (prev: NaverPostStatus) => NaverPostStatus) => {
      setStore((prev) => {
        const updated = fn(prev[id] ?? {});
        const next = { ...prev, [id]: updated };
        saveNaverStore(next);
        return next;
      });
    },
    []
  );

  const toggleStar = useCallback(
    (id: string) => mutate(id, (s) => ({ ...s, starred: !s.starred })),
    [mutate]
  );

  const toggleHide = useCallback(
    (id: string) => mutate(id, (s) => ({ ...s, hidden: !s.hidden })),
    [mutate]
  );

  function getStatus(id: string): NaverPostStatus {
    return store[id] ?? {};
  }

  return (
    <Ctx.Provider value={{ hydrated, getStatus, toggleStar, toggleHide }}>
      {children}
    </Ctx.Provider>
  );
}

export function useNaverReader() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useNaverReader must be inside NaverReaderProvider");
  return ctx;
}
