"use client";
import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from "react";
import { getStore, saveStore, type PostStatus } from "@/lib/reader-store";

type ReaderCtx = {
  hydrated: boolean;
  getStatus: (pk: string) => PostStatus;
  markRead: (pk: string) => void;
  toggleRead: (pk: string) => void;
  toggleStar: (pk: string) => void;
  toggleHide: (pk: string) => void;
  toggleLabel: (pk: string, label: string) => void;
  createLabel: (label: string) => void;
  deleteLabel: (label: string) => void;
  allLabels: string[];
};


const Ctx = createContext<ReaderCtx | null>(null);

// Optimistic update locally + fire-and-forget to GitHub
async function syncToGitHub(pk: string, update: Partial<PostStatus>) {
  try {
    await fetch("/api/reader-status", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pk, update }),
    });
  } catch {
    // silently fail — localStorage is the source of truth for UI
  }
}

export function ReaderProvider({ children }: { children: ReactNode }) {
  const [store, setStore] = useState<Record<string, PostStatus>>({});
  const [extraLabels, setExtraLabels] = useState<string[]>([]);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const local = getStore();
    setStore(local);
    try {
      setExtraLabels(JSON.parse(localStorage.getItem("tc-labels") || "[]"));
    } catch {}
    setHydrated(true);

    // Background: merge remote reader-status.json into local store
    // Remote is the source of truth for starred/hidden/labels across re-collections.
    // Local overrides remote (most recent action wins).
    fetch("/api/reader-status")
      .then((r) => r.ok ? r.json() : {})
      .then((remote: Record<string, PostStatus>) => {
        setStore((prev) => {
          // Merge: for each pk, remote fills in what local doesn't have
          const merged: Record<string, PostStatus> = { ...remote };
          for (const pk of Object.keys(prev)) {
            merged[pk] = { ...remote[pk], ...prev[pk] };
          }
          saveStore(merged);
          return merged;
        });
      })
      .catch(() => {});
  }, []);

  const mutate = useCallback(
    (pk: string, fn: (prev: PostStatus) => PostStatus) => {
      setStore((prev) => {
        const updated = fn(prev[pk] ?? {});
        const next = { ...prev, [pk]: updated };
        saveStore(next);
        // Strip read — too noisy (900+ posts). Only sync starred/hidden/labels to GitHub.
        const { read: _read, ...syncable } = updated;
        if (Object.keys(syncable).length > 0) syncToGitHub(pk, syncable);
        return next;
      });
    },
    []
  );

  const markRead = useCallback(
    (pk: string) => {
      setStore((prev) => {
        if (prev[pk]?.read) return prev; // already read — no-op
        const updated = { ...prev[pk], read: true };
        const next = { ...prev, [pk]: updated };
        saveStore(next);
        return next;
      });
    },
    []
  );

  const toggleRead = useCallback(
    (pk: string) => mutate(pk, (s) => ({ ...s, read: !s.read })),
    [mutate]
  );

  const toggleStar = useCallback(
    (pk: string) => mutate(pk, (s) => ({ ...s, starred: !s.starred })),
    [mutate]
  );

  const toggleHide = useCallback(
    (pk: string) => mutate(pk, (s) => ({ ...s, hidden: !s.hidden })),
    [mutate]
  );

  const toggleLabel = useCallback(
    (pk: string, label: string) =>
      mutate(pk, (s) => {
        const cur = s.labels ?? [];
        const labels = cur.includes(label)
          ? cur.filter((l) => l !== label)
          : [...cur, label];
        return { ...s, labels };
      }),
    [mutate]
  );

  const createLabel = useCallback((label: string) => {
    setExtraLabels((prev) => {
      if (prev.includes(label)) return prev;
      const next = [...prev, label].sort();
      localStorage.setItem("tc-labels", JSON.stringify(next));
      return next;
    });
  }, []);

  const deleteLabel = useCallback(
    (label: string) => {
      setStore((prev) => {
        const next = { ...prev };
        for (const pk of Object.keys(next)) {
          if (next[pk].labels?.includes(label)) {
            const updated = { ...next[pk], labels: next[pk].labels!.filter((l) => l !== label) };
            next[pk] = updated;
            syncToGitHub(pk, updated);
          }
        }
        saveStore(next);
        return next;
      });
      setExtraLabels((prev) => {
        const next = prev.filter((l) => l !== label);
        localStorage.setItem("tc-labels", JSON.stringify(next));
        return next;
      });
    },
    []
  );

  const usedLabels = [
    ...new Set(Object.values(store).flatMap((s) => s.labels ?? [])),
  ].sort();
  const allLabels = [...new Set([...extraLabels, ...usedLabels])].sort();

  function getStatus(pk: string): PostStatus {
    return store[pk] ?? {};
  }

  return (
    <Ctx.Provider
      value={{
        hydrated,
        getStatus,
        markRead,
        toggleRead,
        toggleStar,
        toggleHide,
        toggleLabel,
        createLabel,
        deleteLabel,
        allLabels,
      }}
    >
      {children}
    </Ctx.Provider>
  );
}

export function useReader() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useReader must be inside ReaderProvider");
  return ctx;
}
