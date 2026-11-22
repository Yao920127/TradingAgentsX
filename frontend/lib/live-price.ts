/**
 * Helpers for the results page "Live" price mode.
 *
 * Liveline always draws "now" at the right edge of the chart. Yahoo's last bar
 * can be minutes (or, when the market is closed, days) old, so the series is
 * shifted to end at the moment it arrived, and labels shift it back.
 */
import type {
  LiveBarSession,
  LiveCandle,
  LiveMarketType,
  LivePricePoint,
  LiveQuote,
  LiveSessionRange,
  LiveVolumeBar,
} from "./types";

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

/** Which session a bar time falls in; bars outside every range count as regular. */
export function sessionAt(ranges: readonly LiveSessionRange[], time: number): LiveBarSession {
  return ranges.find((r) => time >= r.start && time <= r.end)?.session ?? "regular";
}

/** True when the series includes pre-market or post-market bars. */
export function hasExtendedHours(ranges: readonly LiveSessionRange[]): boolean {
  return ranges.some((r) => r.session !== "regular");
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

/** Candidate bucket sizes (minutes) for aggregating per-minute volume bars. */
const VOLUME_BUCKET_MINUTES = [1, 2, 5, 10, 15, 30, 60];
/** Upper bound of volume bars drawn, so each bar stays wide enough to read. */
export const MAX_VOLUME_BARS = 150;

export interface AggregatedVolumeBar {
  /** Bucket start, epoch seconds. */
  time: number;
  volume: number;
  /** Close of the bucket is at or above the previous bucket's close. */
  isUp: boolean;
}

export interface AggregatedVolume {
  bars: AggregatedVolumeBar[];
  bucketMinutes: number;
}

/**
 * Merge per-minute volume into coarser buckets (smallest of 1/2/5/10/15/30/60 min that
 * keeps the bar count within MAX_VOLUME_BARS), coloured by price direction.
 * Without this, a 16-hour US session (pre + regular + post) renders ~960 hairline bars.
 */
export function aggregateVolume(
  volumes: LiveVolumeBar[],
  candles: LiveCandle[],
  maxBars: number = MAX_VOLUME_BARS,
): AggregatedVolume {
  if (volumes.length === 0) return { bars: [], bucketMinutes: 1 };

  const sortedVolumes = [...volumes].sort((a, b) => a.time - b.time);
  const sortedCandles = [...candles].sort((a, b) => a.time - b.time);
  const spanSeconds = sortedVolumes[sortedVolumes.length - 1].time - sortedVolumes[0].time + LIVE_BAR_SECONDS;
  const rawBars = Math.ceil(spanSeconds / LIVE_BAR_SECONDS);
  const bucketMinutes =
    VOLUME_BUCKET_MINUTES.find((m) => Math.ceil(rawBars / m) <= maxBars) ??
    VOLUME_BUCKET_MINUTES[VOLUME_BUCKET_MINUTES.length - 1];
  const bucketSeconds = bucketMinutes * 60;
  const bucketStart = (time: number) => Math.floor(time / bucketSeconds) * bucketSeconds;

  const volumeByBucket = new Map<number, number>();
  for (const v of sortedVolumes) {
    const key = bucketStart(v.time);
    volumeByBucket.set(key, (volumeByBucket.get(key) ?? 0) + v.volume);
  }

  // first open / last close of every bucket that has candles
  const priceByBucket = new Map<number, { open: number; close: number }>();
  for (const c of sortedCandles) {
    const key = bucketStart(c.time);
    const existing = priceByBucket.get(key);
    priceByBucket.set(key, { open: existing?.open ?? c.open, close: c.close });
  }

  let previousClose: number | null = null;
  const bars = [...volumeByBucket.entries()]
    .sort(([a], [b]) => a - b)
    .map(([time, volume]) => {
      const price = priceByBucket.get(time);
      const reference = previousClose ?? price?.open;
      const isUp = price && reference != null ? price.close >= reference : true;
      if (price) previousClose = price.close;
      return { time, volume, isUp };
    });

  return { bars, bucketMinutes };
}
