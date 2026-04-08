import { getServerSession, type NextAuthOptions } from "next-auth";
import GitHubProvider from "next-auth/providers/github";
import type { Session } from "next-auth";

const allowedEmails = (process.env.ALLOWED_EMAILS || "")
  .split(",")
  .map((v) => v.trim().toLowerCase())
  .filter(Boolean);

const isDevBypass =
  process.env.NODE_ENV !== "production" && process.env.DEV_AUTH_BYPASS === "true";

const devSession: Session = {
  user: {
    name: "Local Dev",
    email: process.env.ALLOWED_EMAILS?.split(",")[0]?.trim() || "local@example.com",
  },
  expires: "2999-12-31T23:59:59.999Z",
};

export const authOptions: NextAuthOptions = {
  providers: [
    GitHubProvider({
      clientId: process.env.GITHUB_ID || "",
      clientSecret: process.env.GITHUB_SECRET || "",
    }),
  ],
  session: { strategy: "jwt" },
  callbacks: {
    async signIn({ user }) {
      if (!allowedEmails.length) return true;
      const email = user.email?.toLowerCase();
      return !!email && allowedEmails.includes(email);
    },
  },
  pages: { signIn: "/login" },
};

export function auth() {
  if (isDevBypass) return Promise.resolve(devSession);
  return getServerSession(authOptions);
}
