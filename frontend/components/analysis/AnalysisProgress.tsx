/**
 * Analysis progress panel
 * Shows which agent is working, which step the pipeline is on, and elapsed time
 */
"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, Circle, Clock, Database, Loader2 } from "lucide-react";
import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import { cn } from "@/lib/utils";
import type { TranslationKeys } from "@/lib/i18n";
import type { ProgressDetail, ProgressStep } from "@/lib/types";

interface AnalysisProgressProps {
  detail: ProgressDetail | null;
  /** Server clock minus client clock, in seconds */
  clockOffset: number;
  /** Client epoch ms when the analysis was submitted */
  startedAt: number | null;
}

// Backend agent keys -> existing names in t.agents
const AGENT_NAME_KEYS: Record<string, keyof TranslationKeys["agents"]> = {
  market_analyst: "market_analyst",
  social_analyst: "social_analyst",
  news_analyst: "news_analyst",
  fundamentals_analyst: "fundamentals_analyst",
  report_summarizer: "report_summarizer",
  bull_researcher: "bull_researcher",
  bear_researcher: "bear_researcher",
  research_manager: "research_manager",
  trader: "trader",
  risky_analyst: "aggressive_debator",
  safe_analyst: "conservative_debator",
  neutral_analyst: "neutral_debator",
  risk_judge: "risk_manager",
};

