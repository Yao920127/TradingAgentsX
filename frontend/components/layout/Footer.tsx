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
            className="text-sm text-gray-500 hover:text-cyan-600 dark:text-gray-400 dark:hover:text-cyan-400 transition-colors"
          >
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}
