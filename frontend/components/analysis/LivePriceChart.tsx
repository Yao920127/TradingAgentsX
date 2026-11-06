"use client";

/**
 * "Live" mode of the price section: current price, today's 1-minute price
 * line / candles (Liveline) and per-minute volume, refreshed automatically.
 */
import { useMemo } from "react";
import { useTheme } from "next-themes";
import { Liveline } from "liveline";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useLanguage } from "@/contexts/LanguageContext";
import { useLivePrice } from "@/hooks/useLivePrice";
import {
  LIVE_BAR_SECONDS,
  anchorQuoteToNow,
  formatMarketTime,
  liveWindowSeconds,
} from "@/lib/live-price";
import type { LiveMarketType, LiveQuote } from "@/lib/types";

const LIVE_LINE_COLOR = "#3b82f6";
const VOLUME_BAR_COLOR = "#93c5fd";

interface LivePriceChartProps {
  ticker: string;
  marketType?: LiveMarketType;
  chartType: "line" | "candlestick";
}

type PriceSectionLabels = ReturnType<typeof useLanguage>["t"]["results"]["priceSection"];

function formatCompactVolume(value: number): string {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
  return value.toString();
}

export function LivePriceChart({ ticker, marketType, chartType }: LivePriceChartProps) {
  const { t, locale } = useLanguage();
  const { resolvedTheme } = useTheme();
  const { quote, receivedAt, hasError } = useLivePrice(ticker, marketType, true);
  const labels = t.results.priceSection;
  const numberLocale = locale === "en" ? "en-US" : "zh-TW";

  const formatPrice = (value: number) =>
    value.toLocaleString(numberLocale, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  const anchored = useMemo(
    () => (quote && receivedAt ? anchorQuoteToNow(quote, receivedAt) : null),
    [quote, receivedAt],
  );
  const offset = anchored?.offset ?? 0;
  const volumeData = useMemo(
    () => (quote?.volumes ?? []).map((v) => ({ ...v, label: formatMarketTime(v.time, marketType) })),
    [quote, marketType],
  );

  return (
    <div className="space-y-6">
      {quote ? (
        <LiveStats quote={quote} labels={labels} marketType={marketType} formatPrice={formatPrice} />
      ) : (
        <p className="text-sm text-muted-foreground">{hasError ? labels.liveError : labels.liveLoading}</p>
      )}
      {quote && hasError && <p className="text-sm text-amber-600">{labels.liveError}</p>}

      <div>
        <h3 className="text-lg font-semibold mb-4">{labels.title}</h3>
        <div className="h-[400px] w-full">
          <Liveline
            data={anchored?.points ?? []}
            value={quote?.price ?? 0}
            mode={chartType === "candlestick" ? "candle" : "line"}
            candles={anchored?.candles}
            candleWidth={LIVE_BAR_SECONDS}
            window={liveWindowSeconds(anchored?.points ?? [])}
            theme={resolvedTheme === "dark" ? "dark" : "light"}
            color={LIVE_LINE_COLOR}
            loading={!quote}
            emptyText={hasError ? labels.liveError : labels.liveLoading}
            referenceLine={
              quote?.previous_close != null
                ? { value: quote.previous_close, label: labels.previousClose }
                : undefined
            }
            formatValue={formatPrice}
            formatTime={(time) => formatMarketTime(time - offset, marketType)}
            grid
            fill
            badge
          />
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">{labels.liveVolume}</h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={volumeData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" minTickGap={30} />
            <YAxis tickFormatter={formatCompactVolume} />
            <Tooltip
              formatter={(value: number | undefined) => [value?.toLocaleString() ?? "-", labels.liveVolume]}
            />
            <Bar dataKey="volume" fill={VOLUME_BAR_COLOR} isAnimationActive={false} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <p className="text-xs text-muted-foreground">{labels.liveDelayNote}</p>
    </div>
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
  const changeColor = isUp ? "text-green-600" : "text-red-600";
  const sign = isUp ? "+" : "";
  const changeText =
    quote.change != null && quote.change_percent != null
      ? `${sign}${formatPrice(quote.change)} (${sign}${quote.change_percent.toFixed(2)}%)`
      : "-";
  const currency = quote.currency ? ` ${quote.currency}` : "";

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard label={labels.livePrice}>
        <p className={`text-2xl font-bold ${changeColor}`}>
          {formatPrice(quote.price)}
          <span className="text-sm font-normal text-muted-foreground">{currency}</span>
        </p>
      </StatCard>
      <StatCard label={labels.change}>
        <p className={`text-lg font-semibold ${changeColor}`}>{changeText}</p>
      </StatCard>
      <StatCard label={labels.previousClose}>
        <p className="text-lg font-semibold">
          {quote.previous_close != null ? formatPrice(quote.previous_close) : "-"}
        </p>
      </StatCard>
      <StatCard label={labels.status}>
        <p className="text-sm font-semibold flex items-center gap-2">
          <span
            aria-hidden
            className={`inline-block h-2 w-2 rounded-full ${quote.market_open ? "bg-green-500 animate-pulse" : "bg-gray-400"}`}
          />
          {quote.market_open ? labels.marketOpen : labels.marketClosed}
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