function formatDuration(totalSeconds: number): string {
  const s = Math.max(0, Math.floor(totalSeconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = String(s % 60).padStart(2, "0");
  return h > 0 ? `${h}:${String(m).padStart(2, "0")}:${sec}` : `${m}:${sec}`;
}

function fill(template: string, values: Record<string, number>): string {
  return template.replace(/\{(\w+)\}/g, (_, k) => String(values[k] ?? ""));
}

export function AnalysisProgress({ detail, clockOffset, startedAt }: AnalysisProgressProps) {
  const { t } = useLanguage();
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const serverNow = now / 1000 + clockOffset;

  const agentName = (key: string) => {
    const k = AGENT_NAME_KEYS[key];
    return k ? t.agents[k] : key;
  };
  const stepName = (key: string) =>
    key === "research_debate" || key === "risk_debate" ? t.progress[key] : agentName(key);
  const stepDesc = (key: string) =>
    t.progress.stepDesc[key as keyof typeof t.progress.stepDesc] ?? "";
  const toolName = (key: string) =>
    t.progress.tools[key as keyof typeof t.progress.tools] ?? key;

  const stepDuration = (step: ProgressStep) => {
    if (step.started_at == null) return null;
    const end = step.completed_at ?? serverNow;
    return formatDuration(end - step.started_at);
  };

  const elapsed = startedAt ? formatDuration((now - startedAt) / 1000) : "0:00";
  const percent = detail ? Math.min(100, Math.max(0, detail.percent)) : 0;
  const steps = detail?.steps ?? [];
  const doneCount = steps.filter((s) => s.status === "completed").length;
  const currentStep = steps.find((s) => s.key === detail?.current_step);

  return (
    <Card className="px-5 py-6 md:px-8 md:py-8 gap-6" aria-live="polite">
      {/* Header: title + elapsed */}
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h2 className="text-lg md:text-xl font-semibold text-gray-900 dark:text-gray-100">
            {t.progress.title}
          </h2>
          {detail && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
              {fill(t.progress.stepsDone, { done: doneCount, total: steps.length })}
            </p>
          )}
        </div>
        <div className="flex flex-col items-end shrink-0">
          <span className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <Clock className="h-3.5 w-3.5" />
            {t.progress.elapsed}
          </span>
          <span className="text-2xl font-mono font-semibold tabular-nums text-gray-900 dark:text-gray-100">
            {elapsed}
          </span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="flex items-center gap-3">
        <div
          className="relative h-2.5 flex-1 rounded-full bg-gray-200/70 dark:bg-white/10 overflow-hidden"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={detail ? percent : undefined}
        >
          {detail ? (
            <div
              className="h-full rounded-full gradient-bg-primary transition-[width] duration-700 ease-out"
              style={{ width: `${Math.max(percent, 2)}%` }}
            />
          ) : (
            <div className="h-full w-1/3 rounded-full gradient-bg-primary animate-pulse" />
          )}
        </div>
        <span className="w-11 text-right text-sm font-mono tabular-nums text-gray-600 dark:text-gray-300">
          {detail ? `${percent}%` : "—"}
        </span>
      </div>

      {/* Current activity */}
      <div className="rounded-2xl bg-blue-50/70 dark:bg-blue-500/10 border border-blue-100 dark:border-blue-400/20 px-4 py-3 flex gap-3">
        {detail?.finished ? (
          <CheckCircle2 className="h-5 w-5 mt-0.5 shrink-0 text-emerald-500" />
        ) : (
          <Loader2 className="h-5 w-5 mt-0.5 shrink-0 animate-spin text-blue-500" />
        )}
        <div className="min-w-0 text-sm">
          {!detail || (!detail.current_agent && !detail.finished) ? (
            <p className="text-gray-700 dark:text-gray-200">{t.progress.initializing}</p>
          ) : detail.finished ? (
            <p className="text-gray-700 dark:text-gray-200">{t.progress.finalizing}</p>
          ) : (
            <>
              <p className="text-gray-800 dark:text-gray-100">
                <span className="font-semibold">{agentName(detail.current_agent!)}</span>{" "}
                {t.progress.working}
                {currentStep?.total_turns != null && (
                  <span className="text-gray-500 dark:text-gray-400">
                    {" · "}
                    {fill(t.progress.turn, {
                      done: Math.min((currentStep.turns_done ?? 0) + 1, currentStep.total_turns),
                      total: currentStep.total_turns,
                    })}
                  </span>
                )}
              </p>
              {detail.current_step && (
                <p className="text-gray-600 dark:text-gray-400 mt-0.5">{stepDesc(detail.current_step)}</p>
              )}
              {detail.current_tools.length > 0 && (
                <p className="text-blue-700 dark:text-blue-300 mt-1 flex items-center gap-1.5">
                  <Database className="h-3.5 w-3.5 shrink-0" />
                  <span className="truncate">
                    {t.progress.fetchingData}
                    {detail.current_tools.map(toolName).join(t.progress.listSeparator)}
                  </span>
                </p>
              )}
            </>
          )}
        </div>
      </div>

      {/* Step list */}
      {steps.length > 0 && (
        <ol className="space-y-1">
          {steps.map((step) => {
            const running = step.status === "running";
            const done = step.status === "completed";
            const duration = stepDuration(step);
            return (
              <li
                key={step.key}
                className={cn(
                  "flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition-colors",
                  running && "bg-blue-50/60 dark:bg-blue-500/10"
                )}
              >
                {done ? (
                  <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-500" />
                ) : running ? (
                  <Loader2 className="h-4 w-4 shrink-0 animate-spin text-blue-500" />
                ) : (
                  <Circle className="h-4 w-4 shrink-0 text-gray-300 dark:text-gray-600" />
                )}
                <span
                  className={cn(
                    "flex-1 min-w-0 truncate",
                    done && "text-gray-700 dark:text-gray-300",
                    running && "font-medium text-gray-900 dark:text-gray-100",
                    !done && !running && "text-gray-400 dark:text-gray-500"
                  )}
                >
                  {stepName(step.key)}
                  {step.total_turns != null && (done || running) && (
                    <span className="ml-2 text-xs font-mono tabular-nums text-gray-500 dark:text-gray-400">
                      {step.turns_done}/{step.total_turns}
                    </span>
                  )}
                </span>
                <span className="shrink-0 text-xs font-mono tabular-nums text-gray-500 dark:text-gray-400">
                  {duration ?? ""}
                </span>
              </li>
            );
          })}
        </ol>
      )}
    </Card>
  );
}
