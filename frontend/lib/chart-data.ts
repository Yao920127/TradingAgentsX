/**
 * Pure data conversion for the lightweight-charts price/volume chart.
 * Kept free of DOM and React so it can be unit-tested.
 */
import type { Time, UTCTimestamp } from "lightweight-charts";
import type { PriceData } from "./types";

export interface LinePoint {
  time: Time;
  value: number;
}

export interface CandlePoint {
  time: Time;
  open: number;
  high: number;
  low: number;
  close: number;
}

export interface VolumePoint {
  time: Time;
  value: number;
  /** Close at or above the previous close. */
  up: boolean;
  /** Pre/post-market bar: drawn more faintly. */
  muted?: boolean;
}

export interface ChartSeriesData {
  line: LinePoint[];
  candles: CandlePoint[];
  volume: VolumePoint[];
}

/**
 * Daily bars ("YYYY-MM-DD") stay business-day strings. Intraday bars
 * ("YYYY-MM-DDTHH:mm", exchange-local time) become UTC seconds with the clock
 * time untouched, so the axis shows exchange time whatever the browser zone is.
 */
export function toChartTime(date: string): Time {
  if (!date.includes("T")) return date;
  const [day, clock] = date.split("T");
  const [year, month, dayOfMonth] = day.split("-").map(Number);
  const [hour, minute] = clock.split(":").map(Number);
  return (Date.UTC(year, month - 1, dayOfMonth, hour, minute) / 1000) as UTCTimestamp;
}

/** Heikin Ashi candles derived from regular OHLC bars. */
export function calculateHeikinAshi(data: PriceData[]): CandlePoint[] {
  const result: CandlePoint[] = [];
  data.forEach((bar, index) => {
    const close = (bar.Open + bar.High + bar.Low + (bar["Adj Close"] ?? bar.Close)) / 4;
    const previous = result[index - 1];
    const open = previous ? (previous.open + previous.close) / 2 : bar.Open;
    result.push({
      time: toChartTime(bar.Date),
      open,
      close,
      high: Math.max(bar.High, open, close),
      low: Math.min(bar.Low, open, close),
    });
  });
  return result;
}

const timeKey = (time: Time): number | string =>
  typeof time === "object" ? `${time.year}-${time.month}-${time.day}` : time;

/** Ascending by time, one point per time (the last one wins). */
function sortedUnique<T extends { time: Time }>(points: T[]): T[] {
  const byTime = new Map<number | string, T>();
  [...points]
    .sort((a, b) => (timeKey(a.time) < timeKey(b.time) ? -1 : timeKey(a.time) > timeKey(b.time) ? 1 : 0))
    .forEach((point) => byTime.set(timeKey(point.time), point));
  return [...byTime.values()];
}

export function buildHistorySeries(priceData: PriceData[]): ChartSeriesData {
  const bars = sortedUnique(priceData.map((bar) => ({ ...bar, time: toChartTime(bar.Date) })));
  const closeOf = (bar: PriceData) => bar["Adj Close"] ?? bar.Close;

  return {
    line: bars.map((bar) => ({ time: bar.time, value: closeOf(bar) })),
    candles: calculateHeikinAshi(bars),
    volume: bars.map((bar, index) => {
      const reference = index === 0 ? bar.Open : closeOf(bars[index - 1]);
      return { time: bar.time, value: bar.Volume, up: closeOf(bar) >= reference };
    }),
  };
}
