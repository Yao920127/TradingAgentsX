/**
 * Stock ticker input with type-ahead suggestions.
 *
 * Shows matching companies (symbol + name) as the user types, sourced from the
 * static client-side dataset in lib/stock-search. Works for US and Taiwan
 * markets and localizes the company name to the current UI language.
 */
"use client";

import { useEffect, useRef, useState } from "react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useLanguage } from "@/contexts/LanguageContext";
import { rankStocks, loadStocks, type MarketType, type StockMatch } from "@/lib/stock-search";

interface TickerComboboxProps {
  value: string;
  onChange: (value: string) => void;
  market: MarketType;
  placeholder?: string;
  emptyText?: string;
}

export function TickerCombobox({
  value,
  onChange,
  market,
  placeholder,
  emptyText,
}: TickerComboboxProps) {
  const { locale } = useLanguage();
  const [open, setOpen] = useState(false);
  const [matches, setMatches] = useState<StockMatch[]>([]);
  const [active, setActive] = useState(0);
  const [loaded, setLoaded] = useState(false);
  const [querying, setQuerying] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Warm the dataset for the current market as soon as the field mounts /
  // the market changes, so the first keystroke is instant.
  useEffect(() => {
    let cancelled = false;
    setLoaded(false);
    loadStocks(market)
      .then(() => {
        if (!cancelled) setLoaded(true);
      })
      .catch(() => {
        if (!cancelled) setLoaded(false);
      });
    return () => {
      cancelled = true;
    };
  }, [market]);

  // Recompute suggestions whenever the query, dataset, market or locale changes.
  useEffect(() => {
    let cancelled = false;
    const q = value.trim();
    if (!q) {
      setMatches([]);
      return;
    }
    setQuerying(true);
    loadStocks(market)
      .then((items) => {
        if (cancelled) return;
        setMatches(rankStocks(items, q, locale, 8));
        setActive(0);
      })
      .catch(() => {
        if (!cancelled) setMatches([]);
      })
      .finally(() => {
        if (!cancelled) setQuerying(false);
      });
    return () => {
      cancelled = true;
    };
  }, [value, market, locale, loaded]);

  // Close the dropdown when clicking outside.
  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, []);

  const select = (m: StockMatch) => {
    onChange(m.symbol);
    setOpen(false);
  };

  const showList = open && value.trim().length > 0;

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!showList) {
      if (e.key === "ArrowDown" && matches.length > 0) {
        setOpen(true);
        e.preventDefault();
      }
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((i) => Math.min(i + 1, matches.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter") {
      if (matches[active]) {
        e.preventDefault();
        select(matches[active]);
      }
    } else if (e.key === "Escape") {
      setOpen(false);
    }
  };

  return (
    <div ref={containerRef} className="relative">
      <Input
        value={value}
        placeholder={placeholder}
        autoComplete="off"
        spellCheck={false}
        onChange={(e) => {
          onChange(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={handleKeyDown}
      />

      {showList && (matches.length > 0 || (!querying && loaded)) && (
        <ul
          role="listbox"
          className="absolute z-50 mt-1 max-h-72 w-full overflow-auto rounded-lg border border-border bg-popover p-1 animate-fade-in"
        >
          {matches.length === 0 ? (
            <li className="px-3 py-2 text-sm text-muted-foreground">
              {emptyText ?? "No matches"}
            </li>
          ) : (
            matches.map((m, i) => (
              <li
                key={`${m.market}-${m.symbol}`}
                role="option"
                aria-selected={i === active}
                onMouseDown={(e) => {
                  // prevent input blur before click handler runs
                  e.preventDefault();
                  select(m);
                }}
                onMouseEnter={() => setActive(i)}
                className={cn(
                  "flex cursor-pointer items-baseline gap-2 rounded-md px-3 py-2 text-sm transition-colors",
                  i === active ? "bg-primary/10 text-primary" : "hover:bg-accent"
                )}
              >
                <span className="font-semibold shrink-0 tabular-nums">
                  {m.symbol}
                </span>
                <span className="truncate text-muted-foreground">{m.name}</span>
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
