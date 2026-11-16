"use client";

import { useEffect } from "react";

/**
 * Custom pointer: a single crisp dot that tracks the cursor exactly. Over
 * interactive elements (links, buttons, inputs, cards) it tints brand cyan.
 *
 * Activates only on devices with a fine, hovering pointer and when motion is
 * allowed — otherwise the native cursor is left untouched (touch screens,
 * prefers-reduced-motion). Driven by rAF + direct style writes, so it never
 * triggers a React re-render.
 */

const INTERACTIVE = "a, button, [role='button'], input, textarea, select, label, summary, .interactive-card, .cursor-pointer";

export function CustomCursor() {
  useEffect(() => {
    const fine = window.matchMedia("(pointer: fine)").matches;
    const canHover = window.matchMedia("(hover: hover)").matches;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!fine || !canHover || reduced) return;

    const dot = document.createElement("div");
    dot.className = "cursor-dot";
    document.body.append(dot);
    document.documentElement.classList.add("has-custom-cursor");

    let tx = window.innerWidth / 2;
    let ty = window.innerHeight / 2;
    let raf = 0;
    let visible = false;

    const render = () => {
      dot.style.transform = `translate3d(${tx}px, ${ty}px, 0) translate(-50%, -50%)`;
      raf = requestAnimationFrame(render);
    };

    const onMove = (e: PointerEvent) => {
      tx = e.clientX;
      ty = e.clientY;
      if (!visible) {
        visible = true;
        document.documentElement.classList.add("cursor-active");
      }
    };

    const onOver = (e: PointerEvent) => {
      const target = e.target as Element | null;
      const hot = !!target?.closest?.(INTERACTIVE);
      dot.classList.toggle("is-hover", hot);
    };

    const onLeave = () => document.documentElement.classList.remove("cursor-active");
    const onEnter = () => document.documentElement.classList.add("cursor-active");

    raf = requestAnimationFrame(render);
    window.addEventListener("pointermove", onMove, { passive: true });
    window.addEventListener("pointerover", onOver, { passive: true });
    document.addEventListener("pointerleave", onLeave);
    document.addEventListener("pointerenter", onEnter);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerover", onOver);
      document.removeEventListener("pointerleave", onLeave);
      document.removeEventListener("pointerenter", onEnter);
      dot.remove();
      document.documentElement.classList.remove("has-custom-cursor", "cursor-active");
    };
  }, []);

  return null;
}
