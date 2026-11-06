import { describe, expect, test } from "bun:test";
import {
  anchorQuoteToNow,
  liveWindowSeconds,
  marketTimeZone,
  formatMarketTime,
  MIN_LIVE_WINDOW_SECONDS,
} from "./live-price";
import type { LiveQuote } from "./types";

const quote: LiveQuote = {
  symbol: "NVDA",
  currency: "USD",
  price: 104,
  previous_close: 100,
  change: 4,
  change_percent: 4,
  market_open: false,
  as_of: 1_000_120,
  points: [
    { time: 1_000_000, value: 100 },
    { time: 1_000_060, value: 101 },
    { time: 1_000_120, value: 103 },
  ],
  candles: [{ time: 1_000_120, open: 102, high: 104, low: 101, close: 103 }],
  volumes: [{ time: 1_000_120, volume: 5 }],
};

describe("anchorQuoteToNow", () => {
  test("shifts every time so the last bar sits at the receive time", () => {
    const anchored = anchorQuoteToNow(quote, 2_000_000);

    expect(anchored.offset).toBe(2_000_000 - 1_000_120);
    expect(anchored.points.map((p) => p.time)).toEqual([1_999_880, 1_999_940, 2_000_000]);
    expect(anchored.candles[0].time).toBe(2_000_000);
    expect(anchored.points[0].value).toBe(100);
  });

  test("does not mutate the original quote", () => {
    anchorQuoteToNow(quote, 2_000_000);
    expect(quote.points[0].time).toBe(1_000_000);
  });
});

describe("liveWindowSeconds", () => {
  test("covers the whole session plus one bar", () => {
    expect(liveWindowSeconds(quote.points)).toBe(MIN_LIVE_WINDOW_SECONDS);
    const day = [{ time: 0, value: 1 }, { time: 6 * 3600, value: 2 }];
    expect(liveWindowSeconds(day)).toBe(6 * 3600 + 60);
  });

  test("falls back to the minimum window when there is no data", () => {
    expect(liveWindowSeconds([])).toBe(MIN_LIVE_WINDOW_SECONDS);
  });
});

describe("market time", () => {
  test("uses the exchange time zone for each market", () => {
    expect(marketTimeZone("us")).toBe("America/New_York");
    expect(marketTimeZone("twse")).toBe("Asia/Taipei");
    expect(marketTimeZone("tpex")).toBe("Asia/Taipei");
    expect(marketTimeZone(undefined)).toBe("America/New_York");
  });

  test("formats Unix seconds as HH:mm in the exchange time zone", () => {
    // 2026-11-06 05:24 UTC = 13:24 Taipei
    expect(formatMarketTime(1_793_942_640, "twse")).toBe("13:24");
  });
});
