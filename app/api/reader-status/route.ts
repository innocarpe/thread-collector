import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/auth";
import type { PostStatus } from "@/lib/reader-store";

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_REPO = process.env.GITHUB_REPO; // "owner/repo"

const STATUS_PATH = "reader-status.json";
const STATUS_API = () =>
  `https://api.github.com/repos/${GITHUB_REPO}/contents/${STATUS_PATH}`;

const ghHeaders = () => ({
  Authorization: `Bearer ${GITHUB_TOKEN}`,
  Accept: "application/vnd.github+json",
  "Content-Type": "application/json",
  "X-GitHub-Api-Version": "2022-11-28",
});

// GET /api/reader-status — return full store from GitHub
export async function GET(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  if (!GITHUB_TOKEN || !GITHUB_REPO) {
    return NextResponse.json({});
  }

  const res = await fetch(STATUS_API(), { headers: ghHeaders() });
  if (res.status === 404) return NextResponse.json({});
  if (!res.ok) return NextResponse.json({});

  const data = await res.json();
  try {
    const content = Buffer.from(data.content, "base64").toString("utf-8");
    return NextResponse.json(JSON.parse(content));
  } catch {
    return NextResponse.json({});
  }
}

// PATCH /api/reader-status
// Body: { pk: string; update: Partial<PostStatus> }
export async function PATCH(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  if (!GITHUB_TOKEN || !GITHUB_REPO) {
    return NextResponse.json({ ok: true, skipped: "no token" });
  }

  const { pk, update } = (await req.json()) as { pk: string; update: Partial<PostStatus> };
  if (!pk || !update) return NextResponse.json({ error: "Missing pk or update" }, { status: 400 });

  const api = STATUS_API();
  const headers = ghHeaders();

  // 1. GET current reader-status.json (may not exist yet)
  const getRes = await fetch(api, { headers });
  let current: Record<string, PostStatus> = {};
  let sha: string | undefined;

  if (getRes.ok) {
    const fileData = await getRes.json();
    sha = fileData.sha;
    try {
      current = JSON.parse(Buffer.from(fileData.content, "base64").toString("utf-8"));
    } catch {
      current = {};
    }
  } else if (getRes.status !== 404) {
    return NextResponse.json({ error: `GitHub GET failed: ${getRes.status}` }, { status: 502 });
  }

  // 2. Merge update
  const prev = current[pk] ?? {};
  const merged = { ...prev, ...update };
  // Remove falsy non-array fields and empty arrays to keep file tidy
  const cleaned: PostStatus = {};
  for (const [k, v] of Object.entries(merged)) {
    if (v === false || v === undefined) continue;
    if (Array.isArray(v) && v.length === 0) continue;
    (cleaned as Record<string, unknown>)[k] = v;
  }
  current[pk] = cleaned;

  // 3. PUT updated file back
  const putBody: Record<string, unknown> = {
    message: `reader: update ${pk}`,
    content: Buffer.from(JSON.stringify(current, null, 2)).toString("base64"),
  };
  if (sha) putBody.sha = sha;

  const putRes = await fetch(api, {
    method: "PUT",
    headers,
    body: JSON.stringify(putBody),
  });

  if (!putRes.ok) {
    const err = await putRes.text();
    return NextResponse.json({ error: `GitHub PUT failed: ${err}` }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}
