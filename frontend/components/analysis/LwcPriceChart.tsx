"use client";

/**
 * TradingView lightweight-charts price + volume chart: price (line or
 * candlesticks) in the top pane, volume histogram in its own pane below, with
 * a crosshair legend. Shared by the history and live views.
 */
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { useTheme } from "next-themes";
import {
  CandlestickSeries,
  ColorType,
  CrosshairMode,
  HistogramSeries,
  LineSeries,
  LineStyle,
  createChart,
  type IChartApi,
  type ISeriesApi,
  type LogicalRange,
  type MouseEventParams,
  type Time,
} from "lightweight-charts";
import type { CandlePoint, LinePoint, VolumePoint } from "@/lib/chart-data";

const UP_COLOR = "#26a69a";
const DOWN_COLOR = "#ef5350";
const MUTED_ALPHA = "66";
const VOLUME_ALPHA = "99";
const MOBILE_QUERY = "(max-width: 639px)";
const LAYOUT = {
  desktop: { height: 520, volumePane: 140, fontSize: 12 },
  mobile: { height: 400, volumePane: 100, fontSize: 10 },
} as const;

/** True below the `sm` breakpoint; false during SSR. */
function useIsMobile(): boolean {
  return useSyncExternalStore(
    (notify) => {
      const query = window.matchMedia(MOBILE_QUERY);
      query.addEventListener("change", notify);
      return () => query.removeEventListener("change", notify);
    },
    () => window.matchMedia(MOBILE_QUERY).matches,
    () => false,
  );
}

/**
 * The chart is a fixed view: no drag-to-pan, wheel/pinch zoom or axis dragging.
 * Touching or hovering only moves the crosshair, so the page keeps scrolling
 * normally on phones and the chart never shifts under the finger.
 */
const FIXED_INTERACTION = {
  handleScroll: { mouseWheel: false, pressedMouseMove: false, horzTouchDrag: false, vertTouchDrag: false },
  handleScale: { mouseWheel: false, pinch: false, axisPressedMouseMove: false, axisDoubleClickReset: false },
  kineticScroll: { mouse: false, touch: false },
} as const;
// Built-in formats on purpose: custom axis formatters make lightweight-charts
// reserve a very wide price axis, which squeezes the plot on phones.
const PRICE_AXIS_FORMAT = { type: "price", precision: 2, minMove: 0.01 } as const;

const PALETTE = {
  light: { text: "#4b5563", grid: "#e5e7eb", line: "#1863dc", border: "#d1d5db" },
  dark: { text: "#9ca3af", grid: "#27272a", line: "#6d9bff", border: "#3f3f46" },
} as const;

export interface ReferenceLine {
  value: number;
  label: string;
}

interface LwcPriceChartProps {
  mode: "line" | "candlestick";
  line: LinePoint[];
  candles: CandlePoint[];
  volume: VolumePoint[];
  volumeLabel: string;
  height?: number;
  /** Axis / crosshair label for UTC-second times. Omit for daily bars. */
  timeFormatter?: (seconds: number) => string;
  referenceLine?: ReferenceLine;
  priceFormatter?: (price: number) => string;
}

interface LegendState {
  time: string;
  open?: number;
  high?: number;
  low?: number;
  close?: number;
  value?: number;
  volume?: number;
  up?: boolean;
}

const formatTime = (time: Time, timeFormatter?: (seconds: number) => string): string => {
  if (typeof time === "number") return timeFormatter ? timeFormatter(time) : String(time);
  if (typeof time === "string") return time;
  return `${time.year}-${String(time.month).padStart(2, "0")}-${String(time.day).padStart(2, "0")}`;
};

