# Style: Enterprise Blue (S26)

## Overview
- **ID**: S26
- **Name**: Enterprise Blue
- **Industries**: Professional
- **Category**: Corporate

## Design DNA
- **Palette Strategy**: Enterprise blue theme, professional and trustworthy. Deep blues and clean whites.
- **Typography**: Conservative sans-serif (Inter). High legibility and trust.
- **Radius Policy**: Subtle rounding (4-6px). Sharp enough for professionalism.
- **Shadow Policy**: Soft, professional depth. Standard elevation.
- **Border Language**: Defined, thin borders for structural clarity.
- **Patterns**: Conservative geometric patterns or none.
- **Motion**: Polished, professional transitions (200-400ms).

## Rules
### Do
- Use trusted blue tones
- Maintain a clean corporate structure
- Ensure high legibility
- Use consistent spacing and grids

### Don't
- Don't use playful animations
- Don't use clashing colors
- Don't use rounded corners excessively
- Don't over-animate transitions

---

## Complete Prompt

# Enterprise Blue SaaS Landing Page Prompt (S26)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S26 Enterprise Blue** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S26 — Enterprise Blue
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

## Style DNA (S26 – Enterprise Blue)

### Style Seeds
- **Palette strategy:** Enterprise blue theme, professional and trustworthy. Deep blues and clean whites.
- **Typography:** Conservative sans-serif (Inter). High legibility and trust.
- **Radius policy:** Subtle rounding (4-6px). Sharp enough for professionalism.
- **Shadow policy:** Soft, professional depth. Standard elevation.
- **Border language:** Defined, thin borders for structural clarity.
- **Patterns/textures:** Conservative geometric patterns or none.
- **Motion:** Polished, professional transitions (200-400ms).

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S26"
    style_name: "Enterprise Blue"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#F8FAFC"
    text:
      primary: "#0F172A"
      secondary: "#334155"
      muted: "#64748B"
    brand:
      primary: "#1E40AF"
      secondary: "#334155"
      accent: "#3B82F6"
    border:
      strong: "#E2E8F0"
      subtle: "#F1F5F9"
    focus:
      ring: "#1E40AF"
  radius:
    none: 0
    sm: 4
    md: 6
    lg: 8
  border:
    width: { hairline: 1, medium: 1, strong: 2 }
  shadow:
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
  layout:
    container: { content: 1120, wide: 1280 }
  motion:
    duration: { fast: 200, normal: 400 }
    easing: ease-in-out
  typography:
    font:
      sans: { primary: "Inter", fallback: ["system-ui", "sans-serif"] }
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
