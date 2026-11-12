"use client";

/**
 * "Live" mode of the price section: current price, today's 1-minute price
 * line / candles (Liveline) and per-minute volume, refreshed automatically.
 * Covers pre-market, regular hours and after hours.
 */
import { useMemo } from "react";
import { useTheme } from "next-themes";
import { Liveline } from "liveline";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceArea,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useLanguage } from "@/contexts/LanguageContext";
import { useLivePrice } from "@/hooks/useLivePrice";
import {
  LIVE_BAR_SECONDS,
  anchorQuoteToNow,
  formatMarketTime,
  hasExtendedHours,
  liveWindowSeconds,
  sessionAt,
} from "@/lib/live-price";
import type {
  LiveBarSession,
  LiveMarketSession,
  LiveMarketType,
  LiveQuote,
  LiveSessionRange,
} from "@/lib/types";

const LIVE_LINE_COLOR = "#3b82f6";
const SESSION_COLORS: Record<LiveBarSession, string> = {
  pre: "#f59e0b",
  regular: "#93c5fd",
  post: "#a78bfa",
};
const SESSION_SHADE_OPACITY = 0.12;

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
  const sessions = quote?.sessions ?? [];
  const showSessions = hasExtendedHours(sessions);
  const volumeData = useMemo(
    () =>
      (quote?.volumes ?? []).map((v) => ({
        ...v,
        label: formatMarketTime(v.time, marketType),
        session: sessionAt(quote?.sessions ?? [], v.time),
      })),
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
                ? { value: quote.previous_close, label: referenceCloseLabel(quote.price_session, labels) }
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
            {showSessions &&
              sessions
                .filter((range) => range.session !== "regular")
                .map((range) => (
                  <ReferenceArea
                    key={`${range.session}-${range.start}`}
                    x1={formatMarketTime(range.start, marketType)}
                    x2={formatMarketTime(range.end, marketType)}
                    fill={SESSION_COLORS[range.session]}
                    fillOpacity={SESSION_SHADE_OPACITY}
                    label={{
                      value: sessionNames(labels)[range.session],
                      position: "insideTop",
                      fontSize: 12,
                      fill: "currentColor",
                    }}
                  />
                ))}
            <Bar dataKey="volume" isAnimationActive={false}>
              {volumeData.map((bar) => (
                <Cell key={bar.time} fill={SESSION_COLORS[bar.session]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
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
            className={`flex items-center gap-1.5 rounded-full border px-2.5 py-1 ${
              isCurrent ? "border-foreground/40 font-semibold" : "border-border text-muted-foreground"
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
  const changeColor = isUp ? "text-green-600" : "text-red-600";
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
            className={`inline-block h-2 w-2 rounded-full ${quote.market_open ? "bg-green-500 animate-pulse" : "bg-gray-400"}`}
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
