import type { AnalysisResponse } from "@/lib/types";

/** Analyst key (backend) → path of its report inside `reports`. */
const PDF_SECTIONS: ReadonlyArray<readonly [string, string]> = [
  ["market", "market_report"],
  ["social", "sentiment_report"],
  ["news", "news_report"],
  ["fundamentals", "fundamentals_report"],
  ["bull", "investment_debate_state.bull_history"],
  ["bear", "investment_debate_state.bear_history"],
  ["research_manager", "investment_debate_state.judge_decision"],
  ["trader", "trader_investment_plan"],
  ["risky", "risk_debate_state.risky_history"],
  ["safe", "risk_debate_state.safe_history"],
  ["neutral", "risk_debate_state.neutral_history"],
  ["risk_manager", "risk_debate_state.judge_decision"],
];

const getPath = (obj: unknown, path: string): unknown =>
  path.split(".").reduce<unknown>(
    (cur, key) =>
      cur && typeof cur === "object" ? (cur as Record<string, unknown>)[key] : undefined,
    obj,
  );

const toText = (value: unknown): string => {
  if (Array.isArray(value)) {
    return value
      .map((b) => (typeof b === "string" ? b : (b as { text?: string })?.text ?? ""))
      .join("");
  }
  return typeof value === "string" ? value : "";
};

const detectLanguage = (reports: unknown): "zh-TW" | "en" => {
  const plan = getPath(reports, "trader_investment_plan");
  if (typeof plan !== "string") return "zh-TW";
  return /[一-龥]/.test(plan) ? "zh-TW" : "en";
};

/** Body for POST /api/pdf/generate, or null when no report has content. */
export function buildPdfRequestBody(result: AnalysisResponse) {
  const analysts = PDF_SECTIONS.filter(
    ([, path]) => toText(getPath(result.reports, path)).trim().length > 0,
  ).map(([key]) => key);
  if (analysts.length === 0) return null;

  return {
    analysts,
    ticker: result.ticker,
    analysis_date: result.analysis_date,
    reports: result.reports,
    price_data: result.price_data,
    price_stats: result.price_stats,
    language: detectLanguage(result.reports),
    deep_think_llm: result.deep_think_llm,
    quick_think_llm: result.quick_think_llm,
  };
}
