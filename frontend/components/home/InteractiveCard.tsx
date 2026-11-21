"use client";

import { useLayoutEffect, useRef } from "react";

/**
 * Homepage card wrapper. Reveals on scroll with a short stagger by grid
 * position (opacity + small translate). No tilt, no spotlight — cards stay
 * flat and bordered per the design system. No-op under reduced motion.
 */
export function InteractiveCard({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const siblings = el.parentElement ? Array.from(el.parentElement.children) : [];
    const idx = Math.max(0, siblings.indexOf(el));
    el.style.transitionDelay = `${Math.min(idx, 9) * 60}ms`;

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
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <div ref={ref} className={`interactive-card ${className}`}>
      {children}
    </div>
  );
}
