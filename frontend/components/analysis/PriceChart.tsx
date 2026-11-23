"use client";

import { useCallback, useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useLanguage } from "@/contexts/LanguageContext";
import type { LiveMarketType, PriceData, PriceStats } from "@/lib/types";
import { LivePriceChart } from "@/components/analysis/LivePriceChart";
import { LwcPriceChart } from "@/components/analysis/LwcPriceChart";
import { buildHistorySeries } from "@/lib/chart-data";
import { availableRanges, sliceByRange, statsForRange, type PriceRangeId } from "@/lib/price-range";

interface PriceChartProps {
  priceData: PriceData[];
  priceStats: PriceStats;
  ticker: string;
  marketType?: LiveMarketType;
}

type PriceMode = "history" | "live";

export function PriceChart({ priceData, priceStats, ticker, marketType }: PriceChartProps) {
  const { t, locale } = useLanguage();
  const [chartType, setChartType] = useState<"line" | "candlestick">("line");
  const [priceMode, setPriceMode] = useState<PriceMode>("history");
  const isLive = priceMode === "live";

  const [range, setRange] = useState<PriceRangeId>("1Y");

  const rangeOptions = useMemo(() => availableRanges(priceData), [priceData]);
  // Fall back to the 1Y/YTD default's longest offered option, or all bars when the data is too short for any range.
  const activeRange = rangeOptions.includes(range) ? range : (rangeOptions[rangeOptions.length - 1] ?? null);
  const rangeData = useMemo(() => sliceByRange(priceData, activeRange), [priceData, activeRange]);
  const series = useMemo(() => buildHistorySeries(rangeData), [rangeData]);
  // Every range is derived from the visible bars so the numbers stay consistent
  // across tabs; intraday new listings keep the backend's own stats.
  const stats = useMemo(
    () => (priceStats.is_new_listing ? priceStats : (statsForRange(rangeData) ?? priceStats)),
    [rangeData, priceStats],
  );

  // 格式化數字
  const formatNumber = useCallback(
    (num: number) =>
      num.toLocaleString(locale === "en" ? "en-US" : "zh-TW", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }),
    [locale],
  );

  // 新上市股票的 price_data 是盤中 K 線，Date 格式為 YYYY-MM-DDTHH:mm（交易所當地時間）
  const isIntraday = Boolean(priceStats.is_new_listing) || priceData.some((d) => d.Date.includes("T"));

  // 盤中 K 線的時間是交易所當地時間（以 UTC 秒存放），固定用 UTC 格式化避免被瀏覽器時區位移
  const formatIntradayTime = useCallback(
    (seconds: number) =>
      new Intl.DateTimeFormat("en-GB", {
        month: "numeric",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
        timeZone: "UTC",
      }).format(new Date(seconds * 1000)),
    [],
  );

  const newListingNotice = priceStats.is_new_listing
    ? t.results.priceSection.newListingNotice
        .replace("{date}", priceStats.listing_date ?? priceStats.start_date)
        .replace("{days}", String(priceStats.daily_bars ?? 1))
        .replace("{interval}", priceStats.interval ?? "")
    : null;

  // Localized labels
  const labels = {
    priceTitle: t.results.priceSection.title,
    dataRange: t.results.priceSection.dataRange,
    growth: t.results.priceSection.growth,
    duration: t.results.priceSection.duration,
    days: t.results.priceSection.days,
    startPrice: t.results.priceSection.startPrice,
    endPrice: t.results.priceSection.endPrice,
    lineChart: t.results.priceSection.lineChart,
    candlestick: t.results.priceSection.candlestick,
    volume: t.results.volumeChart,
  };

  return (
    <Card className="w-full hover-lift animate-scale-up">
      <CardHeader>
        <div className="flex flex-wrap justify-between items-center gap-3">
          <CardTitle className="text-2xl">
            {ticker} {labels.priceTitle}
            {!isLive && !isIntraday && rangeOptions.length > 1 && (locale === "en" ? ` (${t.results.priceSection.ranges[activeRange ?? "1Y"]})` : `（${t.results.priceSection.ranges[activeRange ?? "1Y"]}）`)}
          </CardTitle>
          <div className="flex flex-wrap items-center gap-2">
            <Tabs value={priceMode} onValueChange={(v: string) => setPriceMode(v as PriceMode)}>
              <TabsList>
                <TabsTrigger value="history">{t.results.priceSection.history}</TabsTrigger>
                <TabsTrigger value="live" className="gap-1.5">
                  <span aria-hidden className="inline-block h-1.5 w-1.5 rounded-full bg-destructive" />
                  {t.results.priceSection.live}
                </TabsTrigger>
              </TabsList>
            </Tabs>
            <Tabs value={chartType} onValueChange={(v: string) => setChartType(v as "line" | "candlestick")}>
              <TabsList>
                <TabsTrigger value="line">{labels.lineChart}</TabsTrigger>
                <TabsTrigger value="candlestick">{isLive ? t.results.priceSection.liveCandlestick : labels.candlestick}</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
        </div>

        {!isLive && newListingNotice && (
          <p className="mt-4 rounded-lg border border-coral/50 bg-coral/10 px-4 py-2 text-sm text-foreground ">
            {newListingNotice}
          </p>
        )}

        {!isLive && !isIntraday && rangeOptions.length > 1 && (
          <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2">
            <div className="max-w-full overflow-x-auto">
            <Tabs value={activeRange ?? range} onValueChange={(v: string) => setRange(v as PriceRangeId)}>
              <TabsList>
                {rangeOptions.map((id) => (
                  <TabsTrigger key={id} value={id}>
                    {t.results.priceSection.ranges[id]}
                  </TabsTrigger>
                ))}
              </TabsList>
            </Tabs>
            </div>
            <p className="text-sm text-muted-foreground tabular-nums">
              {labels.dataRange}：{stats.start_date} → {stats.end_date}
            </p>
          </div>
        )}

        {/* 統計資訊（歷史模式；即時模式的統計在 LivePriceChart 內） */}
        {!isLive && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
          <div className="bg-gradient-to-br p-4 rounded-lg border border-deep-green/30 dark:border-pale-green/30 ">
            <p className="text-sm text-muted-foreground">{labels.growth}</p>
            <p className={`text-2xl font-bold ${stats.growth_rate >= 0 ? 'text-deep-green dark:text-pale-green' : 'text-destructive'}`}>
              {stats.growth_rate >= 0 ? '+' : ''}{stats.growth_rate}%
            </p>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
            <p className="text-sm text-muted-foreground">{labels.duration}</p>
            <p className="text-2xl font-bold">{stats.duration_days} {labels.days}</p>
          </div>
          <div className="bg-gradient-to-br from-slate-50 to-gray-100 dark:from-slate-800/40 dark:to-gray-800/40 p-4 rounded-lg border border-slate-200 dark:border-slate-700">
            <p className="text-sm text-muted-foreground">{labels.startPrice}</p>
            <p className="text-lg font-semibold">${formatNumber(stats.start_price)}</p>
            <p className="text-xs text-muted-foreground">{stats.start_date}</p>
          </div>
          <div className="bg-gradient-to-br p-4 rounded-lg border border-coral/50 ">
            <p className="text-sm text-muted-foreground">{labels.endPrice}</p>
            <p className="text-lg font-semibold">${formatNumber(stats.end_price)}</p>
            <p className="text-xs text-muted-foreground">{stats.end_date}</p>
          </div>
        </div>
        )}
      </CardHeader>

      <CardContent className="space-y-6">
        {isLive ? (
          <LivePriceChart ticker={ticker} marketType={marketType} chartType={chartType} />
        ) : (
        <>
        <LwcPriceChart
          mode={chartType}
          line={series.line}
          candles={series.candles}
          volume={series.volume}
          volumeLabel={labels.volume}
          timeFormatter={isIntraday ? formatIntradayTime : undefined}
          priceFormatter={formatNumber}
        />
        </>
        )}
      </CardContent>
    </Card>
  );
}
