/**
 * Footer component
 */
"use client";

import { usePathname } from "next/navigation";

export function Footer() {
  const pathname = usePathname();
  
  if (pathname === "/history/chat") return null;

  return (
    <footer className="border-t bg-gradient-to-r from-blue-50/50 via-cyan-50/50 to-teal-50/50 dark:from-gray-900/50 dark:via-cyan-900/20 dark:to-blue-900/20 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col items-center justify-center gap-2">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            © 2025{" "}
            <span
              className="font-semibold bg-clip-text text-transparent"
              style={{
                backgroundImage: 'linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 40%, #06b6d4 70%, #2dd4bf 100%)',
              }}
            >
              TradingAgentsX
            </span>
            . All rights reserved.
          </div>
          <a
            href="https://github.com/Yao920127/TradingAgentsX"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub"
            className="opacity-90 hover:opacity-100 hover:scale-110 transition-all"
          >
            <svg
              viewBox="0 0 24 24"
              width="22"
              height="22"
              fill="none"
              stroke="url(#footer-github-gradient)"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <defs>
                <linearGradient id="footer-github-gradient" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#1d4ed8" />
                  <stop offset="40%" stopColor="#0ea5e9" />
                  <stop offset="70%" stopColor="#06b6d4" />
                  <stop offset="100%" stopColor="#2dd4bf" />
                </linearGradient>
              </defs>
              <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
              <path d="M9 18c-4.51 2-5-2-7-2" />
            </svg>
          </a>
        </div>
      </div>
    </footer>
  );
}
