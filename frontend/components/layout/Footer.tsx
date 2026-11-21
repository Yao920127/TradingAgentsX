/**
 * Footer component — near-black band, muted links (design system: footer-newsletter surface)
 */
"use client";

import { usePathname } from "next/navigation";

export function Footer() {
  const pathname = usePathname();

  if (pathname === "/history/chat") return null;

  return (
    <footer className="bg-near-black text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="text-xs text-muted-slate">
            © 2025 <span className="font-display text-white">TradingAgentsX</span>. All rights
            reserved.
          </div>
          <a
            href="https://github.com/Yao920127/TradingAgentsX"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub"
            className="text-muted-slate transition-colors hover:text-white"
          >
            <svg
              viewBox="0 0 24 24"
              width="22"
              height="22"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.75"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
              <path d="M9 18c-4.51 2-5-2-7-2" />
            </svg>
          </a>
        </div>
      </div>
    </footer>
  );
}
