/**
 * Shared markdown renderer for agent report bodies.
 * Centralises the prose/table styling that every report surface needs.
 */
"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";
import { normalizeReportMarkdown } from "@/lib/report-format";

interface MarkdownReportProps {
  children: string;
  className?: string;
  /** Slightly tighter type for the narrow debate columns. */
  compact?: boolean;
}

export function MarkdownReport({ children, className, compact = false }: MarkdownReportProps) {
  return (
    <div
      className={cn(
        "prose max-w-none dark:prose-invert",
        compact ? "prose-sm" : "prose-sm xl:prose-base",
        // One size per heading level across every report: only headings are
        // enlarged and bold; body text stays regular (key terms use **bold**).
        compact
          ? "prose-h2:text-base prose-h3:text-sm"
          : "prose-h2:text-lg xl:prose-h2:text-xl prose-h3:text-base xl:prose-h3:text-lg",
        "prose-h2:font-bold prose-h2:mt-6 prose-h2:mb-3 prose-h3:font-semibold prose-h3:mt-4 prose-h3:mb-2",
        "[&>*:first-child]:mt-0",
        // Tables can't wrap, so make each one its own horizontal scroller.
        // `block` is what allows the overflow; the page itself never scrolls sideways.
        "prose-table:block prose-table:overflow-x-auto prose-table:max-w-full",
        "prose-table:border-collapse",
        "prose-td:border prose-td:border-gray-300 dark:prose-td:border-gray-600 prose-td:p-2",
        "prose-th:border prose-th:border-gray-300 dark:prose-th:border-gray-600 prose-th:p-2",
        "prose-th:bg-gray-100 dark:prose-th:bg-gray-800",
        "prose-pre:overflow-x-auto break-words",
        className,
      )}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{normalizeReportMarkdown(children)}</ReactMarkdown>
    </div>
  );
}
