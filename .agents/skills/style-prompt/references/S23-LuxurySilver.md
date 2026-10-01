# Style: Luxury Silver (S23)

## Overview
- **ID**: S23
- **Name**: Luxury Silver
- **Industries**: Luxury, Professional
- **Category**: Luxury

## Design DNA
- **Palette Strategy**: Brushed silver, platinum, and cool whites. Modern luxury, tech-forward.
- **Typography**: Sophisticated modern sans-serif with wide tracking.
- **Radius Policy**: Subtle rounding (4px) or zero. "Machined" look.
- **Shadow Policy**: Cool, diffused silver shadows. Soft metallic reflections.
- **Border Language**: Silver hairline borders and accents.
- **Patterns**: Metallic textures, platinum reflections.
- **Motion**: Smooth, sophisticated transitions (300-600ms).

## Rules
### Do
- Use cool silver and platinum tones
- Combine with deep navy or solid black
- Maintain "machined" look with subtle rounding
- Incorporate metallic motifs

### Don't
- Don't use warm gold or brass
- Don't use heavy textures
- Don't use rounded corners excessively
- Don't use non-luxury colors

---

## Complete Prompt

# Luxury Silver SaaS Landing Page Prompt (S23)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S23 Luxury Silver** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S23 — Luxury Silver
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

## Style DNA (S23 – Luxury Silver)

### Style Seeds
- **Palette strategy:** Brushed silver, platinum, and cool whites. Modern luxury, tech-forward.
- **Typography:** Sophisticated modern sans-serif with wide tracking.
- **Radius policy:** Subtle rounding (4px) or zero. "Machined" look.
- **Shadow policy:** Cool, diffused silver shadows. Soft metallic reflections.
- **Border language:** Silver hairline borders and accents.
- **Patterns/textures:** Metallic textures, platinum reflections.
- **Motion:** Smooth, sophisticated transitions (300-600ms).

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S23"
    style_name: "Luxury Silver"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#E5E5E5"
      secondary: "#D1D5DB"
    text:
      primary: "#111827"
      secondary: "#374151"
      muted: "#6B7280"
    brand:
      primary: "#9CA3AF"
      accent: "#6B7280"
    border:
      strong: "#9CA3AF"
      subtle: "#D1D5DB"
    focus:
      ring: "#9CA3AF"
  radius:
    none: 0
    sm: 4
    md: 8
  border:
    width: { hairline: 1, medium: 1, strong: 2 }
  shadow:
    silver: "0 10px 30px rgba(156, 163, 175, 0.2)"
    platinum: "0 20px 40px rgba(209, 213, 219, 0.3)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 300, normal: 600 }
    easing: "cubic-bezier(0.16, 1, 0.3, 1)"
  typography:
    font:
      sans: { primary: "Montserrat", fallback: ["Inter", "sans-serif"] }
    scale:
      h1: { size: 56, line: 64, weight: 500, tracking: 0.1 }
      h2: { size: 40, line: 48, weight: 500, tracking: 0.05 }
      body: { size: 16, line: 26, weight: 400, tracking: 0.02 }
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
