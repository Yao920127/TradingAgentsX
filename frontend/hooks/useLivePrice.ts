/**
 * Polls the backend for a live quote while `enabled` is true.
 *
 * - Market open: every 10 s. Market closed (or after an error): every 60 s.
 * - Pauses while the tab is hidden and refreshes as soon as it is visible again.
 * - Keeps the last good quote on screen when a refresh fails.
 */
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { LiveMarketType, LiveQuote } from "@/lib/types";

export const LIVE_POLL_OPEN_MS = 10_000;
export const LIVE_POLL_CLOSED_MS = 60_000;

export interface LivePriceState {
  quote: LiveQuote | null;
  /** Browser time (Unix seconds) when `quote` arrived. */
  receivedAt: number | null;
  hasError: boolean;
}

const INITIAL_STATE: LivePriceState = { quote: null, receivedAt: null, hasError: false };

interface KeyedState extends LivePriceState {
  /** Which ticker/market this state belongs to, so a new ticker starts empty. */
  key: string;
}

export function nextPollDelay(quote: LiveQuote | null, failed: boolean): number {
  if (failed || !quote?.market_open) return LIVE_POLL_CLOSED_MS;
  return LIVE_POLL_OPEN_MS;
}

export function useLivePrice(
  ticker: string,
  marketType: LiveMarketType | undefined,
  enabled: boolean,
): LivePriceState {
  const key = `${ticker}|${marketType ?? ""}`;
  const [state, setState] = useState<KeyedState>({ ...INITIAL_STATE, key });

  useEffect(() => {
    if (!enabled || !ticker) return;

    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let lastQuote: LiveQuote | null = null;

    const schedule = (delay: number) => {
      clearTimeout(timer);
      timer = setTimeout(poll, delay);
    };

    async function poll() {
      if (document.hidden) return; // resumed by the visibility listener
      let failed = false;
      try {
        const quote = await api.getLivePrice(ticker, marketType);
        if (cancelled) return;
        lastQuote = quote;
        setState({ quote, receivedAt: Date.now() / 1000, hasError: false, key });
      } catch (error) {
        if (cancelled) return;
        failed = true;
        console.warn("Live price refresh failed:", error);
        setState((prev) =>
          prev.key === key ? { ...prev, hasError: true } : { ...INITIAL_STATE, hasError: true, key },
        );
      }
      schedule(nextPollDelay(lastQuote, failed));
    }

    const onVisibilityChange = () => {
      if (!document.hidden) schedule(0);
    };

    document.addEventListener("visibilitychange", onVisibilityChange);
    schedule(0);

    return () => {
      cancelled = true;
      clearTimeout(timer);
      document.removeEventListener("visibilitychange", onVisibilityChange);
    };
  }, [ticker, marketType, enabled, key]);

  if (state.key !== key) return INITIAL_STATE;
  const { quote, receivedAt, hasError } = state;
  return { quote, receivedAt, hasError };
}
