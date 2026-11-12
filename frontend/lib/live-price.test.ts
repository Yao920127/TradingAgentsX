import { describe, expect, test } from "bun:test";
import {
  anchorQuoteToNow,
  liveWindowSeconds,
  marketTimeZone,
  formatMarketTime,
  hasExtendedHours,
  sessionAt,
  MIN_LIVE_WINDOW_SECONDS,
} from "./live-price";
import type { LiveQuote, LiveSessionRange } from "./types";

const quote: LiveQuote = {
  symbol: "NVDA",
  currency: "USD",
  price: 104,
  previous_close: 100,
  change: 4,
  change_percent: 4,
  market_open: false,
  session: "closed",
  price_session: "regular",
  sessions: [{ session: "regular", start: 1_000_000, end: 1_000_120 }],
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

describe("sessions", () => {
  const ranges: LiveSessionRange[] = [
    { session: "pre", start: 100, end: 160 },
    { session: "regular", start: 220, end: 400 },
    { session: "post", start: 460, end: 520 },
  ];

  test("finds the session a bar time belongs to", () => {
    expect(sessionAt(ranges, 100)).toBe("pre");
    expect(sessionAt(ranges, 400)).toBe("regular");
    expect(sessionAt(ranges, 520)).toBe("post");
  });

  test("treats times outside every range as regular", () => {
    expect(sessionAt(ranges, 9_999)).toBe("regular");
    expect(sessionAt([], 100)).toBe("regular");
  });

  test("detects whether pre or post market bars are present", () => {
    expect(hasExtendedHours(ranges)).toBe(true);
    expect(hasExtendedHours([ranges[1]])).toBe(false);
    expect(hasExtendedHours([])).toBe(false);
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
