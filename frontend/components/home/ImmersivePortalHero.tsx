"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { ChevronDown, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { HeroTradingCanvas } from "@/components/home/HeroTradingCanvas";
import { useLanguage } from "@/contexts/LanguageContext";

/**
 * Immersive scroll hero.
 *
 * The section is tall (see `.portal-section` in globals.css); its inner stage is
 * pinned with `position: sticky`. As the user scrolls we map scroll progress to a
 * single CSS variable `--p` (0 → 1) on the stage; the brand zooms toward the
 * viewer and fades across the whole pinned range, so by the time the section
 * releases, the content below flows straight in on the same background — no
 * floating CTA and no panel seam, keeping the dive continuous.
 */
export function ImmersivePortalHero() {
  const { t } = useLanguage();
  const sectionRef = useRef<HTMLElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const stage = stageRef.current;
    if (!section || !stage) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      stage.style.setProperty("--p", "0");
      return;
    }

    let raf = 0;
    const update = () => {
      raf = 0;
      const rect = section.getBoundingClientRect();
      const travel = section.offsetHeight - window.innerHeight;
      const progress = travel > 0 ? Math.min(Math.max(-rect.top / travel, 0), 1) : 0;
      stage.style.setProperty("--p", progress.toFixed(4));
    };

    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(update);
    };

    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <section ref={sectionRef} className="portal-section">
      <div ref={stageRef} className="portal-stage" style={{ ["--p" as string]: 0 }}>
        <div className="portal-backdrop" aria-hidden />
        <div className="portal-stars" aria-hidden />
        <HeroTradingCanvas />

        {/* Intro — logo, title and primary actions, all diving toward the viewer */}
        <div className="portal-intro">
          <div className="inline-flex items-center gap-2 mb-8 px-4 py-1.5 rounded-full glass text-sm font-semibold text-blue-700 dark:text-blue-200 pointer-events-auto">
            <Sparkles className="w-4 h-4 text-cyan-500" />
            {t.home.subtitle}
          </div>
          <div className="portal-logo-halo">
            <Image
              src="/logo.png"
              alt="TradingAgentsX Logo"
              width={112}
              height={112}
              className="portal-logo-img"
              priority
            />
          </div>
          <h1
            className="text-4xl sm:text-5xl md:text-7xl font-black gradient-text-primary leading-[1.05] mb-5"
            style={{ fontFamily: "Nunito, sans-serif" }}
          >
            {t.home.title}
          </h1>
          <p className="text-sm sm:text-base md:text-lg text-blue-600/80 dark:text-blue-300/80 max-w-xl mx-auto font-medium mb-8 sm:mb-9">
            {t.home.description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pointer-events-auto">
            <Link href="/analysis">
              <Button size="lg" className="text-base px-9 py-3.5 animate-cta-pulse">
                {t.home.startAnalysis} →
              </Button>
            </Link>
            <Link href="/history">
              <Button size="lg" variant="outline" className="text-base px-9 py-3.5">
                {t.home.viewHistory}
              </Button>
            </Link>
          </div>
        </div>

        {/* Scroll cue */}
        <div className="portal-cue flex flex-col items-center gap-1 text-blue-500/70 dark:text-blue-300/70">
          <span className="text-xs font-semibold tracking-wide uppercase">Scroll</span>
          <ChevronDown className="w-5 h-5" />
        </div>
      </div>
    </section>
  );
}
