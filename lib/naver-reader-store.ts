export type NaverPostStatus = {
  starred?: boolean;
  hidden?: boolean;
};

const KEY = "naver-reader";

export function getNaverStore(): Record<string, NaverPostStatus> {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}");
  } catch {
    return {};
  }
}

export function saveNaverStore(store: Record<string, NaverPostStatus>) {
  if (typeof window === "undefined") return;
  localStorage.setItem(KEY, JSON.stringify(store));
}
