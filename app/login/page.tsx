import { redirect } from "next/navigation";
import { auth } from "@/auth";
import { SignInButton } from "@/components/auth-buttons";
import { Chip } from "@/components/ui/chip";

export default async function LoginPage() {
  const session = await auth();
  if (session) redirect("/");

  return (
    <main className="auth-shell">
      <section className="surface auth elevated">
        <div className="auth-eyebrow">Private Access</div>
        <div className="chip-row" style={{ marginBottom: "var(--space-4)" }}>
          <Chip>GitHub OAuth</Chip>
          <Chip>Single-account</Chip>
        </div>
        <h1 className="auth-title">Thread Collector</h1>
        <p className="auth-copy">
          Threads에서 수집한 인사이트 아카이브입니다. 허용된 GitHub 계정으로만 접근할 수 있습니다.
        </p>
        <SignInButton />
      </section>
    </main>
  );
}
