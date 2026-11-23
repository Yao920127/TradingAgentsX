import { describe, expect, test } from "bun:test";
import {
  buildHistorySeries,
  calculateHeikinAshi,
  toChartTime,
} from "./chart-data";
import type { PriceData } from "./types";

const bar = (Date: string, Open: number, High: number, Low: number, Close: number, Volume = 100): PriceData => ({
  Date,
  Open,
  High,
  Low,
  Close,
  Volume,
});

describe("toChartTime", () => {
  test("keeps daily dates as business-day strings", () => {
    expect(toChartTime("2026-11-13")).toBe("2026-11-13");
  });

  test("turns intraday exchange-local time into UTC seconds without shifting it", () => {
    expect(toChartTime("2026-11-13T09:30")).toBe(Date.UTC(2026, 10, 13, 9, 30) / 1000);
  });
});

describe("calculateHeikinAshi", () => {
  test("first candle opens at the real open, later ones at the previous HA midpoint", () => {
    const [first, second] = calculateHeikinAshi([bar("2026-01-01", 10, 12, 9, 11), bar("2026-01-02", 11, 13, 10, 12)]);
    expect(first.open).toBe(10);
    expect(first.close).toBe((10 + 12 + 9 + 11) / 4);
    expect(second.open).toBe((first.open + first.close) / 2);
    expect(second.high).toBeGreaterThanOrEqual(Math.max(second.open, second.close));
    expect(second.low).toBeLessThanOrEqual(Math.min(second.open, second.close));
  });
});

describe("buildHistorySeries", () => {
  const data = [bar("2026-01-01", 10, 12, 9, 11, 500), bar("2026-01-02", 11, 12, 8, 9, 700)];

  test("line mode uses adjusted close when present", () => {
    const withAdj = [{ ...data[0], "Adj Close": 10.5 }, data[1]];
    const { line } = buildHistorySeries(withAdj);
    expect(line.map((p) => p.value)).toEqual([10.5, 9]);
  });

  test("volume is coloured by close versus previous close (first bar vs its open)", () => {
    const { volume } = buildHistorySeries(data);
    expect(volume.map((v) => v.up)).toEqual([true, false]);
    expect(volume.map((v) => v.value)).toEqual([500, 700]);
  });

  test("sorts ascending and drops duplicate times", () => {
    const { line } = buildHistorySeries([data[1], data[0], data[0]]);
    expect(line.map((p) => p.time)).toEqual(["2026-01-01", "2026-01-02"]);
  });
});
