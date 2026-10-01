# Style: Luxury Gold (S22)

## Overview
- **ID**: S22
- **Name**: Luxury Gold
- **Industries**: Luxury, Professional
- **Category**: Luxury

## Design DNA
- **Palette Strategy**: Deep obsidian black and 24K gold. High luxury, heavy contrast.
- **Typography**: Ultra-refined serif (Didot/Bodoni) with high stroke contrast.
- **Radius Policy**: Strict sharp edges (0px) for architectural luxury.
- **Shadow Policy**: Subtle gold glows or deep velvet-like shadows.
- **Border Language**: Gold hairline borders and accents.
- **Patterns**: Ornate geometric patterns, gold foil textures.
- **Motion**: Ultra-smooth, sophisticated transitions (400-800ms).

## Rules
### Do
- Use absolute black and gold
- Apply high-stroke-contrast serifs
- Maintain strict architectural precision
- Incorporate gold foil motifs

### Don't
- Don't use rounded corners
- Don't use drop shadows
- Don't use casual fonts
- Don't use bright, non-luxury colors

---

## Complete Prompt

# Luxury Gold SaaS Landing Page Prompt (S22)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S22 Luxury Gold** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S22 — Luxury Gold
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

## Style DNA (S22 – Luxury Gold)

### Style Seeds
- **Palette strategy:** Deep obsidian black and 24K gold. High luxury, heavy contrast.
- **Typography:** Ultra-refined serif (Didot/Bodoni) with high stroke contrast.
- **Radius policy:** Strict sharp edges (0px) for architectural luxury.
- **Shadow policy:** Subtle gold glows or deep velvet-like shadows.
- **Border language:** Gold hairline borders and accents.
- **Patterns/textures:** Ornate geometric patterns, gold foil textures.
- **Motion:** Ultra-smooth, sophisticated transitions (400-800ms).

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S22"
    style_name: "Luxury Gold"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#000000"
      secondary: "#0A0A0A"
    text:
      primary: "#D4AF37"
      secondary: "#B89B72"
      muted: "#4A4A4A"
    brand:
      primary: "#D4AF37"
      accent: "#FCD34D"
    border:
      strong: "#D4AF37"
      subtle: "#1A1A1A"
    focus:
      ring: "#D4AF37"
  radius:
    none: 0
  border:
    width: { hairline: 0.5, medium: 1, strong: 2 }
  shadow:
    none: none
    gold_glow: "0 0 20px rgba(212, 175, 55, 0.3)"
    velvet: "0 10px 40px rgba(0,0,0,0.9)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 400, normal: 800 }
    easing: "cubic-bezier(0.22, 1, 0.36, 1)"
  typography:
    font:
      serif: { primary: "Bodoni MT", fallback: ["Didot", "serif"] }
      sans: { primary: "Cinzel", fallback: ["sans-serif"] }
    scale:
      h1: { size: 64, line: 72, weight: 400, tracking: 0.1 }
      h2: { size: 48, line: 56, weight: 400, tracking: 0.05 }
      body: { size: 18, line: 28, weight: 400, tracking: 0.05 }
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
