"use client";

/**
 * "Live" mode of the price section: current price, today's 1-minute price
 * line / candles (Liveline) and per-minute volume, refreshed automatically.
 * Covers pre-market, regular hours and after hours.
 */
import { useCallback, useMemo } from "react";
import { LwcPriceChart } from "@/components/analysis/LwcPriceChart";
import { useLanguage } from "@/contexts/LanguageContext";
import { useLivePrice } from "@/hooks/useLivePrice";
import { aggregateVolume, formatMarketTime, hasExtendedHours, sessionAt } from "@/lib/live-price";
import type { CandlePoint, LinePoint, VolumePoint } from "@/lib/chart-data";
import type {
  LiveBarSession,
  LiveMarketSession,
  LiveMarketType,
  LiveQuote,
  LiveSessionRange,
} from "@/lib/types";

const SESSION_COLORS: Record<LiveBarSession, string> = {
  pre: "var(--chart-3)",
  regular: "var(--chart-2)",
  post: "var(--chart-4)",
};

interface LivePriceChartProps {
  ticker: string;
  marketType?: LiveMarketType;
  chartType: "line" | "candlestick";
}

type PriceSectionLabels = ReturnType<typeof useLanguage>["t"]["results"]["priceSection"];

function sessionNames(labels: PriceSectionLabels): Record<LiveBarSession, string> {
  return { pre: labels.sessionPre, regular: labels.sessionRegular, post: labels.sessionPost };
}

function marketStatusLabel(session: LiveMarketSession, labels: PriceSectionLabels): string {
  if (session === "pre") return labels.preMarketOpen;
  if (session === "post") return labels.postMarketOpen;
  if (session === "regular") return labels.marketOpen;
  return labels.marketClosed;
}

/** Label of the close that the change is measured against. */
function referenceCloseLabel(priceSession: LiveBarSession, labels: PriceSectionLabels): string {
  return priceSession === "post" ? labels.regularClose : labels.previousClose;
}

