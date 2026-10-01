# Style: Art Deco (S13)

## Overview
- **ID**: S13
- **Name**: Art Deco
- **Industries**: Luxury, Lifestyle
- **Category**: Luxury

## Design DNA
- **Palette Strategy**: Black, gold, and deep jewel tones. High luxury.
- **Typography**: Geometric serif or Art Deco display fonts. High contrast.
- **Radius Policy**: Sharp or geometric cuts. High precision.
- **Shadow Policy**: Subtle glows or none. Emphasis on geometry.
- **Border Language**: Ornate geometric borders. Gold accents.
- **Patterns**: Sunbursts, fans, geometric overlays.
- **Motion**: Elegant, sophisticated transitions.

## Rules
### Do
- Use geometric patterns
- Apply gold and black palette
- Emphasize luxury and precision
- Use high-contrast typography

### Don't
- Don't use rounded corners excessively
- Don't use casual fonts
- Don't use bright, non-luxury colors
- Don't over-animate with bounce

---

## Complete Prompt

# Art Deco SaaS Landing Page Prompt (S13)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S13 Art Deco** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S13 — Art Deco
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

## Style DNA (S13 – Art Deco)

### Style Seeds
- **Palette strategy:** Black, gold, and deep jewel tones. High luxury.
- **Typography:** Geometric serif or Art Deco display fonts. High contrast.
- **Radius policy:** Sharp or geometric cuts. High precision.
- **Shadow policy:** Subtle glows or none. Emphasis on geometry.
- **Border language:** Ornate geometric borders. Gold accents.
- **Patterns/textures:** Sunbursts, fans, geometric overlays.
- **Motion:** Elegant, sophisticated transitions.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S13"
    style_name: "Art Deco"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#111111"
      secondary: "#1A1A1A"
    text:
      primary: "#D4AF37"
      secondary: "#B89B72"
      muted: "#4A4A4A"
    brand:
      primary: "#D4AF37"
      accent: "#FFD700"
    border:
      strong: "#D4AF37"
      subtle: "#333333"
    focus:
      ring: "#D4AF37"
  radius:
    none: 0
    sm: 0
    md: 0
  border:
    width: { hairline: 0.5, medium: 1, strong: 2 }
  shadow:
    gold_glow: "0 0 15px rgba(212, 175, 55, 0.3)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 300, normal: 600 }
    easing: "cubic-bezier(0.19, 1, 0.22, 1)"
  typography:
    font:
      serif: { primary: "Cormorant Garamond", fallback: ["serif"] }
      sans: { primary: "Montserrat", fallback: ["sans-serif"] }
    scale:
      h1: { size: 60, line: 68, weight: 600, tracking: 0.1 }
      h2: { size: 44, line: 52, weight: 600, tracking: 0.05 }
      body: { size: 18, line: 28, weight: 400, tracking: 0.02 }
  spacing:
    base: 12
    section_py: { mobile: [100, 120], desktop: [160, 200] }
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
