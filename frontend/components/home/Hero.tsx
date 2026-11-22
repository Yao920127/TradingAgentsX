"use client";

import Link from "next/link";
import { useLanguage } from "@/contexts/LanguageContext";
import { Button } from "@/components/ui/button";
import { HeroTradingCanvas } from "@/components/home/HeroTradingCanvas";

/**
 * Home hero — one monumental display headline on the white canvas, a pill CTA
 * with an underlined companion link, then a deep-green "agent console" media
 * card (rounded 22px) carrying the living agent constellation.
 */
export function Hero() {
  const { t } = useLanguage();

  return (
    <section className="container mx-auto px-4 pt-16 pb-12 md:pt-24">
      <div className="mx-auto max-w-5xl text-center">
        <p className="type-mono-label mb-6 text-muted-foreground">{t.home.subtitle}</p>
        <h1 className="font-display text-5xl leading-none tracking-[-0.02em] text-foreground sm:text-7xl md:text-hero">
          {t.home.title}
        </h1>
        <p className="mx-auto mt-8 max-w-2xl text-base text-muted-foreground sm:text-lg">
          {t.home.description}
        </p>
        <div className="mt-10 flex flex-col items-center justify-center gap-5 sm:flex-row sm:gap-8">
          <Button asChild size="lg">
            <Link href="/analysis">{t.home.startAnalysis} →</Link>
          </Button>
          <Link
            href="/history"
            className="text-sm text-foreground underline underline-offset-4 hover:text-action-blue"
          >
            {t.home.viewHistory}
          </Link>
          <Link
            href="/demo"
            className="text-sm text-foreground underline underline-offset-4 hover:text-action-blue"
          >
            {t.demo.viewDemo}
          </Link>
        </div>
      </div>

      <div
        className="relative mt-16 h-[320px] overflow-hidden rounded-lg bg-deep-green sm:h-[420px] md:mt-20"
        role="img"
        aria-label="Agent network"
      >
        <HeroTradingCanvas />
      </div>
    </section>
  );
}
