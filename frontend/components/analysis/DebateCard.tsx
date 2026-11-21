/**
 * One participant of a debate, rendered as a self-contained column.
 * Several of these sit side by side so the whole debate is readable without tab-switching:
 * each body scrolls inside a capped height, and the enlarge button opens the full text in a dialog.
 */
"use client";

import {
  TrendingUp,
  TrendingDown,
  Zap,
  Shield,
  Scale,
  Gavel,
  ClipboardCheck,
  Maximize2,
  type LucideIcon,
} from "lucide-react";
import { MarkdownReport } from "@/components/analysis/MarkdownReport";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { useLanguage } from "@/contexts/LanguageContext";
import { cn } from "@/lib/utils";

export type DebateTone =
  | "bull"
  | "bear"
  | "aggressive"
  | "conservative"
  | "neutral"
  // The manager verdicts, shown alongside the debaters they arbitrate.
  | "investmentPlan"
  | "riskDecision";

interface DebateCardProps {
  tone: DebateTone;
  title: string;
  content: string;
}

const TONE_THEME: Record<
  DebateTone,
  { icon: LucideIcon; header: string; label: string; ring: string }
> = {
  bull: {
    icon: TrendingUp,
    header: "bg-pale-green dark:bg-deep-green/40 ",
    label: "text-deep-green dark:text-pale-green ",
    ring: "border-deep-green/30 dark:border-pale-green/30 ",
  },
  bear: {
    icon: TrendingDown,
    header: "bg-coral-soft/20 dark:bg-destructive/15 ",
    label: "text-destructive ",
    ring: "border-destructive/30 ",
  },
  aggressive: {
    icon: Zap,
    header: "bg-coral-soft/20 dark:bg-destructive/15 ",
    label: "text-destructive ",
    ring: "border-destructive/30 ",
  },
  conservative: {
    icon: Shield,
    header: "bg-pale-green dark:bg-deep-green/40 ",
    label: "text-deep-green dark:text-pale-green ",
    ring: "border-deep-green/30 dark:border-pale-green/30 ",
  },
  neutral: {
    icon: Scale,
    header: "bg-secondary ",
    label: "text-deep-green dark:text-pale-green ",
    ring: "border-border ",
  },
  investmentPlan: {
    icon: ClipboardCheck,
    header: "bg-secondary ",
    label: "text-deep-green dark:text-pale-green ",
    ring: "border-border ",
  },
  riskDecision: {
    icon: Gavel,
    header: "bg-coral/10 ",
    label: "text-foreground ",
    ring: "border-coral/50 ",
  },
};

export function DebateCard({ tone, title, content }: DebateCardProps) {
  const { t } = useLanguage();
  const theme = TONE_THEME[tone];
  const Icon = theme.icon;

  return (
    <div
      className={cn(
        "flex h-full flex-col overflow-hidden rounded-xl border bg-card ",
        theme.ring,
        // Capped so every column stays comparable on screen; the full text opens in a dialog.
        "max-h-[26rem] lg:max-h-[32rem]",
      )}
    >
      <div
        className={cn(
          "flex shrink-0 items-center gap-2 border-b px-4 py-2.5",
          theme.header,
          theme.ring,
        )}
      >
        <Icon className={cn("h-4 w-4 shrink-0", theme.label)} />
        <h3 className={cn("min-w-0 flex-1 truncate text-sm font-semibold", theme.label)}>{title}</h3>

        <Dialog>
          <DialogTrigger asChild>
            <button
              type="button"
              title={t.results.sections.enlarge}
              aria-label={`${t.results.sections.enlarge}: ${title}`}
              className={cn(
                "-mr-1.5 shrink-0 rounded-md p-1.5 opacity-70 transition hover:bg-black/5 hover:opacity-100 dark:hover:bg-white/10",
                theme.label,
              )}
            >
              <Maximize2 className="h-4 w-4" />
            </button>
          </DialogTrigger>
          <DialogContent
            aria-describedby={undefined}
            className={cn(
              "flex max-h-[88vh] flex-col gap-0 overflow-hidden p-0 sm:max-w-4xl",
              theme.ring,
            )}
          >
            <div
              className={cn(
                "flex shrink-0 items-center gap-2 border-b py-3.5 pl-6 pr-12",
                theme.header,
                theme.ring,
              )}
            >
              <Icon className={cn("h-5 w-5 shrink-0", theme.label)} />
              <DialogTitle className={cn("truncate text-base font-semibold", theme.label)}>
                {title}
              </DialogTitle>
            </div>
            <div className="min-h-0 flex-1 overflow-y-auto px-6 py-6 md:px-10">
              <MarkdownReport>{content}</MarkdownReport>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-4 py-4">
        <MarkdownReport compact>{content}</MarkdownReport>
      </div>
    </div>
  );
}
