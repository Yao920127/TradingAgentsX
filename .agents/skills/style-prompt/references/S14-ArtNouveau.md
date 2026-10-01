# Style: Art Nouveau (S14)

## Overview
- **ID**: S14
- **Name**: Art Nouveau
- **Industries**: Luxury, Creative
- **Category**: Luxury

## Design DNA
- **Palette Strategy**: Organic, muted colors. Earth tones mixed with deep jewel accents.
- **Typography**: Fluid, curvy fonts. Organic feel.
- **Radius Policy**: Extremely rounded (20-40px). Organic curves.
- **Shadow Policy**: Subtle, soft shadows.
- **Border Language**: Ornate, flowing borders.
- **Patterns**: Whip-lash curves, organic motifs, flowers.
- **Motion**: Slow, fluid transitions.

## Rules
### Do
- Use organic, flowing lines
- Apply muted earth tones
- Emphasize whip-lash curves
- Use fluid typography

### Don't
- Don't use sharp edges
- Don't use industrial grays
- Don't use rigid grids
- Don't use fast jarring animations

---

## Complete Prompt

# Art Nouveau SaaS Landing Page Prompt (S14)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S14 Art Nouveau** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S14 — Art Nouveau
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

## Style DNA (S14 – Art Nouveau)

### Style Seeds
- **Palette strategy:** Organic, muted colors. Earth tones mixed with deep jewel accents.
- **Typography:** Fluid, curvy fonts. Organic feel.
- **Radius policy:** Extremely rounded (20-40px). Organic curves.
- **Shadow policy:** Subtle, soft shadows.
- **Border language:** Ornate, flowing borders.
- **Patterns/textures:** Whip-lash curves, organic motifs, flowers.
- **Motion:** Slow, fluid transitions.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S14"
    style_name: "Art Nouveau"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FDFCF0"
      secondary: "#F0EAD6"
    text:
      primary: "#2C3E50"
      secondary: "#7F8C8D"
      muted: "#95A5A6"
    brand:
      primary: "#8E44AD"
      accent: "#27AE60"
    border:
      strong: "#D4AF37"
      subtle: "rgba(212,175,55,0.2)"
    focus:
      ring: "#8E44AD"
  radius:
    none: 0
    sm: 12
    md: 20
    lg: 40
    pill: 9999
  border:
    width: { hairline: 1, medium: 2, strong: 3 }
  shadow:
    soft: "0 10px 30px rgba(0,0,0,0.05)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 400, normal: 800 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      serif: { primary: "Fraunces", fallback: ["serif"] }
      sans: { primary: "Quicksand", fallback: ["sans-serif"] }
    scale:
      h1: { size: 56, line: 64, weight: 600, tracking: 0.05 }
      h2: { size: 40, line: 48, weight: 600, tracking: 0.02 }
      body: { size: 18, line: 30, weight: 400, tracking: 0.05 }
  spacing:
    base: 10
    section_py: { mobile: [80, 100], desktop: [140, 180] }
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
