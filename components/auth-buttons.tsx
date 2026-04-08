"use client";

import { signIn, signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";

export function SignInButton() {
  return (
    <Button kind="primary" onClick={() => signIn("github", { callbackUrl: "/" })}>
      GitHub로 로그인
    </Button>
  );
}

export function SignOutButton() {
  return (
    <Button kind="ghost" onClick={() => signOut({ callbackUrl: "/login" })}>
      로그아웃
    </Button>
  );
}