const defaultPrice = (price: number) =>
  price.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const compactVolume = (value: number): string => {
  if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(2)}B`;
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(2)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
  return String(value);
};

const toVolumeData = (volume: VolumePoint[]) =>
  volume.map((v) => ({
    time: v.time,
    value: v.value,
    color: (v.up ? UP_COLOR : DOWN_COLOR) + (v.muted ? MUTED_ALPHA : VOLUME_ALPHA),
  }));

function LwcPriceChartInner({
  mode,
  line,
  candles,
  volume,
  volumeLabel,
  height,
  timeFormatter,
  referenceLine,
  priceFormatter = defaultPrice,
}: LwcPriceChartProps) {
  const { resolvedTheme } = useTheme();
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const priceSeriesRef = useRef<ISeriesApi<"Line"> | ISeriesApi<"Candlestick"> | null>(null);
  const volumeSeriesRef = useRef<ISeriesApi<"Histogram"> | null>(null);
  const hasFittedRef = useRef(false);
  const [legend, setLegend] = useState<LegendState | null>(null);
  const isMobile = useIsMobile();
  const layout = LAYOUT[isMobile ? "mobile" : "desktop"];
  const chartHeight = height ?? layout.height;

  // Latest time formatter for the crosshair handler without re-subscribing.
  const timeFormatterRef = useRef(timeFormatter);
  useEffect(() => {
    timeFormatterRef.current = timeFormatter;
  }, [timeFormatter]);

  const palette = PALETTE[resolvedTheme === "dark" ? "dark" : "light"];
  const paletteRef = useRef(palette);
  useEffect(() => {
    paletteRef.current = palette;
  }, [palette]);

  // Create the chart and its series once (the wrapper remounts on mode change).
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const initial = paletteRef.current;

    const chart = createChart(container, {
      autoSize: true,
      ...FIXED_INTERACTION,
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        fontSize: layout.fontSize,
        textColor: initial.text,
        panes: { separatorColor: initial.border },
      },
      grid: { vertLines: { color: initial.grid }, horzLines: { color: initial.grid } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: initial.border },
      timeScale: { borderColor: initial.border, rightOffset: 2, fixLeftEdge: true, fixRightEdge: true, lockVisibleTimeRangeOnResize: true },
    });

    const priceSeries =
      mode === "candlestick"
        ? chart.addSeries(CandlestickSeries, {
            upColor: UP_COLOR,
            downColor: DOWN_COLOR,
            borderUpColor: UP_COLOR,
            borderDownColor: DOWN_COLOR,
            wickUpColor: UP_COLOR,
            wickDownColor: DOWN_COLOR,
            priceFormat: PRICE_AXIS_FORMAT,
          })
        : chart.addSeries(LineSeries, { color: initial.line, lineWidth: 2, priceFormat: PRICE_AXIS_FORMAT });
    const volumeSeries = chart.addSeries(
      HistogramSeries,
      {
        priceFormat: { type: "volume" },
        priceLineVisible: false,
        lastValueVisible: false,
      },
      1,
    );
    chart.panes()[1]?.setHeight(layout.volumePane);

    chartRef.current = chart;
    priceSeriesRef.current = priceSeries;
    volumeSeriesRef.current = volumeSeries;
    hasFittedRef.current = false;

    const onCrosshair = (param: MouseEventParams<Time>) => {
      if (param.time === undefined) {
        setLegend(null);
        return;
      }
      const priceData = param.seriesData.get(priceSeries);
      const volumeData = param.seriesData.get(volumeSeries);
      const time = formatTime(param.time, timeFormatterRef.current);
      const volumeValue = volumeData && "value" in volumeData ? volumeData.value : undefined;
      if (priceData && "open" in priceData) {
        setLegend({
          time,
          open: priceData.open,
          high: priceData.high,
          low: priceData.low,
          close: priceData.close,
          volume: volumeValue,
          up: priceData.close >= priceData.open,
        });
      } else if (priceData && "value" in priceData) {
        setLegend({ time, value: priceData.value, volume: volumeValue });
      } else {
        setLegend(null);
      }
    };
    chart.subscribeCrosshairMove(onCrosshair);

    return () => {
      chart.unsubscribeCrosshairMove(onCrosshair);
      chart.remove();
      chartRef.current = null;
      priceSeriesRef.current = null;
      volumeSeriesRef.current = null;
    };
  }, [mode, layout.fontSize, layout.volumePane]);

  // Theme + formatters.
  useEffect(() => {
    const axisFormatter = timeFormatter
      ? (time: Time) => (typeof time === "number" ? timeFormatter(time) : String(time))
      : undefined;
    chartRef.current?.applyOptions({
      layout: { textColor: palette.text, panes: { separatorColor: palette.border } },
      grid: { vertLines: { color: palette.grid }, horzLines: { color: palette.grid } },
      rightPriceScale: { borderColor: palette.border },
      timeScale: {
        borderColor: palette.border,
        timeVisible: Boolean(timeFormatter),
        tickMarkFormatter: axisFormatter,
      },
      localization: { timeFormatter: axisFormatter },
    });
    if (mode === "line") priceSeriesRef.current?.applyOptions({ color: palette.line });
  }, [palette, timeFormatter, mode]);

  // Data. Keep the user's scroll/zoom when polling replaces the dataset.
  useEffect(() => {
    const chart = chartRef.current;
    const priceSeries = priceSeriesRef.current;
    const volumeSeries = volumeSeriesRef.current;
    if (!chart || !priceSeries || !volumeSeries) return;

    const saved: LogicalRange | null = hasFittedRef.current ? chart.timeScale().getVisibleLogicalRange() : null;
    if (mode === "candlestick") {
      (priceSeries as ISeriesApi<"Candlestick">).setData(candles);
    } else {
      (priceSeries as ISeriesApi<"Line">).setData(line);
    }
    volumeSeries.setData(toVolumeData(volume));

    if (saved) {
      chart.timeScale().setVisibleLogicalRange(saved);
    } else if (line.length > 0 || candles.length > 0) {
      chart.timeScale().fitContent();
      hasFittedRef.current = true;
    }
  }, [mode, line, candles, volume]);

  // Previous-close reference line.
  const referenceValue = referenceLine?.value;
  const referenceLabel = referenceLine?.label;
  useEffect(() => {
    const series = priceSeriesRef.current;
    if (!series || referenceValue === undefined) return;
    const priceLine = series.createPriceLine({
      price: referenceValue,
      color: palette.text,
      lineStyle: LineStyle.Dashed,
      lineWidth: 1,
      axisLabelVisible: true,
      title: referenceLabel ?? "",
    });
    return () => series.removePriceLine(priceLine);
  }, [referenceValue, referenceLabel, palette.text]);

  const lastVolume = volume[volume.length - 1]?.value;
  const tone = legend?.up === undefined ? undefined : legend.up ? UP_COLOR : DOWN_COLOR;

  return (
    <div className="relative w-full" style={{ height: chartHeight }}>
      <div ref={containerRef} className="h-full w-full" />
      <div className="pointer-events-none absolute left-3 top-2 z-10 flex flex-wrap items-center gap-x-3 gap-y-0.5 rounded-md bg-background/80 px-2 py-1 text-xs tabular-nums backdrop-blur-sm">
        {legend ? (
          <>
            <span className="text-muted-foreground">{legend.time}</span>
            {legend.open !== undefined ? (
              <>
                <span style={{ color: tone }}>O {priceFormatter(legend.open)}</span>
                <span style={{ color: tone }}>H {priceFormatter(legend.high ?? legend.open)}</span>
                <span style={{ color: tone }}>L {priceFormatter(legend.low ?? legend.open)}</span>
                <span style={{ color: tone }}>C {priceFormatter(legend.close ?? legend.open)}</span>
              </>
            ) : (
              legend.value !== undefined && (
                <span style={{ color: palette.line }}>{priceFormatter(legend.value)}</span>
              )
            )}
            {legend.volume !== undefined && (
              <span className="text-muted-foreground">
                {volumeLabel} {compactVolume(legend.volume)}
              </span>
            )}
          </>
        ) : (
          lastVolume !== undefined && (
            <span className="text-muted-foreground">
              {volumeLabel} {compactVolume(lastVolume)}
            </span>
          )
        )}
      </div>
    </div>
  );
}

/** Remounts on mode or breakpoint change so series type and sizing are rebuilt cleanly. */
export function LwcPriceChart(props: LwcPriceChartProps) {
  const isMobile = useIsMobile();
  return <LwcPriceChartInner key={`${props.mode}-${isMobile}`} {...props} />;
}