export function LivePriceChart({ ticker, marketType, chartType }: LivePriceChartProps) {
  const { t, locale } = useLanguage();
  const { quote, hasError } = useLivePrice(ticker, marketType, true);
  const labels = t.results.priceSection;
  const numberLocale = locale === "en" ? "en-US" : "zh-TW";

  const formatPrice = useCallback(
    (value: number) =>
      value.toLocaleString(numberLocale, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
    [numberLocale],
  );

  const sessions = useMemo(() => quote?.sessions ?? [], [quote]);
  const showSessions = hasExtendedHours(sessions);

  const line = useMemo<LinePoint[]>(
    () => (quote?.points ?? []).map((p) => ({ time: p.time as LinePoint["time"], value: p.value })),
    [quote],
  );
  const candles = useMemo<CandlePoint[]>(
    () => (quote?.candles ?? []).map((c) => ({ ...c, time: c.time as CandlePoint["time"] })),
    [quote],
  );
  const { volume, bucketMinutes } = useMemo(() => {
    const { bars, bucketMinutes: minutes } = aggregateVolume(quote?.volumes ?? [], quote?.candles ?? []);
    const points: VolumePoint[] = bars.map((bar) => ({
      time: bar.time as VolumePoint["time"],
      value: bar.volume,
      up: bar.isUp,
      muted: showSessions && sessionAt(sessions, bar.time) !== "regular",
    }));
    return { volume: points, bucketMinutes: minutes };
  }, [quote, sessions, showSessions]);
  const volumeTitle = `${labels.liveVolume}（${labels.liveVolumeInterval.replace("{n}", String(bucketMinutes))}）`;

  const formatTime = useCallback((seconds: number) => formatMarketTime(seconds, marketType), [marketType]);
  const referenceLine = useMemo(
    () =>
      quote?.previous_close != null
        ? { value: quote.previous_close, label: referenceCloseLabel(quote.price_session, labels) }
        : undefined,
    [quote, labels],
  );

  return (
    <div className="space-y-6">
      {quote ? (
        <LiveStats quote={quote} labels={labels} marketType={marketType} formatPrice={formatPrice} />
      ) : (
        <p className="text-sm text-muted-foreground">{hasError ? labels.liveError : labels.liveLoading}</p>
      )}
      {quote && hasError && <p className="text-sm text-foreground">{labels.liveError}</p>}

      <div>
        <div className="mb-4 flex flex-wrap items-center justify-between gap-x-4 gap-y-2">
          <h3 className="text-lg font-semibold">{labels.title}</h3>
          {showSessions && (
            <SessionLegend
              sessions={sessions}
              current={quote?.session ?? "closed"}
              labels={labels}
              marketType={marketType}
            />
          )}
        </div>
        {quote ? (
          <LwcPriceChart
            mode={chartType}
            line={line}
            candles={candles}
            volume={volume}
            volumeLabel={volumeTitle}
            timeFormatter={formatTime}
            referenceLine={referenceLine}
            priceFormatter={formatPrice}
          />
        ) : (
          <div className="flex h-[200px] items-center justify-center text-sm text-muted-foreground">
            {hasError ? labels.liveError : labels.liveLoading}
          </div>
        )}
        {showSessions && (
          <p className="mt-2 text-xs text-muted-foreground">{labels.extendedVolumeNote}</p>
        )}
      </div>

      <p className="text-xs text-muted-foreground">{labels.liveDelayNote}</p>
    </div>
  );
}

interface SessionLegendProps {
  sessions: LiveSessionRange[];
  current: LiveMarketSession;
  labels: PriceSectionLabels;
  marketType?: LiveMarketType;
}

/** Which sessions the chart covers, with their time range in exchange time. */
function SessionLegend({ sessions, current, labels, marketType }: SessionLegendProps) {
  const names = sessionNames(labels);
  return (
    <ul className="flex flex-wrap gap-2 text-xs">
      {sessions.map((range) => {
        const isCurrent = range.session === current;
        return (
          <li
            key={`${range.session}-${range.start}`}
            aria-current={isCurrent ? "true" : undefined}
            className={`flex items-center gap-1.5 rounded-full border px-2.5 py-1 ${ isCurrent ? "border-foreground/40 font-semibold" : "border-border text-muted-foreground"
            }`}
          >
            <span
              aria-hidden
              className="inline-block h-2 w-2 rounded-full"
              style={{ backgroundColor: SESSION_COLORS[range.session] }}
            />
            {names[range.session]}
            <span className="tabular-nums">
              {formatMarketTime(range.start, marketType)}–{formatMarketTime(range.end, marketType)}
            </span>
          </li>
        );
      })}
    </ul>
  );
}

interface LiveStatsProps {
  quote: LiveQuote;
  labels: PriceSectionLabels;
  marketType?: LiveMarketType;
  formatPrice: (value: number) => string;
}

function LiveStats({ quote, labels, marketType, formatPrice }: LiveStatsProps) {
  const isUp = (quote.change ?? 0) >= 0;
  const changeColor = isUp ? "text-deep-green dark:text-pale-green" : "text-destructive";
  const sign = isUp ? "+" : "";
  const changeText =
    quote.change != null && quote.change_percent != null
      ? `${sign}${formatPrice(quote.change)} (${sign}${quote.change_percent.toFixed(2)}%)`
      : "-";
  const currency = quote.currency ? ` ${quote.currency}` : "";
  const priceLabels: Record<LiveBarSession, string> = {
    pre: labels.prePrice,
    regular: labels.livePrice,
    post: labels.postPrice,
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard label={priceLabels[quote.price_session]}>
        <p className={`text-2xl font-bold ${changeColor}`}>
          {formatPrice(quote.price)}
          <span className="text-sm font-normal text-muted-foreground">{currency}</span>
        </p>
      </StatCard>
      <StatCard label={labels.change}>
        <p className={`text-lg font-semibold ${changeColor}`}>{changeText}</p>
      </StatCard>
      <StatCard label={referenceCloseLabel(quote.price_session, labels)}>
        <p className="text-lg font-semibold">
          {quote.previous_close != null ? formatPrice(quote.previous_close) : "-"}
        </p>
      </StatCard>
      <StatCard label={labels.status}>
        <p className="text-sm font-semibold flex items-center gap-2">
          <span
            aria-hidden
            className={`inline-block h-2 w-2 rounded-full ${quote.market_open ? "bg-deep-green dark:bg-pale-green animate-pulse" : "bg-gray-400"}`}
          />
          {marketStatusLabel(quote.session, labels)}
        </p>
        <p className="text-xs text-muted-foreground">
          {labels.updatedAt} {formatMarketTime(quote.as_of, marketType)}
        </p>
      </StatCard>
    </div>
  );
}

function StatCard({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="bg-muted/40 p-4 rounded-lg border border-border">
      <p className="text-sm text-muted-foreground">{label}</p>
      {children}
    </div>
  );
}
