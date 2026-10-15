"use client";

import { useEffect, useRef } from "react";

/**
 * Living trading backdrop for the portal hero.
 *
 * Renders three layers onto one canvas:
 *   1. A drifting constellation of "agent" nodes linked by faint lines when near —
 *      a nod to the 12-agent network behind every analysis.
 *   2. A couple of flowing price-line waves scrolling leftward, like a quiet ticker.
 *   3. A soft pointer-reactive parallax so the whole field leans toward the cursor.
 *
 * Colours are pulled straight from the existing brand palette (blue / sky /
 * cyan / teal / emerald) so it reads as the same product, just alive. Honors
 * prefers-reduced-motion and pauses while the tab is hidden.
 */

type Node = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  r: number;
  color: string;
};

// Brand palette (matches globals.css gradient tokens).
const NODE_COLORS = [
  "59, 130, 246", // blue-500
  "56, 189, 248", // sky-400
  "6, 182, 212", // cyan-500
  "45, 212, 191", // teal-400
  "52, 211, 153", // emerald-400
];

export function HeroTradingCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let width = 0;
    let height = 0;
    let dpr = 1;
    let nodes: Node[] = [];
    let raf = 0;
    let t = 0;

    // Pointer parallax target (eased toward each frame).
    const pointer = { x: 0.5, y: 0.5 };
    const eased = { x: 0.5, y: 0.5 };

    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = canvas.clientWidth;
      height = canvas.clientHeight;
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // Density scales with area, capped so big screens stay smooth.
      const count = Math.min(72, Math.floor((width * height) / 16000));
      nodes = Array.from({ length: count }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.25,
        vy: (Math.random() - 0.5) * 0.25,
        r: 1 + Math.random() * 2,
        color: NODE_COLORS[Math.floor(Math.random() * NODE_COLORS.length)],
      }));
    };

    // One flowing price wave; phase/colour differ per layer.
    const drawWave = (phase: number, amp: number, yBase: number, rgb: string, alpha: number) => {
      ctx.beginPath();
      const step = 14;
      for (let x = -step; x <= width + step; x += step) {
        const y =
          yBase +
          Math.sin(x * 0.006 + phase) * amp +
          Math.sin(x * 0.013 + phase * 1.7) * amp * 0.4;
        if (x === -step) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      const grad = ctx.createLinearGradient(0, 0, width, 0);
      grad.addColorStop(0, `rgba(${rgb}, 0)`);
      grad.addColorStop(0.5, `rgba(${rgb}, ${alpha})`);
      grad.addColorStop(1, `rgba(${rgb}, 0)`);
      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    };

    const frame = () => {
      t += 1;
      ctx.clearRect(0, 0, width, height);

      // Ease pointer for a soft, weighty parallax.
      eased.x += (pointer.x - eased.x) * 0.05;
      eased.y += (pointer.y - eased.y) * 0.05;
      const px = (eased.x - 0.5) * 36;
      const py = (eased.y - 0.5) * 36;

      // ── Flowing price waves (back layer) ──
      drawWave(t * 0.012 + py * 0.01, height * 0.05, height * 0.62 + py * 0.4, "56, 189, 248", 0.28);
      drawWave(t * 0.009 + 2, height * 0.07, height * 0.74 + py * 0.6, "45, 212, 191", 0.22);
      drawWave(t * 0.015 + 4, height * 0.04, height * 0.5 + py * 0.3, "6, 182, 212", 0.16);

      // ── Agent constellation ──
      ctx.save();
      ctx.translate(px, py);

      // Links between nearby nodes.
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i];
          const b = nodes[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const dist = Math.hypot(dx, dy);
          if (dist < 130) {
            const o = (1 - dist / 130) * 0.18;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.strokeStyle = `rgba(99, 153, 241, ${o})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }

      // Nodes with a soft glow + gentle twinkle.
      for (const n of nodes) {
        n.x += n.vx;
        n.y += n.vy;
        if (n.x < -20) n.x = width + 20;
        if (n.x > width + 20) n.x = -20;
        if (n.y < -20) n.y = height + 20;
        if (n.y > height + 20) n.y = -20;

        const twinkle = 0.55 + Math.sin(t * 0.04 + n.x) * 0.25;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${n.color}, ${twinkle})`;
        ctx.shadowColor = `rgba(${n.color}, 0.8)`;
        ctx.shadowBlur = 10;
        ctx.fill();
        ctx.shadowBlur = 0;
      }
      ctx.restore();

      raf = requestAnimationFrame(frame);
    };

    const onPointer = (e: PointerEvent) => {
      pointer.x = e.clientX / window.innerWidth;
      pointer.y = e.clientY / window.innerHeight;
    };

    const onVisibility = () => {
      if (document.hidden) {
        cancelAnimationFrame(raf);
        raf = 0;
      } else if (!raf) {
        raf = requestAnimationFrame(frame);
      }
    };

    resize();
    raf = requestAnimationFrame(frame);
    window.addEventListener("resize", resize);
    window.addEventListener("pointermove", onPointer, { passive: true });
    document.addEventListener("visibilitychange", onVisibility);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
      window.removeEventListener("pointermove", onPointer);
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, []);

  return <canvas ref={canvasRef} className="portal-canvas" aria-hidden />;
}
