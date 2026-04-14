"use client";

import { useState } from "react";
import { MarkdownBody } from "@/components/ui/markdown-body";

type Tab = {
  key: string;
  label: string;
  content?: string;
};

type Props = {
  tabs: Tab[];
  heading: string;
};

export function NaverInsightsTabs({ tabs, heading }: Props) {
  const [active, setActive] = useState(tabs[0]?.key ?? "");
  const current = tabs.find((t) => t.key === active);

  return (
    <div>
      <div className="naver-tabs-bar">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            className={`naver-tab-btn${active === tab.key ? " active" : ""}`}
            onClick={() => setActive(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div style={{ marginTop: "var(--space-5)" }}>
        {current?.content ? (
          <MarkdownBody content={current.content} />
        ) : (
          <p className="soft" style={{ fontSize: "var(--text-sm)" }}>
            아직 생성되지 않았습니다.
          </p>
        )}
      </div>
    </div>
  );
}
