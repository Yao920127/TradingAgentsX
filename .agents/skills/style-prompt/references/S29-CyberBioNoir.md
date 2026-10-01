# Style: Cyber-Bio Noir (S29)

## Overview
- **ID**: S29
- **Name**: Cyber-Bio Noir
- **Industries**: Tech, Lifestyle
- **Category**: Futuristic

## Design DNA
- **Palette Strategy**: Obsidian black base with intense crimson red neon accents. Carbon-fiber textures.
- **Typography**: Teko for headings (dramatic condensed), Michroma for body (geometric), Share Tech Mono for HUD info.
- **Radius Policy**: Zero rounded corners. Sharp chamfered polygon edges.
- **Shadow Policy**: Intense red neon outer glows. Deep inset shadows on armor plates.
- **Border Language**: Thin red glowing hairlines. Extending edge light-strips on hover.
- **Patterns**: Carbon fiber textures, horizontal CRT scanlines. Red ambient smoke.
- **Motion**: Armor plates lifting on hover, pulsing red core glow, spinning decorative elements.

## Rules
### Do
- Use obsidian black (#050505) backgrounds
- Apply crimson red (#dc2626) for all glowing elements
- Use clip-path polygon cuts on all containers
- Incorporate carbon-fiber texture overlays
- Combine Teko + Michroma + Share Tech Mono fonts

### Don't
- Don't use any blue, cyan, or non-red neons
- Don't use rounded corners or pill shapes
- Don't use flat or bright backgrounds
- Don't use organic or soft textures
- Don't use standard box shadows without glow

---

## Complete Prompt

# Cyber-Bio Noir SaaS Landing Page Prompt (S29)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S29 Cyber-Bio Noir** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S29 — Cyber-Bio Noir
- **Industry:** SaaS
- **Use:** Full Landing Page

## Assumptions
- Product name placeholder: **[Automatic naming]**
- Core value prop placeholder: **[One-line Value Proposition]**
- Primary CTA: **Start free trial**
- Secondary CTA: **Book a demo**
- Target audience: **B2B teams and developers**
- No real metrics, certifications, or customer logos are claimed; all proof uses placeholders
- Target stack: **React + Next.js (App Router) + TypeScript + Tailwind CSS** using **CSS variables** for theming

---

## Style DNA (S29 – Cyber-Bio Noir)

### Style Seeds
- **Palette strategy:** Obsidian black base with intense crimson red neon accents. Carbon-fiber textures.
- **Typography:** Teko for headings (dramatic condensed), Michroma for body (geometric), Share Tech Mono for HUD info.
- **Radius policy:** Zero rounded corners. Sharp chamfered polygon edges.
- **Shadow policy:** Intense red neon outer glows. Deep inset shadows on armor plates.
- **Border language:** Thin red glowing hairlines. Extending edge light-strips on hover.
- **Patterns/textures:** Carbon fiber textures, horizontal CRT scanlines. Red ambient smoke.
- **Motion:** Armor plates lifting on hover, pulsing red core glow, spinning decorative elements.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S29"
    style_name: "Cyber-Bio Noir"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#050505"
      secondary: "#020202"
      elevated: "#0a0a0a"
      smoke: "radial-gradient(circle at center, rgba(220,38,38,0.08) 0%, transparent 60%)"
    text:
      primary: "#FFFFFF"
      secondary: "#a1a1aa"
      muted: "#52525b"
      accent: "#dc2626"
    brand:
      primary: "#dc2626"
      accent: "#ef4444"
    armor:
      base: "#121212"
      surface: "#0a0a0a"
      trim: "#dc2626"
      glow: "rgba(220, 38, 38, 0.6)"
    border:
      strong: "#dc2626"
      subtle: "rgba(220, 38, 38, 0.15)"
    focus:
      ring: "#dc2626"
  radius:
    none: 0
    chamfer_plate: "polygon(0 20px, 20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%)"
  border:
    width: { hairline: 1, medium: 2, armor: 4 }
  shadow:
    neon: "0 0 15px rgba(220, 38, 38, 0.7), 0 0 30px rgba(220, 38, 38, 0.3)"
    deep: "inset 0 0 20px rgba(0,0,0,1), 0 5px 15px rgba(0,0,0,0.5)"
  layout:
    container: { content: 1280, wide: 1536 }
  motion:
    duration: { fast: 300, normal: 400, pulse: 2000 }
    easing: "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
  typography:
    font:
      display: { primary: "Teko", fallback: ["sans-serif"] }
      sans: { primary: "Michroma", fallback: ["sans-serif"] }
      mono: { primary: "Share Tech Mono", fallback: ["monospace"] }
    scale:
      h1: { size: 96, line: 80, weight: 600, tracking: -0.02 }
      h2: { size: 56, line: 56, weight: 600, tracking: 0 }
      h3: { size: 36, line: 44, weight: 400, tracking: 0.02 }
  spacing:
    base: 8
    section_py: { mobile: [80, 100], desktop: [120, 160] }
```

---

## Deliverables
- Full hero section with high-impact product visualization
- Multi-column features grid with icon/illustration slots
- Social proof/customer logo strip (using placeholders)
- Pricing table with monthly/annual toggle
- FAQ accordion system
- Final conversion CTA module
- Responsive footer with site map

---

## Accessibility & Responsive
- WCAG AA contrast
- Visible focus rings
- Reduced motion support
- Touch targets ≥ 44px
- Mobile-first layout

---

## Engineering Notes
- CSS variables for all tokens
- Tailwind config mapping tokens
- Use semantic HTML5 elements
- Implement responsive design with mobile-first approach
- Ensure all interactive elements are keyboard accessible
- Include loading states and error handling

---

## Acceptance Checklist
- Clear hierarchy and visual discipline
- Primary CTA visible above the fold
- No fake metrics or certifications
- Trust modules included
- Fully responsive
- Accessible by keyboard
