import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/auth";
import { getPostByPk } from "@/lib/posts";
import type { PostStatus } from "@/lib/reader-store";

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_REPO = process.env.GITHUB_REPO; // "owner/repo"

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

  const post = getPostByPk(pk);
  if (!post) return NextResponse.json({ error: "Post not found" }, { status: 404 });

  const apiBase = `https://api.github.com/repos/${GITHUB_REPO}/contents/${post.filePath}`;
  const headers = {
    Authorization: `Bearer ${GITHUB_TOKEN}`,
    Accept: "application/vnd.github+json",
    "Content-Type": "application/json",
    "X-GitHub-Api-Version": "2022-11-28",
  };

  // 1. GET current file from GitHub
  const getRes = await fetch(apiBase, { headers });
  if (!getRes.ok) {
    return NextResponse.json({ error: `GitHub GET failed: ${getRes.status}` }, { status: 502 });
  }
  const fileData = await getRes.json();
  const currentContent = Buffer.from(fileData.content, "base64").toString("utf-8");
  const sha = fileData.sha;

  // 2. Update frontmatter fields
  const updatedContent = applyStatusToFrontmatter(currentContent, update);

  // 3. PUT updated file back
  const putRes = await fetch(apiBase, {
    method: "PUT",
    headers,
    body: JSON.stringify({
      message: buildCommitMessage(pk, update),
      content: Buffer.from(updatedContent).toString("base64"),
      sha,
    }),
  });

  if (!putRes.ok) {
    const err = await putRes.text();
    return NextResponse.json({ error: `GitHub PUT failed: ${err}` }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}

function applyStatusToFrontmatter(raw: string, update: Partial<PostStatus>): string {
  if (!raw.startsWith("---")) return raw;

  const endIdx = raw.indexOf("---", 3);
  if (endIdx === -1) return raw;

  const fmBlock = raw.slice(3, endIdx).trim();
  const body = raw.slice(endIdx + 3);

  const lines = fmBlock.split("\n");

  // Fields to manage
  const fields: (keyof PostStatus)[] = ["read", "starred", "hidden", "labels"];

  // Remove existing reader fields
  const cleaned = lines.filter((l) => {
    const key = l.split(":")[0].trim();
    return !fields.includes(key as keyof PostStatus);
  });

  // Append updated fields
  for (const [key, val] of Object.entries(update)) {
    if (val === undefined || val === false || (Array.isArray(val) && val.length === 0)) continue;
    if (Array.isArray(val)) {
      cleaned.push(`${key}: [${val.map((v) => JSON.stringify(v)).join(", ")}]`);
    } else {
      cleaned.push(`${key}: ${val}`);
    }
  }

  return `---\n${cleaned.join("\n")}\n---${body}`;
}

function buildCommitMessage(pk: string, update: Partial<PostStatus>): string {
  const parts: string[] = [];
  if (update.read !== undefined) parts.push(update.read ? "read" : "unread");
  if (update.starred !== undefined) parts.push(update.starred ? "starred" : "unstarred");
  if (update.hidden !== undefined) parts.push(update.hidden ? "hidden" : "unhidden");
  if (update.labels !== undefined) parts.push(`labels: [${update.labels.join(", ")}]`);
  return `reader: ${parts.join(", ")} — ${pk}`;
}
