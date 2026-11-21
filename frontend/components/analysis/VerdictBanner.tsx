/**
 * Headline verdict panel shown at the top of a report:
 * the final BUY/SELL/HOLD call plus the numbers needed to judge it at a glance.
 */
"use client";

import { useLanguage } from "@/contexts/LanguageContext";
import { cn } from "@/lib/utils";
import type { DecisionSignal } from "@/lib/report-utils";

interface VerdictBannerProps {
  action: string;
  signal: DecisionSignal;
  /** 0–1, or null when the report contains no parsable value. */
  confidence: number | null;
  analystCount: number;
  /** Percent change over the analysed window, e.g. -3.86. */
  periodChange?: number | null;
  marketLabel?: string | null;
  /** Source filename or task id, shown small and monospaced on the right. */
  sourceLabel?: string | null;
}

const SIGNAL_THEME: Record<
  DecisionSignal,
  { panel: string; text: string; bar: string }
> = {
  buy: {
    panel:
      "border-deep-green/30 dark:border-pale-green/30 bg-pale-green dark:bg-deep-green/40  ",
    text: "text-deep-green dark:text-pale-green ",
    bar: "bg-deep-green dark:bg-pale-green ",
  },
  sell: {
    panel:
      "border-destructive/30 bg-coral-soft/20 dark:bg-destructive/15  ",
    text: "text-destructive ",
    bar: "bg-destructive ",
  },
  hold: {
    panel:
      "border-coral/50 bg-coral/10  ",
    text: "text-foreground ",
    bar: "bg-coral",
  },
  unknown: {
    panel: "border-border bg-muted/40",
    text: "text-muted-foreground",
    bar: "bg-muted-foreground",
  },
};

export function VerdictBanner({
  action,
  signal,
  confidence,
  analystCount,
  periodChange,
  marketLabel,
  sourceLabel,
}: VerdictBannerProps) {
  const { t } = useLanguage();
  const theme = SIGNAL_THEME[signal];
  const v = t.results.verdict;

  const changeTone =
    periodChange == null
      ? "text-muted-foreground"
      : periodChange >= 0
        ? "text-deep-green dark:text-pale-green "
        : "text-destructive ";

  return (
    <section
      className={cn(
        "rounded-2xl border px-5 py-5 sm:px-7 sm:py-6 animate-scale-up",
        theme.panel,
      )}
    >
      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
        {/* Verdict + supporting numbers */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:gap-7 min-w-0">
          <div className="shrink-0">
            <div
              className={cn(
                "font-serif leading-none tracking-tight text-5xl sm:text-6xl",
                theme.text,
              )}
            >
              {signal === "unknown" ? v.undecided : action}
            </div>
            <div className="mt-1.5 text-xs text-muted-foreground">{v.label}</div>
          </div>

          <div className="min-w-0 space-y-2.5 text-sm">
            {confidence != null && (
              <div className="flex items-center gap-3">
                <span className="text-muted-foreground shrink-0">{v.confidence}</span>
                <div className="h-1.5 w-24 sm:w-32 overflow-hidden rounded-full bg-foreground/10">
                  <div
                    className={cn("h-full rounded-full", theme.bar)}
                    style={{ width: `${Math.round(confidence * 100)}%` }}
                  />
                </div>
                <span className="font-medium tabular-nums">
                  {Math.round(confidence * 100)}%
                </span>
              </div>
            )}

            <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
              <span className="text-muted-foreground">
                {v.analystCount}{" "}
                <span className="font-medium tabular-nums text-foreground">
                  {analystCount}
                </span>
                {v.analystCountUnit ? ` ${v.analystCountUnit}` : ""}
              </span>
              {periodChange != null && (
                <span className="text-muted-foreground">
                  {v.periodChange}{" "}
                  <span className={cn("font-medium tabular-nums", changeTone)}>
                    {periodChange >= 0 ? "+" : ""}
                    {periodChange.toFixed(2)}%
                  </span>
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Provenance */}
        <div className="flex shrink-0 flex-row items-center gap-3 lg:flex-col lg:items-end lg:gap-2">
          {marketLabel && (
            <span className="rounded-full border border-border/70 bg-background/60 px-2.5 py-0.5 text-xs text-muted-foreground">
              {marketLabel}
            </span>
          )}
          {sourceLabel && (
            <span className="truncate font-mono text-[11px] text-muted-foreground/70">
              {sourceLabel}
            </span>
          )}
        </div>
      </div>
    </section>
  );
}
