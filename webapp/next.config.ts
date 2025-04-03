import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    // For development (when running in Docker)
    api_end_point: process.env.NODE_ENV === 'development'
      ? "http://127.0.0.1:8000"
      : "http://127.0.0.1:8000",

    // Or for production builds:
    // api_end_point: process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
  },
  // Enable rewrites for API calls
  async rewrites() {
    return [
      {
        source: '/minio/:path*',
        destination: 'http://localhost:9000/:path*'
      }
    ]
  }
};

export default nextConfig;