/**
 * Time-range slicing for the report's price chart. Works on the bars the report
 * already carries (the backend keeps the year before the analysis date), so it
 * needs no extra request and also works for previously saved reports.
 */
import type { PriceData, PriceStats } from "./types";

export type PriceRangeId = "1M" | "3M" | "6M" | "YTD" | "1Y";

export const PRICE_RANGE_IDS: readonly PriceRangeId[] = ["1M", "3M", "6M", "YTD", "1Y"];

/** How many days the first bar may sit after a range start and still count as covering it. */
const COVERAGE_TOLERANCE_DAYS = 7;
const MS_PER_DAY = 86_400_000;

const parseDay = (date: string): number => Date.parse(`${date.slice(0, 10)}T00:00:00Z`);
const formatDay = (ms: number): string => new Date(ms).toISOString().slice(0, 10);

function monthsBefore(endMs: number, months: number): number {
  const end = new Date(endMs);
  return Date.UTC(end.getUTCFullYear(), end.getUTCMonth() - months, end.getUTCDate());
}

/** First day (YYYY-MM-DD) of the range, . */
function rangeStart(id: PriceRangeId, lastDate: string): string {
  const end = parseDay(lastDate);
  switch (id) {
    case "1M":
      return formatDay(monthsBefore(end, 1));
    case "3M":
      return formatDay(monthsBefore(end, 3));
    case "6M":
      return formatDay(monthsBefore(end, 6));
    case "1Y":
      return formatDay(monthsBefore(end, 12));
    case "YTD":
      return `${lastDate.slice(0, 4)}-01-01`;
  }
}

/** `null` means "no range": every loaded bar. */
export function sliceByRange(data: PriceData[], id: PriceRangeId | null): PriceData[] {
  if (data.length === 0 || id === null) return data;
  const start = rangeStart(id, data[data.length - 1].Date);
  return data.filter((bar) => bar.Date.slice(0, 10) >= start);
}

/** Ranges the loaded data actually covers (none when the data is shorter than a month). */
export function availableRanges(data: PriceData[]): PriceRangeId[] {
  if (data.length === 0) return [];
  const first = parseDay(data[0].Date);
  const lastDate = data[data.length - 1].Date;
  return PRICE_RANGE_IDS.filter((id) => {
    const start = rangeStart(id, lastDate);
    if (id === "YTD") return true;
    return first <= parseDay(start) + COVERAGE_TOLERANCE_DAYS * MS_PER_DAY;
  });
}

const closeOf = (bar: PriceData): number => bar["Adj Close"] ?? bar.Close;
const round2 = (value: number): number => Math.round(value * 100) / 100;

/** Same shape as the backend's price stats, computed for a slice of bars. */
export function statsForRange(data: PriceData[]): PriceStats | null {
  if (data.length === 0) return null;
  const first = data[0];
  const last = data[data.length - 1];
  const startPrice = closeOf(first);
  const endPrice = closeOf(last);
  return {
    growth_rate: round2(((endPrice - startPrice) / startPrice) * 100),
    duration_days: Math.round((parseDay(last.Date) - parseDay(first.Date)) / MS_PER_DAY),
    start_date: first.Date.slice(0, 10),
    end_date: last.Date.slice(0, 10),
    start_price: round2(startPrice),
    end_price: round2(endPrice),
  };
}
