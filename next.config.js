/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    // Bundle Threads/ markdown files with Vercel serverless functions
    outputFileTracingIncludes: {
      "/(.*)?": ["./Threads/**"],
    },
  },
};

module.exports = nextConfig;
