import type { Metadata } from "next";
import "./globals.css";
import { ReaderProvider } from "@/components/reader/reader-context";

export const metadata: Metadata = {
  title: "Thread Collector",
  description: "Private Threads insight reader",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <ReaderProvider>{children}</ReaderProvider>
      </body>
    </html>
  );
}
