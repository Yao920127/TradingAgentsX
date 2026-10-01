# Style: Luxury Editorial (S19)

## Overview
- **ID**: S19
- **Name**: Luxury Editorial
- **Industries**: Luxury, Commerce
- **Category**: Luxury

## Design DNA
- **Palette Strategy**: Elegant, fashion editorial theme. Creams, subtle golds, and stark black.
- **Typography**: Refined serif (e.g., Bodoni, Playfair Display) with high stroke contrast.
- **Radius Policy**: Zero radius (0px). Architectural luxury.
- **Shadow Policy**: Very subtle or none. Emphasis on layout and whitespace.
- **Border Language**: Hairline borders (0.5-1px).
- **Patterns**: High-end editorial grids.
- **Motion**: Slow, graceful transitions.

## Rules
### Do
- Use high-contrast serif typography
- Maximize whitespace
- Use refined, muted colors
- Maintain architectural precision

### Don't
- Don't use rounded corners
- Don't use casual sans-serifs exclusively
- Don't use bright, non-luxury colors
- Don't use fast or bouncy animations

---

## Complete Prompt

# Luxury Editorial SaaS Landing Page Prompt (S19)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S19 Luxury Editorial** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S19 — Luxury Editorial
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

## Style DNA (S19 – Luxury Editorial)

### Style Seeds
- **Palette strategy:** Elegant, fashion editorial theme. Creams, subtle golds, and stark black.
- **Typography:** Refined serif (e.g., Bodoni, Playfair Display) with high stroke contrast.
- **Radius policy:** Zero radius (0px). Architectural luxury.
- **Shadow policy:** Very subtle or none. Emphasis on layout and whitespace.
- **Border language:** Hairline borders (0.5-1px).
- **Patterns/textures:** High-end editorial grids.
- **Motion:** Slow, graceful transitions.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S19"
    style_name: "Luxury Editorial"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FDFCF0"
      secondary: "#F9F9F9"
    text:
      primary: "#111111"
      secondary: "#333333"
      muted: "#999999"
    brand:
      primary: "#000000"
      accent: "#D4AF37"
    border:
      strong: "#000000"
      subtle: "rgba(0,0,0,0.1)"
    focus:
      ring: "#D4AF37"
  radius:
    none: 0
    sm: 0
    md: 0
  border:
    width: { hairline: 0.5, medium: 1, strong: 2 }
  shadow:
    none: none
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 400, normal: 800 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      serif: { primary: "Bodoni MT", fallback: ["Playfair Display", "serif"] }
      sans: { primary: "Inter", fallback: ["sans-serif"] }
    scale:
      h1: { size: 60, line: 68, weight: 400, tracking: 0.05 }
      h2: { size: 44, line: 52, weight: 400, tracking: 0.02 }
      body: { size: 18, line: 28, weight: 400, tracking: 0.02 }
  spacing:
    base: 12
    section_py: { mobile: [100, 120], desktop: [180, 240] }
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
