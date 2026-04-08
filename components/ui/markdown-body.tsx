type Props = { content: string };

export function MarkdownBody({ content }: Props) {
  // Strip leading # heading (already rendered as post-title)
  const body = content.replace(/^\s*#[^#][^\n]*\n?/, "").trim();

  // Split on double newlines → paragraphs
  const blocks = body.split(/\n{2,}/).map((b) => b.trim()).filter(Boolean);

  return (
    <div className="markdown-body">
      {blocks.map((block, i) => {
        if (block.startsWith("## ")) {
          return <h2 key={i}>{block.slice(3)}</h2>;
        }
        // Single newlines within a block → <br>
        const lines = block.split("\n");
        return (
          <p key={i}>
            {lines.map((line, j) => (
              <span key={j}>
                {line}
                {j < lines.length - 1 && <br />}
              </span>
            ))}
          </p>
        );
      })}
    </div>
  );
}
