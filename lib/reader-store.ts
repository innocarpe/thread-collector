export type PostStatus = {
  read?: boolean;
  starred?: boolean;
  hidden?: boolean;
  labels?: string[];
};

const KEY = "tc-reader";

export function getStore(): Record<string, PostStatus> {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}");
  } catch {
    return {};
  }
}

export function saveStore(store: Record<string, PostStatus>) {
  if (typeof window === "undefined") return;
  localStorage.setItem(KEY, JSON.stringify(store));
}
