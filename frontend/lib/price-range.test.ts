import { describe, expect, test } from "bun:test";
import { availableRanges, sliceByRange, statsForRange } from "./price-range";
import type { PriceData } from "./types";

const day = (Date: string, Close: number, Volume = 1): PriceData => ({
  Date,
  Open: Close,
  High: Close,
  Low: Close,
  Close,
  Volume,
});

// One bar on the 1st and 15th of every month from 2025-11 to 2026-11.
const bars: PriceData[] = [];
for (let i = 0; i < 25; i++) {
  const month = (10 + Math.floor(i / 2)) % 12;
  const year = 2025 + Math.floor((10 + Math.floor(i / 2)) / 12);
  const dayOfMonth = i % 2 === 0 ? "01" : "15";
  bars.push(day(`${year}-${String(month + 1).padStart(2, "0")}-${dayOfMonth}`, 100 + i));
}
const last = bars[bars.length - 1].Date;

describe("sliceByRange", () => {
  test("1M keeps bars within one month of the last bar", () => {
    const slice = sliceByRange(bars, "1M");
    expect(slice[0].Date >= "2026-10-01").toBe(true);
    expect(slice.length).toBeLessThan(bars.length);
    expect(slice[slice.length - 1].Date).toBe(last);
  });

  test("YTD starts at the first bar of the last bar's year", () => {
    const slice = sliceByRange(bars, "YTD");
    expect(slice[0].Date.startsWith("2026-01")).toBe(true);
  });

  test("null returns everything", () => {
    expect(sliceByRange(bars, null)).toHaveLength(bars.length);
  });
});

describe("availableRanges", () => {
  test("hides ranges the data does not cover", () => {
    const short = bars.slice(-6); // ~3 months
    const ids = availableRanges(short);
    expect(ids).toContain("1M");
    expect(ids).not.toContain("1Y");
  });

  test("offers 1Y when data spans a year", () => {
    expect(availableRanges(bars)).toContain("1Y");
  });
});

describe("statsForRange", () => {
  test("computes growth from first to last close of the slice", () => {
    const stats = statsForRange([day("2026-01-02", 100), day("2026-01-12", 110)]);
    expect(stats).toEqual({
      growth_rate: 10,
      duration_days: 10,
      start_date: "2026-01-02",
      end_date: "2026-01-12",
      start_price: 100,
      end_price: 110,
    });
  });

  test("prefers Adj Close", () => {
    const stats = statsForRange([{ ...day("2026-01-02", 100), "Adj Close": 50 }, { ...day("2026-01-03", 110), "Adj Close": 55 }]);
    expect(stats?.growth_rate).toBe(10);
  });

  test("returns null for no data", () => {
    expect(statsForRange([])).toBeNull();
  });
});
