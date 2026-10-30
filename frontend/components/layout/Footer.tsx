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
            className="text-gray-500 hover:text-cyan-600 dark:text-gray-400 dark:hover:text-cyan-400 transition-colors"
          >
            <svg
              viewBox="0 0 24 24"
              width="22"
              height="22"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M12 .5C5.73.5.5 5.73.5 12c0 5.08 3.29 9.39 7.86 10.91.58.1.79-.25.79-.56v-2c-3.2.7-3.87-1.54-3.87-1.54-.52-1.33-1.28-1.69-1.28-1.69-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.03 1.76 2.69 1.25 3.35.96.1-.74.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.59.23 2.76.11 3.05.74.8 1.18 1.82 1.18 3.08 0 4.42-2.69 5.39-5.25 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.73 18.27.5 12 .5z" />
            </svg>
          </a>
        </div>
      </div>
    </footer>
  );
}
