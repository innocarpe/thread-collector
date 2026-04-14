type Props = { content: string };

function renderMarkdownContent(content: string) {
  const body = content.replace(/^\s*#[^#][^\n]*\n?/, "").trim();
  const blocks = body.split(/\n{2,}/).map((b) => b.trim()).filter(Boolean);
  return blocks
    .map((block) => {
      if (block.startsWith("## ")) {
        return `<h2>${block.slice(3)}</h2>`;
      }
      const lines = block.split("\n");
      return `<p>${lines.map((line) => line.replace(/</g, "&lt;").replace(/>/g, "&gt;")).join("<br />")}</p>`;
    })
    .join("");
}

export function MarkdownBody({ content }: Props) {
  const html = renderMarkdownContent(content);
  return <div className="markdown-body" dangerouslySetInnerHTML={{ __html: html }} />;
}
