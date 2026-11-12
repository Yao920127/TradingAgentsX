import { describe, expect, test } from "bun:test";
import { LIVE_POLL_CLOSED_MS, LIVE_POLL_OPEN_MS, nextPollDelay } from "./useLivePrice";
import type { LiveQuote } from "@/lib/types";

const base = {
  symbol: "NVDA", currency: "USD", price: 1, previous_close: 1, change: 0,
  change_percent: 0, as_of: 0, points: [], candles: [], volumes: [],
  session: "regular", price_session: "regular", sessions: [],
} satisfies Omit<LiveQuote, "market_open">;

describe("nextPollDelay", () => {
  test("polls quickly while the market is open", () => {
    expect(nextPollDelay({ ...base, market_open: true }, false)).toBe(LIVE_POLL_OPEN_MS);
  });

  test("slows down when the market is closed", () => {
    expect(nextPollDelay({ ...base, market_open: false }, false)).toBe(LIVE_POLL_CLOSED_MS);
  });

  test("backs off after a failed refresh or before the first quote", () => {
    expect(nextPollDelay({ ...base, market_open: true }, true)).toBe(LIVE_POLL_CLOSED_MS);
    expect(nextPollDelay(null, false)).toBe(LIVE_POLL_CLOSED_MS);
  });
});
