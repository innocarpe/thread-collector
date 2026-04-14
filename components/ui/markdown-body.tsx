import { marked } from "marked";

type Props = { content: string };

// Strip the top-level # heading — already shown as page/section title
function stripTopHeading(content: string): string {
  return content.replace(/^\s*#(?!#)[^\n]*\n?/, "").trim();
}

export function MarkdownBody({ content }: Props) {
  const body = stripTopHeading(content);
  const html = marked(body, { async: false }) as string;
  return <div className="markdown-body" dangerouslySetInnerHTML={{ __html: html }} />;
}
