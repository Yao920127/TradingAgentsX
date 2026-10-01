# Style: Minimalist Monochrome (S02)

## Overview
- **ID**: S02
- **Name**: Minimalist Monochrome
- **Industries**: Creative, Luxury
- **Category**: Minimalist

## Design DNA
- **Palette Strategy**: Pure black and white with occasional gray. No colors.
- **Typography**: Bold editorial fonts. Strong contrast between sizes. Serif or geometric sans.
- **Radius Policy**: Sharp corners (0-2px). Architectural precision.
- **Shadow Policy**: None or hard shadows only.
- **Border Language**: Thick black rules. Strong dividers.
- **Patterns**: Strong vertical and horizontal rules. Grid lines.
- **Motion**: Minimal. Instant or very quick transitions.

## Rules
### Do
- Use strong black and white contrast
- Emphasize typography hierarchy
- Use bold editorial layouts
- Keep imagery minimal

### Don't
- Don't use colors unless intentional
- Don't add unnecessary elements
- Don't use rounded corners excessively
- Don't use playful animations

---

## Complete Prompt

# Minimalist Monochrome SaaS Landing Page Prompt (S02)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S02 Minimalist Monochrome** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S02 — Minimalist Monochrome
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

## Style DNA (S02 – Minimalist Monochrome)

### Style Seeds
- **Palette strategy:** Pure black and white with occasional gray. No colors.
- **Typography:** Bold editorial fonts. Strong contrast between sizes. Serif or geometric sans.
- **Radius policy:** Sharp corners (0-2px). Architectural precision.
- **Shadow policy:** None or hard shadows only.
- **Border language:** Thick black rules. Strong dividers.
- **Patterns/textures:** Strong vertical and horizontal rules. Grid lines.
- **Motion:** Minimal. Instant or very quick transitions.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S02"
    style_name: "Minimalist Monochrome"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#F5F5F5"
    text:
      primary: "#000000"
      secondary: "#333333"
      muted: "#666666"
    brand:
      primary: "#000000"
      accent: "#000000"
    border:
      strong: "#000000"
      subtle: "#E0E0E0"
    state:
      success: "#000000"
      warning: "#000000"
      error: "#000000"
    focus:
      ring: "#000000"
  radius:
    none: 0
    sm: 0
    md: 2
  border:
    width:
      hairline: 1
      medium: 2
      strong: 3
  shadow:
    none: none
    hard: "4px 4px 0 #000000"
  layout:
    container:
      content: 1120
      wide: 1280
    grid:
      desktop: 12
      tablet: 8
      mobile: 4
    gutter: { mobile: 16, desktop: 24 }
  motion:
    duration: { fast: 0, normal: 100 }
    easing: linear
  typography:
    font:
      sans: { primary: "Playfair Display", fallback: ["serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["ui-monospace"] }
    scale:
      h1: { size: 56, line: 64, weight: 700, tracking: -0.02 }
      h2: { size: 40, line: 48, weight: 700, tracking: -0.01 }
      h3: { size: 28, line: 36, weight: 700, tracking: -0.005 }
      body: { size: 16, line: 24, weight: 450, tracking: 0 }
      small: { size: 14, line: 20, weight: 450, tracking: 0 }
    measure: { hero_max: "48ch", body_max: "72ch" }
  spacing:
    base: 8
    section_py: { mobile: [64, 80], desktop: [112, 128] }
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
