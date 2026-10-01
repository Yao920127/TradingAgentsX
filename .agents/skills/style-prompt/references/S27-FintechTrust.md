# Style: Fintech Trust (S27)

## Overview
- **ID**: S27
- **Name**: Fintech Trust
- **Industries**: Professional, Tech
- **Category**: Corporate

## Design DNA
- **Palette Strategy**: Fintech design, secure and innovative. Navy and emerald green.
- **Typography**: Clean, geometric sans-serif (Inter/SF Pro). High precision.
- **Radius Policy**: Modern, consistent (8px). Tech-forward feel.
- **Shadow Policy**: Soft, professional elevation.
- **Border Language**: Defined borders for structural clarity.
- **Patterns**: Financial data motifs, grids, secure layers.
- **Motion**: Precise, smooth transitions (150-300ms).

## Rules
### Do
- Use secure-feeling blues and greens
- Emphasize precision and trust
- Keep layouts clean and structured
- Use modern geometric typography

### Don't
- Don't make it look casual or playful
- Don't use unstable-looking shapes
- Don't use low-contrast text
- Don't use slow or bouncy animations

---

## Complete Prompt

# Fintech Trust SaaS Landing Page Prompt (S27)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S27 Fintech Trust** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S27 — Fintech Trust
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

## Style DNA (S27 – Fintech Trust)

### Style Seeds
- **Palette strategy:** Fintech design, secure and innovative. Navy and emerald green.
- **Typography:** Clean, geometric sans-serif (Inter/SF Pro). High precision.
- **Radius policy:** Modern, consistent (8px). Tech-forward feel.
- **Shadow policy:** Soft, professional elevation.
- **Border language:** Defined borders for structural clarity.
- **Patterns/textures:** Financial data motifs, grids, secure layers.
- **Motion:** Precise, smooth transitions (150-300ms).

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S27"
    style_name: "Fintech Trust"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#0F172A"
      secondary: "#1E293B"
      surface: "#1E293B"
    text:
      primary: "#F8FAFC"
      secondary: "#94A3B8"
      muted: "#64748B"
    brand:
      primary: "#0F172A"
      secondary: "#1E293B"
      accent: "#059669"
    border:
      strong: "#334155"
      subtle: "#1E293B"
      accent: "#059669"
    focus:
      ring: "#059669"
  radius:
    none: 0
    sm: 4
    md: 8
    lg: 12
  border:
    width: { hairline: 1, medium: 1, strong: 2 }
  shadow:
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
  layout:
    container: { content: 1120, wide: 1280 }
  motion:
    duration: { fast: 150, normal: 300 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      sans: { primary: "Inter", fallback: ["SF Pro Display", "system-ui", "sans-serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["monospace"] }
    scale:
      h1: { size: 48, line: 56, weight: 700, tracking: -0.02 }
      h2: { size: 36, line: 44, weight: 700, tracking: -0.01 }
      body: { size: 16, line: 24, weight: 400, tracking: 0 }
  spacing:
    base: 8
    section_py: { mobile: [64, 80], desktop: [96, 128] }
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
