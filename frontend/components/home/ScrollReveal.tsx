"use client";

import { useLayoutEffect, useRef } from "react";

/**
 * Calm scroll reveal: a section fades in and rises a few pixels once, when it
 * enters the viewport. Opacity + transform only; no-op under reduced motion.
 * `from` is kept for call-site compatibility and is intentionally ignored —
 * the design system avoids directional / 3D section motion.
 */
export function ScrollReveal({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
  from?: "left" | "right" | "center";
}) {
  const ref = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    el.classList.add("reveal-init");
    const io = new IntersectionObserver(
      (entries, obs) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            el.classList.add("is-in");
            obs.unobserve(entry.target);
          }
        }
      },
      { threshold: 0.08, rootMargin: "0px 0px -6% 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <div ref={ref} className={`scroll-reveal ${className}`}>
      {children}
    </div>
  );
}
