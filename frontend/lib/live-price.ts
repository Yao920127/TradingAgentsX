/**
 * Helpers for the results page "Live" price mode.
 *
 * Liveline always draws "now" at the right edge of the chart. Yahoo's last bar
 * can be minutes (or, when the market is closed, days) old, so the series is
 * shifted to end at the moment it arrived, and labels shift it back.
 */
import type { LiveCandle, LiveMarketType, LivePricePoint, LiveQuote } from "./types";

/** One-minute bars. */
export const LIVE_BAR_SECONDS = 60;
export const MIN_LIVE_WINDOW_SECONDS = 5 * 60;

export interface AnchoredQuote {
  /** Seconds added to every Yahoo timestamp. Subtract it to get the real time. */
  offset: number;
  points: LivePricePoint[];
  candles: LiveCandle[];
}

export function anchorQuoteToNow(quote: LiveQuote, receivedAt: number): AnchoredQuote {
  const offset = Math.round(receivedAt) - quote.as_of;
  return {
    offset,
    points: quote.points.map((p) => ({ ...p, time: p.time + offset })),
    candles: quote.candles.map((c) => ({ ...c, time: c.time + offset })),
  };
}

/** Visible time span: the whole session so far, plus one bar of breathing room. */
export function liveWindowSeconds(points: readonly LivePricePoint[]): number {
  if (points.length === 0) return MIN_LIVE_WINDOW_SECONDS;
  const span = points[points.length - 1].time - points[0].time + LIVE_BAR_SECONDS;
  return Math.max(span, MIN_LIVE_WINDOW_SECONDS);
}

export function marketTimeZone(marketType: LiveMarketType | undefined): string {
  return marketType === "twse" || marketType === "tpex" ? "Asia/Taipei" : "America/New_York";
}

/** "HH:mm" in the exchange's own time zone. */
export function formatMarketTime(unixSeconds: number, marketType: LiveMarketType | undefined): string {
  return new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: marketTimeZone(marketType),
  }).format(new Date(unixSeconds * 1000));
}
