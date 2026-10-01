# Style: Retro 80s (Synthwave) (S17)

## Overview
- **ID**: S17
- **Name**: Retro 80s (Synthwave)
- **Industries**: Lifestyle, Creative
- **Category**: Futuristic

## Design DNA
- **Palette Strategy**: 80s synthwave theme. Vibrant pinks, purples, and cyans.
- **Typography**: Retro-style fonts (e.g., Press Start 2P, Exo 2).
- **Radius Policy**: Moderate rounded corners (8-16px).
- **Shadow Policy**: Bright neon glows and multi-colored shadows.
- **Border Language**: Glowing borders with gradient effects.
- **Patterns**: Retro grids, scanned lines, laser beams.
- **Motion**: Energetic, pulsing animations.

## Rules
### Do
- Use 80s retro color palettes
- Apply neon glow effects
- Use grid patterns and laser line motifs
- Incorporate retro-futuristic icons

### Don't
- Don't use modern, flat colors exclusively
- Don't use sharp, industrial corners excessively
- Don't use subtle or muted palettes
- Don't use slow, corporate-style transitions

---

## Complete Prompt

# Retro 80s (Synthwave) SaaS Landing Page Prompt (S17)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S17 Retro 80s (Synthwave)** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S17 — Retro 80s (Synthwave)
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

## Style DNA (S17 – Retro 80s (Synthwave))

### Style Seeds
- **Palette strategy:** 80s synthwave theme. Vibrant pinks, purples, and cyans.
- **Typography:** Retro-style fonts (e.g., Press Start 2P, Exo 2).
- **Radius policy:** Moderate rounded corners (8-16px).
- **Shadow policy:** Bright neon glows and multi-colored shadows.
- **Border language:** Glowing borders with gradient effects.
- **Patterns/textures:** Retro grids, scanned lines, laser beams.
- **Motion:** Energetic, pulsing animations.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S17"
    style_name: "Retro 80s (Synthwave)"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#1A0B2E"
      secondary: "#2D1B4D"
    text:
      primary: "#FF00FF"
      secondary: "#00FFFF"
      muted: "#8B5CF6"
    brand:
      primary: "#FF00FF"
      secondary: "#00FFFF"
      accent: "#FFFF00"
    border:
      strong: "#FF00FF"
      subtle: "rgba(255, 0, 255, 0.3)"
    focus:
      ring: "#FF00FF"
  radius:
    none: 0
    sm: 8
    md: 16
    lg: 24
  border:
    width: { hairline: 1, medium: 2, strong: 4 }
  shadow:
    neon_pink: "0 0 15px rgba(255, 0, 255, 0.7)"
    neon_cyan: "0 0 15px rgba(0, 255, 255, 0.7)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 200, normal: 400, pulse: 2000 }
    easing: "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
  typography:
    font:
      sans: { primary: "Exo 2", fallback: ["system-ui", "sans-serif"] }
      mono: { primary: "Press Start 2P", fallback: ["monospace"] }
    scale:
      h1: { size: 60, line: 68, weight: 800, tracking: 0.1 }
      h2: { size: 40, line: 48, weight: 800, tracking: 0.05 }
      body: { size: 18, line: 28, weight: 400, tracking: 0.02 }
  spacing:
    base: 10
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
